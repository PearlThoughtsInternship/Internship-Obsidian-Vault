# Platform Capabilities

## Overview

The code intelligence platform provides four core capability areas, each addressing a specific aspect of legacy system understanding.

---

## Capability 1: Codebase Indexing

**Purpose**: Transform raw source code into searchable, structured knowledge.

### Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| Multi-language parsing | Python, Java, PHP, TypeScript | tree-sitter grammars |
| 4-mode extraction | Text, Symbol, Runtime, Workflow | See [[../02-Engineering/01-Architecture|Architecture]] |
| Incremental updates | Re-index only changed files | File hash tracking |
| Framework awareness | Django, Spring, Laravel patterns | Custom extractors |

### Success Metrics

| Metric | Target |
|--------|--------|
| Symbol coverage | 90%+ of functions/classes extracted |
| Parse success rate | 99%+ files without errors |
| Index time | < 5 min for 10K files |

---

## Capability 2: Context Generation

**Purpose**: Produce AI-ready context that answers specific questions about the codebase.

### Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| Query-aware retrieval | Return context relevant to question | Semantic + keyword search |
| Business rule extraction | Identify validation, calculation logic | Pattern matching + LLM |
| Workflow tracing | Trace what happens when X occurs | Call graph + entry points |
| Relationship mapping | Entity connections, dependencies | Graph analysis |

### Context Types

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONTEXT GENERATION OUTPUTS                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STRUCTURAL CONTEXT                                                      │
│  ├── Entity list (classes, functions, modules)                          │
│  ├── Relationship map (who uses whom)                                   │
│  └── Dependency graph (imports, calls)                                  │
│                                                                          │
│  SEMANTIC CONTEXT                                                        │
│  ├── Business rules ("discount applies when X")                         │
│  ├── Validation logic ("customer must have email")                      │
│  └── Workflow steps ("on submit: GL entry, stock update")               │
│                                                                          │
│  OPERATIONAL CONTEXT                                                     │
│  ├── Entry points (controllers, routes, handlers)                       │
│  ├── Side effects (what changes state)                                  │
│  └── External integrations (APIs, databases)                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Success Metrics

| Metric | Target |
|--------|--------|
| Context precision | 75%+ of provided context is relevant |
| Answer accuracy improvement | 20%+ vs no context |
| Retrieval latency (p95) | < 500ms |

---

## Capability 3: AI Integration

**Purpose**: Expose platform capabilities to AI assistants for seamless use.

### Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| MCP Server | Model Context Protocol for Claude Code | @modelcontextprotocol/sdk |
| Structured output | JSON schema for LLM consumption | Typed responses |
| Context windowing | Fit context within token limits | Smart truncation |
| Prompt templates | Pre-built prompts for common queries | Template library |

### Integration Patterns

```typescript
// MCP Tool Example
server.tool("trace_workflow", {
  entry_point: "string",  // e.g., "SalesInvoice.on_submit"
  depth: "number"         // How deep to trace
}, async ({ entry_point, depth }) => {
  const graph = await buildCallGraph(entry_point, depth);
  const context = formatForLLM(graph);
  return { context, diagram: toMermaid(graph) };
});
```

### Success Metrics

| Metric | Target |
|--------|--------|
| Tool call success rate | 99%+ |
| Response latency (p95) | < 2s |
| Context utilization | 80%+ of context used by LLM |

---

## Capability 4: Quality Measurement

**Purpose**: Track and improve context quality through systematic experimentation.

### Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| Experiment tracking | Compare approaches systematically | MLflow |
| Context quality metrics | Precision, recall, accuracy | RAGAs framework |
| Answer evaluation | Rate LLM responses | Human + automated |
| Drift detection | Notice quality degradation | Continuous monitoring |

### Experiment Protocol

```yaml
experiment:
  id: "exp-003"
  parameters:
    embedding_model: "bge-large-v1.5"
    chunk_size: 1500
    retrieval: "hybrid"

  baseline:
    question: "How does discount calculation work?"
    accuracy: 2  # Without context

  with_context:
    accuracy: 4  # With platform context

  delta: +2  # Improvement
```

### Success Metrics

| Metric | Target |
|--------|--------|
| Experiments tracked | 100% of iterations logged |
| Quality trend | Improving over time |
| Regression detection | < 24h to detect degradation |

---

## Capability Maturity Model

### Level 1: Extraction
- Parse code files
- Extract functions, classes, imports
- Output JSON

### Level 2: Relationships
- Map call relationships
- Identify entity connections
- Generate dependency graphs

### Level 3: Semantics
- Extract business rules
- Identify workflows
- Map to domain concepts

### Level 4: AI Integration
- Generate LLM-ready context
- Expose via MCP
- Query-relevant retrieval

### Level 5: Validated
- Context quality measured
- Experiments tracked
- Continuous improvement

---

## Related

- [[01-Vision|Product Vision]]
- [[../02-Engineering/01-Architecture|Technical Architecture]]
- [[../03-AI-Platform/01-Context-Generation|Context Generation Details]]
- [[../03-AI-Platform/04-Quality-Metrics|Quality Metrics]]

---

*Last Updated: 2026-01-13*
