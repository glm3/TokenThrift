from tiktoken import encoding_for_model
import requests
from .abstract_api_client import AbstractAPIClient
from ..dto import ApiResponse, PendingRequest


class OpenAIApiClient(AbstractAPIClient):
    TOKEN_COSTS = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        # Add other models with their respective costs here
    }

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.input_token_cost = self.TOKEN_COSTS[model]["input"]
        self.output_token_cost = self.TOKEN_COSTS[model]["output"]
        self.enc = encoding_for_model(model)

    def create_pending_request(self, prompt: str) -> PendingRequest:
        estimated_cost = self.estimate_dollar_cost(prompt)
        prompt_tokens = self.token_count(prompt)
        return PendingRequest(None, prompt, estimated_cost, prompt_tokens)

    def get_input_token_cost(self) -> float:
        return self.input_token_cost / 1000  # Adjusting cost per token

    def get_output_token_cost(self) -> float:
        return self.output_token_cost / 1000  # Adjusting cost per token

    def token_count(self, text: str) -> int:
        return len(self.enc.encode(text))

    def price_function(self, prompt_tokens, completion_tokens):
        return (
            self.get_input_token_cost() * prompt_tokens
            + self.get_output_token_cost() * completion_tokens
        )

    def send_request(self, pending_request: PendingRequest) -> ApiResponse:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": self.model,
            "max_tokens": 100,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": pending_request.prompt},
            ],
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        raw_result = response.json()

        return ApiResponse(
            self.extract_text(raw_result),
            raw_result["usage"]["completion_tokens"],
            self.compute_cost(raw_result),
        )

    def extract_text(self, response_data):
        return response_data["choices"][0]["message"]["content"]

    def compute_cost(self, response_data):
        prompt_tokens = response_data["usage"]["prompt_tokens"]
        completion_tokens = response_data["usage"]["completion_tokens"]
        return self.price_function(prompt_tokens, completion_tokens)

    def estimate_dollar_cost(self, prompt):
        prompt_token = self.token_count(prompt)
        completion_token_count = self.estimate_completion_token_count(prompt)
        return self.price_function(prompt_token, completion_token_count)

    def estimate_completion_token_count(self, prompt: str) -> int:
        return len(prompt)
