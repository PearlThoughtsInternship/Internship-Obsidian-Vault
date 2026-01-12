# AI Coding Tool Architecture Comparison

## How Different Tools Handle Code Understanding

> *Understanding how existing AI coding tools work helps you build better alternatives.*

---

## Executive Summary

Different AI coding tools have fundamentally different architectures:

| Tool | Code Exploration | Context Selection | Token Cost for Exploration |
|------|-----------------|-------------------|---------------------------|
| **OpenCode** | Local preprocessing | Local selection | Free (all local) |
| **Cursor** | Local index + RAG | Local condensation | Free (local indexing) |
| **Aider** | Local repo-map | Local + small LLM | Minimal |
| **Claude Code** | Via LLM tool calls | LLM decides | User pays (tokens) |
| **Continue.dev** | Local embedding | Multi-stage reranking | Free (local) |

**Key Insight**: Most tools do local preprocessing to minimize token usage. Understanding these patterns helps you build better tooling.

---

## How Each Tool Works

### 1. OpenCode (Open Source)

**Repository**: [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)

> "OpenCode uses your project context to understand your code deeply. It scans through your files, recognizes dependencies, and maintains context across multiple commands. **All of this happens without needing to upload your code to the cloud.**"

**Architecture**:
```
User Query
    ↓
LOCAL: File scanning, dependency analysis
LOCAL: Context selection
LOCAL: Build coherent chunk
    ↓
CLOUD: Only send pre-selected context to LLM
    ↓
Response
```

**Strengths**:
- Complete privacy (all exploration local)
- Zero token cost for exploration
- Works offline for most operations

**Weaknesses**:
- Requires local setup and dependencies
- May miss context if local selection is wrong

---

### 2. Cursor AI

**Architecture**:
```
User Query
    ↓
LOCAL: Embedding-based semantic search (pre-built index)
LOCAL: Condensation (signatures, not full code)
LOCAL: Context assembly
    ↓
CLOUD: Send condensed context to LLM
CLOUD: LLM may request expansion (additional tokens)
    ↓
Response
```

**Key Innovations**:

1. **Context Condensation**: Large files compressed to show structure (function signatures) rather than full content
2. **Merkle Tree for Sync**: Efficient change detection via content hashing
3. **Hybrid Search**: RAG (semantic) + string-based (grep) combined
4. **Embedding Cache**: Same code content = skip recomputation

**Lessons to Apply**:
- Cache embeddings by content hash (MD5 of chunk content)
- Return signatures by default, expand on demand
- Use centrality ranking (PageRank-like) for file importance

---

### 3. Aider

**Repository**: [aider.chat](https://aider.chat)

> "The tool creates a repository map—essentially a collection of function signatures and file structures—that gives the LLM context about your entire codebase."

**Architecture**:
```
User Query
    ↓
LOCAL: Generate repo-map (signatures, structure)
LOCAL: Git-aware file selection
LOCAL: User explicitly adds files to context
    ↓
CLOUD: Send repo-map + selected files to LLM
    ↓
Response
```

**Key Innovations**:

1. **Repo Map Format**: Function signatures and file structures (~97% token reduction)
2. **PageRank Centrality**: Rank files by how often they're imported
3. **Git Integration**: Deep git history awareness

**Example Repo Map Output**:
```
src/services/
├── email.service.ts
│   ├── class EmailService
│   │   ├── syncEmails(options: SyncOptions): Promise<SyncResult>
│   │   ├── fetchNew(since: Date): Promise<Email[]>
│   │   └── markAsRead(ids: string[]): Promise<void>
│   └── imports: ConfigService, EmailRepository

Token count: ~500 (vs ~15,000 for full code)
```

---

### 4. Claude Code (Anthropic)

> "For code search, it's **'grep all the way down.'** This means Claude Code sometimes needs to pull in more context to understand what's going on."

**Architecture**:
```
User Query
    ↓
CLOUD: Claude decides to search
CLOUD: Grep tool call → results returned (TOKENS)
CLOUD: Claude decides to read file
CLOUD: Read tool call → content returned (TOKENS)
CLOUD: Claude decides to read another file
CLOUD: Read tool call → content returned (TOKENS)
    ↓
CLOUD: Finally has enough context to respond
    ↓
Response
```

**Strengths**:
- Truly agentic (figures things out without user guidance)
- No setup required (works on any codebase)
- 200K context window actually available
- Deep reasoning when context is present

**Weaknesses**:
- Every exploration step costs tokens
- Re-discovers every session (no persistence)
- No local preprocessing like competitors

---

### 5. Continue.dev

**Repository**: [github.com/continuedev/continue](https://github.com/continuedev/continue)

**Architecture**:
```
User Query
    ↓
LOCAL: Multiple chunking strategies
       ├── BasicChunker: Line-based
       ├── CodeChunker: AST-aware (tree-sitter)
       ├── MarkdownChunker: Docs-specific
       └── FullChunker: Entire file
LOCAL: Hybrid retrieval (BM25 + Vector)
LOCAL: Reranking (25 → 5 results)
    ↓
CLOUD: Send top-ranked context to LLM
    ↓
Response
```

**Key Innovations**:

1. **Multiple Chunking Strategies**: Not one-size-fits-all
2. **Multi-Stage Retrieval**: Broad retrieval → reranking → final selection
3. **Configurable Parameters**: chunk size, overlap, AST awareness

---

## Direct Cost Comparison

### Task: "How does authentication work in this codebase?"

#### OpenCode / Cursor / Continue.dev (Local Preprocessing)
```
1. LOCAL: Search index for "authentication" (0 tokens)
2. LOCAL: Find AuthService, TokenService, etc. (0 tokens)
3. LOCAL: Build condensed context (0 tokens)
4. CLOUD: Send ~3,000 tokens of curated context
5. CLOUD: LLM generates response

Total API tokens: ~4,000
```

#### Claude Code (No Local Preprocessing)
```
1. CLOUD: Claude calls grep("authentication") → 1,200 tokens
2. CLOUD: Claude calls read(auth.service.ts) → 3,200 tokens
3. CLOUD: Claude calls read(token.service.ts) → 2,400 tokens
4. CLOUD: Claude calls read(auth.controller.ts) → 2,000 tokens
5. CLOUD: Claude has context, generates response

Total API tokens: ~10,000
```

**Cost Difference**: ~2.5x more tokens without local preprocessing

---

## Learnings for Your Tools

### From Cursor: Embedding Cache

```typescript
// Cache embeddings by content hash
async function getEmbedding(content: string): Promise<number[]> {
  const contentHash = md5(content);

  // Check cache first
  const cached = await embeddingCache.get(contentHash);
  if (cached) return cached;  // Cache hit - skip computation

  // Generate new embedding
  const embedding = await ollama.embed(content);

  // Cache for future
  await embeddingCache.set(contentHash, embedding);
  return embedding;
}
```

### From Aider: PageRank Centrality

```typescript
// Rank files by import frequency
function rankResults(results: SearchResult[]): SearchResult[] {
  return results
    .map(r => ({
      ...r,
      combinedScore:
        r.semanticScore * 0.6 +       // Semantic similarity
        r.centralityScore * 0.3 +      // PageRank centrality
        r.recencyScore * 0.1           // Recently modified
    }))
    .sort((a, b) => b.combinedScore - a.combinedScore);
}
```

### From Continue.dev: Multi-Stage Retrieval

```
Stage 1: Broad Retrieval (25-50 candidates)
├── Vector search (semantic)
├── Keyword search (BM25)
└── Union results

Stage 2: Centrality Boost
├── Add PageRank scores
├── Boost files in import graph
└── Penalize test/mock files

Stage 3: Freshness Check
├── Verify files haven't changed
└── Mark stale results

Stage 4: Final Ranking (top 5-10)
├── Combined scoring
├── Deduplicate by file
└── Return with metadata
```

---

## Architecture Decision: Local vs Cloud

### Arguments for Local Preprocessing

| Factor | Benefit |
|--------|---------|
| **Cost** | Zero tokens for exploration |
| **Privacy** | Code stays on user machine |
| **Speed** | No network latency for search |
| **Persistence** | Index survives across sessions |

### Arguments for Cloud-Only (Claude Code Approach)

| Factor | Benefit |
|--------|---------|
| **Simplicity** | Works immediately, no setup |
| **Agentic** | LLM decides what to explore |
| **Universal** | Same approach for any codebase |
| **No staleness** | Always reads current state |

### Hybrid Approach (Recommended for Your Tools)

```
LOCAL: Build and maintain index
LOCAL: Semantic search entry points
LOCAL: Context selection and condensation
       ↓
CLOUD: Send optimized context to LLM
CLOUD: LLM reasons about curated context
       ↓
Result: Best of both worlds
```

---

## What Makes Sourcegraph Different

| Capability | AI Coding Tools | Sourcegraph |
|------------|----------------|-------------|
| **Scale** | 1-10 repos | 1M+ repos |
| **Deployment** | Local | Cloud SaaS |
| **Purpose** | Code completion, chat | Enterprise code search |
| **LSP** | Basic | Full go-to-definition |
| **Batch changes** | No | Multi-repo refactoring |

**Key Insight**: Sourcegraph is "Google for code" at enterprise scale. AI coding tools are "assistant for developer" at individual scale. They're complementary, not competitive.

---

## Open Source Tools to Study

### 1. Continue.dev
- **GitHub**: [github.com/continuedev/continue](https://github.com/continuedev/continue)
- **Study**: Chunking strategies, reranking pipeline

### 2. OpenCode
- **GitHub**: [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)
- **Study**: Local-first architecture, zero-cloud exploration

### 3. Aider
- **Website**: [aider.chat](https://aider.chat)
- **Study**: Repo map generation, git integration

### 4. LangChain
- **GitHub**: [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **Study**: Text splitters, retrieval chains

---

## Implementation Recommendations

### For Your Internship Project

1. **Build local-first**: Index locally, search locally, minimize token usage
2. **Use hybrid retrieval**: Combine vector search + keyword search
3. **Cache embeddings**: Content hash → embedding mapping
4. **Implement repo map**: Signatures provide 97% token savings
5. **Add centrality ranking**: Import frequency as quality signal
6. **Multi-stage retrieval**: Broad → rerank → final selection

### Architecture to Build

```
┌─────────────────────────────────────────────────────────────────┐
│                 YOUR CODE INTELLIGENCE TOOL                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LOCAL LAYER (Zero Token Cost)                                  │
│  ├── Index: tree-sitter parsing → SQLite                        │
│  ├── Embeddings: Ollama → LanceDB                              │
│  ├── Search: Vector + BM25 hybrid                               │
│  └── Context: Condensation, repo-map generation                 │
│                                                                 │
│                          ↓                                      │
│                                                                 │
│  CLOUD LAYER (Optimized Token Usage)                           │
│  ├── Send: Pre-selected, condensed context                      │
│  ├── Query: Clear question with minimal context                 │
│  └── Receive: LLM reasoning on curated data                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Related

- [Existing Tools Research](./03-Existing-Tools-Research.md)
- [Technical Architecture - Multi-Mode Knowledge Extraction](./06-Technical-Architecture.md)
- [AI Internship Overview](./00-Index.md)
- [Market Analysis](./04-Market-Analysis.md)
- [Quality Metrics](./07-Quality-Metrics.md)

---

## Sources

- [Continue.dev GitHub](https://github.com/continuedev/continue)
- [OpenCode GitHub](https://github.com/opencode-ai/opencode)
- [Aider Documentation](https://aider.chat/docs/)
- [How Cursor Indexes Codebases Fast](https://read.engineerscodex.com/p/how-cursor-indexes-codebases-fast)
- [Claude Code vs Cursor - Qodo](https://www.qodo.ai/blog/claude-code-vs-cursor/)

---

*Last Updated: 2025-01-12*
