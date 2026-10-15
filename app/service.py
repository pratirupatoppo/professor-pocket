import time

from .llm import OllamaClient
from .retrieval import Retriever


class CampusAssistant:
    def __init__(self) -> None:
        self.retriever = Retriever()
        self.llm = OllamaClient()

    def ask(self, question: str) -> dict:
        started = time.perf_counter()
        evidence = self.retriever.search(question)
        answer = self.llm.answer(question, evidence[:3])
        sources = [
            {
                "document": item["source_filename"],
                "section": item["heading_path"],
                "score": item["score"],
            }
            for item in evidence
        ]
        return {
            "answer": answer,
            "sources": sources,
            "evidence_count": len(evidence),
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        }
