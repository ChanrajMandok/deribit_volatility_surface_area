from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.store.store_observable_interface import StoreObservableInterface
from deribit_arb_app.model.model_observable_order_book import ModelObservableOrderBook
from deribit_arb_app.model.model_observable_index_price import ModelObservableIndexPrice
from deribit_arb_app.store.store_subscribable_interface import StoreSubscribableInterface
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_observable_volatility_index import ModelObservableVolatilityIndex
from deribit_arb_app.store.store_observable_indicator_interface import StoreObservableIndicatorInterface
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread 
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallVolArbitrage

    ############################################################################
    # Stores Declares Store instances utilising Modularity of Store Interfaces #
    ############################################################################

class Stores:

    store_subscribable_indexes                  = StoreSubscribableInterface[str, ModelSubscribableIndex]() 
    store_subscribable_instruments              = StoreSubscribableInterface[str, ModelSubscribableInstrument]()

    store_observable_orderbooks                 = StoreObservableInterface[str, ModelObservableOrderBook]()
    store_observable_index_prices               = StoreObservableInterface[str, ModelObservableIndexPrice]()
    store_observable_volatility_index           = StoreObservableInterface[str, ModelObservableVolatilityIndex]()

    store_indicator_put_call_parity_arbitrage   = StoreObservableIndicatorInterface[str, ModelIndicatorPutCallVolArbitrage]()
    store_indicator_annualised_return_spreads   = StoreObservableIndicatorInterface[str, ModelIndicatorAnnualisedReturnSpread]()
