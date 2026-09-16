# Methodology

1. Split the LLM response into candidate factual claims.
2. Transform the claims and evidence corpus into TF-IDF vectors.
3. Rank evidence using cosine similarity.
4. Assign SUPPORTED, CONTRADICTED, PARTIALLY_SUPPORTED, or UNSUPPORTED using similarity and contradiction rules.
5. Classify likely hallucination type and severity.
6. Generate an evidence-grounded correction when required.
7. Re-verify the correction independently.
8. Aggregate claim results into a reliability percentage and label.

For a production system, replace the heuristic verifier with a trained NLI model and add live multi-source retrieval.
