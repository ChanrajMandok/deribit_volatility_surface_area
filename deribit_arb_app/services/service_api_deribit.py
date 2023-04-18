import asyncio

from typing import Dict, List, Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable

from deribit_arb_app.enums.enum_direction import EnumDirection

from deribit_arb_app.services.service_api_interface import ServiceApiInterface
from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.services.service_deribit_positions import ServiceDeribitPositions
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.services.service_deribit_instruments import ServiceDeribitInstruments
from deribit_arb_app.services.service_deribit_account_summary import ServiceDeribitAccountSummary

    ################################################################################
    # Service Implements Deribit API to provide Framework to trade via Deribit API #
    ################################################################################

class ServiceApiDeribit(ServiceApiInterface):

    def __init__(self):
        self.my_loop = asyncio.get_event_loop()
        if self.my_loop is None:
            self.my_loop = asyncio.new_event_loop()
        super().__init__()

    def get_instruments(
        self,
        currency: str, 
        kind: str) -> Dict[str, ModelInstrument]:

        deribit_instruments = ServiceDeribitInstruments(currency=currency, kind=kind)

        instruments = self.my_loop.run_until_complete(
            asyncio.wait_for(deribit_instruments.get(), timeout=100.0))

        return instruments
        
    def get_open_orders(
        self,
        currency: str) -> Dict[str, Dict[str, List[ModelOrder]]]:

        deribit_orders = ServiceDeribitOrders()

        open_orders = self.my_loop.run_until_complete(
            asyncio.wait_for(deribit_orders.get_open_orders_by_currency(currency=currency),timeout=100.0)
        )

        return open_orders

    def send_order(
        self,
        instrument: ModelInstrument, 
        direction: EnumDirection, 
        amount: float, 
        price: float) -> Optional[ModelOrder]:

        deribit_orders = ServiceDeribitOrders()

        if direction == EnumDirection.BUY:
            order = self.my_loop.run_until_complete(
                deribit_orders.buy_async(
                    instrument_name=instrument.instrument_name, 
                    amount=amount, 
                    price=price)
            )
        elif direction == EnumDirection.SELL:
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

        deribit_orders = ServiceDeribitOrders()

        return self.my_loop.run_until_complete(deribit_orders.cancel(order_id=order_id))

    def get_positions(self, currency) -> Dict[str,Dict[str, ModelPosition]]:

        deribit_positions = ServiceDeribitPositions(currency=currency)

        return self.my_loop.run_until_complete(deribit_positions.get())

    def get_account_summary(self, currency) -> ServiceDeribitAccountSummary:

        deribit_account_summary = ServiceDeribitAccountSummary(currency=currency)

        return self.my_loop.run_until_complete(deribit_account_summary.get())

    async def subscribe(self, subscribables: List[ModelExchangeSubscribable]):

        # deribit quotes service
        deribit_subscribe = ServiceDeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.subscribe(
            subscribables=subscribables, snapshot=False
        ))

        await task

    async def unsubscribe(self, subscribables: List[ModelExchangeSubscribable]):
    
        # deribit quotes service
        deribit_subscribe = ServiceDeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.unsubscribe(
            subscribables=subscribables
        ))

        await task

