RAG Service Lab
================

Use case
--------
RAG Service Lab is a small example project that demonstrates a Retrieval-Augmented Generation (RAG) workflow.  It shows how to:

- Upload and view PDF documents in the browser.
- Ingest PDF content into a vector store (embeddings) for retrieval.
- Query a backend chat endpoint that uses retrieved document chunks to produce context-aware answers.

This repo is intended as a lightweight lab/demo to experiment with ingestion, retrieval, and a minimal chat UI.

Quickstart (PowerShell)
------------------------
1. From the `examples/rag-service-lab` folder set `PYTHONPATH` so the app can import from `src` and then start `uvicorn`:

```powershell
$env:PYTHONPATH = ".\src"; uvicorn main:app
```

2. Open the UI in your browser. If the FastAPI app serves static files, visit `http://127.0.0.1:8000`.
	If not, open the file `examples/rag-service-lab/static/index.html` directly in your browser and point the page at the API host (change fetch URLs in the HTML if necessary).

Notes: to enable automatic reload while developing, you can run:

```powershell
$env:PYTHONPATH = ".\src"; uvicorn main:app --reload
```

What the UI does
---------------
- Upload (Ingest): sends a PDF file to `POST /ingest` (server stores vectors and metadata).
- View (No Ingest): opens the selected PDF locally inside the embedded viewer without sending it to the server.
- Chat: sends messages to `POST /chat` and displays responses; when available, the response includes retrieved document chunks shown under "Retrieved Documents".
- Configuration header: a compact row of small boxes showing the active loader, chunker, LLM, embedding and retriever parameters fetched from `GET /config`.
- Resizable layout: drag the vertical splitter between the PDF viewer and chat to adjust widths.

API (example endpoints)
-----------------------
- `POST /ingest` — multipart form upload, field `file` (PDF). Ingests document, performs extraction/chunking, and stores embeddings.
- `POST /chat` — JSON body `{ "message": "..." }`. Returns a model response plus `retrieved_docs` (array of chunks with `page`, `page_content`, `score`, ...).
- `GET /config` — returns the runtime configuration (extraction, chunking, llm, embeddings, retrieval) used to render the compact header.

File layout (important)
----------------------
- `static/index.html` — single-page UI for uploading, viewing, chatting, and inspecting retrieved chunks.
- `src/` — server source code (FastAPI app and ingestion/retrieval logic).
- `main:app` — server entrypoint used by uvicorn in the examples folder.

Developer notes
---------------
- Viewing a PDF with "View (No Ingest)" is strictly client-side and does not send data to the server.
- After ingesting, the UI no longer auto-opens the document — use the View action to inspect PDFs.
- Retrieved document highlights are placeholders; integrating `pdf.js` will allow precise in-page highlighting and jumping to text fragments.
- The vector store location and embedding backend are configured in the server code — check `src` for details.

Troubleshooting
---------------
- If `/config`, `/chat`, or `/ingest` fail with network/CORS errors, ensure the FastAPI server is running and that CORS is enabled if serving the UI from a different origin.
- If the UI cannot find static files, either serve `static/` from the FastAPI app or open `static/index.html` directly in the browser and update the API host if needed.

Next steps & suggestions
------------------------
- Persist the UI splitter width in `localStorage` so the layout is preserved across reloads.
- Add PDF.js integration to enable text highlighting and navigation to retrieved snippets.
- Add example curl or Python scripts to demonstrate end-to-end ingest → query flows.

License & Attribution
---------------------
This example is provided as-is for experimentation and educational purposes. Check upstream project licenses for third-party components used in the `src` code.



