class PendingRequest:
    def __init__(self, id, prompt, estimated_cost, token_count):
        self.id = id
        self.prompt = prompt
        self.estimated_cost = estimated_cost
        self.token_count = token_count
