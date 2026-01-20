# 🧠 AI Engineering Internship  
## AI-Driven Legacy Modernization

---

## 📌 Overview

This repository contains documentation, research, and implementation work produced during the **AI Engineering Internship**, focused on **AI-Driven Legacy Modernization**.

The internship aims to build **intelligent AI systems that deeply understand enterprise codebases** and accelerate safe migration from legacy systems to modern architectures—without losing critical business logic.

This work goes beyond traditional static analysis or AI coding tools by emphasizing **holistic enterprise intelligence**.

---

## 🎯 Problem Statement

Enterprises rely heavily on legacy systems that are:
- Business-critical but poorly documented
- Often decades old
- Maintained by a shrinking pool of experts

### Why Legacy Modernization Fails
- Business rules exist only in code
- Manual analysis is slow and costly
- Big-bang rewrites lose hidden logic
- Existing AI tools lack semantic and runtime awareness

This internship treats modernization as a **knowledge understanding and extraction problem**, not just a code migration task.

---

## 🚀 Internship Objective

Build AI-powered tools that can:
- Understand enterprise codebases like a senior engineer
- Extract business logic and architectural intent
- Perform impact analysis across systems
- Assist safe and incremental modernization

---

## 🧠 Core Concept: Holistic Enterprise Intelligence

Instead of basic file or symbol indexing, the system builds a **multi-layered knowledge model**:

### Intelligence Layers
1. **Semantic Code Understanding**
   - Function/class-level chunking
   - Context-preserving embeddings

2. **Graph-Based Knowledge**
   - Call graphs
   - Dependency graphs
   - Data-flow relationships

3. **AST-Level Analysis**
   - Business rule extraction
   - Framework-specific patterns

4. **Runtime Intelligence**
   - Execution traces
   - Hot path identification
   - Error and performance patterns

5. **Enterprise Context**
   - Git history
   - Jira tickets
   - Wikis and Architecture Decision Records (ADRs)

---

## 🛠️ What Is Being Built

### Code Synthesizer Tool

A developer-facing AI tool that augments AI editors by providing **deep enterprise system understanding**.

Key capabilities:
- Semantic search by intent
- Impact analysis for code changes
- Business logic discovery
- Legacy → modern parity tracking
- AI-assisted migration workflows

---

## 🧪 Validation Systems

The solution is validated against **real-world enterprise open-source systems**:

| System   | Domain     | Tech Stack |
|--------|------------|------------|
| Bahmni | Healthcare | Java, Spring |
| ERPNext | ERP | Python, Frappe |
| Odoo | Modular ERP | Python, PostgreSQL |

---

## 🧭 Internship Tracks

Each intern focuses on **one primary track**:

- **Track A – Knowledge Extraction**  
  Semantic chunking, call graphs, dependency graphs

- **Track B – Intelligent Retrieval**  
  RAG and GraphRAG for code understanding

- **Track C – Domain Discovery**  
  Bounded-context detection via clustering

- **Track D – Migration Automation**  
  Legacy → modern parity tracking and AI migration agents

---

## 🧑‍💻 Technology Stack

| Layer | Technologies |
|------|-------------|
| Languages | Python, TypeScript |
| Frameworks | FastAPI, NestJS |
| LLMs | GPT-4, Claude, Llama, Groq |
| Embeddings | Sentence Transformers, Ollama |
| Vector DB | LanceDB, SQLite |
| Graph | Graph algorithms, SQL CTEs |
| Parsing | tree-sitter |

---

## 📁 Repository Structure

```text
AI-Internship/
├── 00-Index.md
├── 01-Organizational-Context.md
├── 02-Goals-and-Expectations.md
├── 03-Existing-Tools-Research.md
├── 04-Market-Analysis.md
├── 05-AI-Tools-Comparison.md
├── 06-Technical-Architecture.md
├── 07-Quality-Metrics.md
├── 08-Validation-Projects.md
├── 09-OKR.md
├── 10-What-You-Build.md
├── day1.md
└── README.md
# 🚀 AI Engineering Internship
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
│  0. SETUP    →  Set up Teams & Tools (see Communication section below)  │
│                 Get your webinar link: 00-Session-Links.md              │
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

## Communication & Remote Working

> **New here?** Start with our communication guides.

| Guide | What You'll Learn |
|-------|-------------------|
| [Teams Setup](../How-We-Communicate/01-Teams-Getting-Started.md) | Microsoft Teams setup, troubleshooting, getting full Guest access |
| [Communication Protocol](../How-We-Communicate/02-Communication-Protocol.md) | Which channel to use, threads vs posts, HR queries |
| [Live Sessions](../How-We-Communicate/03-Live-Sessions.md) | 10 AM webinar format, demo showcase, participation |
| [Tools & Workflows](../How-We-Communicate/04-Tools-and-Workflows.md) | Git repos, Loom screencasts, cloud hosting |

These guides apply to all internship programs at PearlThoughts.

---

*Last Updated: 2026-01-13*
