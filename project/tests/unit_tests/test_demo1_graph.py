"""Tests for Demo 1: Heuristic routing for customer feedback."""

import pytest

from agent.demo1_graph import (
    Demo1State,
    build_demo1_graph,
    demo1_graph,
    extract_content,
    route_question_or_compliment,
    run_compliment_code,
    run_question_code,
    beautify,
)


class TestDemo1Nodes:
    """Tests for individual node functions."""

    def test_extract_content(self):
        """Test content extraction from payload."""
        state: Demo1State = {
            "text": "",
            "answer": "",
            "payload": [
                {
                    "customer_remark": "Why is this so expensive?",
                    "time_of_comment": "2025-01-20",
                }
            ],
        }
        result = extract_content(state)
        assert result["text"] == "Why is this so expensive?"

    def test_route_question(self):
        """Test routing to question handler."""
        state: Demo1State = {
            "text": "Why is this so expensive?",
            "answer": "",
            "payload": [],
        }
        result = route_question_or_compliment(state)
        assert result == "question"

    def test_route_compliment(self):
        """Test routing to compliment handler."""
        state: Demo1State = {
            "text": "Great product!",
            "answer": "",
            "payload": [],
        }
        result = route_question_or_compliment(state)
        assert result == "compliment"

    def test_run_question_code(self):
        """Test question handler."""
        state: Demo1State = {
            "text": "Why?",
            "answer": "",
            "payload": [],
        }
        result = run_question_code(state)
        assert "question" in result["answer"].lower()

    def test_run_compliment_code(self):
        """Test compliment handler."""
        state: Demo1State = {
            "text": "Great!",
            "answer": "",
            "payload": [],
        }
        result = run_compliment_code(state)
        assert "compliment" in result["answer"].lower()

    def test_beautify(self):
        """Test beautify node."""
        state: Demo1State = {
            "text": "Test",
            "answer": "Thanks for your question.",
            "payload": [],
        }
        result = beautify(state)
        assert "beautified" in result["answer"].lower()


class TestDemo1Graph:
    """Tests for the full Demo 1 graph."""

    def test_graph_exists(self):
        """Test that graph is compiled."""
        assert demo1_graph is not None

    def test_build_graph(self):
        """Test that graph can be built."""
        graph = build_demo1_graph()
        assert graph is not None

    def test_question_flow(self):
        """Test full question flow through graph."""
        graph = build_demo1_graph()
        payload = [
            {
                "customer_remark": "Why has the packaging changed?",
                "time_of_comment": "2025-01-20",
            }
        ]
        result = graph.invoke({"payload": payload})
        assert "answer" in result
        assert "beautified" in result["answer"].lower()

    def test_compliment_flow(self):
        """Test full compliment flow through graph."""
        graph = build_demo1_graph()
        payload = [
            {
                "customer_remark": "Great product!",
                "time_of_comment": "2025-01-20",
            }
        ]
        result = graph.invoke({"payload": payload})
        assert "answer" in result
        assert "beautified" in result["answer"].lower()

    def test_stream_execution(self):
        """Test streaming execution."""
        graph = build_demo1_graph()
        payload = [{"customer_remark": "Test question?"}]
        steps = list(graph.stream({"payload": payload}))
        assert len(steps) > 0
