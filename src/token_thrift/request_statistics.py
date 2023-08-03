from .dto import PendingRequest, CompletedRequest

class RequestStatistics:
    def __init__(self):
        self.total_estimated_cost = 0
        self.total_actual_cost = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.initial_budget = 0
        self.estimated_remaining_budget = 0
        self.actual_remaining_budget = 0

    def add_pending_request(self, planned_request: PendingRequest):
        self.total_estimated_cost += planned_request.estimated_cost
        self.total_prompt_tokens += planned_request.token_count
        self.estimated_remaining_budget = (
            self.initial_budget - self.total_estimated_cost
        )

    def add_completed_request(self, completed_request: CompletedRequest):
        self.total_actual_cost += completed_request.actual_cost
        self.total_completion_tokens += completed_request.completion_tokens
        self.actual_remaining_budget = self.initial_budget - self.total_actual_cost

    def set_initial_budget(self, budget: float):
        self.initial_budget = budget
        self.estimated_remaining_budget = budget
        self.actual_remaining_budget = budget

    def __str__(self):
        def format_currency(amount):
            if amount < 0.01:
                return "<1c"
            else:
                return "$" + str(round(amount, 2))

        stats = [
            f"Initial Budget: {format_currency(self.initial_budget)}",
            f"Total Estimated Cost: {format_currency(self.total_estimated_cost)}",
            f"Total Actual Cost: {format_currency(self.total_actual_cost)}",
            f"Total Prompt Tokens: {self.total_prompt_tokens}",
            f"Total Completion Tokens: {self.total_completion_tokens}",
            f"Estimated Remaining Budget: {format_currency(self.estimated_remaining_budget)}",
            f"Actual Remaining Budget: {format_currency(self.actual_remaining_budget)}",
        ]
        return "\n".join(stats)
