"""Streamlit application for Enterprise AI Agent."""

import streamlit as st
import os
from dotenv import load_dotenv
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.orchestrator import AgentOrchestrator
from src.tools.rag_tool import RAGTool
from src.tools.ticket_tool import TicketTool

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enterprise AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.agent = None

@st.cache_resource
def initialize_agent():
    """Initialize the AI agent."""
    try:
        # Check for API key (OpenAI or DeepSeek)
        from src.utils.llm_config import get_llm_provider
        provider = get_llm_provider()
        if provider == "deepseek" and not os.getenv("DEEPSEEK_API_KEY"):
            return None, "DEEPSEEK_API_KEY not found. Please set it in your .env file."
        elif provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            return None, "OPENAI_API_KEY not found. Please set it in your .env file."
        
        # Initialize tools
        rag_tool = RAGTool()
        ticket_tool = TicketTool()
        
        # Initialize vector store
        try:
            rag_tool.initialize_vector_store()
            st.info("✅ Policy index initialized (FAISS + TF‑IDF)")
        except Exception as e:
            return None, f"Error loading documents: {str(e)}"
        
        # Initialize agent
        agent = AgentOrchestrator(rag_tool, ticket_tool)
        return agent, None
    except Exception as e:
        return None, f"Error initializing agent: {str(e)}"

def main():
    """Main application."""
    st.title("🤖 Enterprise AI Agent")
    st.markdown("Ask questions about policies or create helpdesk tickets")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection
        from src.utils.llm_config import get_llm_provider, get_provider_name
        provider_options = ["OpenAI", "DeepSeek"]
        default_provider = "DeepSeek" if get_llm_provider() == "deepseek" else "OpenAI"
        
        selected_provider = st.selectbox(
            "LLM Provider",
            provider_options,
            index=0 if default_provider == "OpenAI" else 1,
            help="Select your LLM provider"
        )
        
        # API Key input
        api_key_name = "DEEPSEEK_API_KEY" if selected_provider == "DeepSeek" else "OPENAI_API_KEY"
        api_key_label = f"{selected_provider} API Key"
        api_key = st.text_input(
            api_key_label,
            type="password",
            value=os.getenv(api_key_name, ""),
            help=f"Enter your {selected_provider} API key"
        )
        
        if api_key and api_key != os.getenv(api_key_name):
            # Clear the other provider's key
            if selected_provider == "DeepSeek":
                os.environ["DEEPSEEK_API_KEY"] = api_key
                if "OPENAI_API_KEY" in os.environ:
                    del os.environ["OPENAI_API_KEY"]
            else:
                os.environ["OPENAI_API_KEY"] = api_key
                if "DEEPSEEK_API_KEY" in os.environ:
                    del os.environ["DEEPSEEK_API_KEY"]
            # Clear cache to reinitialize
            st.cache_resource.clear()
            st.session_state.agent = None
            st.session_state.initialized = False
        
        st.divider()
        
        # Initialize button
        if st.button("Initialize Agent", type="primary"):
            with st.spinner("Initializing agent..."):
                agent, error = initialize_agent()
                if error:
                    st.error(error)
                else:
                    st.session_state.agent = agent
                    st.session_state.initialized = True
                    st.success("Agent initialized successfully!")
                    st.rerun()

        # Rebuild index
        if st.button("Rebuild Policy Index"):
            try:
                # Clear resource cache to force rebuild
                st.cache_resource.clear()
                if st.session_state.agent:
                    # Rebuild directly if agent exists
                    st.session_state.agent.rag_tool.initialize_vector_store()
                st.success("Rebuilt policy index successfully.")
            except Exception as e:
                st.error(f"Failed to rebuild index: {e}")
        
        # Status
        if st.session_state.initialized:
            provider_name = get_provider_name()
            st.success(f"✅ Agent Ready ({provider_name})")
        else:
            st.warning("⚠️ Agent Not Initialized")
        
        st.divider()
        st.markdown("### Example Queries")
        st.code('"What is the expense policy for client meals?"')
        st.code('"How do I request vacation time?"')
        st.code('"My laptop is broken and needs replacement"')
    
    # Main chat interface
    if not st.session_state.initialized:
        st.info("👈 Please initialize the agent using the sidebar to get started.")
        return
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question or request help..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent.process(prompt)
                    response = result["response"]
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()

