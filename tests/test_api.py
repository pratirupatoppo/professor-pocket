from app.web import app


def test_homepage_loads():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Smart Campus Information Assistant" in response.data


def test_health_reports_knowledge_base():
    response = app.test_client().get("/api/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert body["knowledge_chunks"] > 0


def test_empty_question_is_rejected():
    response = app.test_client().post("/api/ask", json={"question": " "})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Please enter a question."


def test_question_returns_grounded_response():
    response = app.test_client().post(
        "/api/ask",
        json={"question": "What is the minimum attendance required for the end-semester examination?"},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert "75%" in body["answer"]
    assert "Sources:" not in body["answer"]
    assert body["sources"]
    assert body["latency_ms"] >= 0
