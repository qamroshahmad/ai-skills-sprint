import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Real functions ---
def get_weather(city):
    fake_data = {
        "hamilton": "18°C, partly cloudy",
        "toronto": "20°C, sunny",
        "lisbon": "24°C, clear skies"
    }
    return fake_data.get(city.lower(), "No data for that city")

def convert_currency(amount, from_currency, to_currency):
    fake_rates = {
        ("usd", "cad"): 1.38, ("cad", "usd"): 0.72,
        ("usd", "eur"): 0.92, ("eur", "usd"): 1.09
    }
    rate = fake_rates.get((from_currency.lower(), to_currency.lower()))
    if rate is None:
        return "Conversion rate not available"
    return f"{amount} {from_currency.upper()} = {amount * rate:.2f} {to_currency.upper()}"

def calculate(expression):
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "Invalid expression"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

available_functions = {
    "get_weather": get_weather,
    "convert_currency": convert_currency,
    "calculate": calculate
}

# --- Tool descriptions ---
tools = [
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "Get the current weather for a given city",
        "parameters": {"type": "object", "properties": {
            "city": {"type": "string", "description": "City name"}
        }, "required": ["city"]}
    }},
    {"type": "function", "function": {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another",
        "parameters": {"type": "object", "properties": {
            "amount": {"type": "number"},
            "from_currency": {"type": "string", "description": "e.g. USD"},
            "to_currency": {"type": "string", "description": "e.g. CAD"}
        }, "required": ["amount", "from_currency", "to_currency"]}
    }},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Evaluate a basic math expression",
        "parameters": {"type": "object", "properties": {
            "expression": {"type": "string", "description": "e.g. (45*3)+10"}
        }, "required": ["expression"]}
    }}
]

def ask_assistant(question):
    print(f"\n--- Question: {question} ---")
    messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )
    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"Model chose tool: {name} with args {args}")

        result = available_functions[name](**args)
        print(f"Real result: {result}")

        messages.append(message)
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        print("Final answer:", final.choices[0].message.content)
    else:
        print("No tool needed. Direct answer:", message.content)

# --- Test questions ---
ask_assistant("What's the weather like in Lisbon?")
ask_assistant("How much is 200 USD in CAD?")
ask_assistant("What's (45 * 3) + 10?")
ask_assistant("What's the capital of France?")  # should need NO tool