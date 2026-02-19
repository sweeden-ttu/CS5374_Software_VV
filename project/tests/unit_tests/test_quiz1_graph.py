"""Tests for Quiz 1: Vague Specification Detection Agent."""

import pytest

from agent.quiz1_graph import (
    Quiz1State,
    build_quiz1_graph,
    quiz1_graph,
    check_vagueness,
    fix_vagueness,
    generate_test_case,
    route_after_check,
    VAGUE_SPECIFICATIONS,
)


class TestQuiz1Nodes:
    """Tests for individual node functions."""

    def test_check_vagueness_vague(self):
        """Test vagueness detection for vague specifications."""
        state: Quiz1State = {
            "specification": "The system shall allow for fast, easy data entry",
            "is_vague": False,
            "clarified_spec": "",
            "test_case": "",
        }
        result = check_vagueness(state)
        assert result["is_vague"] is True

    def test_check_vagueness_precise(self):
        """Test vagueness detection for precise specifications."""
        state: Quiz1State = {
            "specification": "The system shall validate all input fields within 200ms",
            "is_vague": False,
            "clarified_spec": "",
            "test_case": "",
        }
        result = check_vagueness(state)
        assert result["is_vague"] is False

    def test_fix_vagueness(self):
        """Test fixing vague specifications."""
        state: Quiz1State = {
            "specification": "The system shall be fast",
            "is_vague": True,
            "clarified_spec": "",
            "test_case": "",
        }
        result = fix_vagueness(state)
        assert "response time" in result["clarified_spec"].lower()

    def test_generate_test_case(self):
        """Test test case generation."""
        state: Quiz1State = {
            "specification": "The system shall respond within 200ms",
            "is_vague": False,
            "clarified_spec": "",
            "test_case": "",
        }
        result = generate_test_case(state)
        assert "test case" in result["test_case"].lower()

    def test_route_after_check_vague(self):
        """Test routing after vagueness check (vague)."""
        state: Quiz1State = {
            "specification": "Test",
            "is_vague": True,
            "clarified_spec": "",
            "test_case": "",
        }
        result = route_after_check(state)
        assert result == "fix"

    def test_route_after_check_precise(self):
        """Test routing after vagueness check (precise)."""
        state: Quiz1State = {
            "specification": "Test",
            "is_vague": False,
            "clarified_spec": "",
            "test_case": "",
        }
        result = route_after_check(state)
        assert result == "testcase"


class TestQuiz1Graph:
    """Tests for the full Quiz 1 graph."""

    def test_graph_exists(self):
        """Test that graph is compiled."""
        assert quiz1_graph is not None

    def test_build_graph(self):
        """Test that graph can be built."""
        graph = build_quiz1_graph()
        assert graph is not None

    def test_vague_specification_flow(self):
        """Test full flow for vague specification."""
        graph = build_quiz1_graph()
        spec = "The system shall allow for fast, easy data entry"
        result = graph.invoke({"specification": spec})
        assert result["is_vague"] is True
        assert result["clarified_spec"] != ""
        assert result["test_case"] != ""

    def test_precise_specification_flow(self):
        """Test full flow for precise specification."""
        graph = build_quiz1_graph()
        spec = "The system shall respond within 200ms"
        result = graph.invoke({"specification": spec})
        assert result["is_vague"] is False
        assert result["test_case"] != ""

    def test_all_vague_specifications(self):
        """Test all vague specifications from the assignment."""
        graph = build_quiz1_graph()
        for spec in VAGUE_SPECIFICATIONS:
            result = graph.invoke({"specification": spec})
            assert result["is_vague"] is True
            assert result["test_case"] != ""


class TestVagueSpecifications:
    """Tests for the provided vague specifications."""

    @pytest.mark.parametrize("spec", VAGUE_SPECIFICATIONS)
    def test_specification_is_detected_as_vague(self, spec):
        """Test that each vague spec is detected as vague."""
        graph = build_quiz1_graph()
        result = graph.invoke({"specification": spec})
        assert result["is_vague"] is True

    @pytest.mark.parametrize("spec", VAGUE_SPECIFICATIONS)
    def test_specification_gets_clarified(self, spec):
        """Test that each vague spec gets clarified."""
        graph = build_quiz1_graph()
        result = graph.invoke({"specification": spec})
        assert result["clarified_spec"] != ""

    @pytest.mark.parametrize("spec", VAGUE_SPECIFICATIONS)
    def test_specification_gets_test_case(self, spec):
        """Test that each spec gets a test case."""
        graph = build_quiz1_graph()
        result = graph.invoke({"specification": spec})
        assert "test case" in result["test_case"].lower()
