from typing import Optional, TypeVar

M = TypeVar('M')

class StoreDeribitInterface:

    def __init__(self):
        self.deribit_model_instance: Optional[M] = None

    def get(self) -> Optional[M]:
        return self.deribit_model_instance

    def set(self, deribit_model_instance: M) -> None:
        self.deribit_model_instance = deribit_model_instance

    def is_set(self) -> bool:
        return self.deribit_model_instance is not None
