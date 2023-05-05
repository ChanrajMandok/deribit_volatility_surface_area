from typing import Dict, List, Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_subscribable import ModelSubscribable

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

    async def get_instruments(
                              self,
                              currency: str, 
                              kind: str) -> Dict[str, ModelInstrument]:

        deribit_instruments = ServiceDeribitInstruments(currency=currency, kind=kind)

        instruments = await deribit_instruments.get()

        return instruments
        
    async def get_open_orders(
                              self,
                              currency: str) -> Dict[str, Dict[str, List[ModelOrder]]]:

        deribit_orders = ServiceDeribitOrders()

        open_orders = await deribit_orders.get_open_orders_by_currency(currency=currency)

        return open_orders

    async def send_order(
        self,
        instrument: ModelInstrument, 
        direction: EnumDirection, 
        amount: float, 
        price: float) -> Optional[ModelOrder]:

        deribit_orders = ServiceDeribitOrders()

        if direction == EnumDirection.BUY:
            order = await deribit_orders.buy_async(
                    instrument_name=instrument.instrument_name, 
                    amount=amount, 
                    price=price)
            
        elif direction == EnumDirection.SELL:
            order = await deribit_orders.sell_async(
                    instrument_name=instrument.instrument_name, 
                    amount=amount, 
                    price=price)

        return order

    async def cancel_order(
        self, 
        order_id: str) -> ModelOrder:

        deribit_orders = ServiceDeribitOrders()

        return await deribit_orders.cancel(order_id=order_id)

    async def get_positions(self, currency) -> Dict[str,Dict[str, ModelPosition]]:

        deribit_positions = ServiceDeribitPositions(currency=currency)

        return await deribit_positions.get()

    async def get_account_summary(self, currency) -> ServiceDeribitAccountSummary:

        deribit_account_summary = ServiceDeribitAccountSummary(currency=currency)

        return await deribit_account_summary.get()

    async def subscribe(self, subscribables: List[ModelSubscribable]):

        # deribit quotes service
        deribit_subscribe = ServiceDeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.subscribe(
            subscribables=subscribables, snapshot=False
        ))

        await task

    async def unsubscribe(self, subscribables: List[ModelSubscribable]):
    
        # deribit quotes service
        deribit_subscribe = ServiceDeribitSubscribe()

        task = self.my_loop.create_task(deribit_subscribe.unsubscribe(
            subscribables=subscribables
        ))

        await task

