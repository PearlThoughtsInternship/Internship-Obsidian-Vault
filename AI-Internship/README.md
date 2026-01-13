# Code Intelligence Platform for Enterprise Modernization

## Vision

A code intelligence platform that helps AI assistants understand enterprise legacy codebases for modernization.

**The Problem**: 85% of business logic lives in code, not documentation. When organizations modernize legacy systems, they struggle to understand what the code actually does.

**Our Solution**: Build tools that index, extract, and provide structured context to AI assistants (Claude Code, Cursor), improving their ability to answer questions about enterprise codebases.

---

## Quick Start

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     YOUR FIRST 30 MINUTES                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. READ     →  04-Internship/01-Before-You-Begin.md                    │
│                 (Understand expectations & mindset)                      │
│                                                                          │
│  2. REVIEW   →  01-Product/01-Vision.md                                 │
│                 (What we're building)                                    │
│                                                                          │
│  3. STUDY    →  02-Engineering/01-Architecture.md                       │
│                 (4-mode extraction approach)                             │
│                                                                          │
│  4. BUILD    →  04-Internship/Exercises/01-Pre-Internship-Requirements  │
│                 (Start coding your tool!)                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Platform Structure

### 01-Product — What We're Building

| Document | Description |
|----------|-------------|
| [Vision](./01-Product/01-Vision.md) | Problem, opportunity, success criteria |
| [Capabilities](./01-Product/02-Capabilities.md) | Platform features specification |
| [Market Context](./01-Product/03-Market-Context.md) | $300B market opportunity |
| [Target Codebases](./01-Product/Target-Codebases/) | ERPNext, Bahmni, OpenElis |

### 02-Engineering — How to Build It

| Document | Description |
|----------|-------------|
| [Architecture](./02-Engineering/01-Architecture.md) | 4-mode knowledge extraction |
| [Code Intelligence](./02-Engineering/Code-Intelligence/) | AST, indexing, graph extraction |
| [Domain Knowledge](./02-Engineering/Domain-Knowledge/) | DDD, bounded contexts |
| [Quality Metrics](./02-Engineering/02-Quality-Metrics.md) | RAGAs, measurement |

### 03-AI-Platform — AI Engineering

| Document | Description |
|----------|-------------|
| [Context Generation](./03-AI-Platform/01-Context-Generation.md) | Query-aware retrieval |
| [LLM Integration](./03-AI-Platform/02-LLM-Integration.md) | MCP, prompts, Groq/Ollama |
| [Observability](./03-AI-Platform/03-Observability.md) | Experiment tracking |
| [Quality Metrics](./03-AI-Platform/04-Quality-Metrics.md) | Context validation |

### 04-Internship — Learning Journey

| Document | Description |
|----------|-------------|
| [Before You Begin](./04-Internship/01-Before-You-Begin.md) | Expectations, mindset |
| [Week-by-Week](./04-Internship/02-Week-by-Week.md) | 4-week progression |
| [What You Build](./04-Internship/03-What-You-Build.md) | Form factors, setup |
| [Background](./04-Internship/Background/) | Legacy systems context |
| [Exercises](./04-Internship/Exercises/) | Hands-on tasks |

### 05-Contributions — Intern Work

| Document | Description |
|----------|-------------|
| [How to Contribute](./05-Contributions/01-How-To-Contribute.md) | Process, standards |
| [Reviews](./05-Contributions/Reviews/) | Cohort feedback |
| [Experiments](./05-Contributions/Experiments/) | Iteration log |

---

## Core Capabilities

| Capability | Description | Documentation |
|------------|-------------|---------------|
| **Codebase Indexing** | Multi-language parsing, 4-mode extraction | [Architecture](./02-Engineering/01-Architecture.md) |
| **Context Generation** | Query-aware, business rule extraction | [Context Generation](./03-AI-Platform/01-Context-Generation.md) |
| **AI Integration** | MCP server, structured output | [LLM Integration](./03-AI-Platform/02-LLM-Integration.md) |
| **Quality Measurement** | Experiment tracking, metrics | [Observability](./03-AI-Platform/03-Observability.md) |

---

## Technology Stack

| Component | Recommended | Alternative |
|-----------|-------------|-------------|
| **Language** | TypeScript | Python |
| **Parsing** | tree-sitter | Language-specific AST |
| **Embeddings** | Ollama + nomic-embed | OpenAI |
| **LLM** | Groq (free, fast) | Ollama local |
| **Vector DB** | LanceDB | ChromaDB |
| **Experiment Tracking** | MLflow | CSV/JSON |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Context Precision | > 75% | % of context that's relevant |
| Answer Accuracy Improvement | > 20% | Before/after with context |
| Retrieval Latency (p95) | < 500ms | Time to generate context |
| Business Rule Accuracy | > 80% | Manual verification |

---

## Reference Implementation

**[code-analyzer-demo](https://github.com/PearlThoughtsInternship/code-analyzer-demo)** — A Python tool demonstrating core concepts

- Shows the learning journey through commit history
- Heavy comments explaining WHY, not just WHAT
- Tested against ERPNext with actual results

**Don't copy it.** Understand it. Build your own version with YOUR insights.

---

## Using This Documentation

### Recommended: Obsidian

Download **[Obsidian](https://obsidian.md/)** for the best experience:
- Graph View for visualizing connections
- Quick Navigation with `Ctrl/Cmd + O`
- Backlinks to see related documents

**Setup**: Open the `AI-Internship` folder as a vault in Obsidian.

### Alternative

All links work on GitHub web UI.

---

## Getting Help

- **Teams/Slack**: #ai-internship channel
- **Documentation**: This vault
- **Mentors**: Available for questions (after you've tried first)

**Remember**: Research first, ask second. We're evaluating your ability to figure things out independently.

---

*Last Updated: 2026-01-13*
