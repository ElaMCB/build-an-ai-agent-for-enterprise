# Demo Guide: Enterprise AI Agent

This guide will walk you through demonstrating the Enterprise AI Agent capabilities.

## Prerequisites

1. Python 3.9+ installed
2. OpenAI API key (get one at https://platform.openai.com/api-keys)
3. All dependencies installed (`pip install -r requirements.txt`)

## Quick Demo Steps

### 1. Initial Setup (One-time)

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and add your OPENAI_API_KEY
```

### 2. Launch the Application

```bash
python run_app.py
```

This will open Streamlit in your browser (usually at `http://localhost:8501`).

### 3. Initialize the Agent

1. In the Streamlit sidebar, enter your OpenAI API key (if not in .env)
2. Click **"Initialize Agent"** button
3. Wait for the confirmation message: "✅ Agent Ready"
4. You should see a message about document chunks being loaded

### 4. Demo Scenarios

#### Scenario 1: Policy Information Retrieval (RAG)

**Query**: "What is the expense policy for client meals?"

**Expected Behavior**:
- Agent uses the `policy_query` tool
- Searches the knowledge base (ChromaDB vector store)
- Returns specific information from expense_policy.txt
- Shows source documents

**Follow-up queries**:
- "How do I request vacation time?"
- "What are the procedures for IT equipment requests?"
- "What's the reimbursement limit for travel meals?"

**What to Highlight**:
- ✅ RAG architecture working
- ✅ Semantic search finding relevant policy sections
- ✅ Source attribution showing which documents were used

#### Scenario 2: Helpdesk Ticket Creation

**Query**: "My laptop is broken and needs replacement"

**Expected Behavior**:
- Agent recognizes this as a ticket creation request
- Uses the `create_ticket` tool
- Creates a ticket with:
  - Unique ticket ID (TKT-00001, TKT-00002, etc.)
  - Subject extracted from the request
  - Description
  - Category: "it" or "equipment"
  - Status: "open"
- Returns ticket confirmation with ID

**Follow-up queries**:
- "I need software license approval for project work"
- "Request access to the internal database"
- "I need a new monitor for my workstation"

**What to Highlight**:
- ✅ Intent recognition (differentiating between questions vs. actions)
- ✅ Tool usage and function calling
- ✅ Ticket persistence (check `data/tickets.json`)

#### Scenario 3: Complex Multi-Step Reasoning

**Query**: "I'm going on a business trip next week. What's the policy for expenses?"

**Expected Behavior**:
- Agent uses `policy_query` to find travel expense information
- Synthesizes information from multiple policy sections
- Provides comprehensive answer about travel policies

**Query**: "How do I get approval for a software license over $500?"

**Expected Behavior**:
- Agent queries policies about software licenses
- Provides step-by-step approval process
- May suggest creating a ticket if appropriate

**What to Highlight**:
- ✅ Chain-of-thought reasoning
- ✅ Combining multiple information sources
- ✅ Contextual understanding

### 5. View Created Tickets

After creating tickets, you can view them:

```bash
# View tickets file
cat data/tickets.json  # Linux/Mac
type data\tickets.json  # Windows
```

Or open `data/tickets.json` in a text editor to see:
- All created tickets
- Ticket IDs, subjects, descriptions
- Status and timestamps

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created a `.env` file
- Add `OPENAI_API_KEY=your-key-here` to the file
- Or enter it in the Streamlit sidebar

### "Error loading documents"
- Check that `data/policies/` folder exists
- Ensure policy `.txt` files are present
- Check file permissions

### Agent returns errors
- Verify OpenAI API key is valid
- Check internet connection
- Review error messages in the Streamlit interface
- Check terminal/console for detailed logs

### "Module not found" errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one

## Recording a Demo

### For Video/Screenshots:

1. **Start Screen Recording** (before launching app)

2. **Show the Setup**:
   - Project structure
   - Policy documents in `data/policies/`
   - Configuration files

3. **Launch Application**:
   - Show `python run_app.py` command
   - Browser opening

4. **Initialize Agent**:
   - Click "Initialize Agent"
   - Show successful initialization

5. **Demonstrate RAG**:
   - Ask policy questions
   - Highlight source documents being retrieved
   - Show accurate answers

6. **Demonstrate Ticket Creation**:
   - Request ticket creation
   - Show ticket ID being generated
   - Open `data/tickets.json` to show persistence

7. **Show Complex Reasoning**:
   - Multi-step queries
   - Agent choosing correct tools
   - Combining information

### For GitHub/GIF Demo:

Create a quick demo script showing:
1. Policy query → Answer with sources
2. Ticket creation → Ticket ID confirmation
3. Complex query → Multi-tool usage

## Key Features to Highlight

✅ **RAG Implementation**: Vector-based semantic search  
✅ **Tool Integration**: Function calling for external actions  
✅ **Intent Recognition**: Automatically routes to correct tool  
✅ **Production Ready**: Error handling, logging, persistence  
✅ **Extensible**: Easy to add new tools and policies  

## Next Steps for Full Demo

- Add more policy documents
- Connect to real helpdesk API (instead of JSON file)
- Add authentication/user management
- Deploy with Docker
- Add monitoring and analytics

---

**Need Help?** Check the main README.md or SETUP.md for more details.

