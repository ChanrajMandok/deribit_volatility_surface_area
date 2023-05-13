import asyncio
from typing import List, Tuple

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind

from deribit_arb_app.services.retrievers.service_retrieve_deribit_liquid_option_instruments import ServiceRetrieveDeribitLiquidOptionInstruments

    #####################################################
    # Service Handles & Manages Liquid instruments List # 
    #####################################################

class ServiceImpliedVolatiltySurfaceAreaInstrumentSubscriptionManager():
    
    def __init__(self):
        self.currency = EnumCurrency.BTC.value
        self.kind = EnumInstrumentKind.OPTION.value
        self.index = ModelIndex(index_name="btc_usd") if self.currency == EnumCurrency.BTC.value else ModelIndex(index_name="btc_usd")        
        self.liquid_instruments_list_retriever = ServiceRetrieveDeribitLiquidOptionInstruments()
        self.previous_instruments = None

    async def manage_instrument_subscribables(self) -> Tuple[List[str], List[str]]:
        while True:
            instruments = await self.liquid_instruments_list_retriever.main(populate=False, currency=self.currency, kind=self.kind)

            if self.previous_instruments is None:
                instruments_subscribe = instruments
                instruments_unsubscribe = []
            else:
                instruments_subscribe = [instrument for instrument in instruments if instrument not in self.previous_instruments]
                instruments_unsubscribe = [instrument for instrument in self.previous_instruments if instrument not in instruments]

            self.previous_instruments = instruments
            await asyncio.sleep(0.25)
            (instruments_subscribe, instruments_unsubscribe)

    async def main(self):
        # Run the check_instruments_changes task indefinitely
        while True:
            try:
                await self.manage_instrument_subscribables()
            except Exception as e:
                print("An error occurred:", e)
            await asyncio.sleep(60)