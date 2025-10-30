"""LLM configuration utility for supporting multiple providers without heavy deps."""

import os
from typing import Optional, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI


def get_llm_provider() -> str:
    """Detect which LLM provider to use based on environment variables."""
    if os.getenv("DEEPSEEK_API_KEY"):
        return "deepseek"
    elif os.getenv("OPENAI_API_KEY"):
        return "openai"
    else:
        return "openai"  # default


class SimpleChatLLM:
    """Minimal chat interface with invoke(prompt_text) -> str using OpenAI-compatible SDK."""

    def __init__(
        self,
        model: str,
        temperature: float,
        base_url: Optional[str],
        api_key: str,
        provider: str,
    ):
        self.model = model
        self.temperature = temperature
        self.provider = provider
        # DeepSeek requires full URL with /v1
        if provider == "deepseek" and base_url:
            if not base_url.endswith("/v1"):
                base_url = base_url.rstrip("/") + "/v1"
        self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    def invoke(self, prompt_text: str):
        """Invoke the LLM with automatic model fallback for DeepSeek."""
        # Try available DeepSeek models in order if current fails
        models_to_try = [self.model]
        if self.provider == "deepseek":
            # Common DeepSeek model names
            fallbacks = ["deepseek-chat", "deepseek-reasoner"]
            models_to_try.extend([m for m in fallbacks if m != self.model])
        
        last_error = None
        for model_name in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt_text}],
                    temperature=self.temperature,
                )
                # Success - update model for next time
                if model_name != self.model:
                    self.model = model_name
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                # If it's not a model error, don't try other models
                if "model" not in error_str and "not exist" not in error_str:
                    raise
                continue
        
        # All models failed
        raise Exception(f"DeepSeek API error with all models: {last_error}")


def get_chat_llm(model: Optional[str] = None, temperature: float = 0):
    """Get a lightweight chat client for the selected provider (OpenAI/DeepSeek)."""
    provider = get_llm_provider()
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment")
        base_url = "https://api.deepseek.com/v1"
        # Default model - try common names
        default_model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        return SimpleChatLLM(default_model, temperature, base_url, api_key, provider="deepseek")
    else:
        api_key = os.getenv("OPENAI_API_KEY", "")
        default_model = model or "gpt-4o-mini"
        return SimpleChatLLM(default_model, temperature, None, api_key, provider="openai")


class SklearnTfidfEmbeddings:
    """Lightweight embeddings using scikit-learn TF-IDF (CPU-only, no native DLLs).
    Provides an interface compatible with LangChain's Embeddings (embed_documents/query).
    """

    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Fit vectorizer on the documents and produce dense vectors
        self.vectorizer = TfidfVectorizer(max_features=4096)
        matrix = self.vectorizer.fit_transform(texts)
        dense = matrix.astype(np.float32).toarray()
        return dense.tolist()

    def embed_query(self, text: str) -> List[float]:
        if self.vectorizer is None:
            # Cold start: fit on the query itself to avoid crashes; vector will be trivial
            self.vectorizer = TfidfVectorizer(max_features=4096)
            matrix = self.vectorizer.fit_transform([text])
        else:
            matrix = self.vectorizer.transform([text])
        dense = matrix.astype(np.float32).toarray()[0]
        return dense.tolist()


def get_embeddings():
    # Use pure scikit-learn TF-IDF embeddings to avoid torch/onnxruntime
    return SklearnTfidfEmbeddings()


def get_provider_name() -> str:
    """Get the current provider name."""
    return get_llm_provider().upper()
