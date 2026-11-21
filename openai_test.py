
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Find the .env file in the same folder as this script
env_path = Path(__file__).resolve().parent / ".env"

# Load the API key
load_dotenv(dotenv_path=env_path)

# Check that the key exists
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(f"API key not found. Check this file: {env_path}")

print("API key successfully loaded!")

# Initialise OpenAI client
client = OpenAI(api_key=api_key)

print("OpenAI client initialised successfully!")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the best football team in the world?"}
    ]
)

print("\nOpenAI response:")
print(response.choices[0].message.content)


