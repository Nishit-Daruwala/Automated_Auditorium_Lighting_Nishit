# Phase 3: Knowledge Layer (Dual RAG)

## Workflow
Phase 3 operates as a "Retrieval-Augmented Generation" (RAG) system built around LangChain and FAISS vectors. It is a Knowledge Base lookup layer designed to bridge the gap between abstract emotions and concrete lighting design techniques.

1. **Information Vectorization:** Uses pre-embedded chunks of professional lighting knowledge (both Facts and Design Biases).
2. **Intent Matching:** When Phase 2 yields an emotion (e.g., "Tension" with high intensity), Phase 3 queries the FAISS vector database.
3. **Retrieval Strategy:** Phase 3 pulls context on how professional lighting designers typically represent that semantic state (e.g., "Use stark, high contrast angles. Harsh cold whites mixed with deep saturated blues. Fast dramatic shifts.").

## How it Connects
This phase acts as an intermediary database lookup. It takes the output from **Phase 2 (Emotions)** and provides **Phase 4 (Lighting Decision)** with concrete, industry-standard examples and historical reference data so that the LLM generating the DMX/Cues doesn't have to guess how to light a "sad" or "happy" scene.
