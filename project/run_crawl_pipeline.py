#!/usr/bin/env python3
"""Run the full LangGraph crawl -> validate -> cleanup pipeline.

Loads API keys from project/.env (OPENAI_API_KEY, LANGSMITH_API_KEY, LANGCHAIN_*),
then runs the compiled LangGraph:
1. Multi-source date-aware crawler (writes to legal-luminary/_posts)
2. Evidence validator (writes legal-luminary/_data/important_articles.json)
3. Cleanup + LangChain summarization (overwrites posts in _posts)

Usage (from project root):
  PYTHONPATH=src python run_crawl_pipeline.py

Or run the pipeline module directly:
  PYTHONPATH=src python -m agent.crawl_validate_cleanup_pipeline

Requires: project/.env with OPENAI_API_KEY (and optionally LANGSMITH_API_KEY); langgraph; playwright.
Before first run: playwright install chromium
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Project root = directory containing this script
PROJECT_ROOT = Path(__file__).resolve().parent

# Load project .env first so API keys are available before importing LangGraph/agents
from dotenv import load_dotenv
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
else:
    load_dotenv()

# Add src to path so "agent" package is importable
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))


def main() -> int:
    from agent.crawl_validate_cleanup_pipeline import (
        run_pipeline,
        POSTS_DIR,
        VALIDATED_DIR,
    )

    print("LangGraph: Crawl -> Validate -> Cleanup & Summarize")
    print("API keys loaded from: project/.env")
    print("Output: legal-luminary/_posts and legal-luminary/_data")
    print("=" * 60)

    result = run_pipeline(posts_dir=POSTS_DIR, validated_dir=VALIDATED_DIR)

    print("\nPipeline finished.")
    print(f"  Posts dir: {result.get('posts_dir')}")
    print(f"  Data dir: {result.get('validated_dir')}")
    print(f"  Crawl total posts: {result.get('crawl_date_aware_count', 'N/A')}")
    print(f"  New posts written: {result.get('crawl_new_count', 'N/A')}")
    print(f"  Validated output: {result.get('validated_output_path', 'N/A')}")
    print(f"  Validated articles: {len(result.get('validated_articles', []))}")
    print(f"  Cleanup results: {len(result.get('cleanup_results', []))}")
    if result.get("errors"):
        print("  Errors:")
        for e in result["errors"]:
            print(f"    - {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
