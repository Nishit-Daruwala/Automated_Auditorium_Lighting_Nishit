# Phase 3: Knowledge Layer (Dual RAG)

## Entry Points
- `phase_3/__init__.py` → Exposes `get_retriever()`, acting as the main entry point to initialize and interact with the Phase 3 RAG engine.
- `phase_3/ingestion/knowledge_ingestion.py` → Standalone entry point used specifically to build the local FAISS vector stores from source JSON files.

## Exit Points
- `phase_3/rag_retriever.py` → Returns design rule metadata, formatted palette dictionaries (via `retrieve_palette`), and context string blocks (via `build_context_for_llm`) ready for ingestion by downstream Phase 4 Lighting Decision Engines.
- `phase_3/ingestion/knowledge_ingestion.py` → Saves binary FAISS index artifacts directly to the `rag/` directory.

## Python Files Used

- `__init__.py`
  - **Role:** Main exporter module.
  - **Functions / Classes:** Exports `get_retriever`.
  - **Connected Files:** `rag_retriever.py`.

- `rag_retriever.py`
  - **Role:** Dual RAG retriever utilizing LangChain and FAISS. Connects the system to the Auditorium hardware knowledge base and the Design Semantics knowledge base.
  - **Functions / Classes:** `Phase3Retriever` (with methods `retrieve_auditorium_context`, `retrieve_semantics_context`, `retrieve_palette`, `build_context_for_llm`), `get_retriever`.
  - **Input Sources:** Queries encompassing emotion names (e.g., "fear", "joy"), script types ("drama"), or scene descriptors (e.g., "spotlight").
  - **Output Results:** Retrieved metadata dicts or text payloads mapping queries to design rules and fixture sets.
  - **Connected Files:** Uses `rag/auditorium` and `rag/lighting_semantics` index directories locally.

- `ingestion/knowledge_ingestion.py`
  - **Role:** Ingestion script to build out the internal FAISS vector databases from raw JSON documents.
  - **Functions / Classes:** `load_json`, `create_fixture_documents`, `create_semantics_documents`, `main`.
  - **Input Sources:** Reads from `knowledge/auditorium/fixtures.json` and `knowledge/semantics/baseline_semantics.json`.
  - **Output Results:** Generates embedded `FAISS` indexes using HuggingFace `all-MiniLM-L6-v2`.

- `extract_book_rules.py`
  - **Role:** Helper script that extracts raw theoretical sentences via keyword matching from stage lighting textbook PDFs.
  - **Functions / Classes:** `extract_text_from_pdf`, `find_rules`, `main`.
  - **Input Sources:** Provided textbook PDFs in `docs/*.pdf`.
  - **Output Results:** Extracted rule snippets saved to `knowledge/semantics/raw_book_extraction.json`.

- `test_emotional_hierarchy.py`, `test_fixtures.py`, `validate_schema.py`
  - **Role:** Scripts verifying schema formats and RAG functional retrieval tests.
