# Technology Stack

## Overview

This document defines the technology choices for the code intelligence platform. The platform is **built in Python** (matching ERPNext's language) with **Go as the target migration stack** for the legacy system being analyzed.

---

## Architecture Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TWO TECH STACKS IN PLAY                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. THE TOOL (What You Build)                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Language:        Python 3.11+                                               │
│  Why:             Team familiarity, ERPNext ecosystem, AI/ML libraries       │
│  Deployment:      CLI + MCP Server                                           │
│                                                                              │
│  2. THE TARGET (What You Analyze & Migrate To)                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Source:          ERPNext (Python/Frappe Framework)                          │
│  Target:          Go (Golang)                                                │
│  Why Go:          Performance, type safety, cloud-native, enterprise ready   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tool Stack (Python)

### Core Dependencies

```toml
# pyproject.toml

[project]
name = "code-intelligence"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    # Parsing
    "tree-sitter>=0.21.0",
    "tree-sitter-python>=0.21.0",
    "tree-sitter-javascript>=0.21.0",

    # Embeddings & Vector Search
    "sentence-transformers>=2.2.0",
    "lancedb>=0.4.0",
    "fastembed>=0.2.0",

    # LLM Integration
    "openai>=1.10.0",
    "anthropic>=0.18.0",
    "langfuse>=2.0.0",

    # Evaluation
    "ragas>=0.1.0",
    "datasets>=2.16.0",

    # Experiment Tracking
    "mlflow>=2.10.0",
    "dvc>=3.40.0",

    # CLI
    "typer>=0.9.0",
    "rich>=13.7.0",

    # MCP Server
    "mcp>=0.1.0",
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",

    # Utilities
    "pydantic>=2.6.0",
    "networkx>=3.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]
```

### Project Structure

```
code-intelligence/
├── src/
│   ├── extraction/           # AST parsing, symbol extraction
│   │   ├── parsers/          # Language-specific parsers
│   │   │   ├── python.py
│   │   │   ├── javascript.py
│   │   │   └── frappe.py     # ERPNext-specific
│   │   ├── symbols.py        # Symbol extraction
│   │   └── relationships.py  # Call graph, imports
│   │
│   ├── indexing/             # Vector DB, embeddings
│   │   ├── embeddings.py     # Generate embeddings
│   │   ├── vectordb.py       # LanceDB operations
│   │   └── hybrid.py         # Keyword + semantic search
│   │
│   ├── context/              # Context generation
│   │   ├── retriever.py      # Query → relevant context
│   │   ├── formatter.py      # Format for LLM consumption
│   │   └── domain.py         # Domain concept extraction
│   │
│   ├── evaluation/           # Quality measurement
│   │   ├── metrics.py        # RAGAs integration
│   │   ├── experiments.py    # MLflow integration
│   │   └── baseline.py       # Baseline comparison
│   │
│   ├── mcp/                  # MCP Server
│   │   ├── server.py         # FastMCP server
│   │   └── tools.py          # Tool definitions
│   │
│   └── cli/                  # Command-line interface
│       ├── main.py           # Typer CLI
│       └── commands/
│           ├── index.py
│           ├── search.py
│           └── evaluate.py
│
├── experiments/              # Experiment data (DVC tracked)
│   ├── baseline/
│   ├── test_sets/
│   └── results/
│
├── data/                     # Generated data (DVC tracked)
│   ├── embeddings/
│   └── indexes/
│
├── tests/
│   ├── extraction/
│   ├── indexing/
│   └── evaluation/
│
├── pyproject.toml
├── dvc.yaml                  # DVC pipeline
└── mlflow.db                 # Local MLflow tracking
```

### Key Library Choices

| Category | Library | Why |
|----------|---------|-----|
| **Parsing** | tree-sitter | Fast, reliable, multi-language AST parsing |
| **Embeddings** | sentence-transformers | Best OSS embedding models (bge, e5) |
| **Vector DB** | LanceDB | Embedded, no server needed, fast |
| **LLM Client** | openai + anthropic | Direct API access, no abstraction overhead |
| **Evaluation** | RAGAs | Standard metrics, well-documented |
| **Tracking** | MLflow | Self-hosted, SQLite backend |
| **Observability** | Langfuse | OSS, self-hosted LLM tracing |
| **CLI** | Typer | Modern, type-safe CLI framework |
| **MCP** | FastMCP | Python MCP server implementation |

---

## Migration Target Stack (Go)

### Why Go for ERPNext Migration?

| Factor | Python (ERPNext) | Go (Target) |
|--------|------------------|-------------|
| **Performance** | Interpreted, GIL | Compiled, concurrent |
| **Type Safety** | Dynamic typing | Static typing |
| **Deployment** | Complex (dependencies) | Single binary |
| **Concurrency** | Threading limited | Goroutines native |
| **Cloud Native** | Possible | Built for it |
| **Enterprise** | Common | Preferred |

### Target Go Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ERPNext → GO MIGRATION TARGET                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DOMAIN LAYER (DDD)                                                          │
│  ├── entities/              # Core business entities                        │
│  │   ├── invoice.go         # SalesInvoice equivalent                       │
│  │   ├── customer.go                                                        │
│  │   └── item.go                                                            │
│  │                                                                          │
│  ├── repositories/          # Data access interfaces                        │
│  │   ├── invoice_repo.go                                                    │
│  │   └── customer_repo.go                                                   │
│  │                                                                          │
│  └── services/              # Business logic                                │
│      ├── pricing.go         # Discount calculation                          │
│      ├── accounting.go      # GL Entry creation                             │
│      └── inventory.go       # Stock management                              │
│                                                                              │
│  INFRASTRUCTURE                                                              │
│  ├── postgres/              # PostgreSQL repositories                       │
│  ├── grpc/                  # gRPC service definitions                      │
│  └── http/                  # REST API handlers                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Python → Go Mapping Patterns

The code intelligence tool should help identify these patterns:

| ERPNext (Python) | Go Equivalent |
|------------------|---------------|
| DocType class | struct with methods |
| `on_submit` hook | domain event handler |
| `validate()` method | `Validate() error` method |
| Frappe ORM | Repository pattern |
| WhiteList API | gRPC/REST handler |
| Child Table | slice of embedded structs |
| Link field | foreign key / ID reference |

**Example Mapping**:

```python
# ERPNext (Python)
class SalesInvoice(Document):
    def validate(self):
        self.validate_qty()
        self.calculate_taxes()

    def on_submit(self):
        self.make_gl_entries()
        self.update_stock()
```

```go
// Go Target
type SalesInvoice struct {
    ID          string
    CustomerID  string
    Items       []InvoiceItem
    Status      InvoiceStatus
    // ...
}

func (i *SalesInvoice) Validate() error {
    if err := i.validateQty(); err != nil {
        return err
    }
    return i.calculateTaxes()
}

type InvoiceSubmittedHandler struct {
    glService    *accounting.GLService
    stockService *inventory.StockService
}

func (h *InvoiceSubmittedHandler) Handle(event InvoiceSubmitted) error {
    if err := h.glService.CreateEntries(event.Invoice); err != nil {
        return err
    }
    return h.stockService.UpdateStock(event.Invoice)
}
```

---

## Development Environment

### Required Tools

```bash
# Python environment
python --version  # 3.11+
pip install uv    # Fast package installer

# Initialize project
uv venv
uv pip install -e ".[dev]"

# Tree-sitter grammars (one-time)
python -c "import tree_sitter_python"

# MLflow (local server)
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

# Langfuse (optional, self-hosted)
docker run -d -p 3000:3000 langfuse/langfuse
```

### IDE Setup (VS Code)

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  },
  "ruff.organizeImports": true
}
```

### Type Checking

```bash
# Run mypy
mypy src/

# Run ruff (linting)
ruff check src/
ruff format src/
```

---

## CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"

      - name: Lint
        run: ruff check src/

      - name: Type check
        run: mypy src/

      - name: Test
        run: pytest tests/ -v

  evaluate:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Set up DVC
        uses: iterative/setup-dvc@v1

      - name: Pull test data
        run: dvc pull experiments/test_sets/

      - name: Run evaluation
        run: python -m src.cli.main evaluate --test-set golden-v1

      - name: Check quality threshold
        run: |
          accuracy=$(cat results/latest.json | jq '.accuracy')
          if (( $(echo "$accuracy < 0.75" | bc -l) )); then
            echo "Quality below threshold: $accuracy < 0.75"
            exit 1
          fi
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  END-TO-END DATA FLOW                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. INDEXING PIPELINE                                                        │
│     ERPNext Source → tree-sitter → Symbols → Embeddings → LanceDB           │
│                                                                              │
│  2. QUERY PIPELINE                                                           │
│     User Query → Embedding → Vector Search → Rerank → Format → LLM Context  │
│                                                                              │
│  3. EVALUATION PIPELINE                                                      │
│     Test Set → Query Pipeline → LLM Response → RAGAs Metrics → MLflow       │
│                                                                              │
│  4. MCP INTEGRATION                                                          │
│     Claude Code → MCP Tool Call → Query Pipeline → Context → Claude Code    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Decision Log

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Language | Python | TypeScript, Go | Team familiarity, AI/ML ecosystem |
| Vector DB | LanceDB | Chroma, Qdrant, Pinecone | Embedded, no server, fast |
| Embeddings | bge-large-en-v1.5 | OpenAI ada-002, e5-large | OSS, high quality, no API cost |
| Tracking | MLflow | W&B, Neptune | Self-hosted, SQLite, free |
| Observability | Langfuse | LangSmith | OSS, self-hosted, no vendor lock |
| Parsing | tree-sitter | ast module, libcst | Multi-language, fast, reliable |
| CLI | Typer | Click, argparse | Modern, type-safe, auto-help |

---

## Related

- [Architecture Overview](./01-Architecture.md)
- [Enterprise Tooling](../03-AI-Platform/05-Enterprise-Tooling.md)
- [Evolution Framework](../01-Product/03-Evolution-Framework.md)

---

*Last Updated: 2026-01-14*
