# Context Quality Experiment Guide

## Purpose

This guide helps you validate whether your code analyzer actually improves AI assistant responses about legacy codebases.

---

## The Core Question

> Does Claude Code/Cursor give **better answers** about ERPNext/Bahmni when provided with your extracted context?

---

## Experiment Design

### Setup

1. **Target Codebase**: ERPNext (or Bahmni)
2. **Target Module**: Pick ONE (e.g., Sales Invoice, Patient Registration)
3. **AI Assistant**: Claude Code, Cursor, or Gemini API
4. **Evaluator**: You (developer who understands the codebase)

### Protocol

```
┌─────────────────────────────────────────────────────────────┐
│  CONTEXT QUALITY EXPERIMENT                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: BASELINE                                           │
│  ├── Ask AI: "How does X work in ERPNext?"                  │
│  ├── Record answer (without any context)                    │
│  └── Rate: Accuracy (1-5), Completeness (1-5)               │
│                                                             │
│  Step 2: WITH CONTEXT                                       │
│  ├── Generate context using your tool                       │
│  ├── Provide context to AI (paste or MCP)                   │
│  ├── Ask same question                                      │
│  └── Rate: Accuracy (1-5), Completeness (1-5)               │
│                                                             │
│  Step 3: COMPARE                                            │
│  ├── Delta = (With Context Score) - (Baseline Score)        │
│  ├── Document what the context added                        │
│  └── Document what was still missing                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Test Questions (ERPNext Sales Invoice)

Use these questions to test your context quality:

### Business Logic Questions

| Question | What Good Answer Contains |
|----------|---------------------------|
| "What happens when a Sales Invoice is submitted?" | on_submit hook, GL entries, Stock ledger updates |
| "How is discount calculated?" | DiscountController, pricing rules, item-level vs invoice-level |
| "What validations run on Invoice creation?" | Required fields, stock availability, credit limit checks |
| "How do payment terms work?" | PaymentSchedule, due dates, partial payment handling |

### Relationship Questions

| Question | What Good Answer Contains |
|----------|---------------------------|
| "What entities does Sales Invoice relate to?" | Customer, Item, Warehouse, GL Entry, Stock Ledger |
| "What services does Sales Invoice call?" | Pricing, Stock, Accounting services |
| "What can trigger a Sales Invoice?" | Sales Order, Delivery Note, POS |

### Workflow Questions

| Question | What Good Answer Contains |
|----------|---------------------------|
| "What's the flow from Quote to Invoice?" | Quotation → Sales Order → Delivery Note → Sales Invoice |
| "How does cancellation work?" | Cancel method, GL reversal, stock reversal |

---

## Scoring Rubric

### Accuracy (1-5)

| Score | Criteria |
|-------|----------|
| 5 | All statements are factually correct |
| 4 | Minor inaccuracies that don't affect understanding |
| 3 | Some incorrect statements but core is right |
| 2 | Major inaccuracies |
| 1 | Mostly wrong or hallucinated |

### Completeness (1-5)

| Score | Criteria |
|-------|----------|
| 5 | Covers all relevant aspects, mentions edge cases |
| 4 | Covers main points, missing some details |
| 3 | Covers basic flow, missing important steps |
| 2 | Very superficial, missing key components |
| 1 | Barely addresses the question |

---

## Recording Results

Create a YAML file for each experiment:

```yaml
# experiment-001.yaml
date: "2026-01-14"
question: "What happens when a Sales Invoice is submitted?"
module: "sales_invoice"
context_version: "v1"

baseline:
  accuracy: 2
  completeness: 2
  notes: "AI mentioned GL entries but missed stock updates"

with_context:
  accuracy: 4
  completeness: 4
  notes: "Correctly identified on_submit, GL entries, stock ledger"

delta:
  accuracy: +2
  completeness: +2

context_helped_with:
  - "Identified the on_submit hook"
  - "Listed downstream service calls"

context_missing:
  - "Payment reconciliation flow"
  - "Email notification triggers"
```

---

## Aggregating Results

Track across experiments:

```
┌────────────────────────────────────────────────────────────┐
│ EXPERIMENT DASHBOARD                                        │
├────────────────────────────────────────────────────────────┤
│ Total Experiments: 10                                       │
│ Average Delta (Accuracy): +1.8                              │
│ Average Delta (Completeness): +2.1                          │
│                                                             │
│ Best Performing Context: call_graphs.md                     │
│ Worst Performing: raw_functions.json                        │
│                                                             │
│ Questions Where Context Helped Most:                        │
│   - Workflow questions (+2.5 avg)                           │
│   - Relationship questions (+2.2 avg)                       │
│   - Business logic questions (+1.5 avg)                     │
└────────────────────────────────────────────────────────────┘
```

---

## Tools for Tracking

### Option 1: MLflow (Recommended)

```bash
# Log experiment
mlflow run . -P question="What happens on submit?" \
             -P context_version="v1" \
             -P baseline_accuracy=2 \
             -P with_context_accuracy=4

# Compare experiments
mlflow ui  # View at localhost:5000
```

### Option 2: Simple CSV

```csv
date,question,context_version,baseline_accuracy,baseline_completeness,context_accuracy,context_completeness
2026-01-14,on_submit_flow,v1,2,2,4,4
2026-01-15,discount_calc,v1,3,2,4,5
```

### Option 3: JSON Lines

```jsonl
{"date":"2026-01-14","question":"on_submit_flow","baseline":{"accuracy":2},"with_context":{"accuracy":4}}
{"date":"2026-01-15","question":"discount_calc","baseline":{"accuracy":3},"with_context":{"accuracy":4}}
```

---

## What Success Looks Like

| Metric | Target |
|--------|--------|
| Average Accuracy Delta | >= +1.5 |
| Average Completeness Delta | >= +1.5 |
| % of Questions Improved | >= 70% |
| % of Questions Made Worse | < 5% |

---

## Next Steps After Validation

Once you've validated context quality:

1. **Iterate**: Improve context generation based on gaps
2. **Scale**: Test on more modules
3. **Integrate**: Build MCP server to expose context to Claude Code
4. **Document**: Write up findings for the team

---

## Related

- [[01-Assessment-Framework|Assessment Framework]]
- [[../07-Technical-Architecture/02-Quality-Metrics|Quality Metrics]]
- [[../06-Code-Intelligence/03-Indexing-Strategies|Indexing Strategies]]

---

*Created: 2026-01-13*
