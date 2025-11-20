from dotenv import load_dotenv
load_dotenv()

from leo_prompt_optimizer import (
    optimize_prompt,
    set_client,
    set_groq_api_key,
    set_openai_api_key,
)

# Optionally: set API key manually
# set_groq_api_key("[YOUR GROQ KEY]")
# or
# set_openai_api_key("[YOUR OPEN AI KEY]")

# Mandatory: configure the client
set_client(provider="groq")

# Example draft prompt
draft = """

"""

context = """
"""

# Optional: context
user_input = None
llm_output = None

# Optimize
optimized = optimize_prompt(
    prompt_draft=draft,
    top_instruction=context
)

print("\n✅ --- Optimized Prompt ---\n")
print(optimized)
