# Optimizer file
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

class BaseProvider(ABC):
    @abstractmethod
    def complete(self, messages: List[Dict[str, str]], model: str) -> str:
        pass

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        # Priority: 1. Manual Argument -> 2. Environment Variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ OpenAI API Key not found. Pass it to the provider or set OPENAI_API_KEY in .env")
            
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def complete(self, messages, model):
        response = self.client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content

class GroqProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found.")
            
        from groq import Groq  # <-- Use Groq here
        self.client = Groq(api_key=self.api_key)

    def complete(self, messages, model):
        response = self.client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY not found.")
            
        from anthropic import Anthropic
        self.client = Anthropic(api_key=self.api_key)

    def complete(self, messages, model):
        # Anthropic separates System prompt from Messages list
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        
        response = self.client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_msg,
            messages=user_msgs
        )
        return response.content[0].text

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found.")
        
        # Correct SDK initialization for 'google-genai'
        from google import genai
        self.client = genai.Client(api_key=self.api_key)

    def complete(self, messages, model):
        # Extract system instruction
        system_instruction = next((m["content"] for m in messages if m["role"] == "system"), None)
        
        # Format history (Gemini uses 'user' and 'model')
        contents = []
        for m in messages:
            if m["role"] == "system": continue
            role = "user" if m["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        
        # Generate content
        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config={'system_instruction': system_instruction} if system_instruction else None
        )
        return response.text

class LeoOptimizer:
    def __init__(self, provider: BaseProvider, default_model: str):
        self.provider = provider
        self.default_model = default_model
        self.env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'prompts')
        ))
        self.system_prompt = self._load_template('system_prompt_v0.2.j2')

    def _load_template(self, name: str) -> str:
        return self.env.get_template(name).render()

    def optimize(
        self,
        prompt_draft: str,
        user_input_example: Optional[str] = None,
        llm_output_example: Optional[str] = None,
        top_instruction: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Structured message building
        user_payload = [f"Prompt draft of the user:\n{prompt_draft}"]
        if user_input_example: user_payload.append(f"Example Input:\n{user_input_example}")
        if llm_output_example: user_payload.append(f"Example Output:\n{llm_output_example}")
        if top_instruction: user_payload.append(f"Instruction:\n{top_instruction}")

        messages.append({"role": "user", "content": "\n\n".join(user_payload)})
        
        return self.provider.complete(messages, model or self.default_model)