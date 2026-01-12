# AI Engineering Internship

## Theme: AI-Driven Legacy Modernization

> *Building intelligent tools that understand enterprise codebases and accelerate migration from legacy systems to modern architectures.*

---

## How to Use This Documentation

### Recommended: Obsidian Desktop App

Download **[Obsidian](https://obsidian.md/)** for the best experience:
- **Graph View**: Visualize document connections
- **Quick Navigation**: `Ctrl/Cmd + O` to jump anywhere
- **Backlinks**: See which documents reference the current one

**Setup**: Open the `AI-Internship` folder as a vault in Obsidian.

---

## Documentation Structure

### 01 - Getting Started
| # | Document | Description |
|---|----------|-------------|
| 1.1 | [[01-Getting-Started/01-Organizational-Context\|Organizational Context]] | Your role in PearlThoughts |
| 1.2 | [[01-Getting-Started/02-Goals-and-Expectations\|Goals & Expectations]] | 4-week plan, deliverables |
| 1.3 | [[01-Getting-Started/03-What-You-Build\|What You Build]] | Form factors, AI setup, workflow |

### 02 - Understanding Legacy Systems
| # | Document | Description |
|---|----------|-------------|
| 2.1 | [[02-Understanding-Legacy/01-What-Is-Legacy\|What Is Legacy Code?]] | Hidden value in old systems |
| 2.2 | [[02-Understanding-Legacy/02-Why-Modernize\|Why Modernize?]] | Business case, rewrite fallacy |
| 2.3 | [[02-Understanding-Legacy/03-Real-World-Examples\|Real-World Examples]] | COBOL banking, NHS, airlines |
| 2.4 | [[02-Understanding-Legacy/04-Terminology-Glossary\|Terminology Glossary]] | All key terms defined |

### 03 - Market Research
| # | Document | Description |
|---|----------|-------------|
| 3.1 | [[03-Market-Research/01-Existing-Tools-Research\|Existing Tools Research]] | GitHub Copilot, Amazon Q, etc. |
| 3.2 | [[03-Market-Research/02-Market-Analysis\|Market Analysis]] | $300B+ market opportunity |
| 3.3 | [[03-Market-Research/03-AI-Coding-Tools-Comparison\|AI Coding Tools Comparison]] | How Cursor, Aider work internally |

### 04 - Target Projects
| # | Document | Description |
|---|----------|-------------|
| 4.1 | [[04-Target-Projects/01-Choosing-Your-Project\|Choosing Your Project]] | Decision matrix |
| 4.2 | [[04-Target-Projects/02-ERPNext-Domain-Analysis\|ERPNext Analysis]] | Frappe framework, DocTypes |
| 4.3 | [[04-Target-Projects/03-OpenElis-Domain-Analysis\|OpenElis Analysis]] | Laboratory LIMS system |
| 4.4 | [[04-Target-Projects/04-Bahmni-Core-Domain-Analysis\|Bahmni Analysis]] | Healthcare EMR system |
| 4.5 | [[04-Target-Projects/05-Validation-Projects\|Validation Projects]] | Testing against real systems |

### 05 - DDD Concepts
| # | Document | Description |
|---|----------|-------------|
| 5.1 | [[05-DDD-Concepts/01-Why-DDD-Matters\|Why DDD Matters]] | Why AI tool builders need DDD |
| 5.2 | [[05-DDD-Concepts/02-Bounded-Contexts\|Bounded Contexts]] | Context boundaries, ACL |
| 5.3 | [[05-DDD-Concepts/03-Strategic-Design\|Strategic Design]] | Subdomains, context mapping |
| 5.4 | [[05-DDD-Concepts/04-Tactical-Patterns\|Tactical Patterns]] | Entities, Aggregates, Events |
| 5.5 | [[05-DDD-Concepts/05-Applied-To-Projects\|Applied to Projects]] | DDD in ERPNext/OpenElis/Bahmni |

### 06 - Code Intelligence
| # | Document | Description |
|---|----------|-------------|
| 6.1 | [[06-Code-Intelligence/01-What-Is-Code-Intelligence\|What Is Code Intelligence?]] | Core concepts, architecture |
| 6.2 | [[06-Code-Intelligence/02-AST-vs-Text-Chunking\|AST vs Text Chunking]] | Parsing strategies compared |
| 6.3 | [[06-Code-Intelligence/03-Indexing-Strategies\|Indexing Strategies]] | Complete indexing pipeline |
| 6.4 | [[06-Code-Intelligence/04-Graph-Extraction\|Graph Extraction]] | Call graphs, relationships |
| 6.5 | [[06-Code-Intelligence/05-Commercial-Tools\|Commercial Tools]] | Cursor, Sourcegraph, Amazon Q |
| 6.6 | [[06-Code-Intelligence/06-CodeCompass-Learnings\|CodeCompass Learnings]] | Real implementation insights |

### 07 - Technical Architecture
| # | Document | Description |
|---|----------|-------------|
| 7.1 | [[07-Technical-Architecture/01-Architecture-Overview\|Architecture Overview]] | 4-mode knowledge extraction |
| 7.2 | [[07-Technical-Architecture/02-Quality-Metrics\|Quality Metrics]] | RAGAs, MLflow, test cases |

### 08 - Exercises
| # | Document | Description |
|---|----------|-------------|
| 8.1 | [[08-Exercises/01-Pre-Internship-Requirements\|Pre-Internship Requirements]] | **START HERE** - Week 1 tasks |
| 8.2 | [[08-Exercises/02-Submission-Checklist\|Submission Checklist]] | Deliverables, quality criteria |
| 8.3 | [[08-Exercises/03-OKR\|OKR]] | Objectives & Key Results |

---

## Quick Start Path

```
For interns starting TODAY:

1. Read → 08-Exercises/01-Pre-Internship-Requirements
2. Choose → 04-Target-Projects/01-Choosing-Your-Project
3. Learn → 02-Understanding-Legacy/04-Terminology-Glossary
4. Understand → 05-DDD-Concepts/01-Why-DDD-Matters
5. Build → 06-Code-Intelligence/03-Indexing-Strategies
6. Submit → 08-Exercises/02-Submission-Checklist
```

---

## The Problem We're Solving

Every enterprise faces the same challenge: **legacy systems that are too valuable to abandon but too complex to understand**.

### Scale of Technical Debt

- **$300B+ annual market** for legacy modernization
- **70% of modernization projects fail** due to lost business logic
- **85% of critical business rules** exist only in code

### Why Current Tools Fail

| Approach | Problem |
|----------|---------|
| Manual Analysis | Takes years, expensive |
| Big Bang Rewrite | Loses embedded logic, high failure |
| Current AI Tools | Surface-level only, miss semantics |

---

## What You'll Build

A tool that understands code like an expert developer — not just syntax, but semantics, relationships, and business intent.

### Key Capabilities

| Capability | AI Technique |
|------------|--------------|
| Semantic Search | RAG, Embeddings |
| Graph Traversal | GraphRAG |
| Domain Discovery | Clustering |
| Impact Analysis | Graph Algorithms |

---

## Technology Stack

| Layer | Technologies |
|-------|--------------|
| Languages | TypeScript, Python |
| Embeddings | Ollama, OpenAI |
| Vector Store | LanceDB, SQLite |
| Parsing | tree-sitter |
| LLM | Claude, GPT-4 |

---

*Last Updated: 2026-01-12*
