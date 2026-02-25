from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from models import ReviewRequest, ReviewResponse, StandardsChunk
from rag_pipeline import run_rag_review
from standards_loader import load_standards_corpus


@lru_cache(maxsize=1)
def get_all_standards_chunks() -> tuple[StandardsChunk, ...]:
    """
    Load and cache the standards corpus once per process.
    """
    base_dir = Path(__file__).parent
    standards_dir = base_dir / "standards"
    chunks = load_standards_corpus(standards_dir)
    return tuple(chunks)


def run_review(request: ReviewRequest) -> ReviewResponse:
    """
    Public entry point for running a CodeSensei review.
    """
    all_chunks = get_all_standards_chunks()
    return run_rag_review(request, all_chunks=all_chunks)

