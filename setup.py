from setuptools import setup, find_packages

setup(
    name="token_thrift",
    version="0.1",
    description="A Python library for queue-based management of API requests to AI services like OpenAI.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author="glm3",
    url="https://github.com/yourusername/token_thrift",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,  # this will include non-python files like README, .env etc.
)
