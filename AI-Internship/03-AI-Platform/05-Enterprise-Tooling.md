# Enterprise AI/ML Tooling Stack

## Purpose

This document outlines the recommended tooling stack for building, tracking, and validating the code intelligence platform. All tools are selected for:
- Python compatibility (our implementation language)
- Enterprise readiness (can be self-hosted, auditable)
- Headless operation (works in CI/CD, no mandatory UI)

---

## Tool Categories Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CODE INTELLIGENCE PLATFORM - TOOLING LAYERS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER 1: EXPERIMENT TRACKING                                                │
│  ├── MLflow              (parameters, metrics, artifacts)                   │
│  ├── Weights & Biases    (visualization, sweeps)                            │
│  └── DVC                 (data/model versioning)                            │
│                                                                              │
│  LAYER 2: LLM OBSERVABILITY                                                  │
│  ├── Langfuse            (tracing, cost, latency) [OSS, self-hosted]        │
│  ├── Phoenix (Arize)     (embedding analysis)                               │
│  └── OpenTelemetry       (production tracing)                               │
│                                                                              │
│  LAYER 3: RAG EVALUATION                                                     │
│  ├── RAGAs               (faithfulness, relevancy, recall)                  │
│  ├── TruLens             (groundedness, hallucination)                      │
│  └── DeepEval            (LLM-as-judge metrics)                             │
│                                                                              │
│  LAYER 4: CODE ANALYSIS                                                      │
│  ├── tree-sitter         (AST parsing)                                      │
│  ├── Jedi/Pyright        (Python type analysis)                             │
│  └── SonarQube           (complexity, technical debt)                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Must-Have (Week 1-2)

### 1.1 MLflow - Experiment Tracking

**Purpose**: Track parameters, metrics, and artifacts across experiments.

```bash
pip install mlflow
```

```python
import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")  # Local, headless
mlflow.set_experiment("context-quality")

with mlflow.start_run(run_name="exp-001-bge-large"):
    # Log parameters
    mlflow.log_params({
        "embedding_model": "BAAI/bge-large-en-v1.5",
        "chunk_size": 1500,
        "chunk_overlap": 200,
        "retrieval_k": 10,
        "reranker": "none"
    })

    # Run experiment
    results = run_evaluation(test_set)

    # Log metrics
    mlflow.log_metrics({
        "context_precision": results.precision,
        "context_recall": results.recall,
        "answer_accuracy": results.accuracy,
        "latency_p95_ms": results.latency_p95
    })

    # Log artifacts
    mlflow.log_artifact("results/experiment-001.json")
```

**Why MLflow**:
- Self-hosted, no cloud dependency
- SQLite backend for simplicity
- Comparison UI for visualizing experiments
- Model registry for versioning

---

### 1.2 RAGAs - RAG Evaluation

**Purpose**: Evaluate retrieval and generation quality with standardized metrics.

```bash
pip install ragas
```

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_entity_recall
)
from datasets import Dataset

# Prepare evaluation data
eval_data = {
    "question": ["What happens when Sales Invoice is submitted?"],
    "answer": ["When submitted, it creates GL entries and updates stock..."],
    "contexts": [["on_submit hook in sales_invoice.py...", "GL Entry creation..."]],
    "ground_truth": ["Creates GL entries, updates stock ledger, sends notifications"]
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation
results = evaluate(
    dataset,
    metrics=[
        faithfulness,        # Is answer grounded in context?
        answer_relevancy,    # Does answer address the question?
        context_precision,   # Is retrieved context relevant?
        context_recall,      # Did we retrieve all relevant context?
    ]
)

print(results)
# {'faithfulness': 0.85, 'answer_relevancy': 0.92, 'context_precision': 0.78, 'context_recall': 0.81}
```

**RAGAs Metrics Explained**:

| Metric | What It Measures | Target |
|--------|------------------|--------|
| `faithfulness` | Are claims in answer supported by context? | > 0.85 |
| `answer_relevancy` | Does answer address the question? | > 0.80 |
| `context_precision` | Is retrieved context relevant? | > 0.75 |
| `context_recall` | Did we retrieve all relevant info? | > 0.80 |
| `context_entity_recall` | Are key entities present? | > 0.70 |

---

### 1.3 Langfuse - LLM Observability (Self-Hosted)

**Purpose**: Trace LLM calls, measure latency, track costs.

```bash
pip install langfuse
```

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="http://localhost:3000"  # Self-hosted
)

@observe()
def generate_context(query: str) -> str:
    """Traced function - automatically logged to Langfuse."""
    # Retrieval step
    with langfuse_context.span(name="retrieval"):
        docs = retriever.search(query, k=10)

    # Reranking step
    with langfuse_context.span(name="reranking"):
        ranked = reranker.rerank(query, docs)

    # Format context
    context = format_for_llm(ranked[:5])

    return context

@observe(as_type="generation")
def ask_llm(question: str, context: str) -> str:
    """LLM call - tracks tokens, cost, latency."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
```

**Self-Hosting Langfuse**:
```bash
# Docker Compose
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
# Access at http://localhost:3000
```

**Why Langfuse over LangSmith**:
- Fully open source (MIT license)
- Self-hosted (data stays on your infrastructure)
- No vendor lock-in
- Free for unlimited traces

---

### 1.4 DVC - Data Version Control

**Purpose**: Version embeddings, golden datasets, and evaluation results.

```bash
pip install dvc
```

```bash
# Initialize
dvc init

# Track large files (embeddings, indexes)
dvc add data/embeddings/erpnext-bge-large.lance
dvc add data/golden/test-questions-v1.json

# Push to remote storage
dvc remote add -d storage s3://your-bucket/dvc
dvc push

# Reproduce specific experiment
git checkout exp-003
dvc checkout
# Now you have the exact embeddings from that experiment
```

**What to Version with DVC**:

| Asset | Why Version |
|-------|-------------|
| `embeddings/*.lance` | Reproduce retrieval experiments |
| `golden/*.json` | Stable test sets across experiments |
| `models/*.pkl` | Reranker checkpoints |
| `results/*.json` | Experiment outputs for analysis |

---

## Tier 2: High Value (Week 3-4)

### 2.1 Phoenix (Arize AI) - Embedding Analysis

**Purpose**: Analyze embedding quality, detect clusters, find outliers.

```bash
pip install arize-phoenix
```

```python
import phoenix as px
from phoenix.trace import SpanEvaluations

# Launch Phoenix
session = px.launch_app()

# Log embeddings for analysis
px.Client().log_embeddings(
    dataframe=df,
    embedding_column="embedding",
    text_column="chunk_text"
)

# Analyze clusters
# - Are domain concepts clustering together?
# - Are there outliers (bad chunks)?
# - Is there drift between versions?
```

**Use Cases**:
- Validate that business concepts cluster together
- Find poorly chunked documents (outliers)
- Compare embedding models visually

---

### 2.2 TruLens - RAG Tracing with Groundedness

**Purpose**: Deep tracing with hallucination detection.

```bash
pip install trulens-eval
```

```python
from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback import Groundedness

tru = Tru()

# Define feedback functions
groundedness = Groundedness()
f_groundedness = Feedback(groundedness.groundedness_measure_with_cot_reasons).on(
    Select.Record.calls[0].rets  # The LLM response
).aggregate(np.mean)

# Wrap your RAG chain
tru_recorder = TruChain(
    rag_chain,
    app_id="code-intelligence-v1",
    feedbacks=[f_groundedness]
)

# Use the wrapped chain
with tru_recorder:
    response = rag_chain.invoke("How does discount calculation work?")

# View results
tru.run_dashboard()
```

**TruLens Metrics**:

| Metric | Description |
|--------|-------------|
| `groundedness` | % of response claims supported by context |
| `qs_relevance` | Is context relevant to the question? |
| `context_relevance` | Does context answer what was asked? |

---

### 2.3 DeepEval - LLM-as-Judge Evaluation

**Purpose**: Use LLMs to evaluate LLM outputs systematically.

```bash
pip install deepeval
```

```python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric
)
from deepeval.test_case import LLMTestCase

# Define test case
test_case = LLMTestCase(
    input="What validations run on Sales Invoice creation?",
    actual_output="Sales Invoice validates: 1) Required fields...",
    expected_output="Validates required fields, stock availability, credit limits",
    retrieval_context=["validate() method checks...", "on_validate hook..."]
)

# Define metrics
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.8),
    ContextualRelevancyMetric(threshold=0.7)
]

# Run evaluation
results = evaluate([test_case], metrics)
```

**When to Use DeepEval vs RAGAs**:
- RAGAs: Standard metrics, well-documented, good defaults
- DeepEval: More customizable, better CI/CD integration, pytest-style

---

## Tier 3: Production & Scale (Week 5+)

### 3.1 OpenTelemetry - Production Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("generate_context")
def generate_context(query: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("query.length", len(query))
    # ... implementation
```

### 3.2 Evidently AI - Drift Detection

```python
from evidently.report import Report
from evidently.metrics import EmbeddingsDriftMetric

report = Report(metrics=[
    EmbeddingsDriftMetric(embeddings_name="context_embeddings")
])

report.run(reference_data=baseline_df, current_data=current_df)
report.save_html("drift_report.html")
```

### 3.3 Great Expectations - Data Validation

```python
import great_expectations as gx

context = gx.get_context()

# Validate embeddings dataset
expectation_suite = context.add_expectation_suite("embedding_quality")
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="embedding")
)
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="embedding", min_value=768, max_value=768
    )
)
```

---

## Tool Selection Matrix

| Tool | Category | License | Self-Host | Python SDK | Priority |
|------|----------|---------|-----------|------------|----------|
| **MLflow** | Experiment Tracking | Apache 2.0 | Yes | Yes | Must |
| **RAGAs** | RAG Evaluation | Apache 2.0 | N/A (library) | Yes | Must |
| **Langfuse** | LLM Observability | MIT | Yes | Yes | Must |
| **DVC** | Data Versioning | Apache 2.0 | Yes | Yes | Must |
| **Phoenix** | Embedding Analysis | Apache 2.0 | Yes | Yes | High |
| **TruLens** | RAG Tracing | MIT | Yes | Yes | High |
| **DeepEval** | LLM Evaluation | Apache 2.0 | N/A (library) | Yes | High |
| **OpenTelemetry** | Prod Tracing | Apache 2.0 | Yes | Yes | Medium |
| **Evidently** | Drift Detection | Apache 2.0 | Yes | Yes | Medium |

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EXPERIMENT & EVALUATION PIPELINE                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   DVC        │    │   MLflow     │    │   Langfuse   │                  │
│  │  (versions)  │───▶│  (tracking)  │───▶│  (tracing)   │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │  Embeddings  │    │   Metrics    │    │   Traces     │                  │
│  │  Golden Sets │    │   Params     │    │   Costs      │                  │
│  │  Results     │    │   Artifacts  │    │   Latency    │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                              │
│  EVALUATION LAYER                                                            │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   RAGAs      │    │   TruLens    │    │   DeepEval   │                  │
│  │ (precision,  │    │(groundedness,│    │ (LLM-judge,  │                  │
│  │  recall)     │    │ QS relevance)│    │  custom)     │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         │                   │                   │                           │
│         └───────────────────┴───────────────────┘                           │
│                             │                                               │
│                             ▼                                               │
│                    ┌──────────────────┐                                    │
│                    │  Quality Score   │                                    │
│                    │  vs Baseline     │                                    │
│                    └──────────────────┘                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start Commands

```bash
# 1. Initialize tracking
pip install mlflow ragas langfuse dvc

# 2. Setup MLflow
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

# 3. Setup Langfuse (self-hosted)
docker run -d -p 3000:3000 langfuse/langfuse

# 4. Initialize DVC
dvc init
dvc remote add -d local /path/to/storage

# 5. Run first experiment
python experiments/baseline.py
```

---

## Related

- [Observability & Experiments](./03-Observability.md)
- [Quality Metrics Guide](./04-Quality-Metrics.md)
- [Context Generation](./01-Context-Generation.md)

---

*Last Updated: 2026-01-14*
