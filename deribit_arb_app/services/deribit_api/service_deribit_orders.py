import json
import uuid

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_authentication import \
                                                     ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector

    #################################################
    # Service sends orders to Deribit via Websocket #
    #################################################

class ServiceDeribitOrders():
    """
    Handles sending and managing orders on the Deribit platform via Websocket.
    """

    def __init__(self) -> None:
        self.deribit_messaging = ServiceDeribitMessaging()


    async def send_instruction(self, params: dict, method: str):
        """Sends instructions to the Deribit API."""
        
        msg_id = self.deribit_messaging.generate_id(method)

        self.msg = ModelMessage(msg_id=self.msg_id,
                                method=self.method,
                                params=self.params
                                )

        async with ServiceDeribitWebsocketConnector() as websocket:
            await ServiceDeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                
                # handle the message and get the id
                id, data = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == msg_id:
                    return data


    async def buy_async(self, instrument_name: str, amount: float, price: float) -> ModelOrder:
        """ Sends a buy instruction to the Deribit API."""

        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": "limit",
            "price": price,
            "label": str(uuid.uuid4())
        }

        method = "private/buy"

        return await self.send_instruction(params, method)


    async def sell_async(self, instrument_name: str, amount: float, price: float) -> ModelOrder:
        """Sends a buy instruction to the Deribit API."""

        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": "limit",
            "price": price,
            "label": str(uuid.uuid4())
        }

        method = "private/sell"

        return await self.send_instruction(params, method)


    async def cancel(self, order_id: str) -> ModelOrder:
        """Sends a cancel order instruction to the Deribit API."""

        params = {
            "order_id": order_id
        }

        method = "private/cancel"

        return await self.send_instruction(params, method)


    async def cancel_all(self):
        """Sends an instruction to the Deribit API to cancel all orders."""

        params = {
        }

        method = "private/cancel_all"

        await self.send_instruction(params, method)


    async def get_open_orders_by_currency(self, currency: str):
        """ Retrieves all open orders for a given currency from the Deribit API."""

        params = {
            "currency": currency
        }

        method = "private/get_open_orders_by_currency"

        return await self.send_instruction(params, method)


    async def get_margins(self, instrument_name: str, amount: float, price: float):
        """Retrieves margin details for a given instrument from the Deribit API."""
        
        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "price": price
        }

        method = "private/get_margins"

        await self.send_instruction(params, method)