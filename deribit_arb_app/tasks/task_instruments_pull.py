from deribit_arb_app.services.api_deribit import ApiDeribit
from deribit_arb_app.tasks.task_interface import TaskInterface


class TaskInstrumentPull(TaskInterface):

    def __init__(self) -> None:
        self.api_deribit = ApiDeribit()
        super().__init__()

    def run(self):
        self.api_deribit.get_instruments(currency='BTC', kind='future')
        self.api_deribit.get_instruments(currency='BTC', kind='option')