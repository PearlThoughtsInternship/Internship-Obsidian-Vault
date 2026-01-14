# Product Evolution Framework

## Purpose

This document defines how the code intelligence platform evolves from basic extraction to validated AI integration. Based on Microsoft's "Crawl-Walk-Run" framework and Chip Huyen's AI Engineering principles.

---

## Core Principle: Prove Value at Every Level

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  THE PROOF REQUIREMENT                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PROBLEM                                                                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Vanilla AI Editor (Claude Code/Cursor) + ERPNext = Generic responses       │
│                                                                              │
│  SOLUTION                                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  AI Editor + Code Intelligence Context = Domain-aware responses             │
│                                                                              │
│  PROOF REQUIRED                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Measurable improvement in:                                                  │
│  • Relevance - Does response match actual domain?                           │
│  • Completeness - Are bounded contexts surfaced?                            │
│  • Accuracy - Does it understand ERPNext's business rules?                  │
│                                                                              │
│  Without proof, the tool is just another experiment.                        │
│  With proof, it's a product that delivers value.                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Evolution Phases

### Phase 0: Baseline (Before Building Anything)

**Duration**: Week 1 (first 2 days)

**Purpose**: Establish what "vanilla" AI performance looks like.

```yaml
baseline_experiment:
  setup:
    ai_tool: "Claude Code"
    codebase: "ERPNext"
    context_provided: "none"  # Just the AI's built-in knowledge

  test_set:
    - question: "What happens when a Sales Invoice is submitted?"
    - question: "How is discount calculated in ERPNext?"
    - question: "What validations run on Invoice creation?"
    # ... 47 more questions (total: 50)

  capture:
    - response_text: "Full AI response"
    - accuracy_score: "1-5 (expert rated)"
    - completeness_score: "1-5 (expert rated)"
    - files_mentioned: "List of files AI referenced"
    - concepts_mentioned: "Domain concepts identified"
```

**Deliverable**: `experiments/baseline-v1.json`

```json
{
  "version": "baseline-v1",
  "date": "2026-01-14",
  "tool": "Claude Code 1.0",
  "context": "none",
  "aggregate_metrics": {
    "avg_accuracy": 2.3,
    "avg_completeness": 2.1,
    "file_accuracy": 0.35,
    "domain_concept_recall": 0.28
  },
  "questions": [
    {
      "id": "q001",
      "question": "What happens when a Sales Invoice is submitted?",
      "response": "When a Sales Invoice is submitted in ERPNext...",
      "accuracy": 2,
      "completeness": 2,
      "files_mentioned": ["sales_invoice.py"],
      "files_should_mention": ["sales_invoice.py", "gl_entry.py", "stock_ledger_entry.py"],
      "concepts_mentioned": ["submit", "GL Entry"],
      "concepts_should_mention": ["on_submit", "GL Entry", "Stock Ledger", "Payment Schedule"]
    }
  ]
}
```

---

### Phase 1: CRAWL - Static Extraction

**Duration**: Weeks 1-3

**Goal**: Parse ERPNext, extract symbols, generate basic context.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CRAWL PHASE DELIVERABLES                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXTRACTION                                                                  │
│  ├── AST parsing with tree-sitter                                           │
│  ├── Function/class extraction                                              │
│  ├── Import/dependency mapping                                              │
│  └── DocType schema extraction (ERPNext-specific)                           │
│                                                                              │
│  OUTPUT                                                                      │
│  ├── symbols.json - All functions, classes, methods                         │
│  ├── imports.json - Import graph                                            │
│  └── doctypes.json - ERPNext DocType schemas                                │
│                                                                              │
│  VALIDATION                                                                  │
│  ├── Coverage: 90%+ symbols extracted                                       │
│  ├── Parse success: 99%+ files without errors                               │
│  └── Manual audit: Spot-check 20 files for correctness                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Success Criteria**:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Symbol coverage | 90%+ | `extracted_symbols / total_symbols` |
| Parse success rate | 99%+ | `files_parsed / total_files` |
| Index time | < 5 min | Time full ERPNext indexing |

**Experiment at End of Crawl**:
```yaml
experiment_crawl:
  context_provided: "Raw symbol list for relevant module"
  expected_improvement: "10-15% accuracy increase"
  measure_against: "baseline-v1"
```

---

### Phase 2: WALK - Semantic Understanding

**Duration**: Weeks 4-6

**Goal**: Add relationships, embeddings, semantic search.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  WALK PHASE DELIVERABLES                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RELATIONSHIPS                                                               │
│  ├── Call graphs (function A calls function B)                              │
│  ├── Class hierarchies (inheritance)                                        │
│  ├── DocType relationships (links, child tables)                            │
│  └── Event flows (hooks, triggers)                                          │
│                                                                              │
│  SEMANTIC LAYER                                                              │
│  ├── Embeddings for all symbols (bge-large-en-v1.5)                        │
│  ├── Vector index (LanceDB)                                                 │
│  ├── Semantic search (query → relevant symbols)                             │
│  └── Hybrid retrieval (keyword + semantic)                                  │
│                                                                              │
│  DOMAIN EXTRACTION                                                           │
│  ├── Business rules identified                                              │
│  ├── Validation logic extracted                                             │
│  ├── Workflow states mapped                                                 │
│  └── Bounded contexts proposed                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Success Criteria**:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Retrieval precision@10 | 70%+ | RAGAs `context_precision` |
| Retrieval recall | 75%+ | RAGAs `context_recall` |
| Query latency (p95) | < 500ms | Langfuse tracing |

**Experiment at End of Walk**:
```yaml
experiment_walk:
  context_provided: "Semantically retrieved context"
  expected_improvement: "25-35% accuracy increase vs baseline"
  measure_against: "baseline-v1, experiment_crawl"
```

---

### Phase 3: RUN - AI Integration

**Duration**: Weeks 7-9

**Goal**: MCP server, Claude Code integration, validated quality.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN PHASE DELIVERABLES                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AI INTEGRATION                                                              │
│  ├── MCP Server exposing tools                                              │
│  │   ├── search_code(query) → relevant symbols                             │
│  │   ├── trace_workflow(entry_point) → call graph                          │
│  │   ├── get_doctype(name) → schema + relationships                        │
│  │   └── explain_domain(module) → bounded context summary                  │
│  │                                                                          │
│  ├── Claude Code configuration                                              │
│  └── Cursor integration (if time permits)                                   │
│                                                                              │
│  QUALITY VALIDATION                                                          │
│  ├── A/B experiments (with context vs without)                              │
│  ├── Statistical significance testing                                       │
│  ├── Regression suite (catch quality drops)                                 │
│  └── User satisfaction survey (internal)                                    │
│                                                                              │
│  DOCUMENTATION                                                               │
│  ├── API reference                                                          │
│  ├── Integration guide                                                      │
│  └── Evaluation report                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Success Criteria**:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Accuracy delta vs baseline | +30%+ | `(enhanced - baseline) / baseline` |
| Completeness delta | +25%+ | Same calculation |
| File accuracy | 75%+ | Correct files referenced |
| Domain concept recall | 70%+ | Correct concepts mentioned |
| Questions improved | 80%+ | % where enhanced > baseline |
| Questions degraded | < 5% | % where enhanced < baseline |

---

## Measurement Framework

### KPIs by Phase

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  KPI EVOLUTION                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE      │ PRIMARY KPI              │ SECONDARY KPIs                     │
│  ───────────│──────────────────────────│────────────────────────────────────│
│  Baseline   │ Avg accuracy score       │ Completeness, file accuracy        │
│  Crawl      │ Symbol coverage          │ Parse success, index time          │
│  Walk       │ Retrieval precision      │ Recall, latency                    │
│  Run        │ Accuracy delta           │ User satisfaction, regression rate │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Version Tracking Schema

```typescript
interface ExperimentVersion {
  id: string;                    // "v0.3.2"
  date: string;                  // "2026-01-14"
  phase: "crawl" | "walk" | "run";

  // What changed
  changes: string[];             // ["Added bge-large embeddings", "Increased chunk size"]

  // Configuration
  config: {
    embedding_model: string;
    chunk_size: number;
    retrieval_k: number;
    reranker: string | null;
  };

  // Results on standard test set
  results: {
    accuracy: number;            // Average 1-5
    completeness: number;
    precision: number;           // RAGAs
    recall: number;
    latency_p95_ms: number;
  };

  // Comparison
  vs_baseline: {
    accuracy_delta: number;      // +0.31 (31% improvement)
    completeness_delta: number;
    precision_delta: number;
  };

  vs_previous: {
    version: string;             // "v0.3.1"
    accuracy_delta: number;
  };
}
```

### Dashboard View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CODE INTELLIGENCE PLATFORM — PROGRESS DASHBOARD                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CURRENT: v0.5.0 (Walk Phase)          TARGET: +30% accuracy vs baseline    │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   ACCURACY      │  │  COMPLETENESS   │  │   PRECISION     │             │
│  │                 │  │                 │  │                 │             │
│  │    3.8 / 5      │  │    3.5 / 5      │  │    0.78         │             │
│  │    ▲ +65%       │  │    ▲ +67%       │  │    (target: 75%)│             │
│  │   vs baseline   │  │   vs baseline   │  │                 │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  VERSION HISTORY (Accuracy)                                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  5.0 │                                          TARGET ─────────────────   │
│      │                                                                      │
│  4.0 │                                    ╭─────● v0.5.0 (current)         │
│      │                              ╭─────╯                                 │
│  3.0 │                        ╭─────╯  ● v0.4.0                            │
│      │                  ╭─────╯                                             │
│  2.5 │            ╭─────╯  ● v0.3.0                                        │
│      │      ╭─────╯                                                         │
│  2.0 │──────● baseline                                                      │
│      └──────────────────────────────────────────────────────────────────   │
│        Week 1    Week 3    Week 5    Week 7    Week 9    Week 11           │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  RECENT EXPERIMENTS                                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  │ Version │ Change              │ Accuracy │ Delta    │ Status          │ │
│  │─────────│─────────────────────│──────────│──────────│─────────────────│ │
│  │ v0.5.0  │ Added reranker      │ 3.8      │ +0.3     │ ✅ Deployed     │ │
│  │ v0.4.1  │ Larger chunks (2K)  │ 3.5      │ +0.2     │ ✅ Deployed     │ │
│  │ v0.4.0  │ bge-large embedding │ 3.3      │ +0.4     │ ✅ Deployed     │ │
│  │ v0.3.0  │ Semantic search     │ 2.9      │ +0.6     │ ✅ Deployed     │ │
│  │ baseline│ No context          │ 2.3      │ -        │ 📊 Reference    │ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Weekly Checkpoint Template

```yaml
# weekly-checkpoint-week-04.yaml
week: 4
phase: "Walk"
date: "2026-02-10"

# What was built
deliverables:
  - "Implemented embedding generation with bge-large"
  - "Set up LanceDB vector index"
  - "Basic semantic search working"

# Current metrics
metrics:
  symbol_coverage: 0.94
  retrieval_precision: 0.68
  retrieval_recall: 0.72
  latency_p95_ms: 380

# vs targets
target_comparison:
  precision: { current: 0.68, target: 0.70, status: "on_track" }
  recall: { current: 0.72, target: 0.75, status: "on_track" }

# vs baseline
baseline_comparison:
  accuracy_delta: "+28%"
  completeness_delta: "+32%"

# Blockers
blockers:
  - "ERPNext hook extraction incomplete"

# Next week focus
next_week:
  - "Complete hook extraction"
  - "Add hybrid retrieval (keyword + semantic)"
  - "Run full experiment on test set"
```

---

## Crawl-Walk-Run Summary

| Phase | Focus | Human Role | AI Role | Proof |
|-------|-------|------------|---------|-------|
| **Crawl** | Extraction | Reviews all output | Generates suggestions | Coverage metrics |
| **Walk** | Retrieval | Validates relevance | Retrieves context | Precision/recall |
| **Run** | Integration | Uses tool normally | Provides context autonomously | Accuracy delta |

---

## Related

- [Platform Capabilities](./02-Capabilities.md)
- [Enterprise Tooling](../03-AI-Platform/05-Enterprise-Tooling.md)
- [Quality Metrics](../03-AI-Platform/04-Quality-Metrics.md)
- [Technology Stack](../02-Engineering/03-Technology-Stack.md)

---

*Last Updated: 2026-01-14*
