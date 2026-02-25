## CodeSensei - RAG-Powered Code Review Mentor

CodeSensei is a small web app that performs **style-and-standards-focused code review** grounded strictly in a small dataset of four local coding standards documents.

The hard constraint is enforced end-to-end: **every piece of feedback must be traceable to at least one explicit rule** in the standards corpus. If no relevant rule exists, CodeSensei stays silent instead of guessing.

### High-level Architecture

- **Frontend** (`streamlit_app.py`):
  - Streamlit app where the user:
    - Pastes a block of code
    - Selects a programming language
    - Optionally adds context (e.g., "this is a REST controller")
    - Clicks a button and sees a structured review (verdict, issues, citations, positives).

- **Backend core** (`app_core.py` and supporting modules):
  - Pure Python function `run_review(...)` used by Streamlit.
  - On first use, loads the local standards dataset and builds an in-memory vector index.

- **RAG Layer** (`standards_loader.py`, `vector_store.py`, `rag_pipeline.py`, `llm_client.py`, `prompts.py`, `models.py`):
  - Loads a small dataset of **4 standards documents** under `standards/`:
    - General style guide
    - Python style guide
    - JavaScript/TypeScript style guide
    - HTTP API design guidelines
  - **Chunking strategy**:
    - Character-based chunks (default: 600 chars) with 150-char overlap.
    - Motivations:
      - Large enough to preserve rule context (heading + description + examples).
      - Small enough to avoid irrelevant noise and to fit comfortably into the LLM context.
  - **Vector database**:
    - In-memory TF-IDF index using scikit-learn.
    - Each chunk has:
      - `rule_id` (stable identifier for citation, e.g. `GEN-STYLE-001`)
      - `doc_name`, `section_title`, `language_scope`, and raw `text`.
  - **Multi-step RAG pipeline**:
    1. Infer **review facets** from the submitted code (e.g., naming, comments, error handling, REST design).
    2. For each facet, run a separate semantic retrieval query into the vector store.
    3. Merge and **deduplicate rules** by `rule_id`, keeping the strongest scoring evidence.
    4. If no relevant rules are found (or language not covered), short-circuit with a "no coverage" verdict.
    5. Otherwise, call the LLM with:
       - Strict system prompt defining the **CodeSensei persona** and responsibilities.
       - Structured user prompt that includes:
         - Language
         - User context
         - Code
         - Retrieved guideline chunks, clearly labeled with `[RULE_ID]` so the model can cite them.

### Persona and Scope

- **Who is CodeSensei?**
  - A senior staff engineer and code reviewer.
  - Expert in code style, readability, API design, and team-specific standards.

- **What is its job?**
  - Check code **only** for:
    - Style and formatting
    - Naming and structure
    - API design and HTTP semantics
    - Error handling, logging, and observability
    - Known anti-patterns and code smells
  - **Every issue must reference at least one `rule_id` from the provided guidelines.**

- **What is NOT its job?**
  - It does **not** review business logic correctness.
  - It does **not** assess performance, security, or scalability unless the standards explicitly mention them.
  - It does **not** invent or assume rules that are not present in the retrieved chunks.

### Output Format

The backend instructs the model to return **strict JSON** in this shape:

```json
{
  "verdict": "approve" | "approve_with_nits" | "request_changes" | "no_coverage",
  "summary": "High-level summary of the review.",
  "positive_feedback": [
    {
      "message": "Something done well and why it aligns with a rule.",
      "rule_ids": ["GEN-STYLE-001"]
    }
  ],
  "issues": [
    {
      "id": "ISSUE-1",
      "severity": "nit" | "minor" | "major",
      "description": "Clear description of the problem.",
      "affected_code": "Free-text reference to lines or snippets.",
      "rule_ids": ["GEN-STYLE-002", "PY-NAMING-003"]
    }
  ]
}
```

### Handling Contradictions and Uncovered Languages

- **Contradicting guidelines**:
  - The system prompt tells the LLM to:
    - Prefer more specific or more recent rules when rules conflict.
    - Explicitly mention the conflict in the review summary when relevant.
    - Never double-count the same rule as multiple issues without clear distinction.

- **Languages not covered in the corpus**:
  - The retrieval layer tracks `language_scope` for each rule.
  - If no chunk matches the target language with a score above a configurable threshold, the pipeline:
    - Returns a `no_coverage` verdict.
    - Provides a short, friendly explanation that CodeSensei cannot safely apply any standards for that language.

### Running the App

From the `Review` directory:

```bash
pip install -r requirements.txt
```

Set your Groq API key (for example in PowerShell on Windows):

```bash
$env:GROQ_API_KEY="your_api_key_here"
```

Then start the Streamlit app:

```bash
streamlit run streamlit_app.py
```

This will open CodeSensei in your browser.


