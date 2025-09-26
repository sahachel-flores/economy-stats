from setuptools import setup, find_packages

setup(
    name="economy-stats",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "python-dotenv", 
        "openai",
        "sqlalchemy",
        "newsapi-python",
        "newspaper3k",
        "requests",
        "beautifulsoup4",
    ]
)
