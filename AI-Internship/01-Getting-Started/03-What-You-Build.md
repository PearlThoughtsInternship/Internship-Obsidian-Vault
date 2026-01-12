# What You Build: Practical Guide

## From Theory to Code

> *This document answers: "What do I actually build? How do I test it? What do I do each day?"*

---

## Form Factor Choices

You have several options for what form your tool takes. Each has trade-offs.

### Option A: CLI Tool

A command-line interface that runs locally.

```bash
# Example usage
my-tool index ./path/to/codebase
my-tool search "how does authentication work"
my-tool graph AuthController.login
```

| Aspect | Details |
|--------|---------|
| **Pros** | Simple to build, easy to test, portable, works anywhere |
| **Cons** | No IDE integration, manual invocation required |
| **Effort** | Low |
| **Good for** | Learning, prototyping, validation |

### Option B: MCP Server

Model Context Protocol server that AI assistants (Claude Code, etc.) can call.

```typescript
// Your tool exposes capabilities as MCP tools
server.tool("search_code", { query: string }, async ({ query }) => {
  return await yourSearchPipeline(query);
});
```

| Aspect | Details |
|--------|---------|
| **Pros** | Works with Claude Code directly, AI decides when to use |
| **Cons** | Newer standard, requires MCP-compatible client |
| **Effort** | Medium |
| **Good for** | AI-native workflows, Claude Code integration |

### Option C: VS Code Extension

Extension that runs inside VS Code.

| Aspect | Details |
|--------|---------|
| **Pros** | Rich IDE integration, UI possibilities |
| **Cons** | VS Code-specific, more complex build process |
| **Effort** | High |
| **Good for** | Developer experience, visual features |

### Option D: Language Server (LSP)

Language Server Protocol implementation.

| Aspect | Details |
|--------|---------|
| **Pros** | Works with any LSP client (VS Code, Neovim, etc.) |
| **Cons** | Complex protocol, steep learning curve |
| **Effort** | High |
| **Good for** | Editor-agnostic IDE features |

### Option E: Library/SDK

Reusable code that others can import.

```typescript
import { CodeIndexer, SemanticSearch } from 'your-library';

const indexer = new CodeIndexer({ language: 'java' });
await indexer.index('./src');
```

| Aspect | Details |
|--------|---------|
| **Pros** | Composable, reusable, clean separation |
| **Cons** | Needs wrapper for end-user usage |
| **Effort** | Low-Medium |
| **Good for** | Building blocks for other tools |

### Option F: Hybrid (CLI + MCP)

Start with CLI, then expose as MCP server.

```
┌─────────────────────────────────────────────────────────────┐
│  CLI (Week 2-3)                                             │
│  └── bun run cli index/search/graph                         │
│           │                                                 │
│           ▼                                                 │
│  MCP Server (Week 3-4)                                      │
│  └── Wraps CLI commands as MCP tools                        │
│           │                                                 │
│           ▼                                                 │
│  Claude Code calls your tools                               │
└─────────────────────────────────────────────────────────────┘
```

| Aspect | Details |
|--------|---------|
| **Pros** | Testable independently, then AI-integrated |
| **Cons** | Two interfaces to maintain |
| **Effort** | Medium |
| **Good for** | Incremental development, validation at each step |

---

## AI Infrastructure: Recommended Free Options

For this internship, we recommend using **free AI services** that provide excellent quality without cost.

---

### Recommended: Embeddings (for indexing code)

Embeddings convert code into vectors for semantic search.

**Use Ollama (Local, Free, No Limits)**

| Model | Size | Quality | Speed | Install |
|-------|------|---------|-------|---------|
| **`nomic-embed-text`** | ~270MB | Good | Fast | `ollama pull nomic-embed-text` |
| `bge-large-en-v1.5` | ~1.3GB | Better | Medium | `ollama pull bge-large` |
| `mxbai-embed-large` | ~670MB | Good | Fast | `ollama pull mxbai-embed-large` |
| `all-minilm-l6-v2` | ~50MB | Basic | Very fast | `ollama pull all-minilm` |

**Why local embeddings?**
- Zero cost, unlimited usage
- No rate limits
- Works offline
- Data stays on your machine

---

### Recommended: LLM Models (for Q&A, synthesis)

#### Primary: Groq (Free Cloud, Very Fast)

| Model | Quality | Speed | Rate Limit |
|-------|---------|-------|------------|
| **`llama-3.3-70b-versatile`** | Excellent | Very fast | ~30 req/min |
| `llama-3.1-8b-instant` | Good | Extremely fast | ~30 req/min |
| `mixtral-8x7b-32768` | Good | Fast | ~30 req/min |

**Setup:**
1. Sign up at [console.groq.com](https://console.groq.com)
2. Get free API key
3. Use in your code:

```typescript
const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${GROQ_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'llama-3.3-70b-versatile',
    messages: [{ role: 'user', content: 'Explain this code...' }]
  })
});
```

#### Secondary: Ollama (Local, Free, No Limits)

| Model | Size | Quality | Use Case |
|-------|------|---------|----------|
| **`llama3.2:8b`** | ~4.7GB | Good | General Q&A |
| `codellama:7b` | ~4GB | Good | Code-specific |
| `deepseek-coder:6.7b` | ~4GB | Good | Code generation |
| `mistral:7b` | ~4GB | Good | Fast general use |

**Hardware requirements:**
- 8GB RAM minimum
- 16GB RAM recommended
- GPU optional but speeds up inference

#### Other Free Options

| Provider | Free Tier | Best For | Sign Up |
|----------|-----------|----------|---------|
| **Groq** | Generous free tier | Fast inference | [groq.com](https://console.groq.com) |
| **Google AI Studio** | 60 req/min free | Gemini models | [aistudio.google.com](https://aistudio.google.com) |
| **Together.ai** | $25 free credit | Many models | [together.ai](https://together.ai) |
| **Mistral** | Free tier | Mistral models | [mistral.ai](https://mistral.ai) |
| **OpenRouter** | Some free models | Model variety | [openrouter.ai](https://openrouter.ai) |

---

### Recommended Stack

```
┌─────────────────────────────────────────────────────────────┐
│  RECOMMENDED AI STACK (100% FREE)                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  EMBEDDINGS: Ollama + nomic-embed-text                      │
│  ├── Local, unlimited usage                                 │
│  ├── Good quality for code search                           │
│  └── No API key needed                                      │
│                                                             │
│  LLM (Primary): Groq                                        │
│  ├── Free tier with generous limits                         │
│  ├── Very fast (faster than OpenAI)                         │
│  └── Llama 3.3 70B is excellent quality                     │
│                                                             │
│  LLM (Fallback): Ollama + llama3.2                          │
│  ├── When offline or rate limited                           │
│  ├── No limits                                              │
│  └── Good quality, slower than cloud                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Setting Up the Recommended Stack

#### Step 1: Install Ollama (for embeddings + fallback LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended embedding model
ollama pull nomic-embed-text

# Pull fallback LLM model
ollama pull llama3.2

# Verify installation
ollama list
```

#### Step 2: Get Groq API Key (for primary LLM)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Navigate to API Keys
4. Create new API key
5. Save in `.env` file:

```bash
# .env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

#### Step 3: Use in Your Code

```typescript
// Embeddings via Ollama (local)
async function getEmbedding(text: string): Promise<number[]> {
  const response = await fetch('http://localhost:11434/api/embeddings', {
    method: 'POST',
    body: JSON.stringify({
      model: 'nomic-embed-text',
      prompt: text
    })
  });
  const data = await response.json();
  return data.embedding;
}

// LLM via Groq (free cloud, fast)
async function askLLM(prompt: string): Promise<string> {
  const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'llama-3.3-70b-versatile',
      messages: [{ role: 'user', content: prompt }]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content;
}

// Fallback to Ollama if Groq rate limited
async function askLLMWithFallback(prompt: string): Promise<string> {
  try {
    return await askLLM(prompt);
  } catch (error) {
    // Fallback to local Ollama
    const response = await fetch('http://localhost:11434/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        model: 'llama3.2',
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await response.json();
    return data.message.content;
  }
}
```

---

## Language Choices

### Primary Language Options

| Language | Pros | Cons | Ecosystem |
|----------|------|------|-----------|
| **TypeScript** | Type safety, large ecosystem, MCP SDK | Requires Node/Bun runtime | Effect-TS, tree-sitter bindings |
| **Python** | AI/ML libraries, RAGAs native | Slower, packaging complexity | LangChain, tree-sitter |
| **Go** | Fast, single binary | Smaller AI ecosystem | Limited tree-sitter support |
| **Rust** | Very fast, memory safe | Steep learning curve | tree-sitter native |

### Component-Specific Choices

| Component | Options | Notes |
|-----------|---------|-------|
| **CLI framework** | TypeScript: `@effect/cli`, `commander` | |
| | Python: `click`, `typer` | |
| **AST parsing** | tree-sitter (any language) | Bindings for TS, Python, Rust |
| **Vector DB** | LanceDB, ChromaDB, SQLite+extensions | LanceDB is embedded, no server |
| **Graph storage** | SQLite, Neo4j, Graphology (in-memory) | SQLite simplest |
| **MCP SDK** | TypeScript: `@modelcontextprotocol/sdk` | Official SDK |
| | Python: `mcp` | Official SDK |

---

## Testing Your Work

### Testing Layers

| Layer | What to Test | Tools | When |
|-------|--------------|-------|------|
| **Unit** | Individual functions (chunker, parser) | Vitest, pytest | Every commit |
| **Retrieval Quality** | Does search find right code? | RAGAs, custom metrics | Daily |
| **Integration** | Full pipeline works | Shell scripts, CLI tests | Daily |
| **MCP** | Server responds correctly | MCP Inspector | When building MCP |
| **Real Usage** | Works on actual codebase | Manual with target project | Weekly |

### Unit Testing Examples

```typescript
// Vitest example
import { describe, it, expect } from 'vitest';
import { chunkCode } from './chunker';

describe('chunkCode', () => {
  it('splits at function boundaries', () => {
    const code = `
      function foo() { return 1; }
      function bar() { return 2; }
    `;
    const chunks = chunkCode(code, { language: 'typescript' });
    expect(chunks).toHaveLength(2);
    expect(chunks[0]).toContain('foo');
    expect(chunks[1]).toContain('bar');
  });
});
```

### Retrieval Quality Testing

Create test cases in YAML:

```yaml
# test-cases.yaml
test_suite: "retrieval-tests"

test_cases:
  - id: "find-auth-logic"
    query: "How does user authentication work?"
    expected_files:
      - AuthService.java
      - TokenService.java
    must_contain_concepts:
      - "password validation"
      - "token generation"

  - id: "find-discount-calculation"
    query: "Where is discount calculated?"
    expected_files:
      - DiscountService.java
    must_not_return:
      - DiscountServiceTest.java  # Don't return test files
```

Run and measure:

```bash
# Your CLI could have a test command
my-tool test:retrieval test-cases.yaml

# Output:
# ✅ find-auth-logic: PASS (precision: 0.9, recall: 0.85)
# ❌ find-discount-calculation: FAIL (missing DiscountService.java)
#
# Summary: 1/2 passed (50%)
```

### MCP Server Testing

```bash
# Use MCP Inspector to test your server
npx @modelcontextprotocol/inspector your-server

# Or test with curl
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "search_code", "arguments": {"query": "authentication"}}}'
```

---

## Daily and Weekly Workflow

### Daily Structure Options

#### Option 1: Build-Test-Document Cycle

```
Morning (2-3 hrs)     → BUILD
├── Pick task from weekly goals
├── Implement feature
└── Write tests alongside

Afternoon (2-3 hrs)   → TEST & VALIDATE
├── Run on target codebase
├── Check retrieval metrics
└── Fix issues found

End of Day (30 min)   → DOCUMENT
├── Update progress notes
├── Log blockers
└── Commit code
```

#### Option 2: Spike-Implement Cycle

```
Day 1: SPIKE
├── Research approach
├── Prototype solution
└── Validate feasibility

Day 2-3: IMPLEMENT
├── Build production version
├── Write tests
└── Integrate with existing code

Day 4: VALIDATE
├── Test on real codebase
├── Measure quality
└── Document learnings
```

#### Option 3: Pairing Sessions

```
Solo Work (4 hrs)
├── Independent coding
└── Self-directed learning

Pair Session (2 hrs)
├── Code review with peer
├── Problem-solve together
└── Share learnings
```

### Weekly Checkpoint Structure

| Day | Focus | Deliverable |
|-----|-------|-------------|
| Monday | Plan week, set goals | Written goals for the week |
| Tuesday-Thursday | Build and test | Working code, passing tests |
| Friday | Demo and reflect | Show progress to mentor, update OKR |

### Progress Tracking Methods

#### Method 1: OKR Updates

Update [09-OKR.md](./09-OKR.md) weekly with:
- Key results achieved
- Metrics measured
- Blockers encountered

#### Method 2: Daily Standups (Async)

```markdown
## 2025-01-15

**Yesterday:** Implemented tree-sitter parser for Java
**Today:** Adding function extraction, writing tests
**Blockers:** None
**Metrics:** 85% of functions extracted correctly
```

#### Method 3: Demo Videos

Record 2-min Loom videos showing:
- What you built
- How it works
- What's next

---

## How Pieces Fit Together

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    END-TO-END FLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TARGET CODEBASE                                            │
│  (Bahmni, ERPNext, Odoo)                                    │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  INDEXING PIPELINE                                  │    │
│  │  ├── File discovery (glob patterns)                 │    │
│  │  ├── Parsing (tree-sitter AST)                      │    │
│  │  ├── Chunking (text + symbol modes)                 │    │
│  │  ├── Embedding (Ollama/OpenAI)                      │    │
│  │  └── Storage (LanceDB vectors, SQLite metadata)     │    │
│  └─────────────────────────────────────────────────────┘    │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  RETRIEVAL PIPELINE                                 │    │
│  │  ├── Query embedding                                │    │
│  │  ├── Vector search (semantic similarity)            │    │
│  │  ├── Keyword search (BM25)                          │    │
│  │  ├── Hybrid merge + reranking                       │    │
│  │  └── Return top results                             │    │
│  └─────────────────────────────────────────────────────┘    │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  GRAPH PIPELINE (Optional)                          │    │
│  │  ├── Call graph extraction                          │    │
│  │  ├── Dependency mapping                             │    │
│  │  └── Visualization (Mermaid)                        │    │
│  └─────────────────────────────────────────────────────┘    │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  INTERFACES                                         │    │
│  │  ├── CLI (direct usage)                             │    │
│  │  ├── MCP Server (AI assistant integration)          │    │
│  │  └── Library (programmatic use)                     │    │
│  └─────────────────────────────────────────────────────┘    │
│           │                                                 │
│           ▼                                                 │
│  DEVELOPER / AI ASSISTANT                                   │
│  Gets answers about legacy code                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Example

```
Query: "How does discount calculation work?"

1. CLI/MCP receives query
        │
        ▼
2. Embed query with same model used for indexing
   "How does discount..." → [0.23, -0.45, 0.12, ...]
        │
        ▼
3. Search LanceDB for similar vectors
   → DiscountService.java (0.89 similarity)
   → PriceCalculator.java (0.82 similarity)
   → DiscountTest.java (0.79 similarity)
        │
        ▼
4. Rerank results
   → Boost by centrality (how often imported)
   → Penalize test files
   → DiscountService.java (final: 0.91)
   → PriceCalculator.java (final: 0.80)
        │
        ▼
5. Return results with metadata
   {
     file: "DiscountService.java",
     lines: "45-78",
     content: "public class DiscountService...",
     relevance: 0.91
   }
```

---

## Getting Started Checklist

### Week 1: Setup & Research

```
□ Set up development environment
□ Install Ollama and pull models
□ Clone target codebase (Bahmni/ERPNext/Odoo)
□ Read existing tools research
□ Choose your track (A, B, C, or D)
□ Choose form factor (CLI, MCP, etc.)
□ Choose language (TypeScript, Python, etc.)
□ Set up project structure
```

### Week 2: Build Foundation

```
□ Implement file discovery
□ Implement parsing (tree-sitter)
□ Implement chunking
□ Implement embedding pipeline
□ Store in LanceDB + SQLite
□ Write unit tests
□ Test on small part of target codebase
```

### Week 3: Build Retrieval

```
□ Implement vector search
□ Implement keyword search (optional)
□ Implement hybrid ranking
□ Create test cases (YAML)
□ Measure retrieval quality (RAGAs)
□ Iterate to improve metrics
□ Build MCP server (if chosen)
```

### Week 4: Validate & Document

```
□ Test on full target codebase
□ Demo to mentor
□ Document architecture
□ Document learnings
□ Record final metrics
□ Package for handoff
```

---

## Related

- [AI Internship Overview](./00-Index.md)
- [Goals & Expectations](./02-Goals-and-Expectations.md)
- [Technical Architecture](./06-Technical-Architecture.md)
- [Quality Metrics](./07-Quality-Metrics.md)
- [Validation Projects](./08-Validation-Projects.md)

---

*Last Updated: 2025-01-12*
