from .queues import AbstractQueue, ListQueue
from .api_client import AbstractAPIClient, OpenAIApiClient
from .dto import CompletedRequest
from .request_statistics import RequestStatistics


class TokenThrift:
    def __init__(
        self,
        api_key: str,
        initial_budget: float,
        queue: AbstractQueue = None,
        api_client: AbstractAPIClient = None,
    ):
        if not api_key:
            raise ValueError("API Key must not be empty.")
        if initial_budget <= 0:
            raise ValueError("Budget must be positive.")

        self.queue = queue if queue is not None else ListQueue()
        self.request_statistics = RequestStatistics()
        self.request_statistics.set_initial_budget(initial_budget)
        self.api_client = api_client or OpenAIApiClient(api_key)

    def enqueue_request(self, prompt: str):
        pending_request = self.api_client.create_pending_request(prompt)
        if (
            pending_request.estimated_cost
            > self.request_statistics.estimated_remaining_budget
        ):
            raise Exception("Insufficient funds for this request")

        self.queue.enqueue(pending_request)
        self.request_statistics.add_pending_request(pending_request)

        print(f"Request enqueued: {prompt}")

    def process_requests_sequentially(self, callback):
        while not self.queue.is_empty():
            pending_request = self.queue.dequeue()
            api_response = self.api_client.send_request(pending_request)

            completed_request = CompletedRequest(pending_request, api_response)

            callback(completed_request)

            self.request_statistics.add_completed_request(completed_request)
