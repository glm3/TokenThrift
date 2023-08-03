import pytest
from token_thrift.token_thrift import TokenThrift


class TestTokenThriftBudgeting:

    @classmethod
    def setup_class(cls):
        cls.api_key = 'test_api_key'
        cls.token_thrift = TokenThrift('test_api_key', 100.0)

    def test_remaining_budget_after_enqueue(self):
        prompt = "Translate the following English text to French: '{}'"
        text = "Hello, world!"
        formatted_prompt = prompt.format(text)

        self.token_thrift.enqueue_request(formatted_prompt)

        assert self.token_thrift.get_remaining_dollar_budget() < 100.0
        assert self.token_thrift.get_remaining_dollar_budget() >= 0

    def test_budget_exceeded(self):
        thrift = TokenThrift(self.api_key, 0.01)  # very small budget

        # construct a prompt that will definitely exceed the budget
        long_prompt = "Translate the following text to French: " + "Hello, world! " * 1000

        # now try to enqueue the request, expecting an exception
        with pytest.raises(Exception, match="Insufficient funds for this request"):
            thrift.enqueue_request(long_prompt)
