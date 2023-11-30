from typing import Optional, TypeVar

M = TypeVar('M')

class StoreSingleValueInterface:

    def __init__(self):
        self.model_instance: Optional[M] = None


    def get(self) -> Optional[M]:
        return self.model_instance


    def set(self, model_instance: M) -> None:
        self.model_instance = model_instance


    def is_set(self) -> bool:
        return self.model_instance is not None
