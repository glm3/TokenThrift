import os
from dotenv import load_dotenv
from rich.console import Console
from token_thrift.token_thrift import TokenThrift

load_dotenv()

console = Console()

def print_idea(completed_request):
    console.print("============================================")
    console.print("Topic", style="bold underline")
    console.print(f"{completed_request.prompt}")
    console.print("============================================")
    console.print("Blog Post Idea", style="bold underline")
    console.print(f"{completed_request.completion}")
    console.print("============================================")
    console.print("Cost", style="bold underline")
    console.print(f"${completed_request.actual_cost}")
    console.print("============================================")


def main():
    api_key = os.environ['API_KEY']
    budget_in_dollars = 10

    thrift = TokenThrift(api_key, budget_in_dollars)

    topics = [
        "AI in healthcare",
        "Remote work",
        "Electric cars",
        "Dystopian future",
        "Space exploration",
        "Yoga and mental health"
    ]

    for topic in topics:
        prompt = f"Generate a blog post idea about {topic}."
        thrift.enqueue_request(prompt)

    thrift.process_requests_sequentially(print_idea)

    print(thrift.request_statistics)


if __name__ == "__main__":
    main()


