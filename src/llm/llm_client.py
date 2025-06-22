import os
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, provider=None):
        self.provider = provider
        self.client = None

        if os.getenv("OPENAI_API_KEY") and provider in [None, 'openai']:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.client = openai
            self.provider = "openai"

        elif os.getenv("GOOGLE_API_KEY") and provider in [None, 'gemini']:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.client = genai.GenerativeModel()
            self.provider = "gemini"

        elif os.getenv("GROQ_API_KEY") and provider in [None, 'groq']:
            from groq import Groq
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.provider = "groq"

        else:
            raise EnvironmentError("No supported LLM API keys found (OPENAI, GOOGLE, GROQ)")

    def chat(self, messages: List[dict], model: str = None) -> str:
        """
        Chat-style prompt
        messages: [{"role": "user", "content": "..."}, ...]
        """
        if self.provider == "openai":
            model = model or "gpt-4o"
            res = self.client.chat.completions.create(model=model, messages=messages)
            return res.choices[0].message.content.strip()

        elif self.provider == "gemini":
            chat = self.client.start_chat(history=[])
            parts = [m["content"] for m in messages if m["role"] == "user"]
            prompt = "\n\n".join(parts)
            res = chat.send_message(prompt)
            return res.text.strip()

        elif self.provider == "groq":
            model = model or "mixtral-8x7b-32768"
            res = self.client.chat.completions.create(model=model, messages=messages)
            return res.choices[0].message.content.strip()

        else:
            raise ValueError("Unsupported provider")

    def complete(self, prompt: str, model: str = None, max_tokens: int = 512) -> str:
        """
        Plain completion-style prompt
        """
        if self.provider == "openai":
            model = model or "gpt-3.5-turbo-instruct"
            res = self.client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            return res.choices[0].text.strip()

        elif self.provider == "gemini":
            res = self.client.generate_content(prompt)
            return res.text.strip()

        elif self.provider == "groq":
            model = model or "mixtral-8x7b-32768"
            res = self.client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            return res.choices[0].text.strip()

        else:
            raise ValueError("Unsupported provider")
