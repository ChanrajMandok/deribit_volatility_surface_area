import asyncio

from singleton_decorator import singleton

from deribit_arb_app.schedulers import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_observable_instrument_list import \
                                      ModelObservableInstrumentList
from deribit_arb_app.utils.utils_asyncio import get_or_create_eventloop
from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.utils.utils_asyncio import loop_create_task_log_exception
from deribit_arb_app.services.managers.service_instruments_subscription_manager import \
                                                  ServiceInstrumentsSubscriptionManager

    ###################################################################################################
    # Observer monitors VSA Instrument List (Store) and notifys Subscription Manager of state changes #
    ###################################################################################################

@singleton
class ObserverStoreObservableInstrumentList(ObserverInterface):

    def __init__(self, implied_volatility_queue: asyncio.Queue) -> None:
        super().__init__()
        self.observer = None
        self.store_observable_instrument_list = Stores.store_observable_instrument_list
        self.service_instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(implied_volatility_queue)
        
    def attach_observer(self, instance: ModelObservableInstrumentList):
        """ Attach this observer to the instance """
        self.observer = instance
        self.store_observable_instrument_list.get_observable(instance).attach(self)

    def detach_observer(self, instance: ModelObservableInstrumentList):
        """ Detach this observer from the instance """
        self.store_observable_instrument_list.get_observable(instance).detach(self)
        self.observer = None
    
    def get(self) -> ModelObservableInstrumentList:
        return self.observer
    
    def update(self):
        observable = Stores.store_observable_instrument_list.get_observable(self.observer)
        observable_instance = observable.instance
        index = observable_instance.index
        instruments_list = observable_instance.instruments 
        volatility_index = observable_instance.volatility_index
        
        task = self.service_instruments_subscription_manager.manage_instrument_subscribables(
            index=index,
            instruments=instruments_list,
            volatility_index=volatility_index            
        )
        
        loop = get_or_create_eventloop()        
        loop_create_task_log_exception(awaitable=task, logger=logger, 
                            loop=loop, origin=f"{self.__class__.__name__}")
        print(asyncio.all_tasks(loop=loop))