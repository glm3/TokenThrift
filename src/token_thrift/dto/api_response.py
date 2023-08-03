class ApiResponse:
    def __init__(self, text, completion_tokens, cost):
        self.text = text
        self.completion_tokens = completion_tokens
        self.cost = cost
