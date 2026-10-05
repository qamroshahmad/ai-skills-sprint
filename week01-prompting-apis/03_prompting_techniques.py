import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(system_prompt, user_prompt):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

# --- PART 1: Zero-shot vs Few-shot classification ---
print("##### PART 1: Zero-shot vs Few-shot #####\n")

tricky_review = "The battery life is incredible but it heats up like a stove and the screen flickers randomly."

zero_shot = ask(
    "Classify the sentiment as Positive, Negative, or Mixed. Reply with one word only.",
    tricky_review
)
print("ZERO-SHOT:", zero_shot)

few_shot_prompt = """Classify the sentiment as Positive, Negative, or Mixed. Reply with one word only.

Example 1: "Great price but arrived broken." -> Mixed
Example 2: "Absolutely love it, works perfectly." -> Positive
Example 3: "Stopped working after one day, total waste of money." -> Negative

Now classify:"""

few_shot = ask(few_shot_prompt, tricky_review)
print("FEW-SHOT:", few_shot)
print()

# --- PART 2: Chain-of-thought ---
print("##### PART 2: Chain-of-Thought #####\n")

math_problem = "A store had 85 apples. They sold 37 in the morning and 19 in the afternoon, then received a delivery of 50 more. How many apples does the store have now?"

direct = ask(None, math_problem + " Reply with only the final number.")
print("DIRECT ANSWER:", direct)

cot = ask(None, math_problem + " Think step by step, showing your work, before giving the final answer.")
print("CHAIN-OF-THOUGHT:\n", cot)
print()

# --- PART 3: Structured JSON output ---
print("##### PART 3: Structured JSON Output #####\n")

json_prompt = """Extract the person's name, age, and city from this text.
Return ONLY valid JSON in this exact format, nothing else, no markdown fences:
{"name": "...", "age": ..., "city": "..."}

Text: "Hi, I'm Maria, I'm 29 years old and I live in Lisbon."""

json_output = ask(None, json_prompt)
print("RAW OUTPUT:", json_output)

try:
    parsed = json.loads(json_output)
    print("PARSED SUCCESSFULLY:", parsed)
    print("Name:", parsed["name"], "| Age:", parsed["age"], "| City:", parsed["city"])
except json.JSONDecodeError as e:
    print("JSON PARSING FAILED:", e)