from django.db import models

# Create your models here.

from deribit_arb_app.model.model_trade import ModelTrade
from deribit_arb_app.model.model_quote import ModelQuote
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_observable_order_book import \
                                       ModelObservableOrderBook
from deribit_arb_app.model.model_observable_index_price import \
                                       ModelObservableIndexPrice
from deribit_arb_app.model.model_observable import ModelObservable
from deribit_arb_app.model.model_historical_funding_rate import \
                                       ModelHistoricalFundingRate
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable import ModelSubscribable
from deribit_arb_app.model.model_observable_volatility_index import \
                                       ModelObservableVolatilityIndex
from deribit_arb_app.model.model_authorization import ModelAuthorization
from deribit_arb_app.model.model_account_summary import ModelAccountSummary
from deribit_arb_app.model.model_orderbook_summary import ModelOrderbookSummary
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.model.indicator_models.model_indicator_volatility_surface_area import \
                                                         ModelIndicatorVolatilitySurfaceArea
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import \
                                                         ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import \
                                                             ModelIndicatorPutCallVolArbitrage