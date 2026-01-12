# Commercial Code Intelligence Tools

> **Know the landscape**: What exists, what's missing, where you can contribute

---

## The Market

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CODE INTELLIGENCE LANDSCAPE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CATEGORY 1: AI Code Editors                                            │
│  └── Cursor, GitHub Copilot, Codeium                                    │
│  └── Focus: Autocomplete, inline suggestions                            │
│                                                                          │
│  CATEGORY 2: Enterprise Code Search                                     │
│  └── Sourcegraph, GitHub Code Search                                    │
│  └── Focus: Finding code across large orgs                              │
│                                                                          │
│  CATEGORY 3: Migration Tools                                            │
│  └── Amazon Q, GitHub Copilot Agents, Cast                              │
│  └── Focus: Language/framework upgrades                                 │
│                                                                          │
│  CATEGORY 4: Code Understanding (You're building here!)                 │
│  └── Limited options, mostly research                                   │
│  └── Focus: Deep semantic understanding                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Category 1: AI Code Editors

### Cursor

| Aspect | Details |
|--------|---------|
| **What it does** | AI-powered code editor (VS Code fork) |
| **Indexing** | Local codebase indexing, embeddings |
| **Strength** | Excellent autocomplete, chat with codebase |
| **Limitation** | Single repo focus, no cross-repo understanding |

**How it works:**
```
1. Index local codebase (embeddings)
2. On query: Vector search → Retrieve relevant code
3. Send code + query to LLM
4. Return AI-generated answer/code
```

**What's missing:**
- No knowledge graph (relationships)
- No business rule extraction
- No migration tracking

### GitHub Copilot

| Aspect | Details |
|--------|---------|
| **What it does** | AI pair programmer |
| **Indexing** | Limited local context |
| **Strength** | Excellent code completion |
| **Limitation** | Context window limits, no deep understanding |

**Architecture:**
```
Local file context (few KB) → GitHub LLM → Completions
```

**What's missing:**
- No full codebase understanding
- No graph/relationship awareness
- No enterprise knowledge integration

### Comparison

| Feature | Cursor | Copilot | CodeCompass (Ours) |
|---------|--------|---------|-------------------|
| Autocomplete | Yes | Yes | No |
| Chat with code | Yes | Yes | Yes |
| Full codebase indexing | Yes | Limited | Yes |
| Knowledge graph | No | No | Yes |
| Cross-repo search | No | No | Yes |
| Business rule extraction | No | No | Yes |
| Migration tracking | No | No | Yes |

---

## Category 2: Enterprise Code Search

### Sourcegraph

| Aspect | Details |
|--------|---------|
| **What it does** | Universal code search across all repos |
| **Scale** | Handles millions of repos |
| **Strength** | Fast search, great regex support |
| **Pricing** | Enterprise ($$$) |

**Key features:**
- Cross-repository search
- Code navigation (go to definition)
- Batch changes
- Code monitoring

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  SOURCEGRAPH ARCHITECTURE                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Code Hosts ───► Indexer ───► Trigram Index ───► Search                │
│  (GitHub, etc)              (Zoekt)                                     │
│                                                                          │
│  + Code Intelligence (Language Servers)                                 │
│  + Cody (AI Chat)                                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**What's missing (for modernization):**
- No semantic understanding
- No business context
- No migration tracking
- Text search, not intent search

### GitHub Code Search

| Aspect | Details |
|--------|---------|
| **What it does** | Search across GitHub repos |
| **Scale** | 200M+ public repos |
| **Strength** | Fast, integrated with GitHub |
| **Limitation** | Text-based, no semantics |

---

## Category 3: Migration/Modernization Tools

### Amazon Q Developer (formerly CodeWhisperer)

| Aspect | Details |
|--------|---------|
| **What it does** | AI-assisted cloud migration |
| **Languages** | Java, .NET, COBOL |
| **Strength** | AWS ecosystem integration |
| **Limitation** | AWS-focused, limited languages |

**Capabilities:**
- Java 8 → Java 17 upgrades
- .NET Framework → .NET Core
- COBOL analysis (limited)
- SQL Server → PostgreSQL

### GitHub Copilot Agents

| Aspect | Details |
|--------|---------|
| **What it does** | Automated code transformations |
| **Focus** | Framework upgrades |
| **Strength** | GitHub ecosystem |
| **Limitation** | Limited scope |

**Available agents:**
- npm upgrade agent
- Dependency update agent
- Security fix agent

### CAST Highlight

| Aspect | Details |
|--------|---------|
| **What it does** | Portfolio analysis, technical debt |
| **Approach** | Static analysis, metrics |
| **Strength** | Executive dashboards |
| **Limitation** | High-level, not code-level AI |

**What it measures:**
- Technical debt (in $ terms)
- Cloud readiness
- Security vulnerabilities
- Code complexity

---

## Category 4: Research & Open Source

### GPT-Migrate

| Aspect | Details |
|--------|---------|
| **Repository** | github.com/joshpxyne/gpt-migrate |
| **What it does** | AI-powered framework migration |
| **Approach** | LLM translates code file by file |
| **Limitation** | Works on small projects, high error rate |

**How it works:**
```
1. Read source file
2. Send to GPT-4 with target language instructions
3. Write translated file
4. Attempt to run/compile
5. Fix errors with more LLM calls
```

### Konveyor (CNCF)

| Aspect | Details |
|--------|---------|
| **What it does** | Kubernetes migration assistance |
| **Approach** | Rule-based analysis |
| **Strength** | Open source, community-driven |
| **Focus** | Containerization |

### TransCoder (Meta AI)

| Aspect | Details |
|--------|---------|
| **What it does** | Cross-language translation |
| **Approach** | Neural machine translation |
| **Languages** | C++, Java, Python |
| **Limitation** | Research, not production-ready |

---

## What's Missing in the Market

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GAP ANALYSIS                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WHAT EXISTS:                                                           │
│  ✓ Code completion (Cursor, Copilot)                                    │
│  ✓ Code search (Sourcegraph)                                            │
│  ✓ Simple migrations (Amazon Q)                                         │
│  ✓ Static analysis (Cast)                                               │
│                                                                          │
│  WHAT'S MISSING:                                                        │
│  ✗ Deep semantic understanding                                          │
│  ✗ Business rule extraction                                             │
│  ✗ Knowledge graph for code                                             │
│  ✗ Cross-codebase reasoning                                             │
│  ✗ Parity tracking (legacy ↔ modern)                                   │
│  ✗ Enterprise context integration (tickets, wikis)                      │
│                                                                          │
│  THIS IS YOUR OPPORTUNITY.                                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Approaches Comparison

| Approach | Pros | Cons | Used By |
|----------|------|------|---------|
| **Text search** | Fast, simple | No semantics | Sourcegraph |
| **Vector search** | Semantic similarity | Misses relationships | Cursor |
| **Graph** | Relationships, impact | Complex to build | Limited |
| **LLM translation** | Flexible | Error-prone | GPT-Migrate |
| **Rule-based** | Predictable | Limited scope | Amazon Q |

### The Right Approach: Hybrid

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HYBRID APPROACH (CODECOMPASS)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. GRAPH (Structure)                                                   │
│     └── Who calls whom, what extends what                               │
│     └── Impact analysis, dependency tracking                            │
│                                                                          │
│  2. VECTOR (Semantics)                                                  │
│     └── Find similar code, intent search                                │
│     └── Entry point discovery                                           │
│                                                                          │
│  3. LLM (Synthesis)                                                     │
│     └── Generate explanations                                           │
│     └── Answer natural language queries                                 │
│                                                                          │
│  COMBINE ALL THREE for comprehensive understanding.                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Existing tools are narrow** - Good at one thing, miss the big picture
2. **Graph + Vector + LLM** is the winning combination
3. **Enterprise context** (business rules, history) is largely ignored
4. **Migration tracking** is manual in most tools
5. **The gap is real** - There's room for innovation

---

## For Your Week-1 Project

You don't need to build everything. Focus on **one piece**:

| Piece | Difficulty | Impact |
|-------|------------|--------|
| Symbol extraction | Easy | Foundation |
| Call graph | Medium | Relationships |
| Vector search | Medium | Semantic queries |
| Business rule detection | Hard | High value |

Start simple, iterate.

---

## Related

- [What Is Code Intelligence?](./01-What-Is-Code-Intelligence.md)
- [CodeCompass Learnings](./06-CodeCompass-Learnings.md)
- [AST vs Text Chunking](./02-AST-vs-Text-Chunking.md)
- [Week 1 Requirements](../08-Exercises/01-Pre-Internship-Requirements.md)
