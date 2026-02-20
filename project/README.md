# CS5374 LangGraph Project - Software Verification and Validation

[![CI](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml)

This project integrates LangGraph demos and assignments for CS5374 Software Verification and Validation at Texas Tech University.

## Project Structure

```
project/
├── src/agent/
│   ├── __init__.py           # Module exports
│   ├── graph.py              # Main integrated graph
│   ├── demo1_graph.py        # Demo 1: Heuri/home/sdw3098/Pictures/Screenshotsstic routing
│   ├── demo2_graph.py        # Demo 2: LLM routing (Ollama)
│   ├── demo2_langsmith_graph.py  # Demo 2 with LangSmith tracing
│   ├── quiz1_graph.py        # Quiz 1: Vague Specification Detection
│   ├── quiz1_langsmith_graph.py  # Quiz 1 with LangSmith tracing
│   ├── data_loader.py        # Texas legal data loader
│   └── experiments.py        # LangGraph experiments
├── tests/
│   ├── unit_tests/
│   │   ├── test_demo1_graph.py
│   │   ├── test_quiz1_graph.py
│   │   └── ...
│   └── conftest.py
├── pyproject.toml
├── .env.example
└── README.md
```

## Demos

### Demo 1: Heuristic Routing
Simple LangGraph that routes customer feedback based on a heuristic (presence of '?').
- **File**: `src/agent/demo1_graph.py`
- **Routing**: Heuristic-based (question mark detection)
- **Nodes**: extract_content → route → (question|compliment) → beautify

### Demo 2: LLM-Based Routing
LangGraph using Ollama LLM to classify customer feedback.
- **File**: `src/agent/demo2_graph.py`
- **Routing**: LLM-based classification
- **Model**: Ollama (granite-code:20b)

### Demo 2 with LangSmith
Same as Demo 2 but with LangSmith tracing enabled.
- **File**: `src/agent/demo2_langsmith_graph.py`
- **Features**: LangSmith observability

## Assignments

### Quiz 1: Vague Specification Detection Agent
Detects vague specifications and generates test cases.
- **File**: `src/agent/quiz1_graph.py`
- **Workflow**: check_vagueness → (fix_vagueness)? → generate_test_case
- **Input**: Specification string
- **Output**: Test case specification

### Quiz 1 with LangSmith
Quiz 1 with LangSmith tracing for Part B of Assignment 1.
- **File**: `src/agent/quiz1_langsmith_graph.py`
- **Features**: LangSmith tracing enabled

### Demo: LangSmith Content Validation
Content validation pipeline with domain verification using allowlist.
- **File**: `src/agent/langsmith_demo.py`
- **Pipeline**: 4 nodes - extract_content → evidence_verification → content_generation → evaluator
- **Test Oracle**: Uses `config/allowlist.json` for domain verification
- **Output**: Evidence artifacts to `output/langsmith_demo/`

### Demo: Workflow Case Study
Complete workflow demonstrating ACCEPT/REJECT paths based on source verification.
- **File**: `src/agent/workflow_case_study.py`
- **Workflow**: START → PROCESS → DECISION → ACTION → VALIDATE → END
- **Features**: Full state management with transition tracking

## New Demos (Updated)

### config/allowlist.json
- Copied from legal-luminary demo
- Contains trusted domains for Bell County, Texas area
- Used as Test Oracle for domain verification in langsmith_demo

### src/agent/graph.py (Updated)
- Added `langsmith_demo` and `workflow_case_study` graph types
- New routing and runner functions for both demos

### tests/unit_tests/test_langsmith_demo.py
- Unit tests for both new demos

### Running New Demos

```python
from agent.graph import graph

# Run LangSmith validation demo
result = graph.invoke({
    "graph_type": "langsmith_demo",
    "source_text": "content to validate...",
    "source_url": "https://bellcountytx.gov"
})

# Run workflow case study
result = graph.invoke({
    "graph_type": "workflow_case_study",
    "article_title": "News Article",
    "source_url": "killeendailyherald.com",
    "content": "Article content"
})
```

## Getting Started

### 1. Install Dependencies

```bash
cd project
pip install -e . "langgraph-cli[inmem]"
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `OPENAI_API_KEY` - For GPT-4 based Quiz 1
- `LANGCHAIN_API_KEY` - For LangSmith tracing
- `LANGCHAIN_TRACING_V2` - Set to "true" to enable tracing

### 3. Run Demos

```bash
# Run Demo 1
python -m agent.demo1_graph

# Run Quiz 1
python -m agent.quiz1_graph

# Run Quiz 1 with LangSmith
python -m agent.quiz1_langsmith_graph
```

### 4. Start LangGraph Server

```bash
langgraph dev
```

### 5. Crawl pipeline (conda)

The crawl → validate → cleanup pipeline uses **conda** for environment management. It writes posts to `legal-luminary/_posts` and rankings to `legal-luminary/_data/important_articles.json`.

**Create and activate the conda environment:**

```bash
cd project
conda env create -f environment.yml
conda activate agent-pipeline
playwright install chromium
```

**Configure API keys** (copy `.env.example` to `.env` and set `OPENAI_API_KEY`, optional `LANGSMITH_API_KEY`).

**Run the pipeline:**

```bash
PYTHONPATH=src python run_crawl_pipeline.py
```

Or run the pipeline module directly:

```bash
PYTHONPATH=src python -m agent.crawl_validate_cleanup_pipeline
```

**Update the environment** after changing `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

## Running Tests

```bash
cd project
pytest tests/
```

## Usage Examples

### Using the Integrated Graph

```python
from agent import graph, build_quiz1_graph

# Run Quiz 1
quiz1 = build_quiz1_graph()
result = quiz1.invoke({
    "specification": "The system shall be fast and easy to use"
})
print(result["test_case"])
```

### Running with LangSmith Tracing

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"

from agent import build_quiz1_langsmith_graph

graph = build_quiz1_langsmith_graph()
result = graph.invoke({"specification": "The system shall be secure"})
```

## Vague Specifications (Quiz 1)

The following specifications are detected as vague:

1. "The system shall allow for fast, easy data entry"
2. "Install high-quality flooring"
3. "The application must be secure"
4. "The report will include, as appropriate, investigation findings"
5. "The project will be completed in a timely manner"

## Assignment Deliverables

### Part A: Functional/Structural Testing
See assignments/Assignment1-CS5374-Spring2026.md

### Part B: LangSmith Tracing
- Source code: `src/agent/quiz1_langsmith_graph.py`
- Run the script and check LangSmith dashboard for traces

## Documentation

For more information on LangGraph:
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)
- [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)

---

*CS5374 – Software Verification and Validation | Texas Tech University*
