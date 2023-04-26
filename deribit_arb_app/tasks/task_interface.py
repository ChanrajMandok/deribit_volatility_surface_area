from abc import ABC, abstractmethod

class TaskInterface(ABC):

    @abstractmethod
    def run(self) -> None:
        """
        runs the task.
        """
        pass
