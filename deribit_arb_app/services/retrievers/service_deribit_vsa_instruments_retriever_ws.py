from decimal import Decimal

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_api_deribit import \
                                                     ServiceApiDeribit
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull

    #################################################################
    # Retriever Retrieves Liquid Instruments Markets to Make up VSA #
    #################################################################

class ServiceDeribitVsaInstrumentsRetrieverWs():

    def __init__(self):        
        self.service_api_deribit = ServiceApiDeribit()
        self.store_subscribable_instruments = Stores.store_subscribable_instruments

    async def async_setup(self, currency:str, kind:str):
        await TaskInstrumentsPull().run(currency=currency, kind=kind)

    async def main(self, currency:str, kind:str, 
                         minimum_liquidity_threshold:int) -> list[ModelSubscribableInstrument]:
        
        store_subscribable_instruments = self.store_subscribable_instruments.get_subscribables()
        if not store_subscribable_instruments: 
            await self.async_setup(currency=currency, kind=kind)
        instruments = list(filter(lambda x: x.kind == kind and x.base_currency == currency, store_subscribable_instruments.values()))
        orderbook_summaries = await self.service_api_deribit.get_orderbook_summary_via_currency(currency=currency, kind=kind)
        liquid_instrument_names = [x.instrument_name for x in orderbook_summaries if \
                          x.volume_usd is not None and x.volume_usd > Decimal(str(minimum_liquidity_threshold))]
        result = [x for x in instruments if x.name in liquid_instrument_names]
        logger.info(f"{self.__class__.__name__}: Liquid Instruments Retrieved")
        return result