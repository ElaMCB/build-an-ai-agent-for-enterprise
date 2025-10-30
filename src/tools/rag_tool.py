"""RAG Tool for policy information retrieval."""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from src.utils.llm_config import get_embeddings, get_chat_llm
import os
from typing import List


class RAGTool:
    """Tool for querying policy documents using RAG."""
    
    def __init__(self, vector_store_path: str = "./data/vector_db"):
        self.vector_store_path = vector_store_path
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.retriever = None
        
    def initialize_vector_store(self, documents_path: str = "./data/policies"):
        """Initialize the vector store with policy documents."""
        # Load documents
        documents = []
        for filename in os.listdir(documents_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(documents_path, filename)
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)
        
        if not documents:
            raise ValueError(f"No documents found in {documents_path}")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store (using FAISS for better Windows compatibility)
        self.vector_store = FAISS.from_documents(
            documents=splits,
            embedding=self.embeddings
        )
        # Save FAISS index
        self.vector_store.save_local(self.vector_store_path)
        # Create retriever
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        return len(splits)
    
    def query(self, question: str) -> dict:
        """Query the knowledge base without langchain.chains dependency."""
        # Ensure vector store / retriever
        if self.vector_store is None or self.retriever is None:
            # Load existing FAISS index if available; otherwise initialize
            if os.path.exists(self.vector_store_path) and os.listdir(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            else:
                self.initialize_vector_store()

        # Retrieve relevant documents
        docs = self.retriever.get_relevant_documents(question)
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

