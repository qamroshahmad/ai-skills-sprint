import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Call 1: OpenAI directly ---
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain what a token is in one sentence."}]
)

print("=== OpenAI response ===")
print(response.choices[0].message.content)
print("Token usage:", response.usage)
print()

# --- Call 2: Microsoft Foundry (OpenAI-compatible endpoint) ---
foundry_client = OpenAI(
    api_key=os.getenv("FOUNDRY_API_KEY"),
    base_url=f"{os.getenv('FOUNDRY_ENDPOINT')}/openai/v1"
)

foundry_response = foundry_client.chat.completions.create(
    model="gpt-4-1-mini",
    messages=[{"role": "user", "content": "Explain what a token is in one sentence."}]
)

print("=== Foundry response ===")
print(foundry_response.choices[0].message.content)
print("Token usage:", foundry_response.usage)