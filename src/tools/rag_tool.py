"""RAG Tool for policy information retrieval (no heavy deps)."""

from langchain_community.vectorstores import FAISS
from src.utils.llm_config import get_embeddings, get_chat_llm
import os
from typing import List, Tuple


class RAGTool:
    """Tool for querying policy documents using RAG."""
    
    def __init__(self, vector_store_path: str = "./data/vector_db"):
        self.vector_store_path = vector_store_path
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.retriever = None
        
    def initialize_vector_store(self, documents_path: str = "./data/policies"):
        """Initialize the vector store with policy documents (manual loader/splitter)."""
        texts, metadatas = self._load_and_chunk_documents(documents_path)
        if not texts:
            raise ValueError(f"No documents found in {documents_path}")

        # Create vector store (using FAISS for better Windows compatibility)
        self.vector_store = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )
        # Save FAISS index
        self.vector_store.save_local(self.vector_store_path)
        # Ready for similarity search
        self.retriever = None

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
        
        return len(splits)
    
    def query(self, question: str) -> dict:
        """Query the knowledge base without langchain.chains dependency."""
        # Ensure vector store
        if self.vector_store is None:
            # Load existing FAISS index if available; otherwise initialize
            if os.path.exists(self.vector_store_path) and os.listdir(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
            else:
                self.initialize_vector_store()

        # Retrieve relevant documents
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n\n".join(d.page_content for d in docs)

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
            "sources": [d.metadata.get("source", "Unknown") for d in docs],
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

