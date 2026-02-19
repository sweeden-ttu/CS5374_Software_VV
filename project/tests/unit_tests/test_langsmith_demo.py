"""Tests for LangSmith demo and workflow case study integration."""

import pytest


class TestLangSmithDemo:
    """Tests for LangSmith validation demo."""

    def test_import(self):
        from agent.langsmith_demo import (
            build_langsmith_demo_graph,
            run_validation_pipeline,
            langsmith_demo_graph,
        )

        assert langsmith_demo_graph is not None

    def test_build_graph(self):
        from agent.langsmith_demo import build_langsmith_demo_graph

        graph = build_langsmith_demo_graph()
        assert graph is not None

    def test_compute_hash(self):
        from agent.langsmith_demo import compute_hash

        h1 = compute_hash("test content")
        h2 = compute_hash("test content")
        h3 = compute_hash("different content")

        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 64

    def test_canonicalize_url(self):
        from agent.langsmith_demo import canonicalize_url

        assert canonicalize_url("https://example.com/") == "example.com"
        assert canonicalize_url("http://example.com") == "example.com"
        assert canonicalize_url("https://www.example.com/") == "www.example.com"

    def test_run_pipeline_rejected(self):
        from agent.langsmith_demo import run_validation_pipeline

        result = run_validation_pipeline(
            source_text="Short", source_url="https://unknown-domain.com"
        )

        assert result.get("verified") is False
        assert result.get("decision") == "REJECT"

    def test_run_pipeline_accepted(self):
        from agent.langsmith_demo import run_validation_pipeline

        result = run_validation_pipeline(
            source_text="This is a longer piece of content that should pass the minimum threshold check for content validation.",
            source_url="https://bellcountytx.gov/page",
        )

        assert result.get("verified") is True
        assert result.get("decision") == "ACCEPT"


class TestWorkflowCaseStudy:
    """Tests for workflow case study."""

    def test_import(self):
        from agent.workflow_case_study import (
            build_workflow_case_study_graph,
            run_workflow_case_study,
            workflow_case_study_graph,
        )

        assert workflow_case_study_graph is not None

    def test_build_graph(self):
        from agent.workflow_case_study import build_workflow_case_study_graph

        graph = build_workflow_case_study_graph()
        assert graph is not None

    def test_run_workflow_accepted(self):
        from agent.workflow_case_study import run_workflow_case_study

        result = run_workflow_case_study(
            article_title="Test Article",
            source_url="killeendailyherald.com",
            content="This is a test article with enough content to pass validation checks.",
        )

        assert result.get("workflow_id") is not None
        assert result.get("decision", {}).get("final_decision") == "ACCEPT"
        assert len(result.get("transitions", [])) >= 4

    def test_run_workflow_rejected(self):
        from agent.workflow_case_study import run_workflow_case_study

        result = run_workflow_case_study(
            article_title="Test Article",
            source_url="unknown-source.com",
            content="This is a test article with enough content to pass validation checks.",
        )

        assert result.get("decision", {}).get("final_decision") == "REJECT"


class TestIntegratedGraph:
    """Tests for the updated integrated graph."""

    def test_graph_types(self):
        from agent.graph import GraphType

        graph_types = list(GraphType.__args__)
        assert "langsmith_demo" in graph_types
        assert "workflow_case_study" in graph_types

    def test_imports(self):
        from agent.graph import (
            langsmith_demo_graph,
            workflow_case_study_graph,
            run_validation_pipeline,
            run_workflow_case_study,
        )

        assert langsmith_demo_graph is not None
        assert workflow_case_study_graph is not None

    def test_route_to_graph(self):
        from agent.graph import route_to_graph, State

        state: State = {
            "graph_type": "langsmith_demo",
            "payload": [],
            "specification": "",
            "source_text": "",
            "source_url": "",
            "article_title": "",
            "content": "",
            "result": {},
        }
        assert route_to_graph(state) == "langsmith_demo"

        state["graph_type"] = "workflow_case_study"
        assert route_to_graph(state) == "workflow_case_study"
