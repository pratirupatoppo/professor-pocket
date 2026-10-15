from flask import Flask, jsonify, render_template, request

from .service import CampusAssistant

app = Flask(__name__, template_folder="../templates", static_folder="../static")
assistant = None


def get_assistant() -> CampusAssistant:
    global assistant
    if assistant is None:
        assistant = CampusAssistant()
    return assistant


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        service = get_assistant()
        return jsonify(
            {
                "status": "ok",
                "knowledge_chunks": len(service.retriever.chunks),
                "model": service.llm.model,
            }
        )
    except (FileNotFoundError, RuntimeError) as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    try:
        return jsonify(get_assistant().ask(question))
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception:
        app.logger.exception("Unexpected chatbot request failure")
        return jsonify({"error": "The assistant encountered an unexpected error."}), 500


if __name__ == "__main__":
    app.run(debug=True)
