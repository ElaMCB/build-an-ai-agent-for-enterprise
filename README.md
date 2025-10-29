
### Core Components

- **Agent Orchestrator**: Central controller implementing ReAct pattern for reasoning and tool selection
- **RAG Module**: Vector-based retrieval from policy documents with semantic search
- **Tool Framework**: Extensible system for API integrations and external actions
- **Knowledge Base**: Document processing pipeline with chunking and embedding storage

## Technical Stack

- **Language**: Python 3.9+
- **AI Framework**: LangChain for agent orchestration
- **Vector Database**: ChromaDB for document retrieval
- **Frontend**: Streamlit for user interface
- **API Layer**: FastAPI for service endpoints
- **Deployment**: Docker containerization

## Installation and Setup

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/enterprise-ai-agent.git
cd enterprise-ai-agent

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
