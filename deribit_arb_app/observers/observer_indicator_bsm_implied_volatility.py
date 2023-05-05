from singleton_decorator import singleton

from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.services.service_implied_volatilty_bsm_builder import ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty

    ###################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatilty #
    ###################################################################################################

@singleton
class ObserverIndicatorBsmImpliedVoaltility(ObserverInterface):

    def __init__(self, iiv_instance:ModelIndicatorBsmImpliedVolatility) -> None:
        super.__init__()
        self.__indicator_bsm_implied_volatility     = None
        self.instrument                             = iiv_instance.instrument
        self.index                                  = iiv_instance.index 

        self.store_subject_order_books              = StoreSubjectOrderBooks()
        self.store_subject_index_prices             = StoreSubjectIndexPrices()
        self.store_subject_indicator_bsm_iv         = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.service_implied_volatilty_bsm_builder  = ServiceImpliedVolatilityBsmBuilder(iiv_instance)

        # Attach observer to instrument orderbook and index 
        self.store_subject_order_books.get_subject(self.instrument).attach(self)
        self.store_subject_index_prices.get_subject(self.index).attach(self)

    def update(self) -> None: 
        self.__indicator_bsm_implied_volatility = self.service_implied_volatilty_bsm_builder.build()
        if self.__indicator_bsm_implied_volatility is None:
            return 
        print(f"{self.__indicator_bsm_implied_volatility.key}: {round(self.__indicator_bsm_implied_volatility.value, 6)}")
        self.store_subject_indicator_bsm_iv.update_subject(self.__indicator_bsm_implied_volatility)

    def get(self) -> ModelIndicatorBsmImpliedVolatility :
        return self.__indicator_bsm_implied_volatility
    
    def __exit__(self):
        self.store_subject_order_books.get_subject(self.instrument).attach(self)
        self.store_subject_index_prices.get_subject(self.index).attach(self)

        ##todo potientially observe a complete list of instruments in one go, this may be less completx and optimise the code more effectivly