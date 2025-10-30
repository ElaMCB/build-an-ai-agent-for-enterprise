"""RAG Tool for policy information retrieval (Windows-friendly, no heavy deps)."""

import os
from typing import List, Tuple
import numpy as np
from src.utils.llm_config import get_embeddings, get_chat_llm


class RAGTool:
    """Tool for querying policy documents using RAG."""
    
    def __init__(self, vector_store_path: str = "./data/vector_db"):
        self.vector_store_path = vector_store_path
        self.embeddings = get_embeddings()
        self.texts: List[str] = []
        self.metadatas: List[dict] = []
        self.doc_vectors: np.ndarray | None = None
        
    def initialize_vector_store(self, documents_path: str = "./data/policies"):
        """Initialize the vector store with policy documents (manual loader/splitter)."""
        texts, metadatas = self._load_and_chunk_documents(documents_path)
        if not texts:
            raise ValueError(f"No documents found in {documents_path}")

        # Build in-memory TF-IDF matrix (no FAISS/torch/onnx)
        self.texts = texts
        self.metadatas = metadatas
        vectors = self.embeddings.embed_documents(texts)
        self.doc_vectors = np.asarray(vectors, dtype=np.float32)

    def _load_and_chunk_documents(self, documents_path: str) -> Tuple[List[str], List[dict]]:
        """Load .txt files and chunk them into overlapping segments."""
        def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
            chunks = []
            start = 0
            n = len(text)
            while start < n:
                end = min(start + chunk_size, n)
                chunks.append(text[start:end])
                if end == n:
                    break
                start = max(end - overlap, 0)
            return chunks

        texts: List[str] = []
        metadatas: List[dict] = []
        for filename in os.listdir(documents_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(documents_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for chunk in chunk_text(content):
                        texts.append(chunk)
                        metadatas.append({"source": file_path})
                except Exception:
                    continue
        return texts, metadatas
    
    def query(self, question: str) -> dict:
        """Query the knowledge base without langchain.chains dependency."""
        # Ensure index
        if self.doc_vectors is None or len(self.texts) == 0:
            self.initialize_vector_store()

        # Retrieve relevant documents using cosine similarity
        qvec = np.asarray(self.embeddings.embed_query(question), dtype=np.float32)
        doc_mat = self.doc_vectors  # shape: (n_docs, dim)
        # Cosine similarity = (A·B) / (||A|| ||B||)
        doc_norms = np.linalg.norm(doc_mat, axis=1) + 1e-8
        qnorm = np.linalg.norm(qvec) + 1e-8
        sims = (doc_mat @ qvec) / (doc_norms * qnorm)
        top_k = int(min(3, sims.shape[0]))
        top_idx = np.argsort(-sims)[:top_k]
        context = "\n\n".join(self.texts[i] for i in top_idx)

        # Build prompt and call LLM directly
        prompt_text = (
            "You are a helpful assistant that answers questions about company policies.\n"
            "Use the following context to answer the question. If you don't know, say you don't know.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )
        llm = get_chat_llm(model="gpt-4o-mini", temperature=0)
        response = llm.invoke(prompt_text)
        answer = getattr(response, "content", None) or str(response)

        return {
            "answer": answer,
            "sources": [self.metadatas[i].get("source", "Unknown") for i in top_idx],
        }
    
    def get_tool_description(self) -> str:
        """Return tool description for agent."""
        return """Use this tool to answer questions about company policies, including:
        - Expense policies and reimbursement procedures
        - Vacation and time off requests
        - IT equipment and software requests
        - Access requests and procedures
        Search the knowledge base of policy documents."""
    
    def get_tool_name(self) -> str:
        """Return tool name."""
        return "policy_query"

