# Fixing ChromaDB Installation Issues

## Problem
ChromaDB requires Microsoft Visual C++ Build Tools on Windows, which causes installation failures.

## Solution Options

### Option 1: Use FAISS Instead (Recommended - Already Updated)
I've updated the code to use FAISS instead of ChromaDB. FAISS has better Windows support with pre-built wheels.

**Install FAISS:**
```bash
pip install faiss-cpu
```

**The code has been automatically updated to use FAISS.**

### Option 2: Install Visual C++ Build Tools
If you prefer ChromaDB:

1. Download Visual C++ Build Tools:
   - Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download "Build Tools for Visual Studio"
   - Install with "Desktop development with C++" workload

2. Restart your terminal

3. Install ChromaDB:
   ```bash
   pip install chromadb
   ```

### Option 3: Use Conda (Easier for Native Dependencies)

Conda handles native dependencies better:

```bash
conda create -n ai-agent python=3.11
conda activate ai-agent
conda install -c conda-forge chromadb
pip install -r requirements.txt
```

## Quick Fix - Install FAISS (Fastest)

Since I've updated the code to use FAISS, just install it:

```bash
# In your virtual environment
pip install faiss-cpu

# Then install other packages
pip install streamlit langchain langchain-openai langchain-community openai python-dotenv pydantic fastapi uvicorn tiktoken Pillow
```

Then run your app - it will use FAISS instead of ChromaDB!

