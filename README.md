# 🧠 leo-prompt-optimizer
[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/Leow92/prompt_optimizer)
[![PyPI version](https://badge.fury.io/py/leo-prompt-optimizer.svg)](https://pypi.org/project/leo-prompt-optimizer/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/leo-prompt-optimizer?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/leo-prompt-optimizer)


**leo-prompt-optimizer** is a production-grade library and CLI tool that transforms raw prompt drafts into structured, high-performance instructions using a 9-step engineering framework.

Stop "vibes-based" prompting. Use a data-driven approach to optimize, evaluate, and benchmark your prompts across **OpenAI, Groq, Anthropic, and Gemini**.

---

## 🌟 Key Features

* ⚡ **Lightning Fast**: Optimized for high-throughput providers like Groq for near-instant iteration.
* 📊 **LLM-as-a-Judge**: Built-in G-Eval metrics, hallucination detection, and schema adherence checks.
* 🖥️ **Rich CLI**: Beautiful terminal reports with side-by-side diffs and performance tables.
* 🧩 **XML-Structured Output**: Automatically reformats prompts into `<role>`, `<task>`, and `<instructions>` blocks for better LLM steerability.

---

## 📦 Installation

```bash
pip install leo-prompt-optimizer

```

---

## 🖥️ CLI: The "Pro" Workflow

Optimize a prompt and immediately benchmark it against test cases to see if it actually performs better.

```bash
leo-prompt --prompt-file draft.txt \
           --provider-name groq \
           --tests tests.json \
           --model your-model-id

```

### What happens under the hood?

1. **Optimization**: Your draft is expanded into a structured "System Prompt."
2. **Execution**: Both the *Original* and *Optimized* prompts run against your `tests.json`.
3. **Evaluation**: A "Judge" model compares the outputs and generates a performance report.

---

## 🔧 Python API Usage

Perfect for integrating prompt optimization into your CI/CD pipelines or internal tools.

### 1. Initialize Provider

```python
from leo_prompt_optimizer import GroqProvider, LeoOptimizer, PromptEvaluator

# Automatically loads API keys from .env (GROQ_API_KEY, OPENAI_API_KEY, etc.)
provider = GroqProvider()
optimizer = LeoOptimizer(provider, default_model="your-optimizer-model-id")

```

### 2. Optimize & Evaluate

```python
draft = "Write a code review for this python function."

# 🚀 Step 1: Optimize
optimized = optimizer.optimize(draft)

# 📊 Step 2: Evaluate
evaluator = PromptEvaluator(provider, optimizer.env, judge_model="your-judge-model-id")
result = evaluator.evaluate(
    original_prompt=draft,
    optimized_prompt=optimized,
    test_input="def add(a, b): return a + b"
)

# The result object prints a beautiful ASCII dashboard automatically
print(result)

```

---

## 🧪 The Evaluation Framework

The library provides objective scores to replace subjective testing:

| Metric | Description |
| --- | --- |
| **G-Eval (1-5)** | A multi-dimensional score for coherence and instruction following. |
| **Token Efficiency** | Percentage of tokens saved (or added) for the structural improvement. |
| **Schema Adherence** | Pass/Fail check for structured outputs (JSON/Markdown). |
| **Hallucination Risk** | Detects if the model is fabricating facts not present in the input. |

---

## 🤖 Supported Providers

| Provider | Environment Variable |
| --- | --- |
| **Groq** | `GROQ_API_KEY` |
| **OpenAI** | `OPENAI_API_KEY` |
| **Anthropic** | `ANTHROPIC_API_KEY` |
| **Gemini** | `GOOGLE_API_KEY` |

---

## 📘 Optimized Format Example

Your raw drafts are transformed into high-signal instructions:

```xml
<role>You are a Senior Python Security Auditor...</role>
<task>Analyze the provided function for SQL injection vulnerabilities...</task>
<instructions>
1. Identify all string-formatting operations.
2. Check for missing parameterized queries...
</instructions>
<output-format>Return a JSON object with 'severity' and 'fix'.</output-format>

```

