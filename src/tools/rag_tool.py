"""RAG Tool for policy information retrieval."""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from typing import List


class RAGTool:
    """Tool for querying policy documents using RAG."""
    
    def __init__(self, vector_store_path: str = "./data/vector_db"):
        self.vector_store_path = vector_store_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.qa_chain = None
        
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
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.vector_store_path
        )
        
        # Create QA chain
        template = """You are a helpful assistant that answers questions about company policies.
        Use the following pieces of context to answer the question. If you don't know the answer,
        just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        return len(splits)
    
    def query(self, question: str) -> dict:
        """Query the knowledge base."""
        if not self.qa_chain:
            # Lazy initialization
            self.initialize_vector_store()
        
        result = self.qa_chain.invoke({"query": question})
        
        return {
            "answer": result["result"],
            "sources": [doc.metadata.get("source", "Unknown") for doc in result.get("source_documents", [])]
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

