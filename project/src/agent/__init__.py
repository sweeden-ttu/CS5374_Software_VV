"""LangGraph Agent for CS5374 Software Verification and Validation.

This module provides integrated LangGraph demos and assignments:
- Demo 1: Heuristic routing for customer feedback
- Demo 2: LLM-based routing with Ollama
- Demo 2 LangSmith: LLM routing with LangSmith tracing
- Quiz 1: Vague Specification Detection Agent
- Quiz 1 LangSmith: Vague Spec Detection with LangSmith tracing
"""

from agent.graph import (
    graph,
    demo1_graph,
    demo2_graph,
    demo2_langsmith_graph,
    quiz1_graph,
    quiz1_langsmith_graph,
    build_demo1_graph,
    build_demo2_graph,
    build_demo2_langsmith_graph,
    build_quiz1_graph,
    build_quiz1_langsmith_graph,
    Demo1State,
    Demo2State,
    Demo2LangSmithState,
    Quiz1State,
    Quiz1LangSmithState,
    State,
    Context,
    GraphType,
)

__all__ = [
    "graph",
    "demo1_graph",
    "demo2_graph",
    "demo2_langsmith_graph",
    "quiz1_graph",
    "quiz1_langsmith_graph",
    "build_demo1_graph",
    "build_demo2_graph",
    "build_demo2_langsmith_graph",
    "build_quiz1_graph",
    "build_quiz1_langsmith_graph",
    "Demo1State",
    "Demo2State",
    "Demo2LangSmithState",
    "Quiz1State",
    "Quiz1LangSmithState",
    "State",
    "Context",
    "GraphType",
]
