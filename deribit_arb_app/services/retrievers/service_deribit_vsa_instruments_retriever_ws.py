from decimal import Decimal
from typing import List

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.deribit_api.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument

    #################################################################
    # Retriever Retrieves Liquid Instruments Markets to Make up VSA #
    #################################################################

class ServiceDeribitVsaInstrumentsRetrieverWs():

    ## retrieved instruments list does not include the index instrumet (eg. btc_usd), this must be added at the execution service. 

    def __init__(self):        
        self.service_api_deribit = ServiceApiDeribit()

    async def async_setup(self, currency:str, kind:str):
        await TaskInstrumentsPull().run(currency=currency, kind=kind)
        self.store_subscribable_instruments = Stores.store_subscribable_instruments

    async def main(self, currency:str, kind:str, 
                         minimum_liquidity_threshold:int) -> List[ModelSubscribableInstrument]:
        
        await self.async_setup(currency=currency, kind=kind)
        store_subscribable_instruments = self.store_subscribable_instruments.get_subscribables()
        instruments = list(filter(lambda x: x.kind == kind and x.base_currency == currency, store_subscribable_instruments.values()))
        orderbook_summaries = await self.service_api_deribit.get_orderbook_summary_via_currency(currency=currency, kind=kind)
        liquid_instrument_names = [x.instrument_name for x in orderbook_summaries if \
                          x.volume_usd is not None and x.volume_usd > Decimal(str(minimum_liquidity_threshold))]
        result = [x for x in instruments if x.name in liquid_instrument_names]
        return result
        
        
        