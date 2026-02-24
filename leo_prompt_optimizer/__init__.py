"""
leo_prompt_optimizer
--------------------

A Python library to optimize LLM prompts from drafts, user inputs, and LLM outputs.
It uses open-source models (via Groq API or OpenAI) to refine prompts into structured, high-quality instructions.

See documentation: https://pypi.org/project/leo-prompt-optimizer/
"""

from leo_prompt_optimizer.optimizer import (
    LeoOptimizer, 
    OpenAIProvider,
    GroqProvider,
    AnthropicProvider,
    GeminiProvider,
    MistralProvider
)

from leo_prompt_optimizer.evaluator import (
    PromptEvaluator,
    BatchEvaluator
)

__all__ = [
    "LeoOptimizer",
    "OpenAIProvider",
    "GroqProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "MistralProvider",
    "PromptEvaluator",
    "BatchEvaluator"
]

__version__ = "1.0.7"
