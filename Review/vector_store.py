from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models import StandardsChunk


@dataclass
class RetrievedRule:
    chunk: StandardsChunk
    score: float


class StandardsVectorStore:
    """
    Simple in-memory TF-IDF vector store for standards chunks.
    """

    def __init__(self) -> None:
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix: np.ndarray | None = None
        self._chunks: List[StandardsChunk] = []

    @property
    def is_fitted(self) -> bool:
        return self._vectorizer is not None and self._matrix is not None and len(self._chunks) > 0

    def fit(self, chunks: Sequence[StandardsChunk]) -> None:
        self._chunks = list(chunks)
        texts = [c.text for c in self._chunks]
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = self._vectorizer.fit_transform(texts)

    def query(self, query_text: str, top_k: int = 8) -> List[RetrievedRule]:
        if not self.is_fitted or self._vectorizer is None or self._matrix is None:
            raise RuntimeError("Vector store has not been fitted with any standards.")

        query_vec = self._vectorizer.transform([query_text])
        sims = cosine_similarity(query_vec, self._matrix)[0]

        if top_k <= 0:
            top_k = len(self._chunks)

        top_indices = np.argsort(sims)[::-1][:top_k]
        results: List[RetrievedRule] = []
        for idx in top_indices:
            score = float(sims[idx])
            if score <= 0:
                continue
            results.append(RetrievedRule(chunk=self._chunks[int(idx)], score=score))
        return results

