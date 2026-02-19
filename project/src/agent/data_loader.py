"""Data loaders for Texas legal datasets.

Loads and processes data from various Texas legal data sources.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# Default data directory
DEFAULT_DATA_DIR = Path("/run/media/sdw3098/RepoPart1/legal-luminary/_data")


@dataclass
class DatasetMetadata:
    """Metadata for a legal dataset."""

    id: str/run/media/sdw3098/RepoPart1/legal-luminary
    name: str
    description: str
    category: str
    tags: List[str]
    view_count: int
    download_count: int
    url: str
    quality_score: Optional[float] = None


@dataclass
class LegalDataset:
    """A legal dataset with metadata."""

    metadata: DatasetMetadata
    raw_data: Dict[str, Any]


class TexasLegalDataLoader:
    """Loads Texas legal datasets from JSON files."""

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR):
        """Initialize the data loader.

        Args:
            data_dir: Directory containing the data files.
        """
        self.data_dir = data_dir

    def load_legal_datasets(self) -> Dict[str, Any]:
        """Load the legal datasets JSON file.

        Returns:
            Dictionary containing the legal datasets data.
        """
        filepath = self.data_dir / "texas_legal_datasets_langgraph.json"
        with open(filepath, "r") as f:
            return json.load(f)

    def load_news_feed(self) -> Dict[str, Any]:
        """Load the news feed JSON file.

        Returns:
            Dictionary containing news feed data.
        """
        filepath = self.data_dir / "news-feed.json"
        with open(filepath, "r") as f:
            return json.load(f)

    def load_comptroller_forms(self) -> Dict[str, Any]:
        """Load the comptroller forms JSON file.

        Returns:
            Dictionary containing comptroller forms data.
        """
        filepath = self.data_dir / "comptroller_forms.json"
        with open(filepath, "r") as f:
            return json.load(f)

    def get_datasets_by_category(self, category: str) -> List[DatasetMetadata]:
        """Get datasets by category.

        Args:
            category: The category to filter by.

        Returns:
            List of DatasetMetadata objects.
        """
        data = self.load_legal_datasets()
        datasets = data.get("datasets", {}).get(category, [])
        result = []
        for ds in datasets:
            metadata = DatasetMetadata(
                id=ds.get("id", ""),
                name=ds.get("name", ""),
                description=ds.get("description", ""),
                category=ds.get("category", ""),
                tags=ds.get("tags", []),
                view_count=ds.get("viewCount", 0),
                download_count=ds.get("downloadCount", 0),
                url=ds.get("url", ""),
            )
            result.append(metadata)
        return result

    def get_all_legal_datasets(self) -> List[DatasetMetadata]:
        """Get all legal datasets.

        Returns:
            List of all DatasetMetadata objects.
        """
        data = self.load_legal_datasets()
        datasets = data.get("datasets", {})
        result = []
        for category, dataset_list in datasets.items():
            for ds in dataset_list:
                metadata = DatasetMetadata(
                    id=ds.get("id", ""),
                    name=ds.get("name", ""),
                    description=ds.get("description", ""),
                    category=ds.get("category", ""),
                    tags=ds.get("tags", []),
                    view_count=ds.get("viewCount", 0),
                    download_count=ds.get("downloadCount", 0),
                    url=ds.get("url", ""),
                )
                result.append(metadata)
        return result

    def get_news_items(self) -> List[Dict[str, Any]]:
        """Get all news items from the news feed.

        Returns:
            List of news item dictionaries.
        """
        data = self.load_news_feed()
        return data.get("all_items", [])

    def get_hi/run/media/sdw3098/RepoPart1/legal-luminarygh_quality_datasets(self, min_score: float = 75.0) -> List[DatasetMetadata]:
        """Get datasets with quality scores above threshold.

        Args:
            min_score: Minimum quality score threshold.

        Returns:
            List of high-quality DatasetMetadata objects.
        """
        data = self.load_legal_datasets()
        langgraph_state = data.get("langGraphState", {})
        quality_scores = langgraph_state.get("quality_scores", {}).get("scores", [])

        result = []
        for qs in quality_scores:
            if qs.get("qualityScore", 0) >= min_score:
                ds_id = qs.get("id", "")
                # Find the dataset in the original data
                for category, dataset_list in data.get("datasets", {}).items():
                    for ds in dataset_list:
                        if ds.get("id") == ds_id:
                            metadata = DatasetMetadata(
                                id=ds.get("id", ""),
                                name=ds.get("name", ""),
                                description=ds.get("description", ""),
                                category=ds.get("category", ""),
                                tags=ds.get("tags", []),
                                view_count=ds.get("viewCount", 0),
                                download_count=ds.get("downloadCount", 0),
                                url=ds.get("url", ""),
                                quality_score=qs.get("qualityScore"),
                            )
                            result.append(metadata)
                            break
        return result


def get_data_loader(data_dir: Optional[Path] = None) -> TexasLegalDataLoader:
    """Get a Texas legal data loader instance.

    Args:
        data_dir: Optional custom data directory.

    Returns:
        TexasLegalDataLoader instance.
    """
    return TexasLegalDataLoader(data_dir or DEFAULT_DATA_DIR)
