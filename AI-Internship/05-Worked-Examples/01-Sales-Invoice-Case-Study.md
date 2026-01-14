# Worked Example: Sales Invoice RAG Pipeline

## Overview

This document applies RAG (Retrieval Augmented Generation) principles from AI Engineering literature to build a code intelligence system for ERPNext's Sales Invoice module. It serves as the reference implementation for the internship program.

---

## Why Sales Invoice?

Sales Invoice is the ideal first target because it:
- Touches **4 bounded contexts**: Selling, Accounts, Stock, CRM
- Has **rich business logic**: validation, calculation, hooks
- Demonstrates **ERPNext patterns**: DocType lifecycle, controllers, child tables
- Has **clear migration path**: well-defined Go target architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SALES INVOICE - BOUNDED CONTEXT MAP                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                    ┌──────────────┐                                         │
│                    │   SELLING    │                                         │
│                    │  (Primary)   │                                         │
│                    └──────┬───────┘                                         │
│                           │                                                  │
│           ┌───────────────┼───────────────┐                                 │
│           │               │               │                                  │
│           ▼               ▼               ▼                                  │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                            │
│    │ ACCOUNTS │    │  STOCK   │    │   CRM    │                            │
│    │ GL Entry │    │ SL Entry │    │ Customer │                            │
│    └──────────┘    └──────────┘    └──────────┘                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 1: RAG Pipeline Architecture for Code

### 1.1 Text RAG vs Code RAG

| Aspect | Text RAG | Code RAG |
|--------|----------|----------|
| **Chunking** | Paragraphs, sentences | Functions, classes, methods |
| **Boundaries** | Natural language breaks | AST node boundaries |
| **Metadata** | Title, author, date | File path, line numbers, symbol type |
| **Relationships** | Hyperlinks, citations | Call graphs, imports, inheritance |
| **Context** | Surrounding paragraphs | Imports, class hierarchy, callers |

### 1.2 Code RAG Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CODE RAG PIPELINE - TWO-PHASE ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: INDEXING (Offline)                                                 │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  Source Files                                                                │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │ tree-sitter │────▶│   Chunks    │────▶│ Embeddings  │                   │
│  │   Parser    │     │ (Functions) │     │ (bge-large) │                   │
│  └─────────────┘     └─────────────┘     └─────────────┘                   │
│                            │                    │                           │
│                            ▼                    ▼                           │
│                     ┌─────────────┐     ┌─────────────┐                    │
│                     │   SQLite    │     │   LanceDB   │                    │
│                     │   (Graph)   │     │  (Vectors)  │                    │
│                     └─────────────┘     └─────────────┘                    │
│                                                                              │
│  PHASE 2: RETRIEVAL (Online)                                                 │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  User Query: "What happens when Sales Invoice is submitted?"                 │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────┐                                                            │
│  │   Query     │                                                            │
│  │  Embedding  │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                    │
│    ┌────┴────┐                                                              │
│    ▼         ▼                                                              │
│ ┌──────┐ ┌──────┐     ┌─────────────┐     ┌─────────────┐                  │
│ │Vector│ │BM25  │────▶│   Hybrid    │────▶│  Reranker   │                  │
│ │Search│ │Search│     │   Fusion    │     │(cross-enc.) │                  │
│ └──────┘ └──────┘     └─────────────┘     └──────┬──────┘                  │
│                                                   │                         │
│                                                   ▼                         │
│                              ┌─────────────────────────────────┐           │
│                              │  Graph Expansion                 │           │
│                              │  (callers, callees, imports)     │           │
│                              └─────────────┬───────────────────┘           │
│                                            │                                │
│                                            ▼                                │
│                              ┌─────────────────────────────────┐           │
│                              │  Context Construction            │           │
│                              │  (format for LLM)                │           │
│                              └─────────────────────────────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Chunking Strategy for Code

### 2.1 Why AST-Based Chunking?

From **AI Engineering (Chip Huyen)**:
> "When a document is split into chunks without overlap, the chunks might be cut off in the middle of important context."

For code, this is even more critical:
- A function split mid-way is **semantically broken**
- Variable references may be lost
- Control flow becomes incomprehensible

### 2.2 ERPNext-Specific Chunking

```python
from tree_sitter import Parser
from tree_sitter_python import language as python_language

def chunk_erpnext_file(file_path: str) -> list[dict]:
    """
    AST-based chunking for ERPNext Python files.

    Extracts:
    - Class definitions (DocType controllers)
    - Method definitions (business logic)
    - Hook functions (validate, on_submit, etc.)
    - Frappe API calls (whitelisted methods)
    """
    parser = Parser()
    parser.set_language(python_language())

    with open(file_path) as f:
        code = f.read()

    tree = parser.parse(code.encode())
    chunks = []

    for node in traverse_tree(tree.root_node):
        if node.type == 'class_definition':
            chunks.append(extract_class_chunk(node, code, file_path))

        elif node.type == 'function_definition':
            # Check if it's an ERPNext hook
            func_name = get_node_name(node)
            if func_name in ERPNEXT_HOOKS:
                chunks.append(extract_hook_chunk(node, code, file_path))
            else:
                chunks.append(extract_function_chunk(node, code, file_path))

    return chunks

# ERPNext lifecycle hooks to prioritize
ERPNEXT_HOOKS = {
    'validate', 'before_validate', 'after_validate',
    'on_submit', 'before_submit', 'on_cancel',
    'on_update', 'after_insert', 'before_save',
    'on_trash', 'after_delete'
}
```

### 2.3 Chunk Schema for Sales Invoice

```python
@dataclass
class CodeChunk:
    """Schema for indexed code chunks."""

    # Identity
    id: str                      # "sales_invoice.py:SalesInvoice.on_submit"
    file_path: str               # "erpnext/accounts/doctype/sales_invoice/sales_invoice.py"

    # Location
    start_line: int              # 234
    end_line: int                # 267

    # Content
    code: str                    # Full function/class code

    # Metadata
    symbol_type: str             # "method", "class", "function"
    symbol_name: str             # "on_submit"
    parent_class: str | None     # "SalesInvoice"

    # ERPNext-specific
    doctype: str | None          # "Sales Invoice"
    hook_type: str | None        # "on_submit", "validate", etc.
    is_whitelisted: bool         # @frappe.whitelist()

    # Relationships (populated from graph)
    calls: list[str]             # ["make_gl_entries", "update_stock"]
    called_by: list[str]         # ["submit"]
    imports: list[str]           # ["frappe", "erpnext.accounts"]

    # Context (for retrieval augmentation)
    docstring: str | None        # Extracted docstring
    class_docstring: str | None  # Parent class docstring
```

### 2.4 Chunking Output for Sales Invoice

```json
{
  "chunks": [
    {
      "id": "sales_invoice.py:SalesInvoice",
      "symbol_type": "class",
      "symbol_name": "SalesInvoice",
      "doctype": "Sales Invoice",
      "code": "class SalesInvoice(SellingController):\n    ...",
      "start_line": 45,
      "end_line": 890,
      "parent_classes": ["SellingController", "AccountsController", "TransactionBase"]
    },
    {
      "id": "sales_invoice.py:SalesInvoice.validate",
      "symbol_type": "method",
      "symbol_name": "validate",
      "parent_class": "SalesInvoice",
      "hook_type": "validate",
      "code": "def validate(self):\n    super().validate()\n    self.validate_posting_time()\n    ...",
      "start_line": 120,
      "end_line": 145,
      "calls": ["validate_posting_time", "validate_customer", "validate_items"],
      "docstring": "Validate invoice before save"
    },
    {
      "id": "sales_invoice.py:SalesInvoice.on_submit",
      "symbol_type": "method",
      "symbol_name": "on_submit",
      "parent_class": "SalesInvoice",
      "hook_type": "on_submit",
      "code": "def on_submit(self):\n    super().on_submit()\n    self.make_gl_entries()\n    ...",
      "start_line": 234,
      "end_line": 267,
      "calls": ["make_gl_entries", "update_stock_ledger", "update_billing_status"],
      "docstring": "Handle invoice submission - creates accounting and stock entries"
    }
  ]
}
```

---

## Part 3: Hybrid Retrieval for Code

### 3.1 Why Hybrid Search?

From **AI Engineering (Chip Huyen)**:
> "Term-based retrieval is much faster than embedding-based retrieval for both indexing and querying. It works well out of the box."

For code, **both** are essential:
- **BM25 (sparse)**: Exact matches for `on_submit`, `make_gl_entries`, error messages
- **Dense (semantic)**: "What creates accounting entries?" → finds `make_gl_entries`

### 3.2 Hybrid Search Implementation

```python
from lancedb import connect
from rank_bm25 import BM25Okapi
import numpy as np

class HybridCodeRetriever:
    """
    Combines dense (vector) and sparse (BM25) retrieval.
    Uses Reciprocal Rank Fusion (RRF) for score combination.
    """

    def __init__(self, db_path: str):
        self.db = connect(db_path)
        self.chunks_table = self.db.open_table("chunks")
        self._build_bm25_index()

    def _build_bm25_index(self):
        """Build BM25 index from chunk code."""
        chunks = self.chunks_table.to_pandas()
        tokenized = [self._tokenize_code(c) for c in chunks['code']]
        self.bm25 = BM25Okapi(tokenized)
        self.chunk_ids = chunks['id'].tolist()

    def _tokenize_code(self, code: str) -> list[str]:
        """Tokenize code for BM25 - split on whitespace, punctuation."""
        import re
        # Split camelCase and snake_case
        code = re.sub(r'([a-z])([A-Z])', r'\1 \2', code)
        code = code.replace('_', ' ')
        return code.lower().split()

    def search(
        self,
        query: str,
        k: int = 10,
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3
    ) -> list[dict]:
        """
        Hybrid search with RRF fusion.

        Args:
            query: Natural language or code query
            k: Number of results to return
            dense_weight: Weight for semantic search (0-1)
            sparse_weight: Weight for BM25 search (0-1)
        """
        # Dense retrieval
        query_embedding = self._embed(query)
        dense_results = self.chunks_table.search(query_embedding).limit(k * 2).to_list()

        # Sparse retrieval
        query_tokens = self._tokenize_code(query)
        bm25_scores = self.bm25.get_scores(query_tokens)
        sparse_indices = np.argsort(bm25_scores)[-k * 2:][::-1]
        sparse_results = [
            {"id": self.chunk_ids[i], "score": bm25_scores[i]}
            for i in sparse_indices
        ]

        # Reciprocal Rank Fusion
        fused = self._rrf_fusion(
            dense_results,
            sparse_results,
            dense_weight,
            sparse_weight
        )

        return fused[:k]

    def _rrf_fusion(
        self,
        dense: list,
        sparse: list,
        dense_weight: float,
        sparse_weight: float,
        k: int = 60
    ) -> list[dict]:
        """
        Reciprocal Rank Fusion (RRF) from Chip Huyen's AI Engineering:
        Score(D) = Σ(i=1 to n) weight_i / (k + rank_i(D))
        """
        scores = {}

        # Dense scores
        for rank, result in enumerate(dense):
            doc_id = result['id']
            scores[doc_id] = scores.get(doc_id, 0) + dense_weight / (k + rank + 1)

        # Sparse scores
        for rank, result in enumerate(sparse):
            doc_id = result['id']
            scores[doc_id] = scores.get(doc_id, 0) + sparse_weight / (k + rank + 1)

        # Sort by fused score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [{"id": doc_id, "rrf_score": score} for doc_id, score in sorted_results]
```

### 3.3 Query Examples for Sales Invoice

| Query Type | Example | Best Retriever |
|------------|---------|----------------|
| Exact symbol | "on_submit method" | BM25 |
| Error message | "ValidationError: Credit limit exceeded" | BM25 |
| Semantic | "What creates accounting entries?" | Dense |
| Workflow | "Invoice submission process" | Hybrid |
| Business rule | "How is tax calculated?" | Hybrid |

---

## Part 4: Graph-Based Context Expansion

### 4.1 Why Graph + Vector?

From **CodeCompass production learnings**:
> "Vector-only first was a mistake. Could not answer 'what calls this function?' - needed graph."

Vector search finds **similar** code. Graph search finds **related** code.

### 4.2 Graph Schema for Code Relationships

```sql
-- SQLite schema for code graph

CREATE TABLE symbols (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    symbol_type TEXT NOT NULL,  -- 'class', 'method', 'function'
    symbol_name TEXT NOT NULL,
    parent_id TEXT,             -- Parent class/module
    doctype TEXT,               -- ERPNext DocType name
    start_line INTEGER,
    end_line INTEGER,
    code TEXT,
    FOREIGN KEY (parent_id) REFERENCES symbols(id)
);

CREATE TABLE calls (
    caller_id TEXT NOT NULL,
    callee_id TEXT NOT NULL,
    call_type TEXT,             -- 'direct', 'super', 'frappe_api'
    line_number INTEGER,
    PRIMARY KEY (caller_id, callee_id),
    FOREIGN KEY (caller_id) REFERENCES symbols(id),
    FOREIGN KEY (callee_id) REFERENCES symbols(id)
);

CREATE TABLE imports (
    symbol_id TEXT NOT NULL,
    imported_module TEXT NOT NULL,
    imported_name TEXT,
    alias TEXT,
    PRIMARY KEY (symbol_id, imported_module, imported_name),
    FOREIGN KEY (symbol_id) REFERENCES symbols(id)
);

CREATE TABLE inheritance (
    child_id TEXT NOT NULL,
    parent_id TEXT NOT NULL,
    order_index INTEGER,        -- MRO order
    PRIMARY KEY (child_id, parent_id),
    FOREIGN KEY (child_id) REFERENCES symbols(id)
);
```

### 4.3 Graph Expansion Queries

```python
def expand_context_with_graph(
    initial_chunks: list[str],
    db: sqlite3.Connection,
    expansion_depth: int = 2
) -> list[str]:
    """
    Expand retrieved chunks using graph relationships.

    From initial semantic matches, traverse graph to find:
    - Functions called by these chunks
    - Functions that call these chunks
    - Parent classes and inherited methods
    - Related hooks in the same DocType
    """
    expanded = set(initial_chunks)

    for _ in range(expansion_depth):
        new_chunks = set()

        for chunk_id in expanded:
            # Get callees (what does this function call?)
            callees = db.execute("""
                SELECT callee_id FROM calls
                WHERE caller_id = ?
            """, (chunk_id,)).fetchall()
            new_chunks.update(c[0] for c in callees)

            # Get callers (what calls this function?)
            callers = db.execute("""
                SELECT caller_id FROM calls
                WHERE callee_id = ?
            """, (chunk_id,)).fetchall()
            new_chunks.update(c[0] for c in callers)

            # Get parent class methods (inheritance)
            parents = db.execute("""
                SELECT s.id FROM symbols s
                JOIN inheritance i ON s.parent_id = i.parent_id
                WHERE i.child_id = (
                    SELECT parent_id FROM symbols WHERE id = ?
                )
            """, (chunk_id,)).fetchall()
            new_chunks.update(p[0] for p in parents)

        expanded.update(new_chunks)

    return list(expanded)
```

### 4.4 Sales Invoice Graph Traversal Example

```
Query: "What happens when Sales Invoice is submitted?"

STEP 1: Vector Search
────────────────────
Found: SalesInvoice.on_submit (score: 0.92)

STEP 2: Graph Expansion (depth=2)
────────────────────────────────
on_submit
├── calls → make_gl_entries()
│           ├── calls → get_gl_entries()
│           └── calls → make_entry()
├── calls → update_stock_ledger()
│           └── calls → make_sl_entries()
├── calls → update_billing_status()
├── inherits → SellingController.on_submit()
│              └── inherits → AccountsController.on_submit()
└── same_doctype → validate() [related hook]

STEP 3: Context Assembly
────────────────────────
Total chunks: 9 (from graph expansion)
Token budget: 8000
Selected: Top 6 by relevance + importance
```

---

## Part 5: Context Construction

### 5.1 Context Formatting for LLM

From **Hands-On Large Language Models**:
> "The generation step prompts the LLM with the question AND the retrieved information."

For code, structure matters:

```python
def format_context_for_llm(
    chunks: list[CodeChunk],
    query: str,
    token_budget: int = 8000
) -> str:
    """
    Format retrieved code chunks for LLM consumption.

    Structure:
    1. High-level summary (bounded context, key entities)
    2. Relevant code with annotations
    3. Relationship diagram
    """
    context_parts = []

    # Part 1: Domain Summary
    context_parts.append(f"""
## Domain Context: Sales Invoice (Selling Bounded Context)

**DocType**: Sales Invoice
**Module**: erpnext.accounts
**Primary Responsibility**: Record customer sales, create accounting entries, update stock

**Key Relationships**:
- Customer (master) → Sales Invoice (transaction)
- Sales Invoice → Sales Invoice Item (child table)
- Sales Invoice → GL Entry (accounting impact)
- Sales Invoice → Stock Ledger Entry (inventory impact)
""")

    # Part 2: Relevant Code
    context_parts.append("\n## Relevant Code\n")

    tokens_used = estimate_tokens(context_parts[0])

    for chunk in prioritize_chunks(chunks, query):
        chunk_text = format_chunk(chunk)
        chunk_tokens = estimate_tokens(chunk_text)

        if tokens_used + chunk_tokens > token_budget:
            break

        context_parts.append(chunk_text)
        tokens_used += chunk_tokens

    # Part 3: Call Flow Diagram
    context_parts.append(format_call_diagram(chunks))

    return "\n".join(context_parts)

def format_chunk(chunk: CodeChunk) -> str:
    """Format a single chunk with metadata."""
    return f"""
### {chunk.symbol_name} ({chunk.symbol_type})
**File**: `{chunk.file_path}:{chunk.start_line}`
**Hook Type**: {chunk.hook_type or 'N/A'}
**Calls**: {', '.join(chunk.calls[:5]) if chunk.calls else 'None'}

```python
{chunk.code}
```
"""
```

### 5.2 Example Context Output

```markdown
## Domain Context: Sales Invoice (Selling Bounded Context)

**DocType**: Sales Invoice
**Module**: erpnext.accounts
**Primary Responsibility**: Record customer sales, create accounting entries, update stock

**Key Relationships**:
- Customer (master) → Sales Invoice (transaction)
- Sales Invoice → Sales Invoice Item (child table)
- Sales Invoice → GL Entry (accounting impact)
- Sales Invoice → Stock Ledger Entry (inventory impact)

## Relevant Code

### on_submit (method)
**File**: `erpnext/accounts/doctype/sales_invoice/sales_invoice.py:234`
**Hook Type**: on_submit
**Calls**: make_gl_entries, update_stock_ledger, update_billing_status

```python
def on_submit(self):
    super().on_submit()

    if self.update_stock:
        self.update_stock_ledger()

    self.make_gl_entries()
    self.update_billing_status()

    if self.is_return:
        self.update_returns()
```

### make_gl_entries (method)
**File**: `erpnext/accounts/doctype/sales_invoice/sales_invoice.py:456`
**Hook Type**: N/A
**Calls**: get_gl_entries, make_entry

```python
def make_gl_entries(self):
    gl_entries = self.get_gl_entries()

    from erpnext.accounts.general_ledger import make_gl_entries
    make_gl_entries(gl_entries, cancel=(self.docstatus == 2))
```

## Call Flow

```
submit()
  └── on_submit()
        ├── update_stock_ledger()
        │     └── make_sl_entries()
        ├── make_gl_entries()
        │     ├── get_gl_entries()
        │     └── general_ledger.make_gl_entries()
        └── update_billing_status()
```
```

---

## Part 6: Evaluation Framework

### 6.1 RAGAs Metrics Applied to Code

From **Unlocking Data with Generative AI and RAG**:
> "Context Precision: Signal-to-noise ratio; evaluates whether relevant items are ranked higher"

For code intelligence:

| Metric | Definition for Code | Target |
|--------|---------------------|--------|
| **Context Precision** | % of retrieved code that's relevant to query | > 75% |
| **Context Recall** | % of relevant code that was retrieved | > 80% |
| **Faithfulness** | Are claims about code grounded in retrieved context? | > 85% |
| **Answer Accuracy** | Does response correctly describe code behavior? | > 80% |

### 6.2 Code-Specific Evaluation Metrics

```python
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, context_recall

def evaluate_code_rag(
    questions: list[str],
    contexts: list[list[str]],
    answers: list[str],
    ground_truths: list[str]
) -> dict:
    """
    Evaluate code RAG quality using RAGAs + custom metrics.
    """
    # Standard RAGAs evaluation
    ragas_results = evaluate(
        dataset=Dataset.from_dict({
            "question": questions,
            "contexts": contexts,
            "answer": answers,
            "ground_truth": ground_truths
        }),
        metrics=[faithfulness, context_precision, context_recall]
    )

    # Code-specific metrics
    code_metrics = {
        "file_accuracy": calculate_file_accuracy(contexts, ground_truths),
        "symbol_coverage": calculate_symbol_coverage(contexts, ground_truths),
        "call_chain_completeness": calculate_call_chain_completeness(contexts),
        "hook_identification": calculate_hook_identification(contexts)
    }

    return {**ragas_results, **code_metrics}

def calculate_file_accuracy(contexts: list, ground_truths: list) -> float:
    """% of retrieved files that should have been retrieved."""
    correct = 0
    total = 0

    for ctx, gt in zip(contexts, ground_truths):
        retrieved_files = extract_file_paths(ctx)
        expected_files = extract_file_paths(gt)

        correct += len(set(retrieved_files) & set(expected_files))
        total += len(expected_files)

    return correct / total if total > 0 else 0

def calculate_symbol_coverage(contexts: list, ground_truths: list) -> float:
    """% of expected symbols (functions, classes) that were retrieved."""
    # Similar to file accuracy but at symbol level
    pass

def calculate_call_chain_completeness(contexts: list) -> float:
    """Did we retrieve the full call chain for workflow queries?"""
    # Check if on_submit → make_gl_entries → make_entry chain is complete
    pass
```

### 6.3 Test Set for Sales Invoice

```yaml
# test_set_sales_invoice.yaml
version: "v1"
questions:
  - id: "si-001"
    question: "What happens when a Sales Invoice is submitted?"
    expected_files:
      - "erpnext/accounts/doctype/sales_invoice/sales_invoice.py"
      - "erpnext/accounts/general_ledger.py"
      - "erpnext/stock/stock_ledger.py"
    expected_symbols:
      - "SalesInvoice.on_submit"
      - "make_gl_entries"
      - "update_stock_ledger"
    expected_concepts:
      - "GL Entry creation"
      - "Stock Ledger update"
      - "Billing status update"

  - id: "si-002"
    question: "How is discount calculated in Sales Invoice?"
    expected_files:
      - "erpnext/controllers/taxes_and_totals.py"
      - "erpnext/accounts/doctype/pricing_rule/pricing_rule.py"
    expected_symbols:
      - "calculate_taxes_and_totals"
      - "apply_pricing_rule"
    expected_concepts:
      - "Item-level discount"
      - "Invoice-level discount"
      - "Pricing rules"

  - id: "si-003"
    question: "What validations run before Sales Invoice is saved?"
    expected_files:
      - "erpnext/accounts/doctype/sales_invoice/sales_invoice.py"
      - "erpnext/controllers/accounts_controller.py"
    expected_symbols:
      - "SalesInvoice.validate"
      - "validate_posting_time"
      - "validate_customer"
      - "check_credit_limit"
    expected_concepts:
      - "Credit limit check"
      - "Stock availability"
      - "Posting date validation"
```

### 6.4 Baseline vs Enhanced Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EXPERIMENT: Sales Invoice Query - "What happens on submit?"                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BASELINE (Vanilla Claude Code)                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Response: "When a Sales Invoice is submitted in ERPNext, it typically      │
│            creates accounting entries and may update inventory..."          │
│                                                                              │
│  Scores:                                                                     │
│  • Accuracy: 2/5 (vague, some hallucination)                                │
│  • Completeness: 2/5 (missed specific methods)                              │
│  • File Accuracy: 0% (no files mentioned)                                   │
│  • Symbol Coverage: 0% (no symbols mentioned)                               │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  ENHANCED (With Code Intelligence Context)                                   │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Response: "When a Sales Invoice is submitted, the `on_submit` method       │
│            in sales_invoice.py:234 executes:                                │
│            1. `make_gl_entries()` - Creates General Ledger entries          │
│            2. `update_stock_ledger()` - Updates inventory                   │
│            3. `update_billing_status()` - Links to Sales Order..."          │
│                                                                              │
│  Scores:                                                                     │
│  • Accuracy: 5/5 (correct methods, line numbers)                            │
│  • Completeness: 4/5 (covered main flow, some edge cases missed)           │
│  • File Accuracy: 100% (3/3 files correct)                                  │
│  • Symbol Coverage: 85% (6/7 symbols mentioned)                             │
│                                                                              │
│  DELTA: +150% accuracy, +100% completeness                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Go Migration Mapping

### 7.1 ERPNext Pattern → Go Pattern

| ERPNext (Python) | Go Equivalent | Notes |
|------------------|---------------|-------|
| `class SalesInvoice(Document)` | `type SalesInvoice struct` | Entity/Aggregate |
| `def validate(self)` | `func (i *SalesInvoice) Validate() error` | Validation method |
| `def on_submit(self)` | Domain Event Handler | Separate handler struct |
| `self.append("items", {...})` | `i.Items = append(i.Items, Item{})` | Child table |
| `frappe.get_doc()` | Repository pattern | Data access |
| `@frappe.whitelist()` | gRPC/REST handler | API exposure |

### 7.2 Migration Context Generation

The code intelligence tool should generate migration hints:

```markdown
## Migration Hint: SalesInvoice.on_submit → Go

**Source Pattern**: ERPNext hook method
**Target Pattern**: Domain Event + Handler

### Recommended Go Structure:

```go
// Domain Event
type InvoiceSubmitted struct {
    InvoiceID string
    Invoice   *SalesInvoice
    Timestamp time.Time
}

// Event Handler
type InvoiceSubmittedHandler struct {
    glService    *accounting.GLEntryService
    stockService *inventory.StockService
    eventBus     *events.Bus
}

func (h *InvoiceSubmittedHandler) Handle(ctx context.Context, event InvoiceSubmitted) error {
    // 1. Create GL entries (was: make_gl_entries)
    if err := h.glService.CreateEntries(ctx, event.Invoice); err != nil {
        return fmt.Errorf("gl entries: %w", err)
    }

    // 2. Update stock (was: update_stock_ledger)
    if event.Invoice.UpdateStock {
        if err := h.stockService.UpdateLedger(ctx, event.Invoice); err != nil {
            return fmt.Errorf("stock update: %w", err)
        }
    }

    return nil
}
```

### Why This Pattern:
- Separates the "what happened" (event) from "what to do" (handler)
- Each handler can be tested independently
- Easy to add new side effects without modifying SalesInvoice
- Matches DDD aggregate + domain events pattern
```

---

## Part 8: MCP Tool Implementation

### 8.1 MCP Tools for Sales Invoice Context

```python
from mcp import Server, Tool

server = Server("code-intelligence")

@server.tool("search_code")
async def search_code(query: str, doctype: str = None, k: int = 10) -> dict:
    """
    Search for code related to a natural language query.

    Args:
        query: Natural language question about the code
        doctype: Optional ERPNext DocType to filter by
        k: Number of results to return

    Returns:
        Relevant code chunks with metadata
    """
    retriever = HybridCodeRetriever(DB_PATH)

    if doctype:
        results = retriever.search(query, k=k, filter={"doctype": doctype})
    else:
        results = retriever.search(query, k=k)

    # Expand with graph
    expanded = expand_context_with_graph([r['id'] for r in results])

    # Format for LLM
    context = format_context_for_llm(expanded, query)

    return {
        "context": context,
        "sources": [r['id'] for r in results],
        "expanded_count": len(expanded)
    }

@server.tool("trace_workflow")
async def trace_workflow(entry_point: str, depth: int = 3) -> dict:
    """
    Trace what happens when a specific method is called.

    Args:
        entry_point: Method to trace (e.g., "SalesInvoice.on_submit")
        depth: How deep to trace the call graph

    Returns:
        Call flow diagram and relevant code
    """
    graph = build_call_graph(entry_point, depth)

    return {
        "diagram": graph.to_mermaid(),
        "nodes": [format_chunk(n) for n in graph.nodes],
        "edges": graph.edges
    }

@server.tool("explain_doctype")
async def explain_doctype(doctype: str) -> dict:
    """
    Get comprehensive explanation of an ERPNext DocType.

    Args:
        doctype: DocType name (e.g., "Sales Invoice")

    Returns:
        Schema, methods, hooks, relationships
    """
    schema = get_doctype_schema(doctype)
    methods = get_doctype_methods(doctype)
    hooks = get_doctype_hooks(doctype)
    relationships = get_doctype_relationships(doctype)

    return {
        "schema": schema,
        "methods": methods,
        "hooks": hooks,
        "relationships": relationships,
        "bounded_context": infer_bounded_context(doctype)
    }

@server.tool("migration_hint")
async def migration_hint(symbol: str, target_lang: str = "go") -> dict:
    """
    Generate migration hints for a Python symbol to target language.

    Args:
        symbol: Python symbol to migrate (e.g., "SalesInvoice.on_submit")
        target_lang: Target language (default: "go")

    Returns:
        Recommended patterns, code structure, considerations
    """
    source_code = get_symbol_code(symbol)
    pattern = identify_pattern(source_code)

    hint = generate_migration_hint(source_code, pattern, target_lang)

    return {
        "source_pattern": pattern,
        "target_pattern": hint.target_pattern,
        "sample_code": hint.sample_code,
        "considerations": hint.considerations
    }
```

---

## Part 9: Implementation Checklist

### Week 1-2: Extraction (Crawl)
- [ ] Set up tree-sitter Python parser
- [ ] Extract functions, classes, methods from sales_invoice.py
- [ ] Extract ERPNext-specific patterns (hooks, DocType)
- [ ] Build initial chunk schema
- [ ] Validate: 90%+ symbol coverage

### Week 3-4: Retrieval (Walk)
- [ ] Generate embeddings (bge-large-en-v1.5)
- [ ] Set up LanceDB vector index
- [ ] Implement BM25 index
- [ ] Implement hybrid search with RRF
- [ ] Build graph relationships (calls, imports)
- [ ] Validate: 70%+ retrieval precision

### Week 5-6: Integration (Run)
- [ ] Implement MCP server with tools
- [ ] Connect to Claude Code
- [ ] Run baseline vs enhanced experiments
- [ ] Calculate delta metrics
- [ ] Validate: +30% accuracy vs baseline

### Week 7-8: Migration Features
- [ ] Implement pattern detection
- [ ] Generate Go migration hints
- [ ] Add migration_hint MCP tool
- [ ] Document migration patterns

---

## Related Documents

- [Evolution Framework](../01-Product/03-Evolution-Framework.md)
- [Enterprise Tooling](../03-AI-Platform/05-Enterprise-Tooling.md)
- [Technology Stack](../02-Engineering/03-Technology-Stack.md)
- [Quality Metrics Guide](../03-AI-Platform/04-Quality-Metrics.md)

---

*Last Updated: 2026-01-14*
