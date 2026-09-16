# HalluGuard
## AI-Powered LLM Hallucination Detection and Verification System

HalluGuard is an AI-powered, model-agnostic reliability layer for LLM-generated responses. It follows **Claim → Evidence → Verification → Correction → Re-verification → Reliability Report**.

### Demo features
- Claim extraction
- Evidence retrieval and ranking
- SUPPORTED / CONTRADICTED / PARTIALLY_SUPPORTED / UNSUPPORTED verdicts
- Hallucination type and severity
- Evidence-grounded correction
- Independent re-verification
- Reliability score
- Flask REST API + browser dashboard

### Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```
Open **http://127.0.0.1:5000**.

Try the demo claim: `Paris is the capital of Germany.` Then click **Analyze Response**.

### Structure
```text
backend/        Flask API and verification pipeline
data/           reproducible evidence corpus and sample data
frontend/       browser dashboard
evaluation/     evaluation script
tests/          automated tests
docs/            architecture, methodology, API and demo notes
```

### Prototype scope
The default demo is fully local and reproducible. Retrieval uses TF-IDF/cosine similarity and verification uses lightweight semantic and contradiction heuristics. For a production research system, these components can be replaced with trained NLI models, live multi-source retrieval, citation checking and external LLM adapters.

### Team
Keerthana D and Niraimathi C  
Guide: Dr. K. Nagalakshmi

MIT License.
