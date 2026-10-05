import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

question = "Explain what a token is."

system_prompts = {
    "NO SYSTEM PROMPT": None,
    "VAGUE": "You are a helpful assistant.",
    "SPECIFIC": "You are a technical tutor teaching students about large language models (LLMs). When asked ambiguous terms, always interpret them in the context of AI/ML, not finance, crypto, or other domains. Keep answers to 2 sentences max."
}

for label, system_prompt in system_prompts.items():
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print(f"=== {label} ===")
    print(response.choices[0].message.content)
    print()