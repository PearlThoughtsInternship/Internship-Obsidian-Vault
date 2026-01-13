# What We Learned Building CodeCompass

> **Practical insights** from building a real code intelligence system

---

## What Is CodeCompass?

CodeCompass is a **knowledge graph-based legacy modernization platform** we built internally. It indexes codebases, builds relationships, and enables AI-powered code understanding.

This document shares what we learned—the wins, the mistakes, and the hard-won insights.

---

## Architecture That Worked

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CODECOMPASS ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │  Ingestion   │────►│   Indexing   │────►│  Retrieval   │            │
│  │              │     │              │     │              │            │
│  │ • tree-sitter│     │ • SQLite     │     │ • Vector     │            │
│  │ • File scan  │     │   (graph)    │     │   search     │            │
│  │ • Git history│     │ • LanceDB    │     │ • Graph      │            │
│  │              │     │   (vectors)  │     │   traversal  │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│                                                   │                      │
│                                                   ▼                      │
│                                           ┌──────────────┐              │
│                                           │  Synthesis   │              │
│                                           │              │              │
│                                           │ • LLM (Cloud)│              │
│                                           │ • Context    │              │
│                                           │   assembly   │              │
│                                           └──────────────┘              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| **Graph storage** | SQLite + CTEs | Simple, no separate DB, recursive queries |
| **Vector storage** | LanceDB | Embedded, no server, fast |
| **Embeddings** | Local (Ollama) | Privacy, no API costs |
| **Synthesis** | Cloud (OpenRouter) | Quality matters for answers |
| **Parsing** | tree-sitter | Fast, robust, multi-language |

---

## What Worked Well

### 1. Local-First Architecture

**Decision**: Embeddings run locally (Ollama), code never leaves your machine.

**Why it worked**:
- No API costs for embedding millions of symbols
- Privacy for sensitive codebases
- Works offline
- ~35k symbols indexed for $0

**Trade-off**: Slower than cloud, but acceptable.

### 2. SQLite for Everything (Almost)

**Decision**: Use SQLite for graph storage instead of Neo4j.

**Why it worked**:
- Zero setup (just a file)
- Recursive CTEs handle graph traversal
- Single database for metadata + graph
- Easy backup/restore

```sql
-- Graph traversal with recursive CTE
WITH RECURSIVE call_chain AS (
  SELECT id, name, 0 as depth FROM graph_nodes WHERE name = ?
  UNION ALL
  SELECT n.id, n.name, c.depth + 1
  FROM graph_nodes n
  JOIN graph_edges e ON e.target_id = n.id
  JOIN call_chain c ON c.id = e.source_id
  WHERE c.depth < 5
)
SELECT * FROM call_chain;
```

### 3. Hybrid AI Strategy

**Decision**: Local embeddings + Cloud synthesis.

**Why it worked**:
- Embeddings: High volume, low stakes → Local
- Synthesis: Low volume, high stakes → Cloud (better quality)
- Best of both worlds

### 4. AST-Based Chunking from Day 1

**Decision**: Use tree-sitter instead of text chunking.

**Why it worked**:
- Clean function/class boundaries
- Metadata extraction (names, signatures)
- Foundation for graph edges (calls, imports)
- Worth the setup investment

---

## Mistakes We Made

### 1. Started Without Graph (Vector-Only)

**Mistake**: First version used only vector search.

**Problem**:
- "Find related code" returned semantically similar but unrelated code
- Couldn't answer "what calls this function?"
- No structural understanding

**Fix**: Added knowledge graph for relationships.

**Lesson**: **Vector search finds similar code. Graph search finds related code.**

### 2. Over-Indexed Early

**Mistake**: Indexed everything (tests, configs, generated files).

**Problem**:
- Slow indexing
- Noise in search results
- Tests cluttering real code

**Fix**: Added ignore patterns.

```
# .codecompassignore
**/node_modules/**
**/__pycache__/**
**/test_*.py
**/tests/**
**/*.min.js
**/generated/**
```

**Lesson**: **Index less, index better.**

### 3. No Incremental Updates

**Mistake**: Full re-index on every change.

**Problem**:
- 30-minute wait for any codebase change
- Unusable in practice

**Fix**: File hash tracking, only re-index changed files.

**Lesson**: **Incremental indexing is not optional.**

### 4. Ignored Context Window Limits

**Mistake**: Sent too much code to LLM.

**Problem**:
- Exceeded context limits
- Slow responses
- High costs

**Fix**: Better retrieval (top-k, reranking), smarter context assembly.

**Lesson**: **Quality of context > quantity of context.**

---

## Performance Numbers

### Indexing Speed

| Codebase | Files | Symbols | Time |
|----------|-------|---------|------|
| Small (5K LOC) | 50 | 500 | ~30 sec |
| Medium (50K LOC) | 300 | 3,000 | ~3 min |
| Large (500K LOC) | 2,500 | 35,000 | ~20 min |

### Search Speed

| Query Type | Time |
|------------|------|
| Vector search (top-10) | ~50ms |
| Graph traversal (depth-5) | ~100ms |
| Full GraphRAG | ~2-5 sec (includes LLM) |

### Resource Usage

| Resource | Usage |
|----------|-------|
| Disk (vectors) | ~1GB per 100K symbols |
| Memory (indexing) | ~2GB peak |
| Memory (search) | ~500MB |

---

## What We'd Do Differently

### 1. Graph First, Not Vector First

We'd start with the knowledge graph, add vectors later. The graph is more valuable for code understanding.

### 2. Better Metadata from Start

Would extract more metadata during indexing:
- Parameter types
- Return types
- Docstrings
- Complexity metrics

### 3. Streaming Synthesis

Would implement streaming LLM responses earlier. Users waiting 5 seconds with no feedback is bad UX.

### 4. Built-in Evaluation

Would add evaluation harness from day 1:
- Test queries with expected results
- Track precision/recall over time
- Catch regressions

---

## Advice for Your Week-1 Project

### Start Simple

1. **File discovery** → Find .py/.java files
2. **Basic parsing** → Extract function names (regex is fine)
3. **JSON output** → Structured data

Then iterate.

### Don't Over-Engineer

Week 1 is about **learning**, not production quality.

| Good for Week 1 | Save for Later |
|-----------------|----------------|
| Regex parsing | tree-sitter |
| JSON file output | Vector database |
| Manual testing | Automated evaluation |
| Single language | Multi-language |

### Focus on Understanding

The goal is to **understand**:
- How code intelligence works
- What makes a good chunk
- How relationships are extracted
- Why this is hard

Building a working tool is secondary to learning.

---

## Tools We Use

| Purpose | Tool | Why |
|---------|------|-----|
| **Parsing** | tree-sitter | Fast, robust, multi-language |
| **Embeddings** | Ollama (mxbai-embed-large) | Local, free, good quality |
| **Vectors** | LanceDB | Embedded, simple, fast |
| **Graph** | SQLite | No setup, CTEs work well |
| **LLM** | OpenRouter (Claude) | Quality, flexibility |
| **CLI** | Effect-TS | Type-safe, composable |

---

## Key Takeaways

1. **Graph + Vector** is better than either alone
2. **Local embeddings** are good enough and much cheaper
3. **AST chunking** is worth the setup investment
4. **Incremental indexing** is essential
5. **Start simple**, iterate fast
6. **Index less**, index better

---

## Related

- [What Is Code Intelligence?](./01-What-Is-Code-Intelligence.md)
- [AST vs Text Chunking](./02-AST-vs-Text-Chunking.md)
- [Indexing Strategies](./03-Indexing-Strategies.md)
- [Commercial Tools](./05-Commercial-Tools.md)
- [Week 1 Requirements](../08-Exercises/01-Pre-Internship-Requirements.md)
