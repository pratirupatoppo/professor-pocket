import json
import statistics
import time
from pathlib import Path

from .config import DATA_DIR
from .retrieval import Retriever


def evaluate() -> dict:
    questions_path = DATA_DIR / "evaluation" / "questions.json"
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    retriever = Retriever()
    rows = []
    for item in questions:
        started = time.perf_counter()
        results = retriever.search(item["question"], limit=5)
        latency_ms = (time.perf_counter() - started) * 1000
        source_hit = any(result["source_filename"] == item["source"] for result in results)
        term_hit = any(
            all(term.lower() in result["text"].lower() for term in item["terms"])
            for result in results
        )
        rows.append(
            {
                "question": item["question"],
                "source_hit": source_hit,
                "term_hit": term_hit,
                "latency_ms": round(latency_ms, 2),
            }
        )
    report = {
        "question_count": len(rows),
        "source_recall_at_5": round(sum(row["source_hit"] for row in rows) / len(rows), 4),
        "term_recall_at_5": round(sum(row["term_hit"] for row in rows) / len(rows), 4),
        "median_retrieval_latency_ms": round(statistics.median(row["latency_ms"] for row in rows), 2),
        "results": rows,
    }
    output = DATA_DIR / "evaluation" / "retrieval_report.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    result = evaluate()
    print(json.dumps({key: value for key, value in result.items() if key != "results"}, indent=2))
