import json
import pickle
import re
from pathlib import Path

import chromadb
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import CHROMA_COLLECTION, CHROMA_DIR, INDEX_DIR, PROCESSED_DIR, VECTORIZER_PATH


class TfidfEmbeddingFunction:
    def __init__(self, vectorizer: TfidfVectorizer) -> None:
        self.vectorizer = vectorizer

    def is_legacy(self) -> bool:
        return False

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.vectorizer.transform(input).toarray().tolist()

    def name(self) -> str:
        return "campus-tfidf"

    def supported_spaces(self) -> list[str]:
        return ["cosine"]

    def get_config(self) -> dict:
        return {"name": self.name(), "space": "cosine"}


class Retriever:
    def __init__(self, chunks_path: Path | None = None, rebuild: bool = False) -> None:
        path = chunks_path or PROCESSED_DIR / "chunks.json"
        if not path.exists():
            raise FileNotFoundError("Knowledge base is missing. Run `python -m app.ingest` first.")
        self.chunks = json.loads(path.read_text(encoding="utf-8"))
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        try:
            self.vectorizer = joblib.load(VECTORIZER_PATH) if not rebuild else None
        except (EOFError, OSError, pickle.UnpicklingError, ValueError):
            self.vectorizer = None
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.vectorizer.fit(chunk["text"] for chunk in self.chunks)
            joblib.dump(self.vectorizer, VECTORIZER_PATH)
        self.matrix = self.vectorizer.transform(chunk["text"] for chunk in self.chunks)
        self.embedding_function = TfidfEmbeddingFunction(self.vectorizer)
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            configuration={"hnsw": {"space": "cosine"}},
        )
        if rebuild or self.collection.count() != len(self.chunks):
            self._rebuild_collection()

    def _rebuild_collection(self) -> None:
        try:
            self.client.delete_collection(CHROMA_COLLECTION)
        except ValueError:
            pass
        self.collection = self.client.create_collection(
            name=CHROMA_COLLECTION,
            configuration={"hnsw": {"space": "cosine"}},
        )
        self.collection.add(
            ids=[chunk["chunk_id"] for chunk in self.chunks],
            documents=[chunk["text"] for chunk in self.chunks],
            metadatas=[self._metadata(chunk) for chunk in self.chunks],
            embeddings=self.embedding_function([chunk["text"] for chunk in self.chunks]),
        )

    @staticmethod
    def _metadata(chunk: dict) -> dict:
        return {
            key: json.dumps(value) if isinstance(value, list) else str(value)
            for key, value in chunk.items()
            if key != "text"
        }

    @staticmethod
    def _tokens(value: str) -> set[str]:
        return set(re.findall(r"[a-z0-9%₹-]+", value.lower()))

    def search(self, query: str, limit: int = 5) -> list[dict]:
        if not query.strip():
            return []
        results = self.collection.query(
            query_embeddings=self.embedding_function([query]),
            n_results=min(max(limit * 5, limit), len(self.chunks)),
            include=["documents", "metadatas", "distances"],
        )
        query_tokens = self._tokens(query)
        residence_terms = {"residence", "hostel", "mess", "fretbox", "room", "resident"}
        academic_terms = {"semester", "examination", "attendance", "grade", "course", "cgpa", "sgpa"}
        wants_residence = bool(query_tokens & residence_terms)
        wants_academic = bool(query_tokens & academic_terms)
        topic_terms = query_tokens - {"what", "are", "the", "is", "for", "to", "a", "an", "how", "can", "of"}
        chroma_scores = {}
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chroma_scores[metadata["chunk_id"]] = max(0.0, 1.0 - float(distance))

        tfidf_scores = cosine_similarity(
            self.vectorizer.transform([query]),
            self.matrix,
        )[0]
        ranked = []
        for index, score in enumerate(tfidf_scores):
            chunk = self.chunks[index]
            score = 0.7 * float(score) + 0.3 * chroma_scores.get(chunk["chunk_id"], 0.0)
            chunk_tokens = self._tokens(chunk["text"])
            exact_bonus = len(query_tokens & chunk_tokens) * 0.01
            topic_bonus = len(topic_terms & chunk_tokens) * 0.03
            scope_bonus = 0.0
            if wants_residence and chunk.get("scope") == "residence":
                scope_bonus = 0.25
                if "leave" in query_tokens and "leave" in chunk_tokens:
                    scope_bonus += 0.3
            elif wants_academic and chunk.get("scope") == "university-wide":
                scope_bonus = 0.04
            ranked.append((float(score) + exact_bonus + topic_bonus + scope_bonus, chunk))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [{**chunk, "score": round(score, 4)} for score, chunk in ranked[:limit] if score > 0]


def build_index() -> None:
    Retriever(rebuild=True)
    print(f"Built ChromaDB index at {CHROMA_DIR}")


if __name__ == "__main__":
    build_index()
