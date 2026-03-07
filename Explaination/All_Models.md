# Ecosystem Models

The Automated Auditorium Lighting System utilizes a hybrid mix of AI Models for deep text comprehension and deterministic algorithms for structuring and timing. The core AI execution happens inside the Cloud LLM Interface (generally OpenAI format).

## 1. Text Parsing & Formatting Models
* **Phase Used:** Phase 1
* **Model Type:** NLP Libraries & Regex Heuristics
* **How It Works:** Rather than an AI model, Phase 1 relies on strict pattern matching (`re`) to identify standard screenplay indicators like `INT.` or `EXT.` It supplements this with structural rule-based chunking that breaks pure dialogue scripts into budget-based word counts (e.g., 500 words = 1 Scene). If a script is a PDF or DOCX, it utilizes `PyPDF2` or `python-docx` to extract raw plaintext.

## 2. Global Scene Analyzer (OpenAI `gpt-4o-mini`)
* **Phase Used:** Phase 2
* **Model Type:** Large Language Model (LLM)
* **How It Works:** 
  - **Global Anchor Extraction (Phase 2A):** The model reads the *entire* parsed text (up to its token limit) and outputs a "Global Summary" of the overarching plot.
  - **Multi-Head Sliding Window (Phase 2B):** Using the context generated above, the model focuses on *one scene at a time*. It uses strict JSON enforcement to extract structural emotions (Joy, Fear, Tension), a confidence score, and narrative mechanics like irony indices or energy scores. The scene is evaluated not just on its own contents, but on its relation to the overall narrative arc.
  - *Note:* In older legacy versions of this pipeline, `DistilRoBERTa` was used for raw sentiment analysis. The V3 pipeline fully migrated to `gpt-4o-mini` for nuanced context processing.

## 3. Retrieval-Augmented Knowledge Models (RAG via FAISS)
* **Phase Used:** Phase 3
* **Model Type:** Semantic Vector Embedding Search (`langchain`, `sentence-transformers`)
* **How It Works:** The knowledge repository contains text snippets detailing how a professional lighting designer would handle specific emotional states. Phase 3 queries this knowledge base by generating a vector representation of Phase 2's emotional states and executing a K-Nearest Neighbors nearest-match search (via FAISS Cpu). It returns factual design logic (e.g., "Sadness implies dim, cool, saturated blue washes with isolated stark overhead spots") instead of letting the Phase 4 LLM guess.

## 4. Lighting Decision Engine (OpenAI `gpt-4o-mini`)
* **Phase Used:** Phase 4
* **Model Type:** Large Language Model (LLM) + Structured Output Validation (`pydantic`)
* **How It Works:** Using the emotional extraction from Phase 2 and the factual lighting rules from Phase 3, the engine generates specific "Lighting Instructions" arrays. This model creates logical DMX parameters like `rgb` array numbers, Intensity percentages, `focus_area`, and Transition speeds ("snap", "crossfade"), outputting a validated, predictable JSON schema. 

## 5. Playback Orchestration Engine
* **Phase Used:** Phase 5
* **Model Type:** Deterministic Timing Algorithms
* **How It Works:** Not a probabilistic machine learning model. This is physical web code running within `Three.js` (Frontend visualization) or a backend playback controller. It takes the mathematical duration defined in Phase 1 and blends it with the theoretical `Lighting Instructions` of Phase 4 to smoothly interpolate colors and brightness over time visually.
