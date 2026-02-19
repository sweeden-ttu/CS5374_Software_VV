"""LangSmith Prompt Retrieval Demo.

This script demonstrates how to use the .env file to set environment variables
and pull a prompt from LangSmith.

Usage:
    1. Create a LangSmith API key at https://smith.langchain.com/settings
    2. Update the .env file with your API keys, OR set them in system environment
    3. Run: python langsmith_prompt_demo.py
"""

from dotenv import load_dotenv
from langsmith import Client
import os

# First, load .env file (but don't override existing system env vars)
# This allows system environment variables to take precedence
load_dotenv()

# Get API keys - check system env first, then fall back to .env file values
# This ensures we use real API keys from system env if available
system_langsmith_key = os.environ.get("LANGSMITH_API_KEY")
system_openai_key = os.environ.get("OPENAI_API_KEY")

# Also get values directly from .env (bypassing system env check)
from dotenv import dotenv_values
env_values = dotenv_values(".env")
env_langsmith_key = env_values.get("LANGSMITH_API_KEY")
env_openai_key = env_values.get("OPENAI_API_KEY")

# Use system env if available, otherwise use .env file
# But only use .env values if they're not placeholder values
LANGSMITH_API_KEY = system_langsmith_key if system_langsmith_key and system_langsmith_key != "lsv2_pt_your_key_here" else env_langsmith_key
OPENAI_API_KEY = system_openai_key if system_openai_key and system_openai_key != "sk-proj-your_key_here" else env_openai_key

print(f"LANGSMITH_API_KEY: {LANGSMITH_API_KEY[:20] if LANGSMITH_API_KEY else 'None'}...")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY[:20] if OPENAI_API_KEY else 'None'}...")

# Check if API keys are properly set (allow both .env and system env values)
# Only fail if the key is completely missing (None) or has placeholder values
if LANGSMITH_API_KEY is None or LANGSMITH_API_KEY == "lsv2_pt_your_key_here":
    print("\nERROR: Please set your LangSmith API key")
    print("  - Option 1: Set LANGSMITH_API_KEY in system environment")
    print("  - Option 2: Update the .env file with your real API key")
    print("  - Get your API key from: https://smith.langchain.com/settings")
    exit(1)

if OPENAI_API_KEY is None or OPENAI_API_KEY == "sk-proj-your_key_here":
    print("\nERROR: Please set your OpenAI API key")
    print("  - Option 1: Set OPENAI_API_KEY in system environment")
    print("  - Option 2: Update the .env file with your real API key")
    exit(1)

# Set the API key in environment for langsmith
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize the LangSmith client
client = Client()

# Pull the prompt from LangSmith
# Note: "orchestrate-a-dispatch" is a hypothetical prompt name
# You may need to use an actual prompt name from your LangSmith account
try:
    prompt = client.pull_prompt(
        "orchestrate-a-dispatch",
        include_model=True,
        secrets={"OPENAI_API_KEY": OPENAI_API_KEY}
    )
    print("\n" + "="*50)
    print("Successfully retrieved prompt from LangSmith!")
    print("="*50)
    print(f"Prompt: {prompt}")
except Exception as e:
    print(f"\nError pulling prompt: {e}")
    print("\nNote: The prompt 'orchestrate-a-dispatch' may not exist.")
    print("Available prompt names depend on your LangSmith account.")
    print("Check your LangSmith dashboard for available prompts.")
