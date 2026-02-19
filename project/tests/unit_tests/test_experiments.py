"""Unit tests for the experiments module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agent.experiments import (
    ExperimentConfig/run/media/sdw3098/RepoPart1/legal-luminary,
    ExperimentResult,
    ExperimentState,
    analyze_quality,
    categorize_datasets,
    generate_results,
    load_datasets,
    run_experiment,
)


# Test data directory
TEST_DATA_DIR = "/run/media/sdw3098/RepoPart1/legal-luminary/_data"


class TestExperimentConfig:
    """Tests for the ExperimentConfig dataclass."""

    def test_default_config(self):
        """Test default experiment configuration."""
        config = ExperimentConfig()
        
        assert config.experiment_name == "Texas Legal Data Experiment"
        assert config.data_dir == TEST_DATA_DIR
        assert config.min_quality_score == 70.0

    def test_custom_config(self):
        """Test custom experiment configuration."""
        config = ExperimentConfig(
            experiment_name="Custom Experiment",
            data_dir="/custom/path",
            min_quality_score=80.0,
        )
        
        assert config.experiment_name == "Custom Experiment"
        assert config.data_dir == "/custom/path"
        assert config.min_quality_score == 80.0


class TestExperimentResult:
    """Tests for the ExperimentResult dataclass."""

    def test_result_creation(self):
        """Test creating an experiment result."""
        result = ExperimentResult(
            experiment_name="Test Experiment",
            status="complete/run/media/sdw3098/RepoPart1/legal-luminaryd",
            summary={"total_datasets": 10},
            top_datasets=[],
            errors=[],
        )
        
        assert result.experiment_name == "Test Experiment"
        assert result.status == "completed"
        assert result.summary["total_datasets"] == 10


class TestExperimentState:
    """Tests for experiment state structure."""

    def test_initial_state(self):
        """Test creating initial experiment state."""
        state: ExperimentState = {
            "experiment_name": "Test",
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
        
        assert state["experiment_name"] == "Test"
        assert state["datasets_loaded"] is False
        assert isinstance(state["legal_datasets"], list)


class TestLoadDatasets:
    """Tests for the load_datasets function."""

    @pytest.mark.asyncio
    async def test_load_datasets_success(self):
        """Test successful dataset loading."""
        # Create mock runtime
        mock_runtime = MagicMock()
        mock_runtime.context = {}
        
        state: ExperimentState = {
            "experiment_name": "Test",
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
        
        result = await load_datasets(state, mock_runtime)
        
        assert "legal_datasets" in result
        assert "news_items" in result
        assert len(result["errors"]) == 0 or result["datasets_loaded"] is True

    @pytest.mark.asyncio
    async def test_load_datasets_with_invalid_path(self):
        """Test loading with invalid data directory."""
        mock_runtime = MagicMock()
        mock_runtime.context = {}
        
        state: ExperimentState = {
            "experiment_name": "Test",
            "data_dir": "/invalid/path",
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
        
        result = await load_datasets(state, mock_runtime)
        
        # Should have errors for invalid path
        assert len(result["errors"]) > 0


class TestCategorizeDatasets:
    """Tests for the categorize_datasets function."""

    def test_categorize_with_sample_data(self):
        """Test dataset categorization."""
        mock_runtime = MagicMock()
        mock_runtime.context = {"min_quality_score": 70.0}
        
        # Sample datasets
        sample_datasets = [
            {
                "id": "1",
                "name": "Texas Inmate Data",
                "tags": ["tdcj", "inmate"],
                "description": "Test",
            },
            {
                "id": "2",
                "name": "Environmental Report",
                "tags": ["environment", "sso"],
                "description": "Test",
            },
            {
                "id": "3",
                "name": "Attorney License List",
                "tags": ["attorney", "license"],
                "description": "Test",
            },
        ]
        
        state: ExperimentState = {
            "experiment_name": "Test",
            "data_dir": TEST_DATA_DIR,
            "datasets_loaded": True,
            "legal_datasets": sample_datasets,
            "news_items": [],
            "comptroller_data": {},
            "categorized_datasets": {},
            "high_priority_datasets": [],
            "quality_scores": [],
            "average_quality_score": 0.0,
            "experiment_results": {},
            "errors": [],
        }
        
        result = categorize_datasets(state, mock_runtime)
        
        assert "categorized_datasets" in result
        categories = result["categorized_datasets"]
        assert "CRIMINAL_JUSTICE" in categories
        assert "ENVIRONMENTAL" in categories
        assert "ATTORNEY_RESOURCE" in categories

    def test_categorize_empty_datasets(self):
        """Test categorization with empty dataset list."""
        mock_runtime = MagicMock()
        mock_runtime.context = {}
        
        state: ExperimentState = {
            "experiment_name": "Test",
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
        
        result = categorize_datasets(state, mock_runtime)
        
        assert result["categorized_datasets"] == {
            "LAW_VERIFICATION": [],
            "NEWS": [],
            "ATTORNEY_RESOURCE": [],
            "CRIMINAL_JUSTICE": [],
            "ENVIRONMENTAL": [],
            "OTHER": [],
        }


class TestAnalyzeQuality:
    """Tests for the analyze_quality function."""

    def test_quality_analysis_with_data(self):
        """Test quality score calculation."""
        mock_runtime = MagicMock()
        mock_runtime.context = {}
        
        sample_datasets = [
            {
                "id": "1",
                "name": "Dataset with description",
                "description": "This is a test description",
                "tags": ["tag1", "tag2"],
                "viewCount": 100,
                "downloadCount": 50,
            },
            {
                "id": "2",
                "name": "Dataset without description",
                "description": "",
                "tags": [],
                "viewCount": 0,
                "downloadCount": 0,
            },
        ]
        
        state: ExperimentState = {
            "experiment_name": "Test",
            "data_dir": TEST_DATA_DIR,
            "datasets_loaded": True,
            "legal_datasets": sample_datasets,
            "news_items": [],
            "comptroller_data": {},
            "categorized_datasets": {},
            "high_priority_datasets": [],
            "quality_scores": [],
            "average_quality_score": 0.0,
            "experiment_results": {},
            "errors": [],
        }
        
        result = analyze_quality(state, mock_runtime)
        
        assert "quality_scores" in result
        assert "average_quality_score" in result
        assert len(result["quality_scores"]) == 2
        # First dataset should have higher score
        assert result["quality_scores"][0]["qualityScore"] > result["quality_scores"][1]["qualityScore"]

    def test_quality_analysis_empty(self):
        """Test quality analysis with no datasets."""
        mock_runtime = MagicMock()
        
        state: ExperimentState = {
            "experiment_name": "Test",
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
        
        result = analyze_quality(state, mock_runtime)
        
        assert result["average_quality_score"] == 0.0
        assert result["quality_scores"] == []


class TestGenerateResults:
    """Tests for the generate_results function."""

    def test_generate_results_success(self):
        """Test result generation."""
        mock_runtime = MagicMock()
        
        state: ExperimentState = {
            "experiment_name": "Test Experiment",
            "data_dir": TEST_DATA_DIR,
            "datasets_loaded": True,
            "legal_datasets": [{"id": "1"}, {"id": "2"}],
            "news_items": [{"id": "a"}],
            "comptroller_data": {},
            "categorized_datasets": {
                "CRIMINAL_JUSTICE": [{"id": "1"}],
                "OTHER": [{"id": "2"}],
            },
            "high_priority_datasets": [{"id": "1"}],
            "quality_scores": [{"qualityScore": 80}],
            "average_quality_score": 80.0,
            "experiment_results": {},
            "errors": [],
        }
        
        result = generate_results(state, mock_runtime)
        
        assert "experiment_results" in result
        exp_results = result["experiment_results"]
        assert exp_results["status"] == "completed"
        assert exp_results["experiment_name"] == "Test Experiment"
        assert exp_results["summary"]["total_datasets"] == 2
        assert exp_results["summary"]["total_news_items"] == 1


class TestRunExperiment:
    """Tests for the run_experiment function."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_run_experiment_default(self):
        """Test running experiment with default config."""
        config = ExperimentConfig(
            experiment_name="Integration Test",
            data_dir=TEST_DATA_DIR,
        )
        
        result = await run_experiment(config)
        
        assert isinstance(result, ExperimentResult)
        assert result.status in ["completed", "error"]
        # If successful, should have summary data
        if result.status == "completed":
            assert "total_datasets" in result.summary

    @pytest.mark.asyncio
    async def test_run_experiment_with_custom_config(self):
        """Test running experiment with custom configuration."""
        config = ExperimentConfig(
            experiment_name="Custom Test",
            data_dir=TEST_DATA_DIR,
            min_quality_score=50.0,
        )
        
        result = await run_experiment(config)
        
        assert result.experiment_name == "Custom Test"
