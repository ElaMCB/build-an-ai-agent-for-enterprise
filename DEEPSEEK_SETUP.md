# Using DeepSeek API

This project supports both OpenAI and DeepSeek APIs. DeepSeek offers a great alternative with competitive pricing and free tier access.

## Why DeepSeek?

- ✅ **Free Tier**: Generous free tier for testing
- ✅ **Cost-Effective**: Lower pricing than OpenAI
- ✅ **OpenAI-Compatible**: Uses the same API format
- ✅ **Great Performance**: Excellent for enterprise use cases

## Setup with DeepSeek

### 1. Get Your API Key

1. Go to https://platform.deepseek.com/api_keys
2. Sign up or sign in
3. Create a new API key
4. Copy the key

### 2. Configure

Create a `.env` file in the project root:

```env
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
```

### 3. Run the Application

```bash
python run_app.py
```

In the Streamlit UI:
- Select "DeepSeek" from the provider dropdown
- Enter your DeepSeek API key if not in `.env`
- Click "Initialize Agent"

## Important Notes

### Embeddings

For the RAG system (vector search), the project uses embeddings. Here are your options:

1. **Option 1 (Recommended)**: Use OpenAI for embeddings and DeepSeek for chat
   - Add both keys to `.env`:
     ```env
     OPENAI_API_KEY=sk-openai-key  # For embeddings
     DEEPSEEK_API_KEY=sk-deepseek-key  # For chat
     ```
   - Select "DeepSeek" in the UI for chat model
   - Embeddings will automatically use OpenAI

2. **Option 2**: Use DeepSeek for both
   - Only add `DEEPSEEK_API_KEY` to `.env`
   - Note: DeepSeek embeddings may not be fully compatible with OpenAI embeddings API
   - If you encounter issues, use Option 1

### Models

DeepSeek models available:
- `deepseek-chat` - General purpose chat model (default)
- `deepseek-coder` - Code-focused model

The application uses `deepseek-chat` by default, which works great for policy queries and ticket creation.

## Cost Comparison

| Provider | Model | Cost per 1M tokens (approx) |
|----------|-------|----------------------------|
| DeepSeek | deepseek-chat | ~$0.14 input, $0.28 output |
| OpenAI | gpt-4o-mini | ~$0.15 input, $0.60 output |

DeepSeek is significantly cheaper, especially for output tokens!

## Troubleshooting

### "Error with embeddings"
- If you only have DeepSeek key, add an OpenAI key for embeddings
- Embeddings are separate from chat and may need OpenAI API

### "Invalid API key"
- Check your DeepSeek API key is correct
- Ensure it starts with `sk-`
- Verify it's active on the DeepSeek platform

### "Provider not working"
- Make sure you selected "DeepSeek" in the UI
- Check your `.env` file has `DEEPSEEK_API_KEY` set
- Restart the app after changing provider

## Switching Providers

You can easily switch between OpenAI and DeepSeek:

1. In the Streamlit UI, select your preferred provider
2. Enter the corresponding API key
3. Click "Initialize Agent"

The system will automatically reconfigure to use the selected provider.

