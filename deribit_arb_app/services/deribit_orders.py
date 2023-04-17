import asyncio
import json
import uuid
from typing import Dict

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_authentication import DeribitAuthentication
from deribit_arb_app.services.deribit_websocket_connector import DeribitWebsocketConnector
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.model.model_order import ModelOrder


class DeribitOrders:

    def __init__(self) -> None:
        
        self.deribit_messaging = DeribitMessaging()

    async def send_instruction(self, params: Dict, method: str):

        msg_id = self.deribit_messaging.generate_id(method)

        msg = ModelMessage(
            msg_id=msg_id,
            method=method,
            params=params
        )

        async with DeribitWebsocketConnector().get_websocket() as websocket:
            await DeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                
                # handle the message and get the id
                id, data = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == msg_id or id is None:
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

