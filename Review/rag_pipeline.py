from __future__ import annotations

from typing import List, Sequence

from models import ReviewRequest, ReviewResponse, StandardsChunk
from standards_loader import filter_chunks_for_language
from vector_store import StandardsVectorStore, RetrievedRule
from llm_client import generate_review_with_llm


def infer_review_facets(request: ReviewRequest) -> List[str]:
    """
    Heuristic extraction of aspects of the code that should be checked.
    This is intentionally simple and deterministic (no extra LLM call).
    """
    language = request.language.lower()
    code_lower = request.code.lower()
    context_lower = (request.context or "").lower()

    facets: List[str] = [
        "naming conventions and identifier clarity",
        "function length and single-responsibility design",
        "comments and documentation style",
        "error handling and exceptions",
        "duplication and code smells",
    ]

    # If this looks like HTTP / REST code, include API design facets.
    http_markers = ("http", "route", "router", "endpoint", "@app.route", "fastapi", "express", "flask")
    if any(m in code_lower for m in http_markers) or "rest" in context_lower or "api" in context_lower:
        facets.append("HTTP API design, status codes, and error responses")

    # Light language-specific hints.
    if language in ("python", "py"):
        facets.append("Python naming and import organization")
    if language in ("javascript", "typescript", "js", "ts"):
        facets.append("JavaScript/TypeScript async patterns and error handling for promises")

    return facets


def _build_vector_store(chunks: Sequence[StandardsChunk]) -> StandardsVectorStore:
    store = StandardsVectorStore()
    store.fit(chunks)
    return store


def retrieve_relevant_rules(
    request: ReviewRequest,
    all_chunks: Sequence[StandardsChunk],
    top_k_per_facet: int = 5,
    min_score: float = 0.1,
) -> List[StandardsChunk]:
    """
    Multi-step retrieval:
    - Filter corpus for language.
    - Infer facets.
    - For each facet, query the vector store with facet+code.
    - Deduplicate by rule_id, keeping the highest score.
    """
    lang_chunks = filter_chunks_for_language(all_chunks, request.language)
    if not lang_chunks:
        return []

    store = _build_vector_store(lang_chunks)
    facets = infer_review_facets(request)

    best_by_rule: dict[str, RetrievedRule] = {}

    for facet in facets:
        query_text = (
            f"Language: {request.language}\n"
            f"Facet: {facet}\n\n"
            f"Code snippet:\n{request.code[:600]}"
        )
        results = store.query(query_text, top_k=top_k_per_facet)
        for r in results:
            if r.score < min_score:
                continue
            existing = best_by_rule.get(r.chunk.rule_id)
            if existing is None or r.score > existing.score:
                best_by_rule[r.chunk.rule_id] = r

    # Sort by descending score for determinism.
    sorted_rules = sorted(best_by_rule.values(), key=lambda r: r.score, reverse=True)
    return [r.chunk for r in sorted_rules]


def run_rag_review(request: ReviewRequest, all_chunks: Sequence[StandardsChunk]) -> ReviewResponse:
    """
    Top-level RAG pipeline used by the application.
    """
    relevant_chunks = retrieve_relevant_rules(request, all_chunks=all_chunks)

    if not relevant_chunks:
        # No coverage for this language / code.
        return ReviewResponse(
            verdict="no_coverage",
            summary=(
                "No applicable coding standards could be confidently matched for this code and language. "
                "CodeSensei will stay silent rather than guess."
            ),
            positive_feedback=[],
            issues=[],
        )

    return generate_review_with_llm(
        language=request.language,
        code=request.code,
        context=request.context,
        chunks=relevant_chunks,
    )

