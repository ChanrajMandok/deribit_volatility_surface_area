
from typing import Optional, Tuple, Union
import sys
import traceback
import json
import random

from deribit_arb_app.services.deribit_account_summary_handler import DeribitAccountSummaryHandler
from deribit_arb_app.services.deribit_authentication_handler import DeribitAuthenticationHandler
from deribit_arb_app.services.deribit_instruments_handler import DeribitInstrumentsHandler
from deribit_arb_app.services.deribit_orders_handler import DeribitOrdersHandler
from deribit_arb_app.services.deribit_subscription_handler import DeribitSubscriptionHandler
from deribit_arb_app.services.deribit_test_handler import DeribitTestHandler
from deribit_arb_app.services.deribit_positions_handler import DeribitPositionsHandler
from deribit_arb_app.services.deribit_subscription_handler import DeribitSubscriptionHandler


class DeribitMessaging:

    def message_handle(self, response) -> Tuple[Union[int, str, None], object]:

        try:

            response_json = json.loads(response)

            message_type = None
            if "id" in response_json:
                message_type = int(response_json["id"] / 100000)

            method = None
            if "method" in response_json:
                method = response_json["method"]

            data = None

            if message_type == 0:
                data = DeribitPositionsHandler().set_positions(response_json)
            if message_type == 1:
                DeribitAuthenticationHandler().set_authorization(response_json)
            elif message_type == 4:
                data = DeribitInstrumentsHandler().set_instruments(response_json)
            elif message_type == 5:
                data = DeribitAccountSummaryHandler().set_account_summary(response_json)
            elif message_type == 6:
                data = DeribitOrdersHandler().set_order(response_json)
            elif message_type == 7:
                data = DeribitOrdersHandler().set_open_orders(response_json)
            elif message_type == 9:
                DeribitTestHandler().check_response(response_json)
            elif message_type == 10:
                data = DeribitOrdersHandler().set_cancelled_order(response_json)
            elif method == "subscription":
                DeribitSubscriptionHandler().handle(response_json)
            else:
                pass

            if "id" in response_json:
                return response_json["id"], data
            elif "method" in response_json:
                return response_json["method"], None
            else: 
                return None, None

        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)


    def generate_id(self, method) -> int:

        msg_id = random.randrange(0, 10000)

        if method == "public/auth":
            msg_id = 100000 + msg_id
        elif method == "public/subscribe":
            msg_id = 200000 + msg_id
        elif method == "public/subscribe":
            msg_id = 300000 + msg_id
        elif method == "public/get_instruments":
            msg_id = 400000 + msg_id
        elif method == "private/get_account_summary":
            msg_id = 500000 + msg_id
        elif (method == "private/buy") or (method == "private/sell"):
            msg_id = 600000 + msg_id
        elif method == "private/get_open_orders_by_currency":
            msg_id = 700000 + msg_id
        elif method == "public/set_heartbeat":
            msg_id = 800000 + msg_id
        elif method == "public/test":
            msg_id = 900000 + msg_id
        elif method == "private/cancel":
            msg_id = 1000000 + msg_id

        return msg_id



