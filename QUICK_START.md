# Quick Start - Test the Application

## Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install individually if needed:
```bash
pip install langchain langchain-openai langchain-community chromadb streamlit fastapi uvicorn python-dotenv pydantic openai tiktoken Pillow
```

**Note**: If you're using a virtual environment (recommended), activate it first:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

## Step 2: Create .env File

Create a `.env` file in the root directory with your API key (OpenAI or DeepSeek):

**Option 1: Using OpenAI**
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option 2: Using DeepSeek (Recommended - Free tier available)**
```env
DEEPSEEK_API_KEY=sk-your-actual-deepseek-key-here
```

**To get an API key:**

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in the `.env` file

**DeepSeek:**
1. Go to https://platform.deepseek.com/api_keys
2. Sign in or create an account
3. Create a new API key
4. Copy the key and paste it in the `.env` file

**Note:** The application automatically detects which provider to use based on which API key is set. You can also select the provider in the Streamlit UI.

## Step 3: Run the Application

```bash
python run_app.py
```

This will:
- Start the Streamlit server
- Open your browser automatically at `http://localhost:8501`

## Step 4: Initialize and Test

1. **In the Streamlit app sidebar:**
   - If your API key isn't in `.env`, enter it in the "OpenAI API Key" field
   - Click **"Initialize Agent"** button
   - Wait for "✅ Agent Ready" message

2. **Test Policy Queries (RAG):**
   - Type: `"What is the expense policy for client meals?"`
   - Should return policy information with sources

3. **Test Ticket Creation:**
   - Type: `"My laptop is broken and needs replacement"`
   - Should create a ticket with ID like "TKT-00001"

4. **View Created Tickets:**
   - Check `data/tickets.json` file to see all created tickets

## Troubleshooting

### "Module not found" errors
- Make sure dependencies are installed: `pip install -r requirements.txt`
- Check you're using the correct Python environment

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in the root directory
- Check the file has `OPENAI_API_KEY=sk-...` (no quotes around the key)

### Port already in use
- Streamlit uses port 8501 by default
- Close other Streamlit instances or specify a different port:
  ```bash
  streamlit run src/main.py --server.port 8502
  ```

### Vector database errors
- Delete `data/vector_db/` folder and re-initialize
- Make sure policy documents exist in `data/policies/`

## Expected Behavior

✅ **Policy Query**: Agent searches documents and returns accurate answers  
✅ **Ticket Creation**: Agent creates tickets with unique IDs  
✅ **Intent Recognition**: Automatically chooses the right tool  
✅ **Persistence**: Tickets saved to `data/tickets.json`  

## Next Steps

See `DEMO.md` for more detailed demo scenarios and `SETUP.md` for advanced configuration.

