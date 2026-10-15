# Smart Campus Information Chatbot

Mid-semester software prototype for the Thesis-I project **Edge AI-Based Smart
Campus Information Robot Using Small Language Models (SLMs)**.

This phase builds the AI brain only: document ingestion, campus-policy
retrieval, grounded answer generation, and a browser chat interface. Physical
robot hardware, navigation, sensors, speech recognition, and text-to-speech are
not part of this phase.

## Mid-semester phases

1. **Foundation** — Python project, dependencies, configuration, and Flask
   shell. **Complete**
2. **Knowledge base** — clean and chunk the three supplied campus documents
   with source metadata. **Initial version complete**
3. **RAG retrieval** — hybrid exact/vector retrieval and retrieval evaluation.
   **Complete with persistent ChromaDB index and tests**
4. **Chatbot API** — connect retrieved evidence to a local Ollama SLM and add
   missing-evidence handling. **Complete**
5. **Chat interface** — browser chat UI with concise answers and uncertainty
   states. **Complete**
   **Initial version complete**
6. **Evaluation** — curated questions, correctness, retrieval, attribution,
   and latency report. **Next**

## Setup

The current development environment uses Python 3.13.

```powershell
& 'C:\Users\PRATIRUPA\AppData\Local\Programs\Python\Python313\python.exe' -m pip install -r requirements.txt
```

Build the local knowledge base:

```powershell
& 'C:\Users\PRATIRUPA\AppData\Local\Programs\Python\Python313\python.exe' -m app.ingest
```

Build the persistent ChromaDB retrieval index:

```powershell
& 'C:\Users\PRATIRUPA\AppData\Local\Programs\Python\Python313\python.exe' -m app.retrieval
```

Run retrieval tests:

```powershell
& 'C:\Users\PRATIRUPA\AppData\Local\Programs\Python\Python313\python.exe' -m pytest tests\test_retrieval.py -q
```

Start the website:

```powershell
& 'C:\Users\PRATIRUPA\AppData\Local\Programs\Python\Python313\python.exe' run.py
```

Open `http://127.0.0.1:5000`.

## Public deployment as Professor Pocket

The repository includes a Render Blueprint in `render.yaml`. To deploy it,
connect this project to a GitHub repository, create a new Render Blueprint,
and select `render.yaml`. The service is named `professor-pocket`.

Because Render cannot reach the Ollama process on a local Windows computer,
set `OLLAMA_URL` in the Render service environment to a reachable
Ollama-compatible endpoint before asking questions. The web interface and
retrieval index can deploy without it, but generation requests will return a
service error until the model endpoint is configured.

## Local SLM

The Flask API uses Ollama at `http://127.0.0.1:11434` and defaults to the
smaller `qwen2.5:1.5b` model for faster CPU responses. After Ollama is
installed, download the model:

```powershell
ollama pull qwen2.5:1.5b
```

You can select another model without changing code:

```powershell
$env:OLLAMA_MODEL = 'qwen2.5:3b'
```

If Ollama is unavailable, the API returns an explicit service error rather than
showing an ungrounded answer.

The browser intentionally does not display source labels in the answer. Source
metadata remains available in the API response for evaluation and auditing.

## Source documents

The initial knowledge base uses the three policy manuals in this folder.
Generated chunks are written to `data\processed\chunks.json`; generated data is
ignored by Git and can be rebuilt from the original documents.
