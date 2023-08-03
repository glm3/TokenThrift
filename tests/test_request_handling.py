import pytest
from token_thrift.token_thrift import TokenThrift


class TestTokenThriftRequestHandling:

    @classmethod
    def setup_class(cls):
        cls.api_key = "sample_api_key"
        cls.budget_in_dollars = 500

    def test_enqueue_request_valid(self):
        thrift = TokenThrift(self.api_key, self.budget_in_dollars)
        initial_budget = thrift.get_remaining_dollar_budget()

        prompt = "Translate the following text to French: 'Hello, world!'"
        thrift.enqueue_request(prompt)

        total_cost = thrift.convert_tokens_to_dollars(thrift.token_count(prompt), thrift.estimate_completion_token_count(prompt))
        assert thrift.get_remaining_dollar_budget() == initial_budget - total_cost

    def test_enqueue_request_exceeds_budget(self):
        thrift = TokenThrift(self.api_key, 0.01)  # very small budget

        prompt = "Translate the following text to French: 'Hello, world!'"
        with pytest.raises(Exception, match="Insufficient funds for this request"):
            thrift.enqueue_request(prompt)
