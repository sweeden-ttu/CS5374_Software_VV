"""Evidence Validator - Prioritizes relevant legal/political articles.

Scores articles based on keyword relevance for legal and governmental content.
Reads from legal-luminary/_posts, writes ranked output to legal-luminary/_data/important_articles.json.
Override via LEGAL_LUMINARY_POSTS and LEGAL_LUMINARY_DATA in .env.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

_LEGAL_LUMINARY_DEFAULT = Path("/Volumes/RepoPart1/legal-luminary")
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

POSTS_DIR = Path(os.environ.get("LEGAL_LUMINARY_POSTS", str(_LEGAL_LUMINARY_DEFAULT / "_posts")))
VALIDATED_DIR = Path(os.environ.get("LEGAL_LUMINARY_DATA", str(_LEGAL_LUMINARY_DEFAULT / "_data")))
VALIDATED_DIR.mkdir(parents=True, exist_ok=True)

_ALLOWLIST_ENV = os.environ.get("LEGAL_LUMINARY_ALLOWLIST")
if _ALLOWLIST_ENV:
    ALLOWLIST_PATH = Path(_ALLOWLIST_ENV)
else:
    _project_allowlist = _PROJECT_ROOT / "config" / "allowlist.json"
    _ll_allowlist = _LEGAL_LUMINARY_DEFAULT / "demos" / "langsmith_langgraph_demo" / "allowlist.json"
    ALLOWLIST_PATH = _project_allowlist if _project_allowlist.exists() else _ll_allowlist

MAX_AGE_DAYS = 90  # 3 months

PRIORITY_KEYWORDS = [
    ("critical", ["tdcj", "texas department criminal justice", "prison", "inmate"]),
    ("critical", ["senate", "senator", "state senate"]),
    ("critical", ["congress", "congressman", "congresswoman", "us house"]),
    ("critical", ["election", "voter", "ballot", "voting"]),
    ("critical", ["law", "legislature", "legislation", "bill"]),
    ("high", ["investigat", "investigation", "probe", "inquiry"]),
    ("high", ["party", "republican", "democrat", "gop"]),
    ("high", ["candidate", "campaign", "electoral"]),
    ("medium", ["appoint", "appointed", "governor", "judge"]),
    ("medium", ["court", "ruling", "verdict", "judicial"]),
    ("medium", ["attorney", "lawyer", "legal"]),
]

CRITICAL_SCORE = 100
HIGH_SCORE = 50
MEDIUM_SCORE = 25
LOW_SCORE = 10

KEYWORD_SCORES = {
    "critical": CRITICAL_SCORE,
    "high": HIGH_SCORE,
    "medium": MEDIUM_SCORE,
    "low": LOW_SCORE,
}


def load_allowlist() -> Dict[str, Any]:
    if ALLOWLIST_PATH.exists():
        return json.loads(ALLOWLIST_PATH.read_text())
    return {}


def calculate_relevance_score(content: str, title: str = "") -> Dict[str, Any]:
    """Calculate relevance score based on priority keywords."""
    text = (title + " " + content).lower()

    scores = []
    matched_keywords = []

    for priority, keywords in PRIORITY_KEYWORDS:
        for keyword in keywords:
            count = len(re.findall(keyword, text, re.IGNORECASE))
            if count > 0:
                score = KEYWORD_SCORES[priority] * count
                scores.append(score)
                matched_keywords.append(
                    {
                        "keyword": keyword,
                        "priority": priority,
                        "count": count,
                        "score": score,
                    }
                )

    total_score = sum(scores)

    if total_score >= CRITICAL_SCORE:
        relevance = "critical"
    elif total_score >= HIGH_SCORE:
        relevance = "high"
    elif total_score >= MEDIUM_SCORE:
        relevance = "medium"
    else:
        relevance = "low"

    return {
        "total_score": total_score,
        "relevance": relevance,
        "matched_keywords": sorted(
            matched_keywords, key=lambda x: x["score"], reverse=True
        )[:10],
    }


def validate_article(post_path: Path, allowlist: Dict) -> Dict[str, Any]:
    """Validate a single article."""
    content = post_path.read_text(encoding="utf-8", errors="replace")

    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        return {"error": "Invalid frontmatter", "path": str(post_path)}

    frontmatter = frontmatter_match.group(1)

    title_match = re.search(
        r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE
    )
    title = title_match.group(1) if title_match else ""

    date_match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", frontmatter, re.MULTILINE)
    date = date_match.group(1) if date_match else ""

    source_match = re.search(
        r'^source_name:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE
    )
    source = source_match.group(1) if source_match else ""

    url_match = re.search(
        r'^source_url:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE
    )
    url = url_match.group(1) if url_match else ""

    body = content[len(frontmatter_match.group(0)) :].strip()

    relevance = calculate_relevance_score(body, title)

    return {
        "title": title,
        "date": date,
        "source": source,
        "url": url,
        "path": str(post_path),
        "score": relevance["total_score"],
        "relevance": relevance["relevance"],
        "matched_keywords": relevance["matched_keywords"],
    }


def main():
    """Main validator entry point. Reads from legal-luminary/_posts, writes to legal-luminary/_data/important_articles.json."""
    # Re-read env so pipeline overrides take effect
    _posts = Path(os.environ.get("LEGAL_LUMINARY_POSTS", str(_LEGAL_LUMINARY_DEFAULT / "_posts")))
    _data = Path(os.environ.get("LEGAL_LUMINARY_DATA", str(_LEGAL_LUMINARY_DEFAULT / "_data")))
    _data.mkdir(parents=True, exist_ok=True)

    print("Evidence Validator - Priority Keyword Scoring")
    print("=" * 50)
    print(f"  Posts: {_posts}")
    print(f"  Data:  {_data}")

    allowlist = load_allowlist()
    allowed_domains = [d.lower() for d in allowlist.get("domains", [])]

    posts = sorted(
        _posts.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True
    )

    cutoff_date = datetime.now() - timedelta(days=MAX_AGE_DAYS)
    validated = []
    skipped = 0

    for post in posts:
        result = validate_article(post, allowlist)

        if "error" not in result:
            try:
                article_date = datetime.strptime(result["date"], "%Y-%m-%d")
                if article_date < cutoff_date:
                    skipped += 1
                    continue
            except:
                pass
            validated.append(result)

    print(f"Skipped {skipped} articles older than 3 months")

    validated.sort(key=lambda x: x["score"], reverse=True)

    output = {
        "validated_at": datetime.now().isoformat(),
        "total_articles": len(validated),
        "by_relevance": {
            "critical": [a for a in validated if a["relevance"] == "critical"],
            "high": [a for a in validated if a["relevance"] == "high"],
            "medium": [a for a in validated if a["relevance"] == "medium"],
            "low": [a for a in validated if a["relevance"] == "low"],
        },
        "all_articles": validated,
    }

    output_file = _data / "important_articles.json"
    output_file.write_text(json.dumps(output, indent=2))
    print(f"Saved: {output_file}")

    print(f"\n=== Summary ===")
    print(f"Total articles: {len(validated)}")
    print(f"Critical: {len(output['by_relevance']['critical'])}")
    print(f"High: {len(output['by_relevance']['high'])}")
    print(f"Medium: {len(output['by_relevance']['medium'])}")
    print(f"Low: {len(output['by_relevance']['low'])}")

    print(f"\n=== Top 10 Articles ===")
    for i, article in enumerate(validated[:10], 1):
        print(
            f"{i}. [{article['relevance'].upper()}] {article['date']} - {article['title'][:50]}"
        )
        print(
            f"   Score: {article['score']} | Keywords: {', '.join([k['keyword'] for k in article['matched_keywords'][:3]])}"
        )


if __name__ == "__main__":
    main()
