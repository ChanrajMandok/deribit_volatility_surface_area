from deribit_arb_app.tasks.task_interface import TaskInterface
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

    ############################################################################################
    # Task utilised in Testing to Populate Store to allow retrieval of ModelInstrument Objects #
    ############################################################################################

class TaskInstrumentPull(TaskInterface):

    def __init__(self) -> None:
        self.api_deribit = ServiceApiDeribit()
        super().__init__()

    async def run(self):
        await self.api_deribit.get_instruments(currency='BTC', kind='future')
        await self.api_deribit.get_instruments(currency='BTC', kind='option')