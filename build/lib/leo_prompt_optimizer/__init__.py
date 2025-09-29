"""
leo_prompt_optimizer
--------------------

A Python library to optimize LLM prompts from drafts, user inputs, and LLM outputs.
It uses open-source models (via Groq API or OpenAI) to refine prompts into structured, high-quality instructions.

Main functions:
- optimize_prompt(prompt_draft, user_input=None, llm_output=None)
- set_client(provider="groq" or "openai", base_url=None)
- set_groq_api_key(key)
- set_openai_api_key(key)

See documentation: https://pypi.org/project/leo-prompt-optimizer/
"""

from .optimizer import (
    optimize_prompt,
    set_client,
    set_groq_api_key,
    set_openai_api_key,
)

__all__ = [
    "optimize_prompt",
    "set_client",
    "set_groq_api_key",
    "set_openai_api_key",
]

__version__ = "0.1.8"
