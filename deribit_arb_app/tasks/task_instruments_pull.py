from deribit_arb_app.tasks.task_interface import TaskInterface
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

class TaskInstrumentPull(TaskInterface):

    def __init__(self) -> None:
        self.api_deribit = ServiceApiDeribit()
        super().__init__()

    def run(self):
        self.api_deribit.get_instruments(currency='BTC', kind='future')
        self.api_deribit.get_instruments(currency='BTC', kind='option')