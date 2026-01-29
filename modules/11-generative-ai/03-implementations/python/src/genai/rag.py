from __future__ import annotations

from dataclasses import dataclass

from .chunking import chunk_text
from .vectorstore import Doc, ScoredDoc, TfidfVectorStore


@dataclass
class RAGPipeline:
    docs: list[Doc]
    chunk_size: int = 500
    overlap: int = 50

    def __post_init__(self) -> None:
        self._store = TfidfVectorStore()
        self._chunk_docs: list[Doc] = []
        self._build_index()

    def _build_index(self) -> None:
        chunk_docs: list[Doc] = []
        for doc in self.docs:
            chunks = chunk_text(doc.text, self.chunk_size, self.overlap)
            for idx, chunk in enumerate(chunks):
                chunk_id = f"{doc.id}:{idx}"
                chunk_meta = {"parent_id": doc.id, **doc.meta}
                chunk_docs.append(Doc(id=chunk_id, text=chunk, meta=chunk_meta))
        self._chunk_docs = chunk_docs
        self._store.fit(self._chunk_docs)

    def retrieve(self, query: str, k: int = 3) -> list[ScoredDoc]:
        return self._store.query(query, k)

    def synthesize(self, query: str, contexts: list[ScoredDoc]) -> str:
        if not contexts:
            return f"Answer to '{query}'. Sources: []"
        citations = ", ".join(doc.id for doc in contexts)
        return f"Answer to '{query}'. Sources: [{citations}]"
