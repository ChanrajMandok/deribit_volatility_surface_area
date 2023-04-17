from django.db import models

# Create your models here.

from deribit_arb_app.model.model_account_summary import ModelAccountSummary
from deribit_arb_app.model.model_authorization import ModelAuthorization
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable
from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread 
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_quote import ModelQuote
from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.model.model_trade import ModelTrade
from deribit_arb_app.model.model_historical_funding_rate import ModelHistoricalFundingRate