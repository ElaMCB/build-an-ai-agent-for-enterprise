"""LLM configuration utility for supporting multiple providers."""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Optional


def get_llm_provider() -> str:
    """Detect which LLM provider to use based on environment variables."""
    if os.getenv("DEEPSEEK_API_KEY"):
        return "deepseek"
    elif os.getenv("OPENAI_API_KEY"):
        return "openai"
    else:
        return "openai"  # default


def get_chat_llm(model: Optional[str] = None, temperature: float = 0):
    """Get a ChatOpenAI instance configured for the selected provider."""
    provider = get_llm_provider()
    
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        # DeepSeek API endpoint
        base_url = "https://api.deepseek.com/v1"
        # DeepSeek model names: deepseek-chat, deepseek-coder
        default_model = model or "deepseek-chat"
        
        return ChatOpenAI(
            model=default_model,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base=base_url
        )
    else:
        # OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        default_model = model or "gpt-4o-mini"
        
        return ChatOpenAI(
            model=default_model,
            temperature=temperature,
            openai_api_key=api_key
        )


def get_embeddings():
    """Get embeddings instance. 
    Note: For DeepSeek, we use OpenAI-compatible embeddings.
    The embeddings are for vector search and don't need to match the chat model provider."""
    # Check for OpenAI API key first (for embeddings)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return OpenAIEmbeddings(openai_api_key=openai_key)
    
    # If no OpenAI key, try using DeepSeek key (may not work for embeddings)
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key:
        # Try using DeepSeek key with OpenAI embeddings API
        # This may not work - user should have OpenAI key for embeddings
        return OpenAIEmbeddings(openai_api_key=deepseek_key)
    
    # Default fallback
    return OpenAIEmbeddings()


def get_provider_name() -> str:
    """Get the current provider name."""
    return get_llm_provider().upper()

