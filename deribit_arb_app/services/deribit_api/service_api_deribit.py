from typing import Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable import ModelSubscribable
from deribit_arb_app.services.deribit_api.service_api_interface import \
                                                     ServiceApiInterface
from deribit_arb_app.services.deribit_api.service_deribit_orders import \
                                                     ServiceDeribitOrders
from deribit_arb_app.services.deribit_api.service_deribit_positions import \
                                                     ServiceDeribitPositions
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import \
                                                     ServiceDeribitSubscribe
from deribit_arb_app.services.deribit_api.service_deribit_instruments import \
                                                     ServiceDeribitInstruments
from deribit_arb_app.services.deribit_api.service_deribit_account_summary import \
                                                      ServiceDeribitAccountSummary
from deribit_arb_app.services.deribit_api.service_deribit_get_orderbook_summary import \
                                                       ServiceDeribitGetOrderbookSummary
                                                       
    ################################################################################
    # Service Implements Deribit API to provide Framework to trade via Deribit API #
    ################################################################################

class ServiceApiDeribit(ServiceApiInterface):
    """API service for Deribit operations."""

    def __init__(self) -> None:
        super().__init__()
        self._deribit_orders = ServiceDeribitOrders()
        self._deribit_subscribe = ServiceDeribitSubscribe()

    async def get_instruments(self, 
                              kind: str,
                              currency: str) -> dict[str, ModelSubscribableInstrument]:
        """Retrieve available instruments for a given currency and kind."""
        deribit_instruments = ServiceDeribitInstruments(currency=currency, kind=kind)
        return await deribit_instruments.get()

    async def get_open_orders(self,
                               currency: str) -> dict[str, dict[str, list[ModelOrder]]]:
        """Retrieve open orders for a given currency"""
        return await self._deribit_orders.get_open_orders_by_currency(currency=currency)

    async def send_order(self,
                         price: float,
                         amount: float, 
                         direction: EnumDirection, 
                         instrument: ModelSubscribableInstrument) -> Optional[ModelOrder]:
        """Send an order to buy/sell."""
        if direction == EnumDirection.BUY:
            return await self._deribit_orders.buy_async(instrument_name=instrument.name, amount=amount, price=price)
        elif direction == EnumDirection.SELL:
            return await self._deribit_orders.sell_async(instrument_name=instrument.name, amount=amount, price=price)

    async def cancel_order(self,
                           order_id: str) -> ModelOrder:
        """Cancel an existing order. """
        return await self._deribit_orders.cancel(order_id=order_id)

    async def get_positions(self,
                            currency: str) -> dict[str, dict[str, ModelPosition]]:
        """Retrieve positions for a given currency."""
        deribit_positions = ServiceDeribitPositions(currency=currency)
        return await deribit_positions.get()
    
    async def get_account_summary(self,
                                  currency: str) -> ServiceDeribitAccountSummary:
        """Retrieve account summary for a given currency."""
        deribit_account_summary = ServiceDeribitAccountSummary(currency=currency)
        return await deribit_account_summary.get()

    async def subscribe(self, 
                        subscribables: list[ModelSubscribable]):
        """Subscribe to a list of subscribables."""
        
        task = self.my_loop.create_task(self._deribit_subscribe.subscribe(subscribables=subscribables, snapshot=False))
        await task

    async def unsubscribe(self,
                          unsubscribables: list[ModelSubscribable]):
        """Unsubscribe from a list of subscribables."""
        task = self.my_loop.create_task(self._deribit_subscribe.unsubscribe(unsubscribables=unsubscribables))
        await task

    async def get_orderbook_summary_via_currency(self, 
                                                 kind: str,
                                                 currency: str): 
        """Retrieve orderbook summary for a specific currency and kind."""
        service_deribit_get_orderbook_summary = ServiceDeribitGetOrderbookSummary(currency=currency, kind=kind)        
        return await service_deribit_get_orderbook_summary.get()