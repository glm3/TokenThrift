import pytest
from token_thrift.token_thrift import TokenThrift
from token_thrift.api_client.mock_api_client import MockAPIClient
from unittest.mock import MagicMock
import math


class TestTokenThriftRequestProcessing:

    @classmethod
    def setup_class(cls):
        cls.api_key = "sample_api_key"
        cls.budget_in_dollars = 500
        cls.mock_response = "Mock response"
        cls.mock_api_client = MockAPIClient(cls.mock_response)

    def test_process_requests_sequentially(self):
        thrift = TokenThrift(
            self.api_key, self.budget_in_dollars, api_client=self.mock_api_client)
        mock_callback = MagicMock()

        # enqueue some requests
        prompt1 = "Translate the following text to French: 'Hello, world!'"
        prompt2 = "Summarize the book 'To Kill a Mockingbird'"

        total_cost_1 = thrift.convert_tokens_to_dollars(
            thrift.token_count(prompt1), thrift.token_count(self.mock_response))

        total_cost_2 = thrift.convert_tokens_to_dollars(
            thrift.token_count(prompt2), thrift.token_count(self.mock_response))

        thrift.enqueue_request(prompt1)
        thrift.enqueue_request(prompt2)

        thrift.process_requests_sequentially(mock_callback)

        assert mock_callback.call_count == 2  # assert callback was called twice
        assert math.isclose(
            thrift.get_total_dollar_spent(),
            total_cost_1 + total_cost_2,
            rel_tol=1e-9
        )

    # def test_process_requests_concurrently(self):
    #     thrift = TokenThrift(
    #         self.api_key, self.budget_in_dollars, api_client=self.mock_api_client)

    #     # enqueue multiple requests
    #     for _ in range(3):
    #         prompt = "Translate the following text to French: 'Hello, world!'"
    #         estimated_tokens = thrift.estimate_token_count(prompt)
    #         thrift.enqueue_request(prompt, estimated_tokens)

    #     thrift.process_requests_concurrently()

    #     # total tokens spent should be 3 times the estimated tokens per request
    #     assert thrift.get_total_token_spent() == 3 * estimated_tokens
