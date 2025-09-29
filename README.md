# 🧠 leo-prompt-optimizer
[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/Leow92/prompt_optimizer)
[![PyPI version](https://badge.fury.io/py/leo-prompt-optimizer.svg)](https://pypi.org/project/leo-prompt-optimizer/)

**leo-prompt-optimizer** is a Python library that helps developers **optimize raw LLM prompts** into structured, high-performance instructions using real LLM intelligence.

It supports both **Groq (LLaMA, Mixtral, etc.)** and **OpenAI (GPT-3.5, GPT-4)** — making it fast, flexible, and production-ready.

---

## 🚀 Features

- 🛠️ Refines vague, messy, or unstructured prompts
- 🧠 Follows a 9-step prompt engineering framework
- 🧩 Supports contextual optimization (with user input & LLM output)
- 🔁 Works with both Groq **and** OpenAI
- ⚡ Blazing-fast open models via Groq
- 🔐 Secure API key management with `.env` or helper functions
- 🎛️ Lets users pick the model (`gpt-4`, `llama3-70b`, etc.)

---

## 📦 Installation

```bash
pip install leo-prompt-optimizer
```

---

## 🔧 Setup: API Keys & Client

You can provide API keys either via `.env` or programmatically, then **set the provider**.

### ✅ Option A: Use `.env` (recommended)

Create a `.env` file in your project root:

```env
GROQ_API_KEY=sk-your-groq-key
OPENAI_API_KEY=sk-your-openai-key
```

Then in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

### ✅ Option B: Set manually in code

```python
from leo_prompt_optimizer import set_groq_api_key, set_openai_api_key

set_groq_api_key("[YOUR GROQ KEY]")
set_openai_api_key("[YOUR OPENAI KEY]")
```

---

### ✅ Set your provider

Before calling `optimize_prompt`, set the backend provider:

```python
from leo_prompt_optimizer import set_client

# For Groq (default)
set_client(provider="groq")

# For OpenAI (with optional custom base URL)
set_client(provider="openai", base_url="https://openrouter.ai/v1")
```

---

## ✍️ Usage Example with key in .env

```python
from dotenv import load_dotenv
load_dotenv()

from leo_prompt_optimizer import (
    optimize_prompt,
    set_groq_api_key,
    set_openai_api_key,
    set_client
)

# Required: set backend provider
set_client(provider="groq")  # or "openai"
# or if you have a specific base_url : 
set_client(provider="openai", base_url="[YOUR BASE URL]") 

# Prompt example
optimized = optimize_prompt(
    prompt_draft="[YOUR PROMPT]",
    user_input_example="[POTENTIAL INPUT EXAMPLE]", # Optional
    llm_output_example="[POTENTIAL OUTPUT EXAMPLE]", # Optional
    top_instruction="[POTENTIAL EXTRA CONTEXT, SPECIFIC INSTRUCTION TO FOCUS ON FOR THE LLM]", # Optional
    model="[YOUR MODEL]",            # Optional: model choie based on your provider(e.g. "gpt-4", "llama3-70b", etc.)
)

print(optimized)
```

> 🧠 `user_input_example` and `llm_output_example` are optional but improve accuracy. 
> 💬 `top_instruction` is optional — it adds specific guidance to influence the optimization (e.g., tone, audience, format). 
>
> 🎛️ `model` is optional — defaults are:
>
> * `"openai/gpt-oss-20b"` for Groq
> * `"gpt-oss-120b"` for OpenAI

---

## 📘 Output Format

Optimized prompts follow a clear, modular structure:

```text
Role:
[Define the LLM's persona]

Task:
[Clearly state the specific objective]

Instructions:
* Step-by-step subtasks

Context:
[Any relevant background, constraints, domain]

Output Format:
[e.g., bullet list, JSON, summary]

User Input:
[Original user input or example]
```

---

## 🧪 Quick Test (Optional)

```bash
python3 test_import.py
```

Checks that:

* ✅ Import works
* ✅ API keys are found
* ✅ LLM returns a response

---

## 🧯 Common Errors & Fixes

| Error                  | Solution                                                                                                                   |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `Missing API key`      | Add key to `.env` or use `set_groq_api_key()` / `set_openai_api_key()`                                                     |
| `Client not set`       | Use `set_client("groq")` or `set_client("openai")` **before** calling `optimize_prompt()`                                  |
| `Invalid model` or 403 | Model may be deprecated or not available — try another, or check Groq’s [model list](https://console.groq.com/docs/models) |
| `ModuleNotFoundError`  | Check if `leo-prompt-optimizer` is installed in the correct virtual environment                                            |

---

## 💡 Why Use It?

Prompt quality is critical for any GenAI product.

**leo-prompt-optimizer** helps you:

✅ Make prompts explicit and modular
🚫 Reduce hallucinations
🔁 Improve consistency and reuse
🧱 Standardize prompt formats across your stack

---

