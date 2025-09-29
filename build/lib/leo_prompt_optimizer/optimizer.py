import os
from dotenv import load_dotenv

from groq import Groq
from openai import OpenAI

load_dotenv()

# Global client state
_client = None
_provider = None  # "groq" or "openai"

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

  
  <user-input>
[User-provided content here: [PLACEHOLDER] or {variable}]
  </user-input>
```
</optimized-prompt-structure>

  <final-note>
    Wait for the user’s prompt before optimizing.
  </final-note>

</system-prompt>
"""

# 🔐 Optional key setup
def set_groq_api_key(key: str):
    os.environ["GROQ_API_KEY"] = key

def set_openai_api_key(key: str):
    os.environ["OPENAI_API_KEY"] = key

# 🔧 Set a client once
def set_client(provider: str, base_url: str = None):
    global _client, _provider

    provider = provider.lower()
    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("❌ Missing GROQ_API_KEY.")
        _client = Groq(api_key=api_key)
        _provider = "groq"

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ Missing OPENAI_API_KEY.")
        _client = OpenAI(api_key=api_key, base_url=base_url)
        _provider = "openai"

    else:
        raise ValueError(f"❌ Unsupported provider: {provider}. Use 'groq' or 'openai'.")

# 🚀 Main optimizer function
def optimize_prompt(
    prompt_draft: str,
    user_input_example: str = None,
    llm_output_example: str = None,
    top_instruction: str = None,
    model: str = None,
) -> str:
    """
    Optimizes a prompt using the preconfigured client.
    Call `set_client()` once before using this.

    Args:
        prompt_draft: str – the initial prompt to optimize
        user_input_example: str – optional user input example
        llm_output_example: str – optional LLM output example
        top_instruction: str - optional extra context and specific instruction
        model: str – model override (default depends on provider)
    """
    global _client, _provider

    if _client is None or _provider is None:
        raise RuntimeError("❌ No client set. Use set_client('groq') or set_client('openai') first.")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    messages.append({"role": "user", "content": f"Prompt draft of the user:\n{prompt_draft}"})

    if user_input_example:
        messages.append({"role": "user", "content": f"Example of User input:\n{user_input_example}"})

    if llm_output_example:
        messages.append({"role": "user", "content": f"Example of Output:\n{llm_output_example}"})

    if top_instruction:
        messages.append({"role": "user", "content": f"Specific extra context provided by the user:\n{top_instruction}"})

    default_model = "openai/gpt-oss-20b" if _provider == "groq" else "gpt-oss-120b"
    model_name = model or default_model

    response = _client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    return response.choices[0].message.content
