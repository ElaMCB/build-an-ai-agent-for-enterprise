# Deploy to Streamlit Cloud

## Quick Setup

### 1. Main File Path
When Streamlit Cloud asks for the main file path, use:
```
src/main.py
```

### 2. Repository Requirements
- ✅ `requirements.txt` in root (already exists)
- ✅ `src/main.py` exists (main Streamlit app)
- ✅ Policy documents in `data/policies/` (needed for RAG)

### 3. Environment Variables (Secrets)
In Streamlit Cloud settings, add these secrets:

**Required (choose one):**
- `DEEPSEEK_API_KEY` = `sk-...` (your DeepSeek API key)
- OR `OPENAI_API_KEY` = `sk-...` (if using OpenAI)

**Optional:**
- `DEEPSEEK_MODEL` = `deepseek-chat` (or `deepseek-reasoner`)
- `LOG_LEVEL` = `INFO`
- `VECTOR_DB_PATH` = `./data/vector_db`

### 4. Deployment Steps

1. **Push code to GitHub** (if not already)
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"

3. **Configure Deployment**
   - Repository: `your-username/build-an-ai-agent-for-enterprise`
   - Branch: `main`
   - Main file path: `src/main.py`
   - Click "Deploy"

4. **Add Secrets**
   - Go to "Advanced settings" → "Secrets"
   - Add your `DEEPSEEK_API_KEY` (or `OPENAI_API_KEY`)
   - Save

5. **Deploy!**
   - Click "Deploy"
   - Wait for build to complete (~2-5 minutes)
   - Your app will be live at `https://your-app-name.streamlit.app`

## Important Notes

### Data Files
- Policy documents (`data/policies/*.txt`) **must be committed to GitHub**
- They will be read during initialization
- Vector DB will be created in app memory (ephemeral, rebuilds on restart)

### Persistent Storage
- Tickets saved to `data/tickets.json` **are NOT persistent** on Streamlit Cloud
- They reset when the app restarts
- For production, connect to a database or external storage

### Resource Limits
- Streamlit Cloud free tier has memory limits
- FAISS + TF-IDF is lightweight and should work fine
- DeepSeek API calls don't count against Streamlit limits (separate billing)

## Troubleshooting

### "Module not found"
- Ensure `requirements.txt` includes all dependencies
- Check build logs in Streamlit Cloud dashboard

### "API key not found"
- Verify secrets are set correctly in Streamlit Cloud settings
- Use exact names: `DEEPSEEK_API_KEY` (case-sensitive)

### "Error loading documents"
- Ensure `data/policies/` folder and `.txt` files are committed to Git
- Check file paths are correct in the logs

## Alternative: Local File Reference
If you prefer a simpler entry point, you can create `streamlit_app.py` in root:

```python
# streamlit_app.py - Simple redirect to main app
from src.main import main

if __name__ == "__main__":
    main()
```

Then use `streamlit_app.py` as the main file path instead.

