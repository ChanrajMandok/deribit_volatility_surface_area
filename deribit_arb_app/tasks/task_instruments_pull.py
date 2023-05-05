from deribit_arb_app.tasks.task_interface import TaskInterface
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

    ############################################################################################
    # Task utilised in Testing to Populate Store to allow retrieval of ModelInstrument Objects #
    ############################################################################################

class TaskInstrumentsPull(TaskInterface):

    def __init__(self) -> None:
        self.api_deribit = ServiceApiDeribit()
        super().__init__()

    async def run(self , currency:str, kind :str = None):
        if not kind:
            await self.api_deribit.get_instruments(currency=currency, kind='future')
            await self.api_deribit.get_instruments(currency=currency, kind='option')
        elif kind == 'option':
            await self.api_deribit.get_instruments(currency=currency, kind='option')
        elif kind == 'future':
            await self.api_deribit.get_instruments(currency=currency, kind='future')