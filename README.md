# Enterprise AI Agent

A production-grade AI agent demonstrating enterprise capabilities in Retrieval-Augmented Generation (RAG), tool usage, and autonomous reasoning. Built to showcase modern AI engineering principles for internal productivity applications.

## Project Overview

This implementation delivers an intelligent AI agent that addresses core enterprise challenges:

- **Policy Information Retrieval**: Answers employee questions about company policies using RAG architecture
- **Automated Task Execution**: Creates helpdesk tickets and executes actions through tool integration
- **Intent Recognition**: Automatically routes queries to appropriate subsystems using reasoning capabilities
- **Production Readiness**: Containerized deployment with proper logging and error handling

## Architecture

The system follows a modular agent architecture:

```
User Input -> Agent Orchestrator -> Intent Recognition -> Tool Execution -> Response
                                         |
                      |------------------|------------------|
                      |                                      |
                  RAG System                          Ticket Creation
                      |                                      |
              Knowledge Base                           Action API
```

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

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/enterprise-ai-agent.git
cd enterprise-ai-agent
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

5. **Run the application**:
```bash
python run_app.py
```

## GitHub Codespaces

This project is configured for immediate development in GitHub Codespaces:

1. Click "Code" button in repository
2. Select "Codespaces" tab
3. Create new codespace
4. The environment automatically configures with all dependencies

## Usage Examples

### Policy Queries

```
"What is the expense policy for client meals?"
"How do I request vacation time?"
"What are the procedures for IT equipment requests?"
```

### Action Requests

```
"My laptop is broken and needs replacement"
"I need software license approval for project work"
"Request access to the internal database"
```

## Project Structure

```
enterprise-ai-agent/
├── src/
│   ├── agent/
│   │   └── orchestrator.py      # Core agent logic
│   ├── tools/
│   │   ├── rag_tool.py          # Knowledge base queries
│   │   └── ticket_tool.py       # Helpdesk integration
│   └── main.py                  # Streamlit application
├── data/
│   └── policies/                # Sample policy documents
├── tests/                       # Test suites
├── deployment/
│   └── Dockerfile              # Container configuration
└── docs/                       # Architecture documentation
```

## Key Features Demonstrated

### Agentic AI Patterns

- Tool usage and function calling
- Intent recognition and routing
- Chain-of-thought reasoning
- Memory and context management

### Engineering Excellence

- Modular, extensible architecture
- Comprehensive error handling
- Application logging and monitoring
- Containerized deployment
- API-first design

### Production Considerations

- Environment configuration management
- Dependency isolation
- Code quality and testing frameworks
- Documentation and maintainability

## Development

### Running Tests

```bash
pytest tests/
```

### Building Docker Image

```bash
docker build -t enterprise-ai-agent -f deployment/Dockerfile .
```

### API Development

```bash
uvicorn src.api.main:app --reload --port 8000
```

## Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY`: OpenAI API key for LLM access
- `LOG_LEVEL`: Application logging level
- `VECTOR_DB_PATH`: Path for vector database storage

## Contributing

This project follows standard software engineering practices:

- Feature development in separate branches
- Pull request reviews required
- Comprehensive testing before merge
- Documentation updates for new features

## License

MIT License - see LICENSE file for details.
