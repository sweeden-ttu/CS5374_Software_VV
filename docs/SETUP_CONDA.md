# Miniconda environment for CS5374 (granite-code:20b and all Python)

This setup creates a conda environment with **all modules installed in dependency order** so LangChain, LangGraph, LangSmith, and Ollama (granite-code:20b) work correctly.

---

## Option A: Run the setup script (recommended)

**1. Install Miniconda (if needed)**  
- Download: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)  
- Install, then open a **new terminal** (or run `source ~/miniconda3/etc/profile.d/conda.sh`).

**2. From the repo root, run:**

```bash
cd /path/to/CS5374_Software_VV
bash scripts/setup_conda_env.sh
```

**3. Activate and pull the model:**

```bash
conda activate cs5374
ollama pull granite-code:20b
```

**4. Run Python / notebooks:**

```bash
python code/LangGraph_Demo2.py
# or
jupyter lab
```

---

## Option B: Manual commands (paste into terminal)

Run these in order so **base and dependency modules are loaded first**:

```bash
# 1. Go to repo and ensure conda is available
cd /path/to/CS5374_Software_VV
# If conda not found: source ~/miniconda3/etc/profile.d/conda.sh

# 2. Create env with Python 3.11
conda create -n cs5374 python=3.11 -y
conda activate cs5374

# 3. Upgrade packaging
python -m pip install --upgrade pip setuptools wheel

# 4. Base / utilities first
pip install "typing_extensions>=4.0.0" "python-dotenv>=1.0.0"

# 5. LangChain stack (order matters)
pip install langchain-core langchain langchain-community langchain-ollama

# 6. LangGraph stack
pip install langgraph langgraph-sdk langgraph-checkpoint-sqlite "langgraph-cli[inmem]"

# 7. LangSmith and tools
pip install langsmith duckduckgo-search ddgs wikipedia openai

# 8. Jupyter and notebooks
pip install jupyter jupyterlab notebook ipykernel ipywidgets iprogress

# 9. Optional
pip install chromadb pandas

# 10. Verify
python -c "from langchain_ollama import ChatOllama; from langgraph.graph import StateGraph; print('OK')"
```

Then:

```bash
ollama pull granite-code:20b
python code/LangGraph_Demo2.py
```

---

## Environment name and Python version

- **Env name:** `cs5374` (override with `CONDA_ENV_NAME=myenv bash scripts/setup_conda_env.sh`)  
- **Python:** 3.11 (override with `PYTHON_VERSION=3.12 bash scripts/setup_conda_env.sh`)

---

## Consolidated requirements

The repo root **requirements.txt** lists all packages. Install after activating the env with:

```bash
conda activate cs5374
pip install -r requirements.txt
```

For correct load order, prefer running **scripts/setup_conda_env.sh**, which installs base and LangChain/LangGraph modules first.
