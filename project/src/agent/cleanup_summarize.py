"""Manual cleanup and OpenAI summarization for Jekyll posts.

Reads each post, strips junk (Skip to content, ads, nav, repeated headers),
keeps full article content, and asks OpenAI for a summary. Overwrites the
markdown file with the summary as the body and sets excerpt to a short teaser.
"""

from __future__ import annotations

import os
from pathlib import Path

# Load .env for OPENAI_API_KEY
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
except ImportError:
    pass

import re
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# Junk line patterns (same idea as legal-luminary post_quality_validator)
JUNK_LINE_PATTERNS = [
    r"^\s*Skip to content\s*$",
    r"^\s*Skip Navigation\s*$",
    r"^\s*RIGHT NOW\s*$",
    r"^\s*Advertise\s*$",
    r"^\s*ADVERTISE WITH US\s*$",
    r"^\s*Be Remarkable\s*$",
    r"^\s*Restaurant Report Card\s*$",
    r"^\s*Tell Me Something Good\s*$",
    r"^\s*Legal Minute\s*$",
    r"^\s*Minuto Legal\s*$",
    r"^\s*\d+°\s*$",
    r"^\s*(?:Waco|Austin),?\s*TX\s*[»]?\s*$",
    r"^\s*News\s*$",
    r"^\s*Weather\s*$",
    r"^\s*Sports\s*$",
    r"^\s*LOCAL\s*$",
    r"^\s*DEFENDERS\s*$",
    r"^\s*Obituaries\s*$",
    r"^\s*Subscribe\s*$",
    r"^\s*Advertisement(s?)\s*$",
    r"^\s*Sponsored\s*$",
    r"^\s*More Videos\s*$",
]

SOURCE_HEADER = re.compile(r"^##\s*Source Information\s*$", re.IGNORECASE)

# Max characters sent to LLM for summarization (allow longer articles)
MAX_INPUT_CHARS = 12000


def parse_front_matter_and_body(content: str) -> tuple[Dict[str, Any], str]:
    """Parse Jekyll front matter and body. Returns (front_matter_dict, body_text)."""
    fm: Dict[str, Any] = {}
    body = content
    if content.strip().startswith("---") and yaml:
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except Exception:
                pass
            body = parts[2].lstrip("\n")
    return fm, body


def _is_junk_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    for pat in JUNK_LINE_PATTERNS:
        if re.match(pat, s, re.IGNORECASE):
            return True
    return False


def _split_body_and_source(body: str) -> tuple[str, str]:
    """Split body into article part and ## Source Information section."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if SOURCE_HEADER.match(line.strip()):
            return "\n".join(lines[:i]).strip(), "\n".join(lines[i:]).strip()
    return body.strip(), ""


def clean_body(body: str) -> tuple[str, str]:
    """Remove junk lines only; keep full article content. Returns (article_part, source_section)."""
    lines = [ln for ln in body.split("\n") if not _is_junk_line(ln)]
    cleaned = "\n".join(lines).strip()
    article_part, source_section = _split_body_and_source(cleaned)
    return article_part.strip(), source_section.strip()


SUMMARY_SYSTEM_PROMPT = """You are an editor writing a comprehensive summary for a news article.

Your task: read the article and produce a detailed summary that will replace the raw article body on a news site. The summary must:

1. Be written in clear, neutral, third-person prose suitable for a legal/community news site.
2. Cover the main point in the first 1–2 sentences (who, what, when, where).
3. Include key facts, figures, quotes (if notable), and context.
4. Explain why it matters or what happens next when relevant.
5. Be substantive: aim for roughly 2–5 short paragraphs (or equivalent length). Do not reduce the article to a single short sentence unless the source is genuinely a one-line item.
6. Preserve any important names, dates, locations, and outcomes. Do not invent details not present in the source.
7. Output only the summary text, no headings or labels."""


def summarize_with_langchain(title: str, body: str) -> Optional[str]:
    """Produce a comprehensive, detailed article summary with LangChain (OpenAI). Returns None if unavailable."""
    if not HAS_LANGCHAIN:
        return None
    if not body or not body.strip():
        return None
    try:
        import os
        if not os.environ.get("OPENAI_API_KEY"):
            return None
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        text = f"Title: {title}\n\n{body}"[:MAX_INPUT_CHARS]
        messages = [
            SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
            HumanMessage(content=text),
        ]
        response = llm.invoke(messages)
        return (response.content or "").strip() or None
    except Exception:
        return None


def excerpt_from_summary(full_summary: str, max_sentences: int = 2, max_chars: int = 320) -> str:
    """Derive a short excerpt from the full summary (first 1–2 sentences) for front matter."""
    if not full_summary:
        return ""
    s = full_summary.strip()
    parts = re.split(r"(?<=[.!?])\s+", s)
    excerpt = " ".join(parts[:max_sentences]).strip() if parts else s
    if not excerpt:
        excerpt = s
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 3].rsplit(" ", 1)[0] + "..."
    return excerpt


def cleanup_and_summarize_post(post_path: Path) -> Dict[str, Any]:
    """
    Read post, clean junk only (keep full content), get comprehensive LLM summary,
    then overwrite the markdown file with: front matter (excerpt = short teaser) and
    body = full detailed summary + Source Information block.
    Returns dict with keys: path, cleaned, summary_set, error (if any).
    """
    result: Dict[str, Any] = {"path": str(post_path), "cleaned": False, "summary_set": False}
    try:
        content = post_path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front_matter_and_body(content)
        article_part, source_section = clean_body(body)
        title = (fm.get("title") or "") if isinstance(fm.get("title"), str) else ""

        # Get comprehensive detailed summary from LLM; use full article text
        summary = summarize_with_langchain(title, article_part)

        if summary:
            excerpt = excerpt_from_summary(summary)
            if fm.get("news_excerpt") is not False and excerpt:
                fm["excerpt"] = excerpt
            result["summary_set"] = True
            # Body = full LLM summary + Source Information block
            body_to_write = summary
            if source_section:
                body_to_write = body_to_write + "\n\n" + source_section
        else:
            # No LLM summary: keep cleaned article content + source section
            body_to_write = article_part
            if source_section:
                body_to_write = (body_to_write + "\n\n" + source_section) if body_to_write else source_section

        if yaml:
            new_content = "---\n" + yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip() + "\n---\n\n" + body_to_write
        else:
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if fm_match:
                fm_block = fm_match.group(1)
                if summary and excerpt and fm.get("news_excerpt") is not False and "excerpt:" not in fm_block:
                    fm_block = fm_block.rstrip() + "\nexcerpt: " + repr(excerpt) + "\n"
                new_content = "---\n" + fm_block + "\n---\n\n" + body_to_write
            else:
                new_content = "---\n\n---\n\n" + body_to_write

        post_path.write_text(new_content, encoding="utf-8")
        result["cleaned"] = True
    except Exception as e:
        result["error"] = str(e)
    return result


def cleanup_and_summarize_all_posts(posts_dir: Path) -> List[Dict[str, Any]]:
    """Run cleanup + summarization on every .md file in posts_dir (non-dotfiles)."""
    results = []
    for path in sorted(posts_dir.glob("*.md")):
        if path.name.startswith("."):
            continue
        results.append(cleanup_and_summarize_post(path))
    return results


def main() -> None:
    import os
    posts_dir = Path(
        os.environ.get("LEGAL_LUMINARY_POSTS", "/Volumes/RepoPart1/legal-luminary/_posts")
    )
    if not posts_dir.exists():
        print(f"Posts directory not found: {posts_dir}")
        return
    print("Cleanup and summarize posts")
    print("=" * 50)
    print(f"  Posts: {posts_dir}")
    results = cleanup_and_summarize_all_posts(posts_dir)
    cleaned = sum(1 for r in results if r.get("cleaned"))
    summarized = sum(1 for r in results if r.get("summary_set"))
    errors = [r for r in results if r.get("error")]
    print(f"\nDone: {len(results)} posts processed, {cleaned} cleaned, {summarized} summarized.")
    if errors:
        for r in errors:
            print(f"  Error {r['path']}: {r['error']}")


if __name__ == "__main__":
    main()
