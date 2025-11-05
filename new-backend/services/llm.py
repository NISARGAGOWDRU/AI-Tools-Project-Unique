import os
from pydantic import SecretStr
from langchain_openai import ChatOpenAI

def make_llm():
    """
    Returns a LangChain Chat model that talks to LM Studio's OpenAI-compatible API.
    Env vars: 
      - OSS_BASE_URL: Base URL of the LM Studio OpenAI-compatible API
      - MODEL: Model name to use (e.g. "openai/gpt-oss-20b")
    """
    base_url = os.getenv("OSS_BASE_URL", "http://127.0.0.1:1234/v1")
    model = os.getenv("MODEL", "openai/gpt-oss-20b")
    api_key = os.getenv("OSS_API_KEY", "lm-studio")

    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=SecretStr(api_key) if api_key else None,
        temperature=0.2,
        timeout=120,
        max_tokens=800  # 🚀 NEW: Limit output to 800 tokens (~600 words)
    )