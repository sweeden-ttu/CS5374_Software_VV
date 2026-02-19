"""Unit tests for the data loader module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agent.data_loader import (
    DatasetMetadata,
    LegalDataset,
    TexasLegalDataLoader,
    get_data_loader,
)


# Test data directory - use a mock path for testing
TEST_DATA_DIR = Path("/run/media/sdw3098/RepoPart1/legal-luminary/_data")


class TestDatasetMetadata:
    """Tests for the DatasetMetadata dataclass."""

    def test_dataset_metadata_creation(self):
        """Test creating a DatasetMetadata instance."""
        metadata = DatasetMetadata(
            id="test-123",
            name="Test Dataset",
            description="A test dataset description",
            category="TEST",
            tags=["test", "sample"],
            view_count=100,
            download_count=50,
            url="https://example.com/dataset/test-123",
            quality_score=85.0,
        )

        assert metadata.id == "test-123"
        assert metadata.name == "Test Dataset"
        assert metadata.description == "A test dataset description"
        assert metadata.category == "TEST"
        assert metadata.tags == ["test", "sample"]
        assert metadata.view_count == 100
        assert metadata.download_count == 50
        assert metadata.url == "https://example.com/dataset/test-123"
        assert metadata.quality_score == 85.0

    def test_dataset_metadata_default_quality_score(self):
        """Test default quality score is None."""
        metadata = DatasetMetadata(
            id="test-456",
            name="Test Dataset 2",
            description="Another test",
            category="TEST",
            tags=[],
            view_count=0,
            download_count=0,
            url="",
        )

        assert metadata.quality_score is None


class TestTexasLegalDataLoader:
    """Tests for the TexasLegalDataLoader class."""

    @pytest.fixture
    def loader(self) -> TexasLegalDataLoader:
        """Create a data loader instance for testing."""
        return TexasLegalDataLoader(TEST_DATA_DIR)

    def test_loader_initialization(self, loader):
        """Test loader initializes with correct data directory."""
        assert loader.data_dir == TEST_DATA_DIR

    def test_load_legal_datasets(self, loader):
        """Test loading legal datasets returns dictionary."""
        result = loader.load_legal_datasets()
        assert isinstance(result, dict)
        assert "datasets" in result
        assert "metadata" in result

    def test_load_news_feed(self, loader):
        """Test loading news feed returns dictionary."""
        result = loader.load_news_feed()
        assert isinstance(result, dict)
        assert "feeds" in result or "all_items" in result

    def test_load_comptroller_forms(self, loader):
        """Test loading comptroller forms returns dictionary."""
        result = loader.load_comptroller_forms()
        assert isinstance(result, dict)

    def test_get_datasets_by_category(self, loader):
        """Test filtering datasets by category."""
        # Get LAW_VERIFICATION datasets
        law_datasets = loader.get_datasets_by_category("LAW_VERIFICATION")
        assert isinstance(law_datasets, list)
        # All returned items should be DatasetMetadata
        for ds in law_datasets:
            assert isinstance(ds, DatasetMetadata)
            assert ds.category == "LAW_VERIFICATION"

    def test_get_all_legal_datasets(self, loader):
        """Test getting all legal datasets."""
        all_datasets = loader.get_all_legal_datasets()
        assert isinstance(all_datasets, list)
        assert len(all_datasets) > 0
        for ds in all_datasets:
            assert isinstance(ds, DatasetMetadata)

    def test_get_news_items(self, loader):
        """Test getting news items."""
        news_items = loader.get_news_items()
        assert isinstance(news_items, list)

    def test_get_high_quality_datasets(self, loader):
        """Test filtering high quality datasets."""
        high_quality = loader.get_high_quality_datasets(min_score=75.0)
        assert isinstance(high_quality, list)
        for ds in high_quality:
            assert isinstance(ds, DatasetMetadata)
            assert ds.quality_score is not None
            assert ds.quality_score >= 75.0


class TestGetDataLoader:
    """Tests for the get_data_loader factory function."""

    def test_get_data_loader_default(self):
        """Test default data loader creation."""
        loader = get_data_loader()
        assert isinstance(loader, TexasLegalDataLoader)
        assert loader.data_dir == TEST_DATA_DIR

    def test_get_data_loader_custom_dir(self):
        """Test custom data directory."""
        custom_dir = Path("/custom/path")
        loader = get_data_loader(custom_dir)
        assert isinstance(loader, TexasLegalDataLoader)
        assert loader.data_dir == custom_dir


class TestDataLoaderEdgeCases:
    """Tests for edge cases in data loader."""

    @pytest.fixture
    def mock_loader(self) -> TexasLegalDataLoader:
        """Create a loader with mocked data."""
        with patch.object(TexasLegalDataLoader, "__init__", lambda self, data_dir: None):
            loader = TexasLegalDataLoader.__new__(TexasLegalDataLoader)
            loader.data_dir = TEST_DATA_DIR
            return loader

    def test_empty_datasets_handling(self, mock_loader):
        """Test handling of empty or missing dataset fields."""
        # This tests the loader's robustness with various data
        legal_data = mock_loader.load_legal_datasets()
        # Should handle missing keys gracefully
        assert "datasets" in legal_data or "metadata" in legal_data
