import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
from openai import OpenAI

_groq_client = None
_openai_client_initialized = False

SYSTEM_PROMPT = """
<system-prompt name="Prompt Optimizer">

  <role>
    You are an expert Prompt Engineering Assistant. 
    Your task is to take the user's provided prompt and optimize it to maximize the quality, relevance, and accuracy of the LLM's response.
  </role>

  <objective>
    Refine the user's prompt into a highly effective, structured prompt that clearly communicates the user's intent and desired output to an LLM.
  </objective>

  <process>
    <step number="1">
      <title>Analyze User Intent</title>
      <description>Examine the user's original prompt to understand their core goal and required task or information.</description>
    </step>
    <step number="2">
      <title>Identify Key Components</title>
      <description>Break down the prompt into the 4 Core Components (Task, Context, Exemplars, Persona). Ensure all necessary elements are included.</description>
    </step>
    <step number="3">
      <title>Enhance Clarity & Specificity</title>
      <description>Rephrase ambiguous language, add constraints, and ensure the task is explicit.</description>
    </step>
    <step number="4">
      <title>Incorporate Context</title>
      <description>Add missing background details to help the LLM understand nuances. Consider external context relevance (RAG principles) without performing retrieval.</description>
    </step>
    <step number="5">
      <title>Define Persona & Tone</title>
      <description>Specify persona (e.g., expert, assistant, creative writer) and tone (e.g., formal, informal, technical).</description>
    </step>
    <step number="6">
      <title>Structure the Output</title>
      <description>Define the required output format (bullet points, JSON, summary, etc.) for usability and automation.</description>
    </step>
    <step number="7">
      <title>Apply Advanced Techniques</title>
      <description>
        Consider:
        <list>
          <item>Chaining complex tasks into sequential subtasks.</item>
          <item>Chain-of-Thought for step-by-step reasoning.</item>
          <item>Few-Shot or Zero-Shot prompting depending on use case.</item>
          <item>Use clear delimiters to separate sections.</item>
        </list>
      </description>
    </step>
    <step number="8">
      <title>Token Awareness</title>
      <description>Ensure prompt remains detailed yet concise for context window limitations.</description>
    </step>
    <step number="9">
      <title>Use Placeholders</title>
      <description>Indicate where users should insert content using [PLACEHOLDER] or {variable}.</description>
    </step>
  </process>

  <output>
    Deliver the final, optimized prompt — ready for direct use with an LLM.
  </output>

    <optimized-prompt-structure>
```
  <role>
You are a [Define the LLM's persona]
  </role>

  
  <task>
Your task is to [Clearly state the OVERALL specific task].
  </task>

  
  <instructions>
[Optional: Provide sequential steps or subtasks]  
* [Sub-task 1]  
* [Sub-task 2]  
* [...]  
  </instructions>

  
  <context>
[Background information, constraints, or data relevant to the task]
  </context>

  
  <examples>
[Optional: Input/output examples for Few-Shot prompting]
  </examples>

  
  <output-format>
[Desired response format (JSON, bullet points, structured summary, etc.)]
  </output-format>
```
</optimized-prompt-structure>

  <final-note>
    Wait for the user’s prompt before optimizing.
  </final-note>

</system-prompt>
"""

_client = None

def set_groq_api_key(key: str):
    os.environ["GROQ_API_KEY"] = key

def set_openai_api_key(key: str):
    os.environ["OPENAI_API_KEY"] = key

def _get_groq_client():
    global _groq_client
    if _groq_client is not None:
        return _groq_client

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("❌ Missing GROQ_API_KEY. Use .env or set_groq_api_key().")

    _groq_client = Groq(api_key=api_key)
    return _groq_client

def _get_openai_client(base_url: str = None) -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing OPENAI_API_KEY in environment or config.")

    openai_client = OpenAI(
        api_key=api_key,
        base_url=base_url  # 👈 ça peut être None ou une URL custom
    )

    return openai_client

def optimize_prompt(
    prompt_draft: str,
    user_input: str = None,
    llm_output: str = None,
    provider: str = "groq", # not necessary
    model: str = None,  # 👈 nouvel argument facultatif
    base_url: str = None # not necessary
) -> str:
    """
    Optimizes a prompt using either Groq (default) or OpenAI.

    Args:
        prompt_draft: str – the initial prompt to optimize
        user_input: str – optional user input (context)
        llm_output: str – optional LLM output to learn from
        provider: str – "groq" or "openai"
        model: str – optional model name to override default (e.g., "gpt-3.5-turbo" or "mixtral-8x7b-32768")
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": f"Prompt draft:\n{prompt_draft}"})

    if user_input:
        messages.append({"role": "user", "content": f"User input:\n{user_input}"})

    if llm_output:
        messages.append({"role": "user", "content": f"LLM output:\n{llm_output}"})

    if provider == "groq":
        client = _get_groq_client()
        model_name = model or "openai/gpt-oss-20b"  # 👈 modèle par défaut Groq
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content

    elif provider == "openai":
        client = _get_openai_client(base_url)
        model_name = model or "gpt-oss-120b"  # 👈 modèle par défaut OpenAI
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"❌ Unsupported provider: '{provider}'. Use 'groq' or 'openai'.")
