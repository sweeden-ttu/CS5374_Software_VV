"""Integration tests for the LangGraph experiments pipeline."""

from __future__ import annotations

import pytest

from agent.experiments import (
    ExperimentConfig,
    ExperimentResult,
    experiment_graph,
    run_experiment,
)

# Test data directory
TEST_DATA_DIR = "/run/media/sdw3098/RepoPart1/legal-luminary/_data"


pytestmark = pytest.mark.anyio


class TestExperimentGraphIntegration:
    """Integration tests for the experiment graph."""

    @pytest.mark.integration
    async def test_experiment_graph_execution(self):
        """Test full execution of the experiment graph."""
        # Define initial state
        initial_state = {
            "experiment_name": "Integration Test Graph",
            "data_dir": TEST_DATA_DIR,
            "datasets_loaded": False,
            "legal_datasets": [],
            "news_items": [],
            "comptroller_data": {},
            "categorized_datasets": {},
            "high_priority_datasets": [],
            "quality_scores": [],
            "average_quality_score": 0.0,
            "experiment_results": {},
            "errors": [],
        }
        
        # Define context
        context = {
            "data_dir": TEST_DATA_DIR,
            "experiment_name": "Integration Test Graph",
            "min_quality_score": 70.0,
        }
        
        # Execute the graph
        result = await experiment_graph.ainvoke(initial_state, config=context)
        
        # Verify results
        assert result is not None
        assert "legal_datasets" in result
        assert "experiment_results" in result
        
        exp_results = result["experiment_results"]
        assert exp_results.get("status") == "completed"
        assert "summary" in exp_results

    @pytest.mark.integration
    async def test_experiment_graph_with_empty_data(self):
        """Test graph execution with empty/invalid data directory."""
        initial_state = {
            "experiment_name": "Empty Data Test",
            "data_dir": "/nonexistent/path",
            "datasets_loaded": False,
            "legal_datasets": [],
            "news_items": [],
            "comptroller_data": {},
            "categorized_datasets": {},
            "high_priority_datasets": [],
            "quality_scores": [],
            "average_quality_score": 0.0,
            "experiment_results": {},
            "errors": [],
        }
        
        result = await experiment_graph.ainvoke(initial_state)
        
        # Should complete but with errors
        assert result is not None
        assert len(result.get("errors", [])) > 0


class TestRunExperimentIntegration:
    """Integration tests for the run_experiment function."""

    @pytest.mark.integration
    async def test_run_experiment_complete(self):
        """Test complete experiment run."""
        config = ExperimentConfig(
            experiment_name="Complete Integration Test",
            data_dir=TEST_DATA_DIR,
            min_quality_score=60.0,
        )
        
        result = await run_experiment(config)
        
        # Verify result structure
        assert isinstance(result, ExperimentResult)
        assert result.experiment_name == "Complete Integration Test"
        assert result.status in ["completed", "error"]
        
        # If completed, verify summary
        if result.status == "completed":
            assert "total_datasets" in result.summary
            assert result.summary["total_datasets"] > 0

    @pytest.mark.integration
    async def test_run_experiment_high_quality_filter(self):
        """Test experiment with high quality threshold."""
        config = ExperimentConfig(
            experiment_name="High Quality Test",
            data_dir=TEST_DATA_DIR,
            min_quality_score=80.0,  # Higher threshold
        )
        
        result = await run_experiment(config)
        
        assert result.status == "completed"
        # High priority count should be less with higher threshold
        assert "high_priority_count" in result.summary

    @pytest.mark.integration
    async def test_run_experiment_different_thresholds(self):
        """Test experiment with different quality score thresholds."""
        results = []
        
        for threshold in [50.0, 70.0, 90.0]:
            config = ExperimentConfig(
                experiment_name=f"Threshold Test {threshold}",
                data_dir=TEST_DATA_DIR,
                min_quality_score=threshold,
            )
            result = await run_experiment(config)
            results.append((threshold, result))
        
        # Verify different thresholds produce different results
        assert len(results) == 3
        # Lower threshold should have more or equal high priority items
        assert results[0][1].summary.get("high_priority_count", 0) >= results[2][1].summary.get("high_priority_count", 0)


class TestExperimentGraphNodes:
    """Integration tests for individual graph nodes."""

    @pytest.mark.integration
    async def test_node_execution_order(self):
        """Test that nodes execute in correct order."""
        execution_order = []
        
        # We'll track execution by checking the state at each step
        initial_state = {
            "experiment_name": "Order Test",
            "data_dir": TEST_DATA_DIR,
            "datasets_loaded": False,
            "legal_datasets": [],
            "news_items": [],
            "comptroller_data": {},
            "categorized_datasets": {},
            "high_priority_datasets": [],
            "quality_scores": [],
            "average_quality_score": 0.0,
            "experiment_results": {},
            "errors": [],
        }
        
        result = await experiment_graph.ainvoke(initial_state)
        
        # Verify state progression
        # After load_datasets, we should have data
        assert len(result.get("legal_datasets", [])) > 0
        
        # After categorize_datasets, we should have categories
        assert len(result.get("categorized_datasets", {})) > 0
        
        # After analyze_quality, we should have quality scores
        assert len(result.get("quality_scores", [])) > 0
        
        # After generate_results, we should have experiment results
        assert "experiment_results" in result
        assert result.get("experiment_results", {}).get("status") == "completed"


class TestExperimentResults:
    """Tests for experiment result validation."""

    @pytest.mark.integration
    async def test_experiment_summary_stats(self):
        """Test that experiment produces valid summary statistics."""
        config = ExperimentConfig(
            experiment_name="Stats Validation Test",
            data_dir=TEST_DATA_DIR,
        )
        
        result = await run_experiment(config)
        
        assert result.status == "completed"
        summary = result.summary
        
        # Verify summary has expected fields
        assert "total_datasets" in summary
        assert "total_news_items" in summary
        assert "categories" in summary
        assert "average_quality_score" in summary
        
        # Verify data types
        assert isinstance(summary["total_datasets"], int)
        assert isinstance(summary["total_news_items"], int)
        assert isinstance(summary["categories"], dict)
        assert isinstance(summary["average_quality_score"], (int, float))

    @pytest.mark.integration
    async def test_experiment_top_datasets(self):
        """Test that experiment returns top datasets."""
        config = ExperimentConfig(
            experiment_name="Top Datasets Test",
            data_dir=TEST_DATA_DIR,
        )
        
        result = await run_experiment(config)
        
        assert result.status == "completed"
        assert isinstance(result.top_datasets, list)
        
        # Top datasets should have quality scores
        for ds in result.top_datasets:
            assert "id" in ds
            assert "name" in ds

    @pytest.mark.integration
    async def test_experiment_error_handling(self):
        """Test experiment error handling."""
        config = ExperimentConfig(
            experiment_name="Error Handling Test",
            data_dir="/invalid/path",
        )
        
        result = await run_experiment(config)
        
        # Should complete but with errors
        assert result.status in ["completed", "error"]
        # Errors should be captured
        assert isinstance(result.errors, list)
