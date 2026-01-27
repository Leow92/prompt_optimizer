import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from groq import Groq
from openai import OpenAI

load_dotenv()

# Global client state
_client = None
_provider = None  # "groq" or "openai"

# Load Jinja2 templates from the 'prompts' folder
env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'prompts')))

def load_system_prompt(template_name):
    template = env.get_template(template_name)
    return template.render()

SYSTEM_PROMPT_V01 = load_system_prompt('system_prompt_v0.1.j2')
SYSTEM_PROMPT_V02 = load_system_prompt('system_prompt_v0.2.j2')

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

    messages = [{"role": "system", "content": SYSTEM_PROMPT_V02}]
    
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
