# TokenThrift Python Library
TokenThrift is a Python library for queue-based management of API requests to AI services like OpenAI. This can help manage and optimize the cost of using pay-per-use AI services by allowing users to specify a budget and manage requests within that budget.

## 🚀 Features
* 📨 Queue-based management of API requests.
* 💲 Cost estimation and management for each request.
* 🔧 Customizable request execution and processing.

## 📦 Installation
First clone the repository to your local machine:
```shell
git clone https://github.com/glm3/TokenThrift
cd TokenThrift
```

Then install the required dependencies:
```shell
pip install -r requirements.txt
```

## 🎯 Basic Usage
Here's a basic example of how to use the TokenThrift library.

```python
from token_thrift.token_thrift import TokenThrift

def print_idea(completed_request):
    print("============================================")
    print("Topic")
    print(f"{completed_request.prompt}")
    print("============================================")
    print("Generated Idea")
    print(f"{completed_request.completion}")
    print("============================================")
    print("Cost")
    print(f"${completed_request.actual_cost}")
    print("============================================")

def main():
    api_key = "your_openai_api_key"
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
        prompt = f"Generate an idea about {topic}."
        thrift.enqueue_request(prompt)

    thrift.process_requests_sequentially(print_idea)

    print(thrift.request_statistics)

if __name__ == "__main__":
    main()
```

In this example, the library is used to generate ideas for different topics within a given budget.

Note: Remember to replace "your_openai_api_key" with your actual OpenAI API key.

## 🤝 Contributing
We welcome contributions! Please submit PRs for any enhancements or bug fixes.

## ⚖️ License
This project is licensed under the MIT License.
