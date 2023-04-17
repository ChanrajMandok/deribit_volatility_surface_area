from asyncio.tasks import Task
from deribit_arb_app.services.deribit_subscribe import DeribitSubscribe
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable
from deribit_arb_app.services.deribit_account_summary import DeribitAccountSummary
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.services.deribit_positions import DeribitPositions
from typing import Dict, List, Optional
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.services.deribit_orders import DeribitOrders
from deribit_arb_app.services.deribit_instruments import DeribitInstruments
import asyncio
from deribit_arb_app.services.api_interface import ApiInterface
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.enums.direction import Direction
import threading


class ApiDeribit(ApiInterface):

    def __init__(self):
        self.my_loop = asyncio.get_event_loop()
        if self.my_loop is None:
            self.my_loop = asyncio.new_event_loop()
        super().__init__()

    def get_instruments(
        self,
        currency: str, 
        kind: str) -> Dict[str, ModelInstrument]:

        deribit_instruments = DeribitInstruments(currency=currency, kind=kind)

        instruments = self.my_loop.run_until_complete(
            asyncio.wait_for(deribit_instruments.get(), timeout=100.0))

        return instruments
        
    def get_open_orders(
        self,
        currency: str) -> Dict[str, Dict[str, List[ModelOrder]]]:

        deribit_orders = DeribitOrders()

        open_orders = self.my_loop.run_until_complete(
            asyncio.wait_for(deribit_orders.get_open_orders_by_currency(currency=currency),timeout=100.0)
        )

        return open_orders

    def send_order(
        self,
        instrument: ModelInstrument, 
        direction: Direction, 
        amount: float, 
        price: float) -> Optional[ModelOrder]:

        deribit_orders = DeribitOrders()

        if direction == Direction.BUY:
            order = self.my_loop.run_until_complete(
                deribit_orders.buy_async(
                    instrument_name=instrument.instrument_name, 
                    amount=amount, 
                    price=price)
            )
        elif direction == Direction.SELL:
            order = self.my_loop.run_until_complete(
                deribit_orders.sell_async(
                    instrument_name=instrument.instrument_name, 
                    amount=amount, 
                    price=price)
            )

        return order

    def cancel_order(
        self, 
        order_id: str) -> ModelOrder:

        deribit_orders = DeribitOrders()

        return self.my_loop.run_until_complete(deribit_orders.cancel(order_id=order_id))

    def get_positions(self, currency) -> Dict[str,Dict[str, ModelPosition]]:

        deribit_positions = DeribitPositions(currency=currency)

        return self.my_loop.run_until_complete(deribit_positions.get())

    def get_account_summary(self, currency) -> DeribitAccountSummary:

        deribit_account_summary = DeribitAccountSummary(currency=currency)

        return self.my_loop.run_until_complete(deribit_account_summary.get())

    async def subscribe(self, subscribables: List[ModelExchangeSubscribable]):

        # deribit quotes service
        deribit_subscribe = DeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.subscribe(
            subscribables=subscribables, snapshot=False
        ))

        await task

    async def unsubscribe(self, subscribables: List[ModelExchangeSubscribable]):
    
        # deribit quotes service
        deribit_subscribe = DeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.unsubscribe(
            subscribables=subscribables
        ))

        await task

