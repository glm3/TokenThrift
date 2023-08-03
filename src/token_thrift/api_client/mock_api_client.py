from tiktoken import encoding_for_model
from .abstract_api_client import AbstractAPIClient
from ..dto.pending_request import PendingRequest

class MockAPIClient(AbstractAPIClient):

    def __init__(self, mock_response):
        self.mock_response = mock_response
        self.input_token_cost = 0.0015  # Mocked cost per 1K tokens
        self.output_token_cost = 0.002  # Mocked cost per 1K tokens
        self.enc = encoding_for_model("gpt-3.5-turbo")

    def send_request(self, pending_request: PendingRequest):
        prompt_token = self.token_count(pending_request.prompt)
        completion_token_count = self.estimate_completion_token_count(self.mock_response)
        total_cost = self.convert_tokens_to_dollars(prompt_token, completion_token_count)
        return self.mock_response, total_cost

    def estimate_completion_token_count(self, prompt: str) -> int:
        # For simplicity, let's say the estimated completion tokens
        # are equal to the length of the prompt
        return len(prompt)

    def get_input_token_cost(self) -> float:
        return self.input_token_cost / 1000  # Adjusting cost per token

    def get_output_token_cost(self) -> float:
        return self.output_token_cost / 1000  # Adjusting cost per token

    def token_count(self, text: str) -> int:
        return len(self.enc.encode(text))

    def estimate_dollar_cost(self, prompt):
        prompt_token = self.token_count(prompt)
        completion_token_count = self.estimate_completion_token_count(prompt)
        return self.convert_tokens_to_dollars(prompt_token, completion_token_count)

    def convert_tokens_to_dollars(self, prompt_tokens: float, completion_tokens: float):
        return self.get_input_token_cost() * prompt_tokens + self.get_output_token_cost() * completion_tokens
