# Quiz 1: LangGraph Vague Specification Detection Agent

> **CS 5374 – Software Verification and Validation**  
> Texas Tech University  
> Bonus Quiz (1 Mark)

---

## Problem Statement

Build a **LangGraph agent** (with LLM backend) that:

1. Takes a short specification as input
2. Determines whether the specification is **vague** or **not vague**
3. **If not vague:** Creates a test case specification based on the input
4. **If vague:** Transforms it to a precise specification, then creates a test case

---

## System Architecture

```
Input Specification --> Vagueness Check --> Create Test Case
                                           --> Fix Vagueness --> Create Test Case
```

---

## Vague Specification Examples

| # | Domain | Vague Specification | Issue |
|---|--------|---------------------|-------|
| 1 | Software Development | "The system shall allow for fast, easy data entry" | Defines neither "fast" nor "easy" |
| 2 | Construction | "Install high-quality flooring" | No materials, brand, or durability standard |
| 3 | Performance | "The application must be secure" | Lacks security protocols, compliance, or threat models |
| 4 | Reporting | "The report will include, as appropriate, investigation findings" | Scope open to interpretation |
| 5 | Project Timeline | "The project will be completed in a timely manner" | No specific deadline |

---

## Expected Behavior

### Workflow

1. Input specification
2. Analyze for vagueness
3. If vague: clarify specification first
4. Generate test case specification
5. Output result

### Output Format

**For Non-Vague Specifications:**

```
Test Case Specification:
- Input: [specific inputs]
- Expected Output: [expected behavior]
- Preconditions: [required conditions]
```

**For Vague Specifications:**

```
Clarified Specification: [precise version]

Test Case Specification:
- Input: [specific inputs]
- Expected Output: [expected behavior]
- Preconditions: [required conditions]
```

---

## Key Components

| Component | Purpose |
|-----------|---------|
| **Input Node** | Accept specification text |
| **Vagueness Check Node** | LLM-based classification |
| **Fix Node** | Transform vague to precise |
| **Test Case Node** | Generate test specification |
| **Router** | Conditional edge based on vagueness |

---

## Submission Requirements

### Rubric (Total: 2 marks)

| Deliverable | Marks |
|-------------|-------|
| Source code (Python) | 1.0 mark |
| 5 Screenshots of outputs for test inputs | 1.0 mark (0.2 each) |

### Test Inputs

Use the 5 vague specification examples provided above.

### Submission

- **Platform:** Canvas only
- **Deadline:** 12:30 PM (submission entry disabled after)

---

## Starter Implementation

Use this scaffold to get started. You'll need to fill in the LLM API calls.

```python
#!/usr/bin/env python3
"""
Quiz 1: LangGraph Vague Specification Detection Agent
Starter Implementation

To run:
1. Copy this file to your local environment
2. Install dependencies: pip install langchain langchain-openai python-dotenv
3. Copy .env.example to .env and add your API keys
4. Run: python quiz1_starter.py
"""

import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# =============================================================================
# CONFIGURATION
# =============================================================================

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get API key - update this to match your provider
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize LLM - modify model as needed
llm = ChatOpenAI(
    model="gpt-4",
    api_key=OPENAI_API_KEY,
    temperature=0
)

# =============================================================================
# STATE DEFINITION
# =============================================================================

class AgentState(TypedDict):
    """State passed between nodes in the LangGraph agent."""
    specification: str           # Input specification
    is_vague: bool              # Whether spec is vague
    clarified_spec: str         # Fixed specification (if vague)
    test_case: str              # Generated test case

# =============================================================================
# NODE FUNCTIONS
# =============================================================================

def check_vagueness(state: AgentState) -> AgentState:
    """
    Node 1: Determine if the specification is vague or not.
    
    TODO: Replace this with an actual LLM call to classify the specification.
    """
    spec = state["specification"]
    
    # ---------------------------------------------------------------------
    # TODO: Implement LLM call to check vagueness
    # ---------------------------------------------------------------------
    # Example implementation:
    # 
    # messages = [
    #     SystemMessage(content="""You are a specification analyzer.
    #     Determine if the following requirement is vague or unclear.
    #     Consider: missing metrics, undefined terms, ambiguous language.
    #     Respond with only 'VAGUE' or 'NOT_VAGUE'."""),
    #     HumanMessage(content=spec)
    # ]
    # response = llm.invoke(messages)
    # is_vague = "VAGUE" in response.content.upper()
    #
    # For now, we'll use a simple heuristic:
    # ---------------------------------------------------------------------
    
    vague_indicators = ["fast", "easy", "high-quality", "timely", "as appropriate", "secure"]
    is_vague = any(indicator in spec.lower() for indicator in vague_indicators)
    
    return {"is_vague": is_vague}


def fix_vagueness(state: AgentState) -> AgentState:
    """
    Node 2: Transform a vague specification into a precise one.
    
    TODO: Replace with an actual LLM call to clarify the specification.
    """
    spec = state["specification"]
    
    # ---------------------------------------------------------------------
    # TODO: Implement LLM call to clarify vague specification
    # ---------------------------------------------------------------------
    # Example implementation:
    #
    # messages = [
    #     SystemMessage(content="""You are a requirements engineer.
    #     Transform the following vague specification into a precise,
    #     testable requirement. Be specific and include measurable criteria."""),
    #     HumanMessage(content=spec)
    # ]
    # response = llm.invoke(messages)
    # clarified = response.content
    #
    # For now, we'll use simple replacements:
    # ---------------------------------------------------------------------
    
    clarifications = {
        "fast": "response time < 200ms",
        "easy": "requires <= 3 clicks",
        "high-quality": "meets ISO 9001 standards",
        "timely": "within 2 business days",
        "as appropriate": "per investigation protocol Section 4.2",
        "secure": "TLS 1.3 with AES-256 encryption"
    }
    
    clarified = spec
    for vague_term, clarification in clarifications.items():
        if vague_term in clarified.lower():
            clarified = clarified.replace(vague_term, f"[{clarification}]")
    
    return {"clarified_spec": clarified}


def generate_test_case(state: AgentState) -> AgentState:
    """
    Node 3: Generate a test case specification.
    
    TODO: Replace with an actual LLM call to create test case.
    """
    spec = state.get("clarified_spec", state["specification"])
    is_vague = state["is_vague"]
    
    # ---------------------------------------------------------------------
    # TODO: Implement LLM call to generate test case
    # ---------------------------------------------------------------------
    # Example implementation:
    #
    # messages = [
    #     SystemMessage(content="""You are a test engineer.
    #     Create a detailed test case specification including:
    #     - Input: specific test inputs
    #     - Expected Output: expected behavior
    #     - Preconditions: required conditions
    #     Format as structured text."""),
    #     HumanMessage(content=spec)
    # ]
    # response = llm.invoke(messages)
    # test_case = response.content
    #
    # For now, we'll generate a basic test case:
    # ---------------------------------------------------------------------
    
    test_case = f"""Test Case Specification:
- Input: {spec}
- Expected Output: System should meet all specified criteria
- Preconditions: System must be operational, test data available
- Vague Original: {is_vague}"""
    
    return {"test_case": test_case}


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def create_agent() -> StateGraph:
    """Build the LangGraph agent with conditional routing."""
    
    # Create graph
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("check", check_vagueness)
    graph.add_node("fix", fix_vagueness)
    graph.add_node("testcase", generate_test_case)
    
    # Set entry point
    graph.set_entry_point("check")
    
    # Conditional routing based on vagueness
    def route_after_check(state: AgentState) -> str:
        """Decide next step based on whether spec is vague."""
        if state["is_vague"]:
            return "fix"
        return "testcase"
    
    graph.add_conditional_edges(
        "check",
        route_after_check,
        {"fix": "fix", "testcase": "testcase"}
    )
    
    # Connect fix to testcase (after fixing, always generate test case)
    graph.add_edge("fix", "testcase")
    
    # End after testcase
    graph.add_edge("testcase", END)
    
    return graph


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Create the agent
    agent = create_agent().compile()
    
    # Test with example specifications
    test_specs = [
        "The system shall allow for fast, easy data entry",
        "The system shall validate all input fields before submission",
    ]
    
    print("=" * 60)
    print("Quiz 1: LangGraph Vague Specification Detection Agent")
    print("=" * 60)
    
    for spec in test_specs:
        print(f"\nInput: {spec}")
        print("-" * 40)
        
        # Run the agent
        result = agent.invoke({"specification": spec})
        
        print(f"Is Vague: {result['is_vague']}")
        if result.get("clarified_spec"):
            print(f"Clarified: {result['clarified_spec']}")
        print(f"Test Case:\n{result['test_case']}")
        print("=" * 60)
```

---

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install langchain langchain-openai python-dotenv
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Run the starter:**
   ```bash
   python quiz1_starter.py
   ```

---

## Example .env Template

Create a `.env` file in the assignments directory:

```bash
# OpenAI API Key (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-your-key-here

# Optional: LangSmith for tracing (https://smith.langchain.com)
LANGSMITH_API_KEY=ls-your-key-here
LANGSMITH_TRACING=true
```

---

*CS5374 – Software Verification and Validation | Texas Tech University*
