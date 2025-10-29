# Setup Guide

## Environment Configuration

Create a `.env` file in the root directory with the following:

```env
OPENAI_API_KEY=your-openai-api-key-here
LOG_LEVEL=INFO
VECTOR_DB_PATH=./data/vector_db
```

### Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with your OpenAI API key

3. Run the application:
   ```bash
   python run_app.py
   ```

4. In the Streamlit app, click "Initialize Agent" in the sidebar

5. Start asking questions!

## Demo Script

Try these queries to demonstrate different capabilities:

### Policy Queries
- "What is the expense policy for client meals?"
- "How do I request vacation time?"
- "What are the procedures for IT equipment requests?"
- "What's the reimbursement limit for travel meals?"

### Ticket Creation
- "My laptop is broken and needs replacement"
- "I need software license approval for project work"
- "Request access to the internal database"
- "I need a new monitor for my workstation"

### Complex Queries
- "I'm going on a business trip next week. What's the policy for expenses?"
- "How do I get approval for a software license over $500?"

