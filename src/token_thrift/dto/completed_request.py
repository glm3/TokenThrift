from .pending_request import PendingRequest
from .api_response import ApiResponse


class CompletedRequest:
    def __init__(self, pending_request: PendingRequest, api_response: ApiResponse):
        self.pending_request = pending_request
        self.api_response = api_response

    @property
    def prompt(self):
        return self.pending_request.prompt

    @property
    def completion(self):
        return self.api_response.text
    
    @property
    def prompt_tokens(self):
        return self.pending_request.token_count
    
    @property
    def completion_tokens(self):
        return self.api_response.completion_tokens
    
    @property
    def estimated_cost(self):
        return self.pending_request.estimated_cost
    
    @property
    def actual_cost(self):
        return self.api_response.cost
