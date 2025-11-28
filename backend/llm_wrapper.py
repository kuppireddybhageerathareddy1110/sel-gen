import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Recommended active model (FAST + FREE)
MODEL_NAME = "llama-3.1-8b-instant"

def call_llm(prompt: str, system: str = None, temperature: float = 0.0) -> str:
    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=1000,
        temperature=temperature,
    )

    return response.choices[0].message.content
