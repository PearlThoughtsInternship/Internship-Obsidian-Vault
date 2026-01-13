# Observability & Experiments

## Purpose

Track experiments systematically to understand what improves context quality and AI response accuracy.

---

## Why Observability Matters

Without tracking:
- "I think this embedding model is better" (opinion)
- "The answers seem improved" (subjective)
- "Let's try a different approach" (random)

With tracking:
- "bge-large improved recall by 15% over all-minilm" (data)
- "Answer accuracy increased from 60% to 82%" (measured)
- "Chunk size 1500 outperforms 1000 for workflow queries" (evidence)

---

## What to Track

### Experiment Parameters

| Category | Parameters |
|----------|------------|
| **Embedding** | Model, dimensions, batch size |
| **Chunking** | Size, overlap, boundary strategy |
| **Retrieval** | Top-k, reranking, hybrid weights |
| **Context** | Format, token budget, ordering |

### Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Context Precision** | % of context that was relevant | > 75% |
| **Context Recall** | % of relevant content retrieved | > 80% |
| **Answer Accuracy** | % of factually correct statements | > 80% |
| **Answer Completeness** | % of relevant info included | > 70% |
| **Latency (p95)** | Time to generate context | < 500ms |

---

## Experiment Protocol

### Structure

```yaml
# experiment.yaml
id: "exp-003"
date: "2026-01-15"
hypothesis: "bge-large embeddings will improve retrieval for workflow queries"

parameters:
  embedding_model: "bge-large-v1.5"
  chunk_size: 1500
  chunk_overlap: 200
  retrieval_strategy: "hybrid"
  hybrid_weights:
    semantic: 0.7
    keyword: 0.3

test_questions:
  - id: "workflow-1"
    question: "What happens when a Sales Invoice is submitted?"
    expected_files:
      - sales_invoice.py
      - gl_entry.py
    expected_concepts:
      - "on_submit"
      - "GL Entry creation"
      - "stock update"

results:
  precision: 0.82
  recall: 0.78
  avg_accuracy: 0.85
  avg_completeness: 0.80
  p95_latency_ms: 320

comparison:
  vs_baseline: "+18% accuracy"
  vs_exp_002: "+5% recall"

notes: |
  bge-large significantly better for workflow queries.
  Still struggles with validation rule extraction.
```

### Baseline Establishment

Before experiments, establish baseline:

```python
def run_baseline():
    """Measure AI responses without any context."""
    results = []

    for question in test_questions:
        response = llm.generate(question.text)  # No context

        accuracy = human_rate(response, question.expected)
        completeness = human_rate_completeness(response, question.expected)

        results.append({
            "question": question.id,
            "accuracy": accuracy,
            "completeness": completeness
        })

    return aggregate(results)
```

### A/B Comparison

```python
def compare_approaches(approach_a, approach_b, questions):
    """Compare two approaches on same questions."""
    results = {
        "approach_a": [],
        "approach_b": []
    }

    for question in questions:
        # Approach A
        context_a = approach_a.generate_context(question)
        response_a = llm.generate(question, context=context_a)

        # Approach B
        context_b = approach_b.generate_context(question)
        response_b = llm.generate(question, context=context_b)

        # Rate both (blind)
        results["approach_a"].append(rate(response_a))
        results["approach_b"].append(rate(response_b))

    return statistical_comparison(results)
```

---

## Tools for Tracking

### MLflow (Recommended)

```python
import mlflow

mlflow.set_experiment("context-quality")

with mlflow.start_run(run_name="exp-003"):
    # Log parameters
    mlflow.log_params({
        "embedding_model": "bge-large-v1.5",
        "chunk_size": 1500,
        "retrieval_strategy": "hybrid"
    })

    # Run experiment
    results = run_experiment()

    # Log metrics
    mlflow.log_metrics({
        "precision": results.precision,
        "recall": results.recall,
        "accuracy": results.accuracy,
        "latency_p95": results.latency_p95
    })

    # Log artifacts
    mlflow.log_artifact("experiment.yaml")
```

View results:
```bash
mlflow ui  # Opens at localhost:5000
```

### Simple CSV Tracking

```csv
date,experiment_id,embedding_model,chunk_size,precision,recall,accuracy,notes
2026-01-14,exp-001,all-minilm,1000,0.65,0.60,0.58,baseline
2026-01-15,exp-002,bge-large,1000,0.78,0.72,0.75,better embeddings
2026-01-16,exp-003,bge-large,1500,0.82,0.78,0.85,larger chunks help
```

### JSON Lines

```jsonl
{"date":"2026-01-14","id":"exp-001","params":{"model":"all-minilm"},"results":{"precision":0.65}}
{"date":"2026-01-15","id":"exp-002","params":{"model":"bge-large"},"results":{"precision":0.78}}
```

---

## Dashboards

### Experiment Comparison

```
┌────────────────────────────────────────────────────────────────────────┐
│ EXPERIMENT COMPARISON                                                   │
├────────────────────────────────────────────────────────────────────────┤
│ Experiment │ Model       │ Chunk │ Precision │ Recall  │ Accuracy     │
│────────────│─────────────│───────│───────────│─────────│──────────────│
│ exp-001    │ all-minilm  │ 1000  │ 0.65      │ 0.60    │ 0.58         │
│ exp-002    │ bge-large   │ 1000  │ 0.78      │ 0.72    │ 0.75  ↑      │
│ exp-003    │ bge-large   │ 1500  │ 0.82      │ 0.78    │ 0.85  ↑      │
└────────────────────────────────────────────────────────────────────────┘
```

### Quality Over Time

```
Accuracy Trend
1.0 │                                    ╭───
    │                              ╭─────╯
0.8 │                        ╭─────╯
    │                  ╭─────╯
0.6 │            ╭─────╯
    │      ╭─────╯
0.4 │──────╯
    └────────────────────────────────────────
      Week 1   Week 2   Week 3   Week 4
```

---

## Iteration Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ITERATION CYCLE                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. HYPOTHESIS                                                           │
│     └── "Larger chunks will improve workflow understanding"              │
│                                                                          │
│  2. EXPERIMENT                                                           │
│     ├── Change one parameter (chunk_size: 1000 → 1500)                  │
│     ├── Run on standard test set                                        │
│     └── Measure all metrics                                             │
│                                                                          │
│  3. ANALYZE                                                              │
│     ├── Compare to baseline and previous best                           │
│     ├── Identify what improved/degraded                                 │
│     └── Document findings                                               │
│                                                                          │
│  4. DECIDE                                                               │
│     ├── Keep change if improvement                                      │
│     ├── Revert if degradation                                           │
│     └── Form new hypothesis                                             │
│                                                                          │
│  5. REPEAT                                                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Related

- [[01-Context-Generation|Context Generation]]
- [[02-LLM-Integration|LLM Integration]]
- [[04-Quality-Metrics|Quality Metrics (RAGAs)]]

---

*Last Updated: 2026-01-13*
