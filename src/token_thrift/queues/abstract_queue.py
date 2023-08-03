from abc import ABC, abstractmethod
from token_thrift.dto import PendingRequest

class AbstractQueue(ABC):
    @abstractmethod
    def enqueue(self, prompt, cost):
        pass

    @abstractmethod
    def dequeue(self) -> PendingRequest:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass
