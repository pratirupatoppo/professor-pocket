import json
import re
from pathlib import Path

from .config import DOCUMENT_METADATA, INDEX_DIR, PROCESSED_DIR, SOURCE_DIR, SOURCE_FILES


def _clean_line(line: str) -> str:
    cleaned = re.sub(r"\s+", " ", line.replace("\f", " ")).strip()
    return cleaned.replace("\ufffd", " - ").strip()


def _is_page_marker(line: str) -> bool:
    return bool(re.fullmatch(r"\d{1,4}", line)) or line.lower() in {
        "guidelines for resident students",
    }


def _heading(line: str) -> bool:
    if len(line) < 4 or len(line) > 180:
        return False
    if re.match(r"^\d+([.)]\d+)*[.)]?\s+[A-Z]", line):
        return True
    letters = [char for char in line if char.isalpha()]
    if not letters:
        return False
    uppercase = sum(char.isupper() for char in letters) / len(letters)
    return uppercase > 0.75 and len(letters) >= 12 and len(line.split()) >= 2


def _make_chunks(text: str, metadata: dict, chunk_size: int = 1800, overlap: int = 240) -> list[dict]:
    lines = [_clean_line(line) for line in text.splitlines()]
    lines = [line for line in lines if line and not _is_page_marker(line)]
    chunks = []
    section = "General"
    current = []
    current_length = 0

    def emit(keep_overlap: bool = False) -> None:
        nonlocal current, current_length
        if not current:
            return
        body = " ".join(current).strip()
        if body:
            chunks.append(
                {
                    "text": body,
                    "heading_path": section,
                    **metadata,
                }
            )
        tail = body[-overlap:] if keep_overlap else ""
        current = [tail] if tail else []
        current_length = len(tail)

    for line in lines:
        if _heading(line):
            if current_length > 0:
                emit()
            section = line
        if current_length + len(line) + 1 > chunk_size:
            emit(keep_overlap=True)
        current.append(line)
        current_length += len(line) + 1
    emit()

    for index, chunk in enumerate(chunks):
        chunk["chunk_id"] = f"{metadata['document_id']}:{index:04d}"
    return chunks


def build_chunks() -> list[dict]:
    chunks = []
    for filename in SOURCE_FILES:
        path = SOURCE_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Source document not found: {path}")
        metadata = {
            "document_id": Path(filename).stem,
            "source_filename": filename,
            **DOCUMENT_METADATA[filename],
        }
        chunks.extend(_make_chunks(path.read_text(encoding="utf-8", errors="replace"), metadata))
    return chunks


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    chunks = build_chunks()
    output = PROCESSED_DIR / "chunks.json"
    output.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(chunks)} chunks to {output}")


if __name__ == "__main__":
    main()
