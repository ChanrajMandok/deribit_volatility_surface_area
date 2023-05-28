from deribit_arb_app.tasks.task_interface import TaskInterface
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.services.deribit_api.service_api_deribit import ServiceApiDeribit

    ############################################################################################
    # Task utilised in Testing to Populate Store to allow retrieval of ModelInstrument Objects #
    ############################################################################################

class TaskInstrumentsPull(TaskInterface):

    def __init__(self) -> None:
        self.api_deribit = ServiceApiDeribit()
        super().__init__()
        
    async def run(self , currency:str, kind: str = None):
        if not kind:
            await self.api_deribit.get_instruments(currency=currency, kind=EnumInstrumentKind.FUTURE.value)
            await self.api_deribit.get_instruments(currency=currency, kind=EnumInstrumentKind.OPTION.value)
        elif kind == EnumInstrumentKind.OPTION.value:
            await self.api_deribit.get_instruments(currency=currency, kind=EnumInstrumentKind.OPTION.value)
        elif kind == EnumInstrumentKind.FUTURE.value:
            await self.api_deribit.get_instruments(currency=currency, kind=EnumInstrumentKind.FUTURE.value)