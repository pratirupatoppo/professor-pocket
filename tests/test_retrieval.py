import pytest

from app.retrieval import Retriever


@pytest.fixture(scope="module")
def retriever():
    return Retriever()


def test_leave_query_retrieves_residence_policy(retriever):
    results = retriever.search("What are the residence leave procedures?", limit=3)
    assert results
    assert results[0]["source_filename"] == "345_Resident_Student_Policy_2025_26_NC.txt"
    assert "Leave" in results[0]["heading_path"] or "leave" in results[0]["text"].lower()


def test_attendance_query_retrieves_attendance_policy(retriever):
    results = retriever.search(
        "What is the minimum attendance required to appear for the end semester examination?",
        limit=5,
    )
    assert results
    assert any("attendance" in result["text"].lower() for result in results)


def test_empty_query_returns_no_results(retriever):
    assert retriever.search("   ") == []


def test_chroma_index_is_persistent(retriever):
    assert retriever.collection.count() == len(retriever.chunks)


def test_meal_query_retrieves_ug_timings(retriever):
    results = retriever.search("What are the UG residence meal timings?", limit=5)
    assert results
    assert any("UG Residence" in result["text"] and "Lunch" in result["text"] for result in results)
