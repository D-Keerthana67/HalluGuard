# Architecture

HalluGuard is a model-agnostic reliability layer.

**Pipeline:** Claim Extraction → Evidence Retrieval/Ranking → Verification → Hallucination Classification → Correction → Re-verification → Reliability Report.

The prototype uses a local evidence corpus so the demo is reproducible. The retrieval layer uses TF-IDF and cosine similarity; verification combines relevance thresholds with a lightweight contradiction heuristic.
