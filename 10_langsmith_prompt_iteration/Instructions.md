# Instructions: Small Prompt Iteration

> **CS 5374 – Software Verification and Validation**
> Texas Tech University

---

## Quick Start Guide

### Running the Jupyter Notebook

```mermaid
flowchart LR
    A[Install Dependencies] --> B[Configure API Keys]
    B --> C[Open Notebook]
    C --> D[Run Cells]
    D --> E[View Results in LangSmith]
```

---

## Step-by-Step Instructions

### 1. Environment Setup

```bash
# Install required packages
pip install langchain langsmith openai

# Or use requirements.txt
pip install -r requirements.txt
```

### 2. API Configuration

Create a `.env` file or set environment variables:

```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your-langsmith-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

> **Note:** If you don't create a `.env` file, make sure these environment variables are set in your system before running the notebook. You can set them in your terminal as shown above, or add them to your shell profile (e.g., `.bashrc` or `.zshrc`).

### 3. Launch Jupyter

```bash
jupyter notebook updated_small_prompt_iteration.ipynb
```

### 4. Execute Notebook

- Run cells sequentially (Shift + Enter)
- Observe outputs at each step
- Review traces in LangSmith dashboard

### 5. Analyze Results

- Navigate to [LangSmith Dashboard](https://smith.langchain.com)
- Select your project
- Review prompt iterations and metrics

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key Error | Verify environment variables |
| Import Error | Reinstall dependencies |
| No Traces | Check LANGCHAIN_TRACING_V2=true |

---

*CS5374 – Software Verification and Validation | Texas Tech University*
