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

- **Orchestrator**: Lightweight intent router that directs requests to RAG or ticket tool
- **RAG Module**: FAISS + TF‑IDF retrieval over policy documents with semantic-style search
- **Tool Framework**: Extensible system for API integrations and external actions
- **Knowledge Base**: Simple .txt ingestion with local chunking; file‑backed index

## Technical Stack

- **Language**: Python 3.9+
- **LLM Provider (default)**: DeepSeek (`deepseek-chat`) via HTTP API
- **LLM Provider (optional)**: OpenAI (`gpt-4o-mini`) via HTTP API
- **RAG Vector Store**: FAISS (in‑process, file‑backed)
- **Embeddings**: TF‑IDF (scikit‑learn) by default; OpenAI embeddings optional
- **Frontend**: Streamlit for user interface
- **API Layer**: FastAPI for service endpoints
- **Deployment**: Docker containerization

## Installation and Setup

### Prerequisites

- Python 3.9 or higher
- DeepSeek API key (recommended) or OpenAI API key
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
# Copy the example file
# On Windows (PowerShell):
Copy-Item .env.example .env

# On Linux/Mac:
cp .env.example .env

# Then edit .env and add your API key (DeepSeek preferred):
# DeepSeek (preferred): DEEPSEEK_API_KEY=sk-your-key
# OpenAI (optional):    OPENAI_API_KEY=sk-your-key
```

5. **Run the application**:
```bash
python run_app.py
```

Or directly with Streamlit:
```bash
streamlit run src/main.py
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
│   ├── policies/                # Sample policy documents
│   └── tickets.json             # Created tickets (generated)
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

## Demo Instructions

1. **Set up your environment**:
   - Create `.env` with your `DEEPSEEK_API_KEY` (or `OPENAI_API_KEY`)
   - Install dependencies: `pip install -r requirements.txt`

2. **Run the application**:
   ```bash
   python run_app.py
   ```

3. **Initialize the agent**:
   - In the Streamlit sidebar, choose provider (DeepSeek/OpenAI) and click "Initialize Agent"
   - This loads policy documents and builds/loads the FAISS index

4. **Try example queries**:
   - Policy questions: "What is the expense policy for client meals?"
   - Ticket creation: "My laptop is broken and needs replacement"
   - Access requests: "I need access to the internal database"

5. **View created tickets**:
   - Tickets are saved to `data/tickets.json`
   - The agent creates tickets with unique IDs and tracks them

## Contributing

This project follows standard software engineering practices:

- Feature development in separate branches
- Pull request reviews required
- Comprehensive testing before merge
- Documentation updates for new features

## License

MIT License - see LICENSE file for details.
