"""LangSmith + LangGraph Validation Demo.

This module captures evidence artifacts from LLM evaluation of site content
and constructs a verification graph with allowlist-based source validation.

Integrated from legal-luminary demos/langsmith_langgraph_demo.

Pipeline Nodes:
  1. extract_content - Fetch and hash site snapshot
  2. evidence_verification - Router node using allowlist as Test Oracle
  3. content_generation - Create verified content (only if verified)
  4. evaluator_node - Assess quality and toxicity

Usage:
    from agent.langsmith_demo import run_validation_pipeline

    result = run_validation_pipeline(
        source_text="content to validate",
        source_url="https://example.com"
    )
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Literal, Optional, TypedDict

from langgraph.graph import StateGraph, START, END

try:
    from langsmith import Client

    HAS_LANGSMITH = True
except ImportError:
    HAS_LANGSMITH = False


ALLOWLIST_PATH = Path(__file__).parent.parent.parent / "config" / "allowlist.json"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output" / "langsmith_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_allowlist() -> Dict[str, Any]:
    if ALLOWLIST_PATH.exists():
        with open(ALLOWLIST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"domains": [], "contacts": [], "social_media_accounts": []}


def canonicalize_url(url: str) -> str:
    u = url.strip().lower()
    for prefix in ["http://", "https://"]:
        if u.startswith(prefix):
            u = u[len(prefix) :]
    if u.endswith("/"):
        u = u[:-1]
    return u


class ValidationState(TypedDict, total=False):
    snapshot_id: str
    snapshot: Dict[str, Any]
    source_text: str
    source_url: str
    content_hash: str
    domain: str
    verified: bool
    generated: Optional[Dict[str, Any]]
    evaluation: Optional[Dict[str, Any]]
    decision: str
    evidence: list
    error: Optional[str]


def node_extract_content(state: ValidationState) -> Dict[str, Any]:
    source_text = state.get("source_text", "")
    source_url = state.get("source_url", "")

    snapshot_id = str(uuid.uuid4())
    content_hash = compute_hash(source_text)
    domain = canonicalize_url(source_url) if source_url else ""

    snapshot = {
        "id": snapshot_id,
        "text": source_text[:5000],
        "url": source_url,
        "sha256": content_hash,
        "timestamp": now_iso(),
        "domain": domain,
    }

    output_path = OUTPUT_DIR / f"snapshot-{snapshot_id}.json"
    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    return {
        "snapshot_id": snapshot_id,
        "snapshot": snapshot,
        "content_hash": content_hash,
        "domain": domain,
        "evidence": [{"type": "snapshot", "id": snapshot_id}],
    }


def node_evidence_verification(state: ValidationState) -> Dict[str, Any]:
    allowlist = load_allowlist()
    domain = state.get("domain", "")

    domain_valid = False
    matched_domain = None

    for allowed in allowlist.get("domains", []):
        canonical_allowed = canonicalize_url(allowed)
        if domain == canonical_allowed or domain.endswith("." + canonical_allowed):
            domain_valid = True
            matched_domain = canonical_allowed
            break

    content_valid = len(state.get("source_text", "")) > 50

    verification = {
        "id": str(uuid.uuid4()),
        "timestamp": now_iso(),
        "domain": domain,
        "domain_valid": domain_valid,
        "matched_domain": matched_domain,
        "content_valid": content_valid,
        "verified": domain_valid and content_valid,
    }

    output_path = OUTPUT_DIR / f"verification-{verification['id']}.json"
    with open(output_path, "w") as f:
        json.dump(verification, f, indent=2)

    evidence = list(state.get("evidence", []))
    evidence.append({"type": "verification", "id": verification["id"]})

    return {
        "verified": verification["verified"],
        "decision": "ACCEPT" if verification["verified"] else "REJECT",
        "evidence": evidence,
    }


def route_verification(state: ValidationState) -> Literal["generate", "reject"]:
    return "generate" if state.get("verified") else "reject"


def node_content_generation(state: ValidationState) -> Dict[str, Any]:
    if not state.get("verified"):
        return {"generated": None}

    snapshot = state.get("snapshot", {})
    source_url = snapshot.get("url", "")
    content_hash = snapshot.get("sha256", "")
    text = snapshot.get("text", "")

    markdown = f"""---
title: Verified Content
source: {source_url}
verification_hash: {content_hash}
verification_date: {now_iso()}
---

{text}
"""

    generated = {
        "id": str(uuid.uuid4()),
        "content": markdown,
        "path": f"staging/generated-{uuid.uuid4().hex[:8]}.md",
        "timestamp": now_iso(),
    }

    output_path = OUTPUT_DIR / f"generated-{generated['id']}.json"
    with open(output_path, "w") as f:
        json.dump(generated, f, indent=2)

    evidence = list(state.get("evidence", []))
    evidence.append({"type": "generated", "id": generated["id"]})

    return {"generated": generated, "evidence": evidence}


def node_reject(state: ValidationState) -> Dict[str, Any]:
    rejection = {
        "id": str(uuid.uuid4()),
        "timestamp": now_iso(),
        "reason": "Domain not in allowlist or content below threshold",
        "domain": state.get("domain"),
    }

    output_path = OUTPUT_DIR / f"rejection-{rejection['id']}.json"
    with open(output_path, "w") as f:
        json.dump(rejection, f, indent=2)

    evidence = list(state.get("evidence", []))
    evidence.append({"type": "rejection", "id": rejection["id"]})

    return {"evidence": evidence, "error": "Content rejected"}


def node_evaluator(state: ValidationState) -> Dict[str, Any]:
    generated = state.get("generated")
    content = generated.get("content", "") if generated else ""

    score = 0.5
    if "law" in content.lower() or "court" in content.lower():
        score = 0.85
    if len(content) < 100:
        score = 0.3

    toxicity = 0.1 if "offensive" not in content.lower() else 0.9
    accepted = (toxicity < 0.8) and (score >= 0.5)

    evaluation = {
        "id": str(uuid.uuid4()),
        "timestamp": now_iso(),
        "score": score,
        "toxicity": toxicity,
        "accepted": accepted,
    }

    output_path = OUTPUT_DIR / f"evaluation-{evaluation['id']}.json"
    with open(output_path, "w") as f:
        json.dump(evaluation, f, indent=2)

    evidence = list(state.get("evidence", []))
    evidence.append({"type": "evaluation", "id": evaluation["id"]})

    return {"evaluation": evaluation, "evidence": evidence}


def build_langsmith_demo_graph() -> StateGraph:
    graph_builder = StateGraph(ValidationState)

    graph_builder.add_node("extract_content", node_extract_content)
    graph_builder.add_node("evidence_verification", node_evidence_verification)
    graph_builder.add_node("content_generation", node_content_generation)
    graph_builder.add_node("reject", node_reject)
    graph_builder.add_node("evaluator", node_evaluator)

    graph_builder.add_edge(START, "extract_content")
    graph_builder.add_edge("extract_content", "evidence_verification")

    graph_builder.add_conditional_edges(
        "evidence_verification",
        route_verification,
        {"generate": "content_generation", "reject": "reject"},
    )

    graph_builder.add_edge("content_generation", "evaluator")
    graph_builder.add_edge("evaluator", END)
    graph_builder.add_edge("reject", END)

    return graph_builder.compile()


langsmith_demo_graph = build_langsmith_demo_graph()


def run_validation_pipeline(
    source_text: str,
    source_url: str = None,
) -> Dict[str, Any]:
    """Run the validation pipeline on content.

    Args:
        source_text: Text content to validate
        source_url: Optional source URL for domain verification

    Returns:
        Final state with verification results and evidence
    """
    graph = build_langsmith_demo_graph()
    initial_state: ValidationState = {
        "source_text": source_text,
        "source_url": source_url or "",
        "evidence": [],
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    test_content = """
    Bell County Courthouse Information
    
    The Bell County Courthouse serves residents of Bell County, Texas.
    Located in Belton, the courthouse provides various legal services
    including court proceedings, record keeping, and administrative functions.
    
    For more information, contact the Bell County Clerk's office.
    """

    print("=" * 70)
    print("LangSmith Demo: Content Validation Pipeline")
    print("=" * 70)

    print("\n--- Test 1: Invalid Source ---")
    result1 = run_validation_pipeline(
        source_text=test_content, source_url="https://unknown-source.com"
    )
    print(f"Decision: {result1.get('decision')}")
    print(f"Verified: {result1.get('verified')}")

    print("\n--- Test 2: Valid Source ---")
    result2 = run_validation_pipeline(
        source_text=test_content, source_url="https://bellcountytx.gov/courthouse"
    )
    print(f"Decision: {result2.get('decision')}")
    print(f"Verified: {result2.get('verified')}")
    if result2.get("evaluation"):
        print(f"Evaluation Score: {result2['evaluation'].get('score')}")
