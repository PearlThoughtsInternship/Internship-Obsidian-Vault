# Quality Metrics for Modernization Tools

## How to Measure If Your Tools Actually Work

> *Building tools is easy. Proving they work is hard. Here's how to measure quality systematically.*

---

## Categories of Quality Metrics

| Category | What It Measures | Key Tools |
|----------|-----------------|-----------|
| **RAG Quality** | Does retrieval find the right code? | RAGAs, TruLens |
| **Experiment Tracking** | Which settings work best? | MLflow, DVC |
| **Code Analysis** | Code complexity, dead code | SonarQube, PHPStan |
| **Embedding Quality** | Do similar things cluster together? | Phoenix (Arize AI) |
| **Performance** | How fast is the system? | OpenTelemetry |

---

## Category 1: RAG Retrieval Quality

### RAGAs Framework (Python)

**Purpose**: Evaluate RAG system quality with standardized metrics.

**Key Metrics**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| `faithfulness` | Does retrieved code accurately represent the query? | > 0.8 |
| `answer_relevancy` | Is retrieved code relevant for the task? | > 0.85 |
| `context_precision` | Are top results highly relevant? | > 0.75 |
| `context_recall` | Did we find all relevant code? | > 0.8 |

**Why It Matters for Modernization**:
- When searching "student validation rules", faithfulness ensures you get actual validation code
- Context recall ensures you don't miss critical business logic spread across files

**Example Test Case**:
```yaml
- query: "How does discount calculation work?"
  expected_files:
    - DiscountService.java
    - CustomerTier.java
    - PromoCodeValidator.java
  expected_concepts:
    - "percentage discount"
    - "family member discount"
    - "seasonal promotion"
```

---

### Custom Modernization Metrics

Generic metrics (Precision@K) don't capture modernization-specific needs. Build custom metrics:

| Metric | What It Measures | Formula |
|--------|-----------------|---------|
| `controller_action_coverage` | % of controller actions found | Found / Total |
| `validation_completeness` | % of validation rules extracted | Extracted / Actual |
| `relation_accuracy` | % of model relations correctly identified | Correct / Total |
| `business_logic_findability` | Can we find custom methods via semantic search? | MRR score |
| `schema_reconstruction_accuracy` | Does extracted schema match production DB? | Jaccard similarity |

**Implementation**:

```typescript
interface ModernizationMetrics {
  // Coverage metrics
  controllerActionCoverage: number; // 0-1
  validationCompleteness: number; // 0-1
  relationAccuracy: number; // 0-1

  // Findability metrics (retrieval-based)
  businessLogicFindability: number; // Mean Reciprocal Rank
  workflowTracingSuccess: number; // % of queries returning complete flow

  // Extraction quality
  schemaAccuracy: number; // Jaccard similarity vs production
  deadCodeDetection: number; // % of unused code correctly identified
}
```

---

## Category 2: Experiment Tracking

### MLflow (Headless Mode)

**Purpose**: Compare embedding models, chunking strategies, retrieval settings.

**What to Track**:

| Parameter | Values to Compare |
|-----------|-------------------|
| Embedding model | all-minilm, bge-large, nomic-embed |
| Chunk size | 500, 1000, 1500, 2500 tokens |
| Chunk overlap | 50, 100, 200, 300 tokens |
| Search strategy | Vector only, BM25 only, Hybrid |
| Reranking | None, cross-encoder, centrality |

**Workflow**:

```bash
# Start experiment
bun run cli experiment:start "embedding-comparison" \
  --model bge-large-v1.5 \
  --chunk-size 1500 \
  --overlap 200

# Run indexing
bun run cli index --project TargetProject

# Run retrieval tests
bun run cli test:retrieval test-cases.yaml

# Compare experiments
bun run cli experiment:compare exp-001 exp-002 exp-003
```

**Output Example**:
```
┌────────────────────────────────────────────────────────────┐
│ EXPERIMENT COMPARISON                                       │
├────────────────────────────────────────────────────────────┤
│ Experiment │ Model       │ Chunk │ Precision │ Recall     │
│────────────│─────────────│───────│───────────│────────────│
│ exp-001    │ all-minilm  │ 1000  │ 0.72      │ 0.68       │
│ exp-002    │ bge-large   │ 1000  │ 0.85      │ 0.82  ✓    │
│ exp-003    │ bge-large   │ 1500  │ 0.83      │ 0.79       │
└────────────────────────────────────────────────────────────┘
Winner: exp-002 (bge-large, chunk=1000)
```

---

### DVC (Data Version Control)

**Purpose**: Version control for embeddings, indexes, test datasets.

**What to Track**:
- LanceDB snapshots (vector index states)
- Golden test datasets (curated ground truth)
- SQLite database snapshots (knowledge graph)

**Why It Matters**:
- Reproducibility: "What was the state when we hit 90% recall?"
- Rollback: "Revert if new embedding model degrades quality"

**Workflow**:
```bash
# Track LanceDB as artifact
dvc add ~/.codecompass/vectors/symbols.lance
git add symbols.lance.dvc
git commit -m "feat: index with bge-large-v1.5"

# Restore previous version
dvc checkout symbols.lance.dvc@v1.0
```

---

## Category 3: Code Analysis Quality

### SonarQube (Headless Scanner)

**Metrics**:

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| `cognitive_complexity` | How hard is code to understand? | Prioritize refactoring |
| `code_smells` | Anti-patterns | What to fix in modernization |
| `duplicated_lines` | Copy-paste code | Consolidation opportunities |
| `security_hotspots` | Vulnerabilities | Security fixes needed |

**Example Output**:
```
┌────────────────────────────────────────────────────────────┐
│ CODE QUALITY ANALYSIS                                       │
├────────────────────────────────────────────────────────────┤
│ Cognitive Complexity: 2,847 (HIGH)                          │
│ Code Smells: 1,204                                          │
│ Duplicated Lines: 18.7%                                     │
│ Security Hotspots: 23                                       │
│                                                             │
│ TOP COMPLEX FILES:                                          │
│   1. OrderController.java (complexity: 342)                 │
│   2. DiscountService.java (complexity: 289)                 │
│   3. PaymentProcessor.java (complexity: 245)                │
└────────────────────────────────────────────────────────────┘
```

---

### Static Analysis Tools by Language

| Language | Tool | Key Metrics |
|----------|------|-------------|
| Java | SpotBugs, PMD | Unused code, coupling |
| Python | pylint, mypy | Type errors, complexity |
| PHP | PHPStan, PHPMD | Dead code, coupling |
| TypeScript | ESLint, tsc | Type safety |
| Ruby | RuboCop, Reek | Code smells |

**Dead Code Detection Example**:
```bash
# PHP dead code analysis
phpstan analyse /path/to/legacy \
  --level 5 \
  --error-format json \
  > phpstan-results.json

# Output: 47 unused methods found
#   - StudentController::actionOldExport (last used: 2019)
#   - CustomerController::actionLegacyImport (deprecated)
```

---

## Category 4: Embedding Quality

### Phoenix (Arize AI)

**Purpose**: Analyze embedding clusters, detect outliers.

**What to Measure**:

| Metric | What It Tells You |
|--------|-------------------|
| `cluster_coherence` | Do similar files cluster together? |
| `outlier_detection` | Which embeddings are misplaced? |
| `embedding_drift` | Have embeddings changed between versions? |

**Example Analysis**:
```
Query: "billing" controllers

Without centrality:
  1. billing.test.ts (0.92 semantic) - rarely imported
  2. billing.service.ts (0.88 semantic) - core file
  3. billing.helper.ts (0.85 semantic) - rarely imported

With centrality (PageRank):
  1. billing.service.ts (0.88 sem + 0.95 cent = 0.91) ✓
  2. billing.test.ts (0.92 sem + 0.10 cent = 0.58)
  3. billing.helper.ts (0.85 sem + 0.05 cent = 0.52)
```

**Silhouette Score**:
- > 0.7: Good clustering (similar things group together)
- 0.5-0.7: Moderate clustering
- < 0.5: Poor clustering (might need different embedding model)

---

## Category 5: Performance Metrics

### Key Performance Indicators

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| `p50_latency` | < 100ms | Interactive feel |
| `p95_latency` | < 500ms | Acceptable for most queries |
| `p99_latency` | < 2000ms | Worst-case acceptable |
| `throughput` | > 10 qps | Handle concurrent users |
| `index_time` | < 5 min/10K files | Reasonable indexing speed |

### Implementation with OpenTelemetry

```typescript
import { trace } from '@opentelemetry/api';

@Injectable()
export class SearchService {
  async search(query: string): Promise<SearchResult[]> {
    const span = trace.getActiveSpan();
    span?.setAttribute('query', query);

    const startTime = Date.now();
    const results = await this.lancedb.search(query);
    const latency = Date.now() - startTime;

    span?.setAttribute('latency_ms', latency);
    span?.setAttribute('result_count', results.length);

    return results;
  }
}
```

### Load Testing

```bash
bun run cli test:load --queries 1000 --concurrency 10

# Output:
#   p50 latency: 45ms
#   p95 latency: 120ms
#   p99 latency: 350ms
#   Throughput: 22 queries/sec
```

---

## Quality Tiers (Recommended Approach)

### Tier 1: Must-Have (Start Here)

| Tool/Metric | Purpose | Effort |
|-------------|---------|--------|
| **RAGAs** | RAG evaluation | Low |
| **MLflow** | Experiment tracking | Low |
| **Custom Metrics** | Modernization-specific | Medium |

### Tier 2: High Value (Add Week 2-3)

| Tool/Metric | Purpose | Effort |
|-------------|---------|--------|
| **DVC** | Artifact versioning | Low |
| **SonarQube** | Code quality baseline | Medium |
| **Phoenix** | Embedding analysis | Medium |

### Tier 3: Nice-to-Have (If Time Permits)

| Tool/Metric | Purpose | Effort |
|-------------|---------|--------|
| **OpenTelemetry** | Production observability | Medium |
| **Evidently AI** | Drift detection | Medium |
| **Human annotation** | Ground truth collection | High |

---

## Building a Test Suite

### Test Case Format (YAML)

```yaml
test_suite: "legacy-modernization-tests"
version: "1.0"
created: "2025-01-12"

test_cases:
  - id: "find-discount-logic"
    category: "business_logic_findability"
    query: "How does discount calculation work?"
    expected:
      files:
        - DiscountService.java
        - CustomerTier.java
      concepts:
        - "percentage calculation"
        - "family discount"
    priority: "high"

  - id: "find-validation-rules"
    category: "validation_completeness"
    query: "What validation rules exist for Customer?"
    expected:
      rules_count: 12
      must_include:
        - "email format"
        - "phone number"
        - "required fields"
    priority: "high"

  - id: "trace-checkout-flow"
    category: "workflow_tracing"
    query: "What happens when a user checks out?"
    expected:
      steps_count: ">= 5"
      must_include_services:
        - OrderService
        - PaymentService
        - InventoryService
    priority: "medium"
```

### Running Tests

```bash
# Run full test suite
bun run cli test:retrieval test-suite.yaml

# Output:
# ✅ find-discount-logic: PASS (precision: 0.9, recall: 0.85)
# ✅ find-validation-rules: PASS (found 11/12 rules)
# ❌ trace-checkout-flow: FAIL (missing InventoryService)
#
# Summary: 2/3 passed (66%)
```

---

## Quality Dashboard Template

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODERNIZATION TOOL QUALITY DASHBOARD                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RETRIEVAL QUALITY                      COVERAGE                             │
│  ├── Precision@5: 0.85 ✅               ├── Controllers: 92% ✅              │
│  ├── Recall@10: 0.78 ⚠️                 ├── Models: 88% ✅                   │
│  ├── MRR: 0.71 ⚠️                       ├── Validations: 67% ❌              │
│  └── RAGAs Score: 0.82 ✅               └── Workflows: 45% ❌                │
│                                                                              │
│  PERFORMANCE                            CODE QUALITY                         │
│  ├── p50 latency: 45ms ✅               ├── Complexity: HIGH                 │
│  ├── p95 latency: 120ms ✅              ├── Dead code: 15%                   │
│  ├── Throughput: 22 qps ✅              ├── Duplication: 18%                 │
│  └── Index time: 3.2 min ✅             └── Test coverage: 45%               │
│                                                                              │
│  EXPERIMENT STATUS: exp-003 (bge-large, chunk=1500)                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation for Interns

### Week 2: Set Up Quality Framework

1. Install RAGAs (Python wrapper)
2. Create 10-20 test cases for target project
3. Set up MLflow experiment tracking
4. Run baseline experiments

### Week 3: Iterate on Quality

5. Compare embedding models
6. Tune chunking parameters
7. Analyze embedding clusters
8. Improve retrieval based on failed tests

### Week 4: Document Results

9. Generate quality dashboard
10. Document what worked/didn't
11. Compare before/after metrics
12. Include in final report

---

## Related

- [Technical Architecture - Multi-Mode Knowledge Extraction](./06-Technical-Architecture.md)
- [Existing Tools Research](./03-Existing-Tools-Research.md)
- [Goals & Expectations](./02-Goals-and-Expectations.md)
- [Validation Projects](./08-Validation-Projects.md)
- [Back to Index](./README.md)

---

## Sources

- [RAGAs Documentation](https://docs.ragas.io/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Phoenix (Arize AI)](https://phoenix.arize.com/)
- [OpenTelemetry](https://opentelemetry.io/)
- [SonarQube](https://www.sonarqube.org/)

---

*Last Updated: 2025-01-12*
