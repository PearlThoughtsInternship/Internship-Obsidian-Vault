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

**Alternative**: All links also work on GitHub web UI.

---

## Documentation Structure

### 01 - Getting Started
| # | Document | Description |
|---|----------|-------------|
| 1.1 | [Organizational Context](./01-Getting-Started/01-Organizational-Context.md) | Your role in PearlThoughts |
| 1.2 | [Goals & Expectations](./01-Getting-Started/02-Goals-and-Expectations.md) | 4-week plan, deliverables |
| 1.3 | [What You Build](./01-Getting-Started/03-What-You-Build.md) | Form factors, AI setup, workflow |

### 02 - Understanding Legacy Systems
| # | Document | Description |
|---|----------|-------------|
| 2.1 | [What Is Legacy Code?](./02-Understanding-Legacy/01-What-Is-Legacy.md) | Hidden value in old systems |
| 2.2 | [Why Modernize?](./02-Understanding-Legacy/02-Why-Modernize.md) | Business case, rewrite fallacy |
| 2.3 | [Real-World Examples](./02-Understanding-Legacy/03-Real-World-Examples.md) | COBOL banking, NHS, airlines |
| 2.4 | [Terminology Glossary](./02-Understanding-Legacy/04-Terminology-Glossary.md) | All key terms defined |

### 03 - Market Research
| # | Document | Description |
|---|----------|-------------|
| 3.1 | [Existing Tools Research](./03-Market-Research/01-Existing-Tools-Research.md) | GitHub Copilot, Amazon Q, etc. |
| 3.2 | [Market Analysis](./03-Market-Research/02-Market-Analysis.md) | $300B+ market opportunity |
| 3.3 | [AI Coding Tools Comparison](./03-Market-Research/03-AI-Coding-Tools-Comparison.md) | How Cursor, Aider work internally |

### 04 - Target Projects
| # | Document | Description |
|---|----------|-------------|
| 4.1 | [Choosing Your Project](./04-Target-Projects/01-Choosing-Your-Project.md) | Decision matrix |
| 4.2 | [ERPNext Analysis](./04-Target-Projects/02-ERPNext-Domain-Analysis.md) | Frappe framework, DocTypes |
| 4.3 | [OpenElis Analysis](./04-Target-Projects/03-OpenElis-Domain-Analysis.md) | Laboratory LIMS system |
| 4.4 | [Bahmni Analysis](./04-Target-Projects/04-Bahmni-Core-Domain-Analysis.md) | Healthcare EMR system |
| 4.5 | [Validation Projects](./04-Target-Projects/05-Validation-Projects.md) | Testing against real systems |

### 05 - DDD Concepts
| # | Document | Description |
|---|----------|-------------|
| 5.1 | [Why DDD Matters](./05-DDD-Concepts/01-Why-DDD-Matters.md) | Why AI tool builders need DDD |
| 5.2 | [Bounded Contexts](./05-DDD-Concepts/02-Bounded-Contexts.md) | Context boundaries, ACL |
| 5.3 | [Strategic Design](./05-DDD-Concepts/03-Strategic-Design.md) | Subdomains, context mapping |
| 5.4 | [Tactical Patterns](./05-DDD-Concepts/04-Tactical-Patterns.md) | Entities, Aggregates, Events |
| 5.5 | [Applied to Projects](./05-DDD-Concepts/05-Applied-To-Projects.md) | DDD in ERPNext/OpenElis/Bahmni |

### 06 - Code Intelligence
| # | Document | Description |
|---|----------|-------------|
| 6.1 | [What Is Code Intelligence?](./06-Code-Intelligence/01-What-Is-Code-Intelligence.md) | Core concepts, architecture |
| 6.2 | [AST vs Text Chunking](./06-Code-Intelligence/02-AST-vs-Text-Chunking.md) | Parsing strategies compared |
| 6.3 | [Indexing Strategies](./06-Code-Intelligence/03-Indexing-Strategies.md) | Complete indexing pipeline |
| 6.4 | [Graph Extraction](./06-Code-Intelligence/04-Graph-Extraction.md) | Call graphs, relationships |
| 6.5 | [Commercial Tools](./06-Code-Intelligence/05-Commercial-Tools.md) | Cursor, Sourcegraph, Amazon Q |
| 6.6 | [CodeCompass Learnings](./06-Code-Intelligence/06-CodeCompass-Learnings.md) | Real implementation insights |

### 07 - Technical Architecture
| # | Document | Description |
|---|----------|-------------|
| 7.1 | [Architecture Overview](./07-Technical-Architecture/01-Architecture-Overview.md) | 4-mode knowledge extraction |
| 7.2 | [Quality Metrics](./07-Technical-Architecture/02-Quality-Metrics.md) | RAGAs, MLflow, test cases |

### 08 - Exercises
| # | Document | Description |
|---|----------|-------------|
| 8.1 | [Pre-Internship Requirements](./08-Exercises/01-Pre-Internship-Requirements.md) | **START HERE** - Week 1 tasks |
| 8.2 | [Submission Checklist](./08-Exercises/02-Submission-Checklist.md) | Deliverables, quality criteria |
| 8.3 | [OKR](./08-Exercises/03-OKR.md) | Objectives & Key Results |

---

## Quick Start Path

**For interns starting TODAY:**

1. **Read** → [08-Exercises/01-Pre-Internship-Requirements](./08-Exercises/01-Pre-Internship-Requirements.md)
2. **Choose** → [04-Target-Projects/01-Choosing-Your-Project](./04-Target-Projects/01-Choosing-Your-Project.md)
3. **Learn** → [02-Understanding-Legacy/04-Terminology-Glossary](./02-Understanding-Legacy/04-Terminology-Glossary.md)
4. **Understand** → [05-DDD-Concepts/01-Why-DDD-Matters](./05-DDD-Concepts/01-Why-DDD-Matters.md)
5. **Build** → [06-Code-Intelligence/03-Indexing-Strategies](./06-Code-Intelligence/03-Indexing-Strategies.md)
6. **Submit** → [08-Exercises/02-Submission-Checklist](./08-Exercises/02-Submission-Checklist.md)

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
