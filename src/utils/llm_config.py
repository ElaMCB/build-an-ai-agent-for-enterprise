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
    """Minimal chat interface with invoke(prompt_text) -> str using OpenAI SDK."""

    def __init__(self, model: str, temperature: float, base_url: Optional[str], api_key: str):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    def invoke(self, prompt_text: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


def get_chat_llm(model: Optional[str] = None, temperature: float = 0):
    """Get a lightweight chat client for the selected provider (OpenAI/DeepSeek)."""
    provider = get_llm_provider()
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        base_url = "https://api.deepseek.com/v1"
        default_model = model or "deepseek-chat"
        return SimpleChatLLM(default_model, temperature, base_url, api_key)
    else:
        api_key = os.getenv("OPENAI_API_KEY", "")
        default_model = model or "gpt-4o-mini"
        return SimpleChatLLM(default_model, temperature, None, api_key)


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

