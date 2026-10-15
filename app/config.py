from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = PROJECT_ROOT
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
VECTORIZER_PATH = INDEX_DIR / "tfidf_vectorizer.joblib"
CHROMA_COLLECTION = "campus_policy_chunks"

SOURCE_FILES = (
    "345_Resident_Student_Policy_2025_26_NC.txt",
    "MOP1.txt",
    "Mop_UG_AY 2023-24.txt",
)

DOCUMENT_METADATA = {
    "345_Resident_Student_Policy_2025_26_NC.txt": {
        "title": "Guidelines for Resident Students 2025-26",
        "scope": "residence",
        "audience": ["UG", "PG", "PhD", "resident"],
        "academic_year": "2025-26",
        "source_priority": 1,
    },
    "Mop_UG_AY 2023-24.txt": {
        "title": "Student Manual of Policies - Undergraduate Programmes",
        "scope": "university-wide",
        "audience": ["UG"],
        "academic_year": "2023-24",
        "source_priority": 2,
    },
    "MOP1.txt": {
        "title": "XCOMM Student Manual of Policies",
        "scope": "school-specific",
        "school": "XCOMM",
        "audience": ["BSc Mass Communication", "MA Mass Communication"],
        "academic_year": "2020",
        "source_priority": 3,
    },
}
