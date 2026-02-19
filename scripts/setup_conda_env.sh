#!/usr/bin/env bash
# CS5374 – Create Miniconda env for granite-code:20b and all repo Python/LangGraph/LangSmith
# Run from repo root: bash scripts/setup_conda_env.sh
# Requires: Miniconda or Anaconda installed.
# If 'conda' is not found, run from a terminal where you have run 'conda init' or source conda.sh first.

set -e

# Try to load conda if not on PATH (common install locations)
if ! command -v conda &>/dev/null; then
  for _conda in "$HOME/miniconda3/etc/profile.d/conda.sh" \
                "$HOME/anaconda3/etc/profile.d/conda.sh" \
                "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"; do
    if [[ -f "$_conda" ]]; then
      echo "=== Sourcing $_conda ==="
      set +e
      source "$_conda"
      set -e
      break
    fi
  done
fi
if ! command -v conda &>/dev/null; then
  echo "ERROR: conda not found. Install Miniconda from https://docs.conda.io/en/latest/miniconda.html"
  echo "Then open a new terminal or run: source \$HOME/miniconda3/etc/profile.d/conda.sh"
  echo "Then run this script again: bash scripts/setup_conda_env.sh"
  exit 1
fi

ENV_NAME="${CONDA_ENV_NAME:-cs5374}"
PYTHON_VERSION="${PYTHON_VERSION:-3.11}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Using repo root: $REPO_ROOT ==="

# 1. Create conda environment with Python (modules / base first)
echo "=== Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION ==="
conda create -n "$ENV_NAME" "python=$PYTHON_VERSION" -y

# 2. Activate and ensure we're in the env
echo "=== Activating '$ENV_NAME' ==="
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"

# 3. Upgrade core packaging (so all subsequent installs see latest)
echo "=== Upgrading pip, setuptools, wheel ==="
python -m pip install --upgrade pip setuptools wheel

# 4. Install base dependencies first (so all modules load correctly)
echo "=== Installing base / utility packages first ==="
pip install "typing_extensions>=4.0.0" "python-dotenv>=1.0.0"

# 5. LangChain stack (order: core -> main -> community -> ollama)
echo "=== Installing LangChain stack ==="
pip install langchain-core langchain langchain-community langchain-ollama

# 6. LangGraph stack
echo "=== Installing LangGraph stack ==="
pip install langgraph langgraph-sdk langgraph-checkpoint-sqlite "langgraph-cli[inmem]"

# 7. LangSmith
echo "=== Installing LangSmith ==="
pip install langsmith

# 8. Search and tools
echo "=== Installing search/tools ==="
pip install duckduckgo-search ddgs wikipedia

# 9. Notebooks and prompt iteration
echo "=== Installing Jupyter and OpenAI client ==="
pip install openai jupyter jupyterlab notebook ipykernel ipywidgets iprogress

# 10. Optional data libs
echo "=== Installing chromadb, pandas ==="
pip install chromadb pandas

# 11. Verify key imports (modules loaded)
echo "=== Verifying modules load ==="
python -c "
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
print('langchain-core, langchain_ollama, langgraph: OK')
"
python -c "
import langsmith
print('langsmith: OK')
"

echo ""
echo "=== Done. Activate with: conda activate $ENV_NAME ==="
echo "=== Ensure Ollama is running and pull the model: ollama pull granite-code:20b ==="
echo "=== Then run e.g.: python code/LangGraph_Demo2.py ==="
