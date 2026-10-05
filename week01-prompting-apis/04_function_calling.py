import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Piece 1: describe the tool (just a description, no logic) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. Hamilton"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# --- Piece 2: the real function (actual logic, model never sees this code) ---
def get_weather(city):
    fake_data = {
        "hamilton": "18°C, partly cloudy",
        "toronto": "20°C, sunny",
        "lisbon": "24°C, clear skies"
    }
    return fake_data.get(city.lower(), "No data for that city")

# --- Piece 3: send the question, offering the tool ---
messages = [{"role": "user", "content": "What's the weather in Hamilton?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

message = response.choices[0].message

# --- Piece 4: check if the model requested a tool call ---
if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    print("Model wants to call:", function_name, "with args:", function_args)

    # --- Piece 5: actually run it, send result back, get final answer ---
    result = get_weather(**function_args)
    print("Real result from our function:", result)

    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print("\nFinal answer:", final_response.choices[0].message.content)
else:
    print("Model answered directly, no tool needed:", message.content)