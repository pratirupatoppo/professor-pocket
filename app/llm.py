import os

import requests


class OllamaClient:
    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
        self.base_url = (base_url or os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")).rstrip("/")

    def answer(self, question: str, evidence: list[dict]) -> str:
        if not evidence:
            return "I could not find enough information in the verified campus documents to answer that question."
        context = "\n\n".join(
            item["text"]
            for item in evidence
        )
        prompt = (
            "You are the Smart Campus Information Assistant. Answer only from the evidence below. "
            "If the evidence is insufficient, say so. Do not invent rules, dates, fees, contacts, or timings. "
            "If the evidence contains a matching rule, summarize that rule directly even if the section heading "
            "is imperfect. Do not mention sources, documents, evidence, or sections. Keep the answer concise "
            "and procedural, using no more than three short sentences.\n\n"
            f"Question: {question}\n\nEvidence:\n{context}"
        )
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": -1,
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 4096,
                        "num_predict": 128,
                    },
                },
                timeout=90,
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.RequestException as exc:
            raise RuntimeError(
                "Ollama is unavailable. Install and start Ollama, then pull the configured model."
            ) from exc
