# Worked Examples

This folder contains end-to-end case studies that apply AI Engineering principles to enterprise legacy modernization.

---

## Purpose

Each worked example demonstrates:
1. **RAG Pipeline Design** - Chunking, embedding, retrieval strategies
2. **Evaluation Framework** - Metrics, baselines, experiments
3. **Migration Patterns** - ERPNext → Go transformation
4. **MCP Integration** - Tool design for Claude Code/Cursor

---

## Available Examples

| Example | Module | Bounded Contexts | Complexity |
|---------|--------|------------------|------------|
| [Sales Invoice](./01-Sales-Invoice-Case-Study.md) | Accounts | Selling, Accounts, Stock, CRM | High |
| *(planned)* Purchase Order | Buying | Buying, Accounts, Stock | Medium |
| *(planned)* Stock Entry | Stock | Stock, Manufacturing | Medium |

---

## How to Use

1. **Read the case study** to understand the patterns
2. **Run the code examples** in your development environment
3. **Adapt for your target module** (e.g., Purchase Order)
4. **Track experiments** using MLflow as shown
5. **Measure improvement** against baseline

---

## Key Concepts Covered

### From AI Engineering (Chip Huyen)
- Chunking strategies (fixed-length vs AST-based)
- Hybrid retrieval (BM25 + dense embeddings)
- Reciprocal Rank Fusion (RRF)
- Context construction for LLMs
- RAGAs evaluation metrics

### From Hands-On LLMs (Alammar & Grootendorst)
- Grounded generation pattern
- Reranking with cross-encoders
- Two-stage retrieval pipelines

### From DDD Literature
- Bounded context identification
- Aggregate pattern in ERPNext
- Domain events (hooks)
- Repository pattern mapping

---

*Last Updated: 2026-01-14*
