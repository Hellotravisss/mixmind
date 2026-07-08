"""
Retrieval over the plant knowledge base.

Keeps the plant's facts out of the model's weights: the Copilot looks answers up
here and cites the note id, so swapping the knowledge base swaps the plant.

Two backends:
  - keyword: dependency-free overlap scoring (zero-config baseline).
  - tfidf:   sklearn TF-IDF + cosine, weights rare terms higher.
"""
from __future__ import annotations

from .knowledge import KNOWLEDGE, Note


class Retriever:
    def __init__(self, notes: list[Note] = KNOWLEDGE, backend: str = "tfidf") -> None:
        self.notes = notes
        self.backend = backend
        self._vec = None
        self._mat = None
        if backend == "tfidf":
            from sklearn.feature_extraction.text import TfidfVectorizer
            self._vec = TfidfVectorizer(stop_words="english")
            self._mat = self._vec.fit_transform([n.text for n in notes])

    def retrieve(self, query: str, k: int = 2) -> list[Note]:
        if self.backend == "tfidf":
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(self._vec.transform([query]), self._mat)[0]
            order = sims.argsort()[::-1][:k]
            return [self.notes[i] for i in order]
        qw = set(query.lower().replace("?", " ").split())
        scored = sorted(self.notes,
                        key=lambda n: len(qw & set(n.text.lower().split())),
                        reverse=True)
        return scored[:k]
