# Week 1 — Generative AI Prompting & API Calls

First week of an 8-week self-directed sprint on applied generative AI engineering. This week
covers calling LLM APIs directly (OpenAI + Microsoft Foundry), understanding tokens, writing
effective system prompts, prompting techniques (few-shot, chain-of-thought, structured JSON
output), and function/tool calling — including a working 3-tool assistant.

## Setup

1. `python -m venv venv`
2. Activate: `source venv/Scripts/activate` (Windows Git Bash) or `source venv/bin/activate` (Mac/Linux)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your own API keys
5. Run any script: `python 01_first_call.py`

## Scripts

| File | What it covers |
|---|---|
| `01_first_call.py` | First API calls to OpenAI + Microsoft Foundry, comparing token usage |
| `02_system_prompts.py` | How system prompt specificity changes model behavior |
| `03_prompting_techniques.py` | Zero-shot vs few-shot, chain-of-thought, structured JSON output |
| `04_function_calling.py` | Single-tool function calling round trip (weather lookup) |
| `05_multi_tool_assistant.py` | 3-tool assistant with correct tool discrimination |

---

## Day 2: System Prompts

I tested the same ambiguous question ("Explain what a token is.") through three different
system prompts to see how much control a system prompt actually gives you.

**No system prompt** and **a vague one** ("You are a helpful assistant.") produced nearly
identical results: a 5-paragraph essay covering crypto/blockchain, programming, authentication,
gaming, and physical tokens — defaulting to the most statistically common meaning of "token"
online (finance/crypto) rather than the AI/ML meaning I actually wanted.

A **specific** system prompt, by contrast, nailed it in one try:

> "You are a technical tutor teaching students about large language models (LLMs). When asked
> ambiguous terms, always interpret them in the context of AI/ML, not finance, crypto, or other
> domains. Keep answers to 2 sentences max."

Result: a single accurate, on-topic, 2-sentence answer with no hedging or irrelevant context.

**Key takeaway:** a vague system prompt barely changes model behavior at all — it has to
constrain something specific (a domain, a role, or a format) to actually work. "Be helpful"
constrains nothing, so the model just falls back to default behavior.

| System Prompt | Result |
|---|---|
| None | Generic 5-meaning essay, led with crypto |
| "You are a helpful assistant" | Nearly identical to no prompt at all |
| Domain + role + format constraints | Accurate, on-topic, 2 sentences exactly |

## Day 3: Prompting Techniques

**Few-shot vs zero-shot:** Both gave the same correct "Mixed" classification on a tricky
review. Takeaway: few-shot didn't add value here because the model already handled sentiment
correctly zero-shot — few-shot earns its keep on genuinely ambiguous cases or when you need
consistent output formatting across many calls, not as a blanket accuracy boost.

**Chain-of-thought:** Both direct and step-by-step prompting got the correct answer (79) on a
multi-step arithmetic problem. The model didn't need explicit reasoning for math this simple —
CoT likely matters more on harder, multi-step logic problems with room to go wrong.

**Structured JSON output:** Asking explicitly for "ONLY valid JSON, no markdown fences" worked
on the first try — `json.loads()` parsed it with no errors. This avoids a common failure mode
where models wrap JSON output in markdown code fences and silently break naive parsers.

## Day 5: Multi-Tool Assistant

Extended the single-tool loop from Day 4 into a 3-tool assistant (weather, currency
conversion, calculator) and tested whether the model correctly discriminates between them.

Results:
- Weather question -> correctly called get_weather
- Currency question -> correctly called convert_currency
- Math question -> correctly called calculate
- General knowledge question ("capital of France") -> correctly used NO tool, since it
  already knew the answer and didn't need one

Key insight: the model doesn't blindly reach for a tool whenever one is available — it
only requests a tool when it genuinely needs external data or computation it can't reliably
produce itself. This matters for real products: unnecessary tool calls cost extra tokens and
latency, so correct tool-selection behavior is a feature, not an accident.

Also added input sanitization to the calculate() tool — a character whitelist that blocks
anything outside basic arithmetic symbols before running eval(), since letting a model's
output flow unchecked into eval() is a real code-injection risk (the model's chosen
arguments shouldn't be blindly trusted as safe).

