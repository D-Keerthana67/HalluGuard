# API Reference

## GET /api/health
Returns `{ "status": "ok", "service": "HalluGuard" }`.

## POST /api/analyze
Request:
```json
{"text":"Paris is the capital of Germany."}
```
Returns claim-level verdicts, evidence, correction, re-verification, and overall reliability.
