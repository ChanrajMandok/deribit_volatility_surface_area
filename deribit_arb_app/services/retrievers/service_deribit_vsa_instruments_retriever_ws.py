import os
import heapq

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_api_deribit import \
                                                     ServiceApiDeribit
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull

    #################################################################
    # Retriever Retrieves Liquid Instruments Markets to Make up VSA #
    #################################################################

class ServiceDeribitVsaInstrumentsRetrieverWs():
    """
    This class retrieves the most liquid instruments from Deribit's API based on volume.
    It maintains a list of subscribable instruments and uses the Deribit API service for fetching orderbook summaries.
    """

    def __init__(self):        
        self.service_api_deribit = ServiceApiDeribit()
        self.store_subscribable_instruments = Stores.store_subscribable_instruments
        self.__vsa_max_num_subscriptions = int(os.environ.get(
                                                'VSA_MAX_NUMBER_OF_SUBSCRIPTIONS', 25))


    async def async_setup(self,
                          kind: str,
                          currency: str):
        """
        Performs initial setup by pulling instruments based on currency and kind.

        Args:
            kind (str): The type of instrument (e.g., futures, options).
            currency (str): The currency for the instruments (e.g., BTC, ETH).
        """
        await TaskInstrumentsPull().run(currency=currency, kind=kind)


    async def retrieve_liquid_instruments(self,
                                          kind: str,
                                          currency: str) -> list[ModelSubscribableInstrument]:
        """
        Retrieves the most liquid instruments based on orderbook volumes.

        Args:
            kind (str): The type of instrument (e.g., futures, options).
            currency (str): The currency for the instruments (e.g., BTC, ETH).

        Returns:
            list[ModelSubscribableInstrument]: A list of the most liquid instruments.
        """
        store_subscribable_instruments = self.store_subscribable_instruments.get()
        if not store_subscribable_instruments: 
            await self.async_setup(currency=currency, kind=kind)

        orderbook_summaries = await self.service_api_deribit.get_orderbook_summary_via_currency(
            kind=kind, currency=currency)

        # Find the top instruments by volume using a heap for efficiency
        top_instruments_heap = heapq.nlargest(
            self.__vsa_max_num_subscriptions,
            ((summary.volume_usd, summary.instrument_name) for summary in orderbook_summaries \
                                                                if summary.volume_usd is not None),
            key=lambda x: x[0]
        )

        # Extract instrument names from the top of the heap
        top_liquid_instrument_names = {name for _, name in top_instruments_heap}

        # Compile the list of top liquid instruments
        result = [instr for instr in store_subscribable_instruments.values()
                  if instr.kind == kind and instr.base_currency == currency and \
                                                        instr.name in top_liquid_instrument_names]

        # logger.info(f"{self.__class__.__name__}: {self.__vsa_max_num_subscriptions} Liquid Instruments Retrieved")
        return result