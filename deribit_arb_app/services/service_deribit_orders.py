import json
import uuid
from typing import Dict

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_message import ModelMessage

from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_authentication import ServiceDeribitAuthentication
from deribit_arb_app.services.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    #################################################
    # Service sends orders to Deribit via Websocket #
    #################################################

class ServiceDeribitOrders:

    def __init__(self) -> None:
        
        self.deribit_messaging = ServiceDeribitMessaging()

    async def send_instruction(self, params: Dict, method: str):

        msg_id = self.deribit_messaging.generate_id(method)

        msg = ModelMessage(
            msg_id=msg_id,
            method=method,
            params=params
        )

        async with ServiceDeribitWebsocketConnector() as websocket:
            await ServiceDeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                
                # handle the message and get the id
                id, data = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == msg_id:
                    return data

    async def buy_async(self, instrument_name: str, amount: float, price: float) -> ModelOrder:

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

        params = {
            "order_id": order_id
        }

        method = "private/cancel"

        return await self.send_instruction(params, method)


    async def cancel_all(self):

        params = {
        }

        method = "private/cancel_all"

        await self.send_instruction(params, method)


    async def get_open_orders_by_currency(self, currency: str):

        params = {
            "currency": currency
        }

        method = "private/get_open_orders_by_currency"

        return await self.send_instruction(params, method)


    async def get_margins(self, instrument_name: str, amount: float, price: float):

        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "price": price
        }

        method = "private/get_margins"

        await self.send_instruction(params, method)

