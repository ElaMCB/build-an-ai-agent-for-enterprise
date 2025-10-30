# Installation Guide

## Fixing Pip Issues

If you're getting pip errors, try these steps:

### Step 1: Fix Pip
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

### Step 2: Create Virtual Environment (Recommended)

Virtual environments isolate your project dependencies and prevent conflicts.

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (Git Bash): day
```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

After activating the virtual environment:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit langchain langchain-openai langchain-community chromadb openai python-dotenv pydantic fastapi uvicorn tiktoken Pillow
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; print('Streamlit installed successfully!')"
```

## Troubleshooting

### Python 3.14 Compatibility
Python 3.14 is very new. If you encounter issues:
- Try Python 3.11 or 3.12 for better compatibility
- Some packages may not be fully tested on 3.14 yet

### Permission Errors
If you get permission errors, try:
```bash
pip install --user streamlit
```

### Alternative: Use conda
If pip continues to have issues:
```bash
conda create -n ai-agent python=3.11
conda activate ai-agent
pip install -r requirements.txt
```

