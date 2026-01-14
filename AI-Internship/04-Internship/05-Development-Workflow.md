# Development Workflow: End-to-End

## Overview

This document describes the complete intern workflow from environment setup through evidence collection. You will:

1. **Understand** ERPNext by running it
2. **Analyze** ERPNext using your Python tool
3. **Generate** equivalent Go code with AI assistance
4. **Validate** business parity
5. **Measure** your tool's effectiveness vs vanilla AI editors
6. **Document** evidence using AI Engineering patterns

---

## The Big Picture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  INTERN DEVELOPMENT WORKFLOW                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  PHASE 1: UNDERSTAND                                                   │  │
│  │  ─────────────────────────────────────────────────────────────────────│  │
│  │  ERPNext Instance (Cloud/Local)     ERPNext Codebase (VS Code)        │  │
│  │          │                                   │                         │  │
│  │          ▼                                   ▼                         │  │
│  │  "Click Submit on Invoice"      "Read sales_invoice.py"               │  │
│  │          │                                   │                         │  │
│  │          └─────────────┬─────────────────────┘                         │  │
│  │                        ▼                                               │  │
│  │              Understanding: "on_submit creates GL entries"             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  PHASE 2: INDEX & ANALYZE                                              │  │
│  │  ─────────────────────────────────────────────────────────────────────│  │
│  │  Your Python Tool                                                      │  │
│  │          │                                                             │  │
│  │          ├── Parse AST → Extract symbols                              │  │
│  │          ├── Build embeddings → Vector index                          │  │
│  │          ├── Map relationships → Call graph                           │  │
│  │          └── Extract domain → Bounded contexts                        │  │
│  │                        │                                               │  │
│  │                        ▼                                               │  │
│  │              Code Intelligence Index                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  PHASE 3: GENERATE GO CODE                                             │  │
│  │  ─────────────────────────────────────────────────────────────────────│  │
│  │                                                                        │  │
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐           │  │
│  │  │ Your Tool   │─────▶│   Context   │─────▶│  LLM (via   │           │  │
│  │  │ (retrieves) │      │  (focused)  │      │ Claude/GPT) │           │  │
│  │  └─────────────┘      └─────────────┘      └──────┬──────┘           │  │
│  │                                                   │                   │  │
│  │                                                   ▼                   │  │
│  │                                          Go Code Output               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  PHASE 4: VALIDATE PARITY                                              │  │
│  │  ─────────────────────────────────────────────────────────────────────│  │
│  │  ERPNext (Python)              Your Go Code                           │  │
│  │        │                             │                                 │  │
│  │        ▼                             ▼                                 │  │
│  │  "Submit Invoice"             "Submit Invoice"                        │  │
│  │        │                             │                                 │  │
│  │        ▼                             ▼                                 │  │
│  │  GL Entries Created           GL Entries Created                      │  │
│  │        │                             │                                 │  │
│  │        └──────────── = ──────────────┘                                │  │
│  │                 Business Parity ✓                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  PHASE 5: MEASURE & PROVE                                              │  │
│  │  ─────────────────────────────────────────────────────────────────────│  │
│  │                                                                        │  │
│  │  Your Tool + LLM        vs        Vanilla AI Editor                   │  │
│  │  (with context)                   (no context)                        │  │
│  │        │                               │                               │  │
│  │        ▼                               ▼                               │  │
│  │  ┌───────────┐                  ┌───────────┐                         │  │
│  │  │ Tokens: ↓ │                  │ Tokens: ↑ │                         │  │
│  │  │ Quality:↑ │                  │ Quality:↓ │                         │  │
│  │  │ Domain: ✓ │                  │ Domain: ? │                         │  │
│  │  └───────────┘                  └───────────┘                         │  │
│  │                                                                        │  │
│  │  EVIDENCE: Token reduction, context precision, code quality           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Environment Setup

### 1.1 Required Setup

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  YOUR WORKSTATION                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  VS Code Window 1: ERPNext Codebase                                          │
│  ├── /path/to/erpnext/                                                      │
│  ├── /path/to/frappe/                                                       │
│  └── Extensions: Python, Pylance                                            │
│                                                                              │
│  VS Code Window 2: Your Python Tool                                          │
│  ├── /path/to/code-intelligence/                                            │
│  └── Extensions: Python, Pylance, Jupyter                                   │
│                                                                              │
│  VS Code Window 3: Go Output (later)                                         │
│  ├── /path/to/erpnext-go/                                                   │
│  └── Extensions: Go                                                          │
│                                                                              │
│  Browser: ERPNext Instance                                                   │
│  └── https://your-instance.erpnext.com OR http://localhost:8000             │
│                                                                              │
│  Terminal: AI Editor (for comparison)                                        │
│  ├── Claude Code: claude                                                    │
│  ├── Cursor: cursor .                                                       │
│  └── Aider: aider                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 ERPNext Instance Options

| Option | Setup | Best For |
|--------|-------|----------|
| **Frappe Cloud** | Sign up at frappecloud.com | Quick start, no local setup |
| **Docker** | `docker-compose up` | Local development, full control |
| **Bench** | `bench init` | Deep understanding, contribution |

**Minimum Setup (Frappe Cloud)**:
```bash
# 1. Sign up at https://frappecloud.com
# 2. Create a free trial site
# 3. Install ERPNext app
# 4. Access at https://yoursite.frappe.cloud
```

**Local Setup (Docker)**:
```bash
# Clone and start
git clone https://github.com/frappe/frappe_docker
cd frappe_docker
docker-compose up -d

# Access at http://localhost:8080
# Default: Administrator / admin
```

### 1.3 Understanding ERPNext (Before Coding)

**Required Exploration** (Week 1, Day 1-2):

| Task | What You Learn |
|------|----------------|
| Create a Customer | Master data pattern |
| Create an Item | Inventory basics |
| Create a Sales Order | Transaction workflow |
| Create a Delivery Note | Fulfillment process |
| Create a Sales Invoice | **Your target module** |
| Submit the Invoice | **on_submit hooks trigger** |
| Check GL Entries | Accounting impact |
| Check Stock Ledger | Inventory impact |

**Document Your Understanding**:
```yaml
# understanding/sales-invoice-flow.yaml
observed_flow:
  - action: "Click Submit on Sales Invoice"
    ui_result: "Status changes to Submitted"
    backend_effects:
      - "GL Entry created (verified in Accounts > GL Entry)"
      - "Stock Ledger Entry created (if Update Stock checked)"
      - "Outstanding amount updated on Customer"

  - action: "Try to edit submitted invoice"
    ui_result: "Error: Cannot edit submitted document"
    backend_reason: "docstatus = 1 (submitted)"

questions_for_codebase:
  - "Where is on_submit defined?"
  - "What creates the GL Entry?"
  - "How is stock updated?"
```

---

## Phase 2: Build Your Index

### 2.1 Index ERPNext with Your Tool

```bash
# In your Python tool directory
cd /path/to/code-intelligence

# Index the Sales Invoice module
python -m cli index \
  --path /path/to/erpnext/erpnext/accounts/doctype/sales_invoice \
  --include-deps \
  --output ./data/sales_invoice_index

# Index related controllers
python -m cli index \
  --path /path/to/erpnext/erpnext/controllers \
  --filter "selling_controller.py,accounts_controller.py,taxes_and_totals.py" \
  --output ./data/controllers_index

# Verify index quality
python -m cli status --index ./data/sales_invoice_index
```

**Expected Output**:
```
Index Status: sales_invoice_index
═══════════════════════════════════════════════════════════
Files indexed:        12
Symbols extracted:    156
  - Classes:          4
  - Methods:          89
  - Functions:        63

Embeddings:           156 (bge-large-en-v1.5)
Graph edges:          234 (call relationships)

DocTypes found:       1 (Sales Invoice)
Hooks identified:     6 (validate, on_submit, on_cancel, ...)
═══════════════════════════════════════════════════════════
```

### 2.2 Verify Index Quality

```python
# test_index_quality.py
from code_intelligence import CodeIndex

index = CodeIndex.load("./data/sales_invoice_index")

# Test 1: Can we find on_submit?
results = index.search("on_submit method Sales Invoice")
assert "SalesInvoice.on_submit" in [r.id for r in results[:3]]

# Test 2: Can we trace the call chain?
chain = index.trace_calls("SalesInvoice.on_submit", depth=2)
assert "make_gl_entries" in chain.callees

# Test 3: Do we have the validation hooks?
hooks = index.get_hooks("Sales Invoice")
assert "validate" in hooks
assert "on_submit" in hooks

print("Index quality: PASS")
```

---

## Phase 3: Generate Go Code

### 3.1 The Generation Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  GO CODE GENERATION WORKFLOW                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT: "Generate Go equivalent of SalesInvoice.on_submit"                   │
│                                                                              │
│  STEP 1: Your Tool Retrieves Context                                         │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Query → Hybrid Search → Graph Expansion → Context Assembly                 │
│                                                                              │
│  Retrieved Context (focused, ~2000 tokens):                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ## SalesInvoice.on_submit                                            │   │
│  │ File: sales_invoice.py:234                                           │   │
│  │ ```python                                                            │   │
│  │ def on_submit(self):                                                 │   │
│  │     super().on_submit()                                              │   │
│  │     self.make_gl_entries()                                           │   │
│  │     self.update_stock_ledger()                                       │   │
│  │ ```                                                                  │   │
│  │                                                                      │   │
│  │ ## Call Chain                                                        │   │
│  │ on_submit → make_gl_entries → get_gl_entries → make_entry           │   │
│  │                                                                      │   │
│  │ ## Domain Context                                                    │   │
│  │ - Bounded Context: Selling (primary), Accounts (impact)             │   │
│  │ - Aggregate: SalesInvoice (root), Items (children)                  │   │
│  │ - Domain Event: InvoiceSubmitted                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  STEP 2: LLM Generates Go Code                                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Prompt: "Using the context above, generate Go code that implements         │
│           the same behavior as on_submit, following DDD patterns."          │
│                                                                              │
│  Output:                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ // Domain Event                                                      │   │
│  │ type InvoiceSubmitted struct {                                       │   │
│  │     InvoiceID string                                                 │   │
│  │     Invoice   *SalesInvoice                                          │   │
│  │ }                                                                    │   │
│  │                                                                      │   │
│  │ // Handler                                                           │   │
│  │ func (h *InvoiceSubmittedHandler) Handle(event InvoiceSubmitted) {   │   │
│  │     h.glService.CreateEntries(event.Invoice)                         │   │
│  │     h.stockService.UpdateLedger(event.Invoice)                       │   │
│  │ }                                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Generation Script

```python
# generate_go.py
from code_intelligence import CodeIndex, ContextBuilder
from openai import OpenAI

def generate_go_equivalent(
    symbol: str,
    index: CodeIndex,
    model: str = "gpt-4o"
) -> dict:
    """
    Generate Go code equivalent for a Python symbol.

    Returns:
        - go_code: Generated Go code
        - context_used: Context provided to LLM
        - tokens_used: Token count
        - pattern_applied: DDD pattern identified
    """
    # Step 1: Retrieve focused context
    context_builder = ContextBuilder(index)
    context = context_builder.build(
        query=f"Full implementation and behavior of {symbol}",
        include_call_chain=True,
        include_domain_context=True,
        max_tokens=2000
    )

    # Step 2: Build prompt
    prompt = f"""
You are migrating ERPNext (Python/Frappe) to Go.

## Source Context
{context.formatted}

## Task
Generate Go code that implements the same business behavior as `{symbol}`.

## Requirements
1. Follow DDD patterns (entities, value objects, domain events, handlers)
2. Use Go idioms (error handling, interfaces, structs)
3. Preserve all business logic
4. Add comments explaining the mapping from Python

## Output Format
Provide:
1. Go structs for entities
2. Domain event if applicable
3. Handler/service implementation
4. Brief explanation of pattern choices
"""

    # Step 3: Generate with LLM
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return {
        "go_code": response.choices[0].message.content,
        "context_used": context.formatted,
        "context_tokens": context.token_count,
        "response_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
        "pattern_applied": context.domain_info.get("pattern", "unknown")
    }
```

### 3.3 Running Generation

```bash
# Generate Go for on_submit
python generate_go.py \
  --symbol "SalesInvoice.on_submit" \
  --index ./data/sales_invoice_index \
  --output ./generated/sales_invoice_submit.go

# Generate Go for validate
python generate_go.py \
  --symbol "SalesInvoice.validate" \
  --index ./data/sales_invoice_index \
  --output ./generated/sales_invoice_validate.go

# Generate Go for full module
python generate_go.py \
  --module "Sales Invoice" \
  --index ./data/sales_invoice_index \
  --output ./generated/sales_invoice/
```

---

## Phase 4: Validate Business Parity

### 4.1 Parity Testing Strategy

Since real enterprise developers aren't available, **you assume the role of developer** validating the generated code.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PARITY TESTING MATRIX                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CAPABILITY                    │ ERPNext (Python)  │ Your Go Code           │
│  ─────────────────────────────│───────────────────│────────────────────────│
│  Submit Invoice                │ ✓ Works          │ ? Test                 │
│  Creates GL Entry (Debit)      │ ✓ Verified       │ ? Verify same logic    │
│  Creates GL Entry (Credit)     │ ✓ Verified       │ ? Verify same logic    │
│  Updates Stock Ledger          │ ✓ When checked   │ ? Same condition       │
│  Validates Credit Limit        │ ✓ Blocks if over │ ? Same behavior        │
│  Calculates Tax                │ ✓ Correct        │ ? Same calculation     │
│  Handles Partial Payment       │ ✓ Works          │ ? Same flow            │
│  Cancellation Reverses         │ ✓ Verified       │ ? Reverse logic        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Parity Test Cases

```yaml
# parity_tests/sales_invoice.yaml
module: "Sales Invoice"
tests:
  - id: "parity-001"
    name: "Invoice Submission Creates GL Entries"
    erpnext_behavior:
      action: "Submit Sales Invoice for $1000"
      result:
        - "Debit: Accounts Receivable $1000"
        - "Credit: Sales Income $1000"
    go_code_check:
      function: "InvoiceSubmittedHandler.Handle"
      assertions:
        - "calls glService.CreateEntry with debit = receivable_account"
        - "calls glService.CreateEntry with credit = income_account"
        - "amounts equal invoice total"

  - id: "parity-002"
    name: "Stock Update on Submit"
    erpnext_behavior:
      precondition: "Update Stock checkbox is checked"
      action: "Submit Sales Invoice with 10 units of Item A"
      result:
        - "Stock Ledger Entry created"
        - "Warehouse qty reduced by 10"
    go_code_check:
      function: "InvoiceSubmittedHandler.Handle"
      assertions:
        - "if invoice.UpdateStock then stockService.UpdateLedger called"
        - "ledger entry qty = -10"

  - id: "parity-003"
    name: "Credit Limit Validation"
    erpnext_behavior:
      precondition: "Customer credit limit = $5000, outstanding = $4500"
      action: "Try to save Sales Invoice for $1000"
      result: "ValidationError: Credit limit exceeded"
    go_code_check:
      function: "SalesInvoice.Validate"
      assertions:
        - "returns error when outstanding + new > credit_limit"
        - "error message mentions credit limit"
```

### 4.3 Parity Verification Script

```python
# verify_parity.py
import yaml
from go_code_analyzer import analyze_go_file

def verify_parity(test_file: str, go_code_dir: str) -> dict:
    """
    Verify that Go code implements same behavior as ERPNext.

    This is a static analysis + manual verification workflow.
    """
    with open(test_file) as f:
        tests = yaml.safe_load(f)

    results = []

    for test in tests['tests']:
        result = {
            "id": test['id'],
            "name": test['name'],
            "checks": []
        }

        # Analyze Go code
        go_analysis = analyze_go_file(
            f"{go_code_dir}/{test['go_code_check']['function'].split('.')[0]}.go"
        )

        # Check assertions
        for assertion in test['go_code_check']['assertions']:
            check = verify_assertion(assertion, go_analysis)
            result['checks'].append(check)

        result['passed'] = all(c['passed'] for c in result['checks'])
        results.append(result)

    return {
        "total": len(results),
        "passed": sum(1 for r in results if r['passed']),
        "failed": sum(1 for r in results if not r['passed']),
        "details": results
    }
```

---

## Phase 5: Measure & Prove Effectiveness

### 5.1 The Comparison Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EVIDENCE COLLECTION: YOUR TOOL vs VANILLA AI EDITORS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SETUP                                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Same Question Set (50 questions about Sales Invoice)                        │
│  Same LLM Backend (GPT-4o or Claude)                                         │
│  Same Evaluation Criteria                                                    │
│                                                                              │
│  COMPARISON MATRIX                                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ┌───────────────┬────────────────┬────────────────┬────────────────┐      │
│  │ Metric        │ Your Tool      │ Vanilla Claude │ Vanilla Cursor │      │
│  │               │ + LLM          │ Code           │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ Context Tokens│ ~2,000 (avg)   │ ~15,000 (full  │ ~10,000 (auto) │      │
│  │               │ (focused)      │ file dump)     │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ Precision     │ 85%            │ 45%            │ 55%            │      │
│  │ (relevant ctx)│                │                │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ Recall        │ 90%            │ 70%            │ 75%            │      │
│  │ (found needed)│                │                │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ Code Quality  │ 4.2/5          │ 2.8/5          │ 3.1/5          │      │
│  │ (human rated) │                │                │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ DDD Adherence │ 4.5/5          │ 2.0/5          │ 2.5/5          │      │
│  │               │                │                │                │      │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤      │
│  │ Domain Terms  │ 95%            │ 40%            │ 50%            │      │
│  │ Correct       │                │                │                │      │
│  └───────────────┴────────────────┴────────────────┴────────────────┘      │
│                                                                              │
│  KEY INSIGHT                                                                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Your Tool: LESS tokens, MORE precision, HIGHER quality                     │
│  Vanilla:   MORE tokens, LESS precision, LOWER quality                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Evidence Collection Protocol

```python
# collect_evidence.py
"""
Evidence Collection for Code Intelligence Tool Effectiveness

Run the same questions through:
1. Your Tool + LLM
2. Vanilla Claude Code (no context assistance)
3. Vanilla Cursor (default context)
4. Vanilla Aider (default context)

Measure and compare.
"""

import json
from datetime import datetime
from pathlib import Path

class EvidenceCollector:
    def __init__(self, output_dir: str = "./evidence"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def run_comparison(
        self,
        question: str,
        ground_truth: dict,
        approaches: list[str] = ["your_tool", "claude_code", "cursor", "aider"]
    ) -> dict:
        """
        Run same question through all approaches, collect evidence.
        """
        evidence = {
            "question": question,
            "ground_truth": ground_truth,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }

        for approach in approaches:
            result = self._run_approach(approach, question)
            evidence["results"][approach] = {
                # Token metrics
                "context_tokens": result.get("context_tokens", 0),
                "response_tokens": result.get("response_tokens", 0),
                "total_tokens": result.get("total_tokens", 0),

                # Quality metrics (human-rated)
                "accuracy_score": None,  # Fill after human review
                "completeness_score": None,
                "ddd_adherence_score": None,

                # Automated metrics
                "files_mentioned": result.get("files_mentioned", []),
                "symbols_mentioned": result.get("symbols_mentioned", []),
                "domain_terms_used": result.get("domain_terms", []),

                # Raw output
                "response": result.get("response", ""),
                "context_used": result.get("context", "")
            }

        return evidence

    def _run_approach(self, approach: str, question: str) -> dict:
        if approach == "your_tool":
            return self._run_your_tool(question)
        elif approach == "claude_code":
            return self._run_claude_code(question)
        elif approach == "cursor":
            return self._run_cursor(question)
        elif approach == "aider":
            return self._run_aider(question)

    def _run_your_tool(self, question: str) -> dict:
        """Your tool retrieves focused context, then queries LLM."""
        from code_intelligence import CodeIndex, ContextBuilder
        from openai import OpenAI

        index = CodeIndex.load("./data/sales_invoice_index")
        context = ContextBuilder(index).build(question, max_tokens=2000)

        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Use this context:\n{context.formatted}"},
                {"role": "user", "content": question}
            ]
        )

        return {
            "context_tokens": context.token_count,
            "response_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "response": response.choices[0].message.content,
            "context": context.formatted,
            "files_mentioned": context.files,
            "symbols_mentioned": context.symbols,
            "domain_terms": extract_domain_terms(response.choices[0].message.content)
        }

    def _run_claude_code(self, question: str) -> dict:
        """
        Vanilla Claude Code - no special context.
        Run manually and record results.
        """
        # This is run manually:
        # 1. Open terminal in ERPNext directory
        # 2. Run: claude
        # 3. Ask the question
        # 4. Record the response
        return {"manual": True, "instructions": "Run claude in ERPNext dir"}

    def _run_cursor(self, question: str) -> dict:
        """
        Vanilla Cursor - uses default @ context.
        Run manually and record results.
        """
        return {"manual": True, "instructions": "Open Cursor, ask question with @codebase"}

    def _run_aider(self, question: str) -> dict:
        """
        Vanilla Aider - uses default repo map.
        Run manually and record results.
        """
        return {"manual": True, "instructions": "Run aider in ERPNext dir"}
```

### 5.3 Evidence Metrics

```python
# metrics.py
"""
Metrics for evaluating code intelligence effectiveness.
Based on AI Engineering (Chip Huyen) patterns.
"""

@dataclass
class EffectivenessMetrics:
    """Metrics proving your tool's value."""

    # TOKEN EFFICIENCY
    # "Did we use fewer tokens while maintaining quality?"
    token_reduction_pct: float  # (vanilla_tokens - your_tokens) / vanilla_tokens
    tokens_per_quality_point: float  # total_tokens / quality_score

    # CONTEXT QUALITY
    # "Was the context we provided relevant and complete?"
    context_precision: float  # relevant_chunks / total_chunks
    context_recall: float  # retrieved_relevant / total_relevant

    # CODE GENERATION QUALITY
    # "Did the generated code meet requirements?"
    code_accuracy: float  # correct_statements / total_statements
    code_completeness: float  # covered_requirements / total_requirements
    code_compiles: bool  # Does the Go code compile?
    code_tests_pass: bool  # Do parity tests pass?

    # DOMAIN UNDERSTANDING
    # "Did the response demonstrate domain knowledge?"
    domain_term_accuracy: float  # correct_terms / terms_used
    bounded_context_identified: bool
    aggregate_pattern_applied: bool
    domain_events_recognized: bool

    # DDD ADHERENCE
    # "Does generated code follow DDD patterns?"
    ddd_score: float  # 1-5 rating
    patterns_applied: list[str]  # ["aggregate", "domain_event", "repository"]

def calculate_metrics(your_result: dict, vanilla_result: dict, ground_truth: dict) -> EffectivenessMetrics:
    """Calculate all effectiveness metrics."""

    # Token efficiency
    token_reduction = (
        vanilla_result['total_tokens'] - your_result['total_tokens']
    ) / vanilla_result['total_tokens']

    # Context quality (using RAGAs approach)
    precision = len(set(your_result['files_mentioned']) & set(ground_truth['expected_files'])) / \
                len(your_result['files_mentioned']) if your_result['files_mentioned'] else 0

    recall = len(set(your_result['files_mentioned']) & set(ground_truth['expected_files'])) / \
             len(ground_truth['expected_files'])

    # Domain understanding
    domain_terms = ground_truth.get('expected_domain_terms', [])
    terms_used = your_result.get('domain_terms', [])
    domain_accuracy = len(set(terms_used) & set(domain_terms)) / len(terms_used) if terms_used else 0

    return EffectivenessMetrics(
        token_reduction_pct=token_reduction,
        tokens_per_quality_point=your_result['total_tokens'] / your_result.get('quality_score', 1),
        context_precision=precision,
        context_recall=recall,
        code_accuracy=0.0,  # Filled after human review
        code_completeness=0.0,
        code_compiles=False,  # Filled after Go compile
        code_tests_pass=False,
        domain_term_accuracy=domain_accuracy,
        bounded_context_identified=False,  # Filled after review
        aggregate_pattern_applied=False,
        domain_events_recognized=False,
        ddd_score=0.0,
        patterns_applied=[]
    )
```

### 5.4 Evidence Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CODE INTELLIGENCE TOOL — EFFECTIVENESS EVIDENCE                             │
│  Generated: 2026-01-20                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SUMMARY                                                                     │
│  ═══════════════════════════════════════════════════════════════════════   │
│  Questions Evaluated: 50                                                     │
│  Modules Covered: Sales Invoice, Purchase Order, Stock Entry                │
│                                                                              │
│  TOKEN EFFICIENCY                                                            │
│  ───────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  Your Tool        ████████░░░░░░░░░░░░░░░░  2,100 tokens (avg)              │
│  Claude Code      ████████████████████████  15,200 tokens (avg)             │
│  Cursor           ██████████████████░░░░░░  11,400 tokens (avg)             │
│  Aider            █████████████████░░░░░░░  10,800 tokens (avg)             │
│                                                                              │
│  Token Reduction: 86% vs Claude Code, 82% vs Cursor, 81% vs Aider          │
│                                                                              │
│  CONTEXT QUALITY                                                             │
│  ───────────────────────────────────────────────────────────────────────── │
│                                                                              │
│           │ Precision │ Recall  │ F1 Score                                  │
│  ─────────│───────────│─────────│──────────                                 │
│  Your Tool│    85%    │   90%   │   0.87                                    │
│  Claude   │    45%    │   70%   │   0.55                                    │
│  Cursor   │    55%    │   75%   │   0.63                                    │
│  Aider    │    50%    │   72%   │   0.59                                    │
│                                                                              │
│  CODE GENERATION QUALITY (Human Rated 1-5)                                   │
│  ───────────────────────────────────────────────────────────────────────── │
│                                                                              │
│           │ Accuracy │ Complete │ DDD │ Domain │ Overall                    │
│  ─────────│──────────│──────────│─────│────────│─────────                   │
│  Your Tool│   4.2    │   4.0    │ 4.5 │  4.3   │  4.25                      │
│  Claude   │   2.8    │   2.5    │ 2.0 │  2.2   │  2.38                      │
│  Cursor   │   3.1    │   2.8    │ 2.5 │  2.6   │  2.75                      │
│  Aider    │   3.0    │   2.7    │ 2.3 │  2.4   │  2.60                      │
│                                                                              │
│  KEY FINDINGS                                                                │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  1. TOKEN EFFICIENCY                                                         │
│     Your tool uses 86% fewer tokens while achieving higher quality.         │
│     This translates to: lower cost, faster responses, better UX.            │
│                                                                              │
│  2. CONTEXT PRECISION                                                        │
│     Your tool provides 85% relevant context vs 45-55% for vanilla.          │
│     Less noise = better LLM focus = higher quality output.                  │
│                                                                              │
│  3. DOMAIN UNDERSTANDING                                                     │
│     Your tool correctly uses domain terms 95% of the time.                  │
│     Vanilla tools often hallucinate or use wrong terminology.               │
│                                                                              │
│  4. DDD ADHERENCE                                                            │
│     Your tool generates code following DDD patterns (4.5/5).                │
│     Vanilla tools produce procedural code (2.0-2.5/5).                      │
│                                                                              │
│  5. PARITY ACHIEVEMENT                                                       │
│     Generated Go code passes 85% of parity tests.                           │
│     Vanilla-generated code passes only 40% of parity tests.                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Document Evidence

### 6.1 Evidence Report Structure

```markdown
# Code Intelligence Tool - Effectiveness Report

## Executive Summary
Our code intelligence tool demonstrates significant improvements over vanilla AI editors
for enterprise legacy modernization tasks.

**Key Results:**
- 86% token reduction (2,100 vs 15,200 tokens)
- 89% improvement in context precision (85% vs 45%)
- 79% improvement in code quality (4.25 vs 2.38)
- 125% improvement in DDD adherence (4.5 vs 2.0)

## Methodology
[Link to methodology document]

## Detailed Results
[Tables and charts from evidence collection]

## Statistical Significance
[p-values, confidence intervals]

## Reproducibility
[Instructions to reproduce results]

## Limitations
[What we didn't test, potential biases]

## Conclusion
The focused, domain-aware context provided by our tool enables LLMs to generate
higher quality code with significantly fewer tokens, making it a valuable tool
for enterprise legacy modernization projects.
```

### 6.2 Evidence Files to Generate

```
evidence/
├── raw/
│   ├── experiment_001.json      # Raw data per experiment
│   ├── experiment_002.json
│   └── ...
├── metrics/
│   ├── token_efficiency.csv     # Token counts per approach
│   ├── context_quality.csv      # Precision/recall per approach
│   ├── code_quality.csv         # Human ratings
│   └── domain_understanding.csv # Domain term accuracy
├── analysis/
│   ├── statistical_tests.ipynb  # Jupyter notebook with analysis
│   ├── charts/                  # Generated visualizations
│   └── summary_stats.json
├── reports/
│   ├── effectiveness_report.md  # Main report
│   ├── methodology.md           # How we measured
│   └── presentation.pdf         # Slides for stakeholders
└── README.md                    # How to read/reproduce
```

---

## Weekly Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  WEEKLY DEVELOPMENT CYCLE                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MONDAY                                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Review last week's metrics                                               │
│  □ Identify improvement areas                                               │
│  □ Plan this week's experiments                                             │
│                                                                              │
│  TUESDAY-WEDNESDAY                                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Implement tool improvements                                              │
│  □ Run indexing on new modules                                              │
│  □ Generate Go code for target methods                                      │
│                                                                              │
│  THURSDAY                                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Run comparison experiments (Your Tool vs Vanilla)                        │
│  □ Collect evidence                                                         │
│  □ Calculate metrics                                                        │
│                                                                              │
│  FRIDAY                                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Human evaluation of generated code                                       │
│  □ Update evidence dashboard                                                │
│  □ Document findings                                                        │
│  □ Plan next week                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Developer Feedback Loop

### 6.1 Why Developer Feedback Matters

Automated metrics measure **what the tool does**. Developer feedback measures **whether it helps**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EVALUATION = AUTOMATED METRICS + HUMAN FEEDBACK                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AUTOMATED (Objective)              HUMAN (Subjective but Critical)         │
│  ─────────────────────────────────  ─────────────────────────────────────  │
│  • Token count                      • "Did this context help me?"           │
│  • Precision/recall                 • "Was the Go code usable?"             │
│  • RAGAs scores                     • "Did I understand the domain better?" │
│  • Compile success                  • "Would I use this tool daily?"        │
│                                                                              │
│  Both are needed. Automated metrics can be gamed.                           │
│  Human feedback grounds the evaluation in real utility.                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Feedback Collection Protocol

**Who Provides Feedback:**
- Internal developers tasked with modernization projects
- Technical leads reviewing generated code
- Domain experts validating business logic
- Fellow interns (peer review)

**Feedback Touchpoints:**

| When | What | From Whom |
|------|------|-----------|
| After context retrieval | "Was this context relevant?" | Developer using tool |
| After code generation | "Is this Go code usable?" | Developer reviewing |
| After parity testing | "Does this preserve business logic?" | Domain expert |
| Weekly demo | "Would this help your work?" | Modernization team |
| End of sprint | "Net Promoter Score" | All stakeholders |

### 6.3 Feedback Forms

**Quick Feedback (After Each Use):**
```yaml
# feedback/quick_feedback.yaml
session_id: "sess_2026-01-20_001"
timestamp: "2026-01-20T14:30:00"
user: "developer_name"
task: "Generate Go equivalent of SalesInvoice.on_submit"

context_feedback:
  relevance: 4  # 1-5: Was the retrieved context relevant?
  completeness: 4  # 1-5: Did it include everything needed?
  noise_level: 2  # 1-5: How much irrelevant content? (lower is better)
  comment: "Good call chain, missed the tax calculation method"

generation_feedback:
  usability: 4  # 1-5: Could you use this code directly?
  correctness: 3  # 1-5: Is the logic correct?
  ddd_quality: 5  # 1-5: Does it follow DDD patterns?
  comment: "Good structure, needed to fix error handling"

overall:
  time_saved: "30 minutes"  # Estimate vs doing manually
  would_use_again: true
  recommendation: "Add validation method tracing"
```

**Weekly Developer Survey:**
```yaml
# feedback/weekly_survey_week04.yaml
week: 4
respondent: "senior_developer"
role: "Modernization Lead"

tool_effectiveness:
  context_quality: 4
  code_generation_quality: 3
  domain_understanding_help: 5
  workflow_integration: 3

compared_to_vanilla:
  better_than_claude_code: true
  better_than_cursor: true
  specific_advantages:
    - "Domain context is much richer"
    - "Call chain visualization is excellent"
    - "DDD patterns are applied correctly"
  specific_disadvantages:
    - "Setup is more complex"
    - "Sometimes retrieves too much"

recommendations:
  - "Add filtering by module"
  - "Show confidence scores for retrieved context"
  - "Include migration risk assessment"

net_promoter_score: 8  # 1-10: Would you recommend this tool?
```

### 6.4 Feedback Integration into Metrics

```python
# feedback_metrics.py
"""
Integrate human feedback into effectiveness metrics.
"""

@dataclass
class HumanFeedbackMetrics:
    """Aggregated human feedback scores."""

    # Context Quality (human-rated)
    avg_relevance: float          # Average 1-5 rating
    avg_completeness: float
    avg_noise_level: float        # Lower is better

    # Generation Quality (human-rated)
    avg_usability: float
    avg_correctness: float
    avg_ddd_quality: float

    # Overall Value
    avg_time_saved_minutes: float
    would_use_again_pct: float    # % who said yes
    net_promoter_score: float     # Average NPS (1-10)

    # Qualitative
    top_strengths: list[str]
    top_weaknesses: list[str]
    feature_requests: list[str]

def calculate_human_metrics(feedback_files: list[str]) -> HumanFeedbackMetrics:
    """Aggregate human feedback into metrics."""
    # Load all feedback
    feedbacks = [load_feedback(f) for f in feedback_files]

    return HumanFeedbackMetrics(
        avg_relevance=mean([f.context_feedback.relevance for f in feedbacks]),
        avg_completeness=mean([f.context_feedback.completeness for f in feedbacks]),
        avg_noise_level=mean([f.context_feedback.noise_level for f in feedbacks]),
        avg_usability=mean([f.generation_feedback.usability for f in feedbacks]),
        avg_correctness=mean([f.generation_feedback.correctness for f in feedbacks]),
        avg_ddd_quality=mean([f.generation_feedback.ddd_quality for f in feedbacks]),
        avg_time_saved_minutes=mean([parse_time(f.overall.time_saved) for f in feedbacks]),
        would_use_again_pct=sum(1 for f in feedbacks if f.overall.would_use_again) / len(feedbacks),
        net_promoter_score=mean([f.net_promoter_score for f in feedbacks if hasattr(f, 'net_promoter_score')]),
        top_strengths=extract_themes([f.specific_advantages for f in feedbacks]),
        top_weaknesses=extract_themes([f.specific_disadvantages for f in feedbacks]),
        feature_requests=extract_themes([f.recommendations for f in feedbacks])
    )
```

### 6.5 Feedback Dashboard Addition

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DEVELOPER FEEDBACK SUMMARY                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RESPONSES: 12 developers, 47 feedback sessions                              │
│                                                                              │
│  CONTEXT QUALITY (Human-Rated)                                               │
│  ───────────────────────────────────────────────────────────────────────── │
│  Relevance:     ████████████████░░░░  4.2/5                                 │
│  Completeness:  ███████████████░░░░░  3.9/5                                 │
│  Low Noise:     ██████████████░░░░░░  3.7/5 (lower noise = better)         │
│                                                                              │
│  GENERATION QUALITY (Human-Rated)                                            │
│  ───────────────────────────────────────────────────────────────────────── │
│  Usability:     ███████████████░░░░░  3.8/5                                 │
│  Correctness:   ██████████████░░░░░░  3.6/5                                 │
│  DDD Quality:   █████████████████░░░  4.4/5                                 │
│                                                                              │
│  OVERALL VALUE                                                               │
│  ───────────────────────────────────────────────────────────────────────── │
│  Avg Time Saved:      35 minutes per task                                   │
│  Would Use Again:     92%                                                   │
│  Net Promoter Score:  8.2/10 (Promoters: 75%, Detractors: 8%)              │
│                                                                              │
│  TOP FEEDBACK THEMES                                                         │
│  ───────────────────────────────────────────────────────────────────────── │
│  ✅ Strengths:                                                               │
│     • "Domain context is much richer than vanilla editors"                  │
│     • "Call chain visualization saves hours of exploration"                 │
│     • "DDD patterns are correctly applied"                                  │
│                                                                              │
│  ⚠️ Improvements Needed:                                                     │
│     • "Sometimes retrieves too much context"                                │
│     • "Need better filtering by module"                                     │
│     • "Show confidence scores"                                              │
│                                                                              │
│  💡 Feature Requests:                                                        │
│     • Migration risk assessment                                             │
│     • Batch processing for multiple modules                                 │
│     • Integration with existing CI/CD                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.6 Combined Evidence Report Structure

```markdown
# Effectiveness Report - Updated with Human Feedback

## 1. Automated Metrics
[Token efficiency, precision, recall, code quality scores]

## 2. Human Feedback Metrics ← NEW
- **Developer Satisfaction**: 4.1/5 average across all dimensions
- **Time Saved**: 35 minutes average per modernization task
- **Would Recommend**: 92% of developers would use again
- **NPS**: 8.2 (strong promoter territory)

## 3. Qualitative Insights ← NEW
### What Developers Love
- Rich domain context
- Call chain visualization
- DDD pattern application

### What Needs Improvement
- Context filtering
- Confidence scoring
- Batch processing

## 4. Combined Score
**Tool Effectiveness Index**: 0.82
- Automated component (60%): 0.85
- Human feedback component (40%): 0.78

## 5. Conclusion
Both automated metrics AND human feedback confirm the tool provides
significant value over vanilla AI editors for enterprise modernization.
```

---

## Success Criteria

By end of internship, you should demonstrate:

| Metric | Target | Evidence |
|--------|--------|----------|
| Token Reduction | > 70% | Logged experiments |
| Context Precision | > 80% | RAGAs metrics |
| Code Quality | > 4.0/5 | Human evaluation |
| DDD Adherence | > 4.0/5 | Pattern checklist |
| Parity Tests Passing | > 80% | Test results |
| Modules Covered | ≥ 3 | Documentation |
| **Developer Satisfaction** | > 4.0/5 | Feedback surveys |
| **Would Use Again** | > 85% | Developer survey |
| **Net Promoter Score** | > 7.0 | NPS survey |
| **Time Saved** | > 25 min/task | Developer estimates |

---

## Related Documents

- [Sales Invoice Case Study](../05-Worked-Examples/01-Sales-Invoice-Case-Study.md)
- [Enterprise Tooling](../03-AI-Platform/05-Enterprise-Tooling.md)
- [Evolution Framework](../01-Product/03-Evolution-Framework.md)
- [Quality Metrics](../03-AI-Platform/04-Quality-Metrics.md)

---

*Last Updated: 2026-01-14*
