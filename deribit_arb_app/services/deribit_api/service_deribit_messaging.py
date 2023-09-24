import sys
import json
import random
import traceback

from typing import Union

from deribit_arb_app.services.handlers.service_deribit_test_handler import \
                                                   ServiceDeribitTestHandler
from deribit_arb_app.services.handlers.service_deribit_orders_handler import \
                                                   ServiceDeribitOrdersHandler
from deribit_arb_app.services.handlers.service_deribit_positions_handler import \
                                                   ServiceDeribitPositionsHandler
from deribit_arb_app.services.handlers.service_deribit_instruments_handler import \
                                                   ServiceDeribitInstrumentsHandler
from deribit_arb_app.services.handlers.service_deribit_subscription_handler import \
                                                   ServiceDeribitSubscriptionHandler
from deribit_arb_app.services.handlers.service_deribit_unsubcription_handler import \
                                                  ServiceDeribitUnsubscriptionHandler
from deribit_arb_app.services.handlers.service_deribit_authentication_handler import \
                                                   ServiceDeribitAuthenticationHandler
from deribit_arb_app.services.handlers.service_deribit_account_summary_handler import \
                                                    ServiceDeribitAccountSummaryHandler
from deribit_arb_app.services.handlers.service_deribit_orderbook_summary_handler import \
                                                    ServiceDeribitOrderbookSummaryHandler
from deribit_arb_app.services.handlers.service_deribit_cancel_all_positions_handler import \
                                                     ServiceDeribitCancelAllPositionsHandler

    ###################################################
    # Service provides Interface for Deribit messages #
    ###################################################

class ServiceDeribitMessaging():

    def message_handle(self, response) -> tuple[Union[int, str, None], object]:

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
                data = ServiceDeribitPositionsHandler().set_positions(response_json)
            elif message_type == 1:
                ServiceDeribitAuthenticationHandler().set_authorization(response_json)
            elif message_type == 2:
                ServiceDeribitSubscriptionHandler().handle(response_json)
            elif message_type == 3:
                ServiceDeribitUnsubscriptionHandler().handle(response_json)
            elif message_type == 4:
                data = ServiceDeribitInstrumentsHandler().set_instruments(response_json)
            elif message_type == 5:
                data = ServiceDeribitAccountSummaryHandler().set_account_summary(response_json)
            elif message_type == 6:
                data = ServiceDeribitOrdersHandler().set_order(response_json)
            elif message_type == 7:
                data = ServiceDeribitOrdersHandler().set_open_orders(response_json)
            elif message_type == 9:
                ServiceDeribitTestHandler().check_response(response_json)
            elif message_type == 10:
                data = ServiceDeribitOrdersHandler().set_cancelled_order(response_json)
            elif message_type == 11:
                data = ServiceDeribitCancelAllPositionsHandler().cancel_all(response_json)
            elif message_type == 12:
                data = ServiceDeribitOrderbookSummaryHandler().handle(response_json)
            elif method == "subscription":
                ServiceDeribitSubscriptionHandler().handle(response_json)    
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
        elif method == "public/unsubscribe":
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
        elif method == "private/cancel_all":
            msg_id = 1100000 + msg_id
        elif method == "public/get_book_summary_by_currency":
            msg_id = 1200000 + msg_id

        return msg_id



