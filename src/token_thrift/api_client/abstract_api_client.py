from abc import ABC, abstractmethod
from ..queues.abstract_queue import PendingRequest
from ..dto import ApiResponse

class AbstractAPIClient(ABC):

    @abstractmethod
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def create_pending_request(self, prompt: str) -> PendingRequest:
        pass

    @abstractmethod
    def send_request(self, pending_request: PendingRequest) -> ApiResponse:
        pass

    @abstractmethod
    def estimate_completion_token_count(self, prompt: str) -> int:
        pass

    @abstractmethod
    def get_input_token_cost(self) -> float:
        pass

    @abstractmethod
    def get_output_token_cost(self) -> float:
        pass

    @abstractmethod
    def estimate_dollar_cost(self, prompt: str) -> float:
        pass
