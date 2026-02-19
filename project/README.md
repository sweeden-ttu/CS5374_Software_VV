# CS5374 LangGraph Project - Software Verification and Validation

[![CI](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml)

This project integrates LangGraph demos and assignments for CS5374 Software Verification and Validation at Texas Tech University.

## Project Structure

```
project/
├── src/agent/
│   ├── __init__.py           # Module exports
│   ├── graph.py              # Main integrated graph
│   ├── demo1_graph.py        # Demo 1: Heuristic routing
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
