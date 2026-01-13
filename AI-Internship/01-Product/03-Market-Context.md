# Market Context

## The Legacy Modernization Market

### Market Size

| Metric | Value | Source |
|--------|-------|--------|
| Annual market size | $300B+ | McKinsey |
| Fortune 500 with 20+ year old software | 70% | McKinsey 2024 |
| CIOs citing legacy as barrier | 60% | Gartner |
| Technical debt as % of tech estate | 20-40% | Salfati Group 2025 |

### Why Now?

1. **AI capabilities have matured** - LLMs can now understand and reason about code
2. **Enterprise pressure is mounting** - Digital transformation requires modernization
3. **Talent shortage persists** - Not enough developers who understand legacy systems
4. **Cloud migration accelerating** - Legacy systems block cloud adoption

---

## Competitive Landscape

### Tier 1: Cloud Providers

| Tool | Focus | Approach | Gap |
|------|-------|----------|-----|
| GitHub Copilot | .NET, Java upgrades | Multi-agent system | Generic, no business context |
| Amazon Q | COBOL to Java | AI agents + AWS services | AWS-centric |
| Azure Migrate | Infrastructure migration | Assessment + AI | Limited code understanding |

### Tier 2: Specialized Vendors

| Tool | Focus | Approach | Gap |
|------|-------|----------|-----|
| CAST | Portfolio analysis | Static analysis | No AI reasoning |
| vFunction | Monolith decomposition | Architecture analysis | No runtime correlation |
| OpenLegacy | Mainframe APIs | API generation | Mainframe-only |

### Open Source

| Tool | Focus | Approach | Gap |
|------|-------|----------|-----|
| GPT-Migrate | Language translation | LLM-powered transform | Small codebases only |
| Konveyor | Kubernetes migration | Rule-based analysis | No semantic understanding |

---

## Identified Gaps

These gaps represent our opportunity:

| Gap | Current State | Our Approach |
|-----|---------------|--------------|
| **Business Context** | Tools analyze code only | Extract business rules, workflows |
| **Runtime Behavior** | Static analysis only | Correlate with execution traces |
| **Domain Understanding** | Generic patterns | Domain-specific (ERP, healthcare) |
| **AI Context** | Not optimized for LLMs | Structured context for AI assistants |
| **Validation** | Manual testing | Automated quality measurement |

---

## Why Existing Tools Fall Short

### The Business Logic Problem

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WHERE BUSINESS LOGIC LIVES                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  In Documentation:     5%   │░                                          │
│  In People's Heads:   10%   │░░                                         │
│  In THE CODE:         85%   │░░░░░░░░░░░░░░░░░░░░                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

Current tools extract **code structure** but miss **business meaning**:

- They find functions but don't understand what the function does for the business
- They map dependencies but don't trace business workflows
- They analyze syntax but miss the "why" embedded in comments and naming

### The AI Context Problem

AI assistants (Copilot, Cursor, Claude Code) need context to reason about code. Current approaches:

| Approach | Problem |
|----------|---------|
| Full codebase dump | Exceeds token limits |
| File-by-file | Misses cross-file relationships |
| Keyword search | Misses semantic meaning |
| Generic RAG | Not optimized for code structure |

Our platform provides **structured, query-aware context** optimized for LLM consumption.

---

## Market Validation Points

### What Enterprises Are Asking For

From analyst reports and customer interviews:

1. "We need to understand our legacy systems before we can migrate them"
2. "Our documentation is outdated - the truth is in the code"
3. "AI tools don't understand our business domain"
4. "We can't trust automated migration without verification"

### What AI Tool Users Report

From developer surveys:

1. "Copilot is great for new code but doesn't understand our existing system"
2. "I spend hours providing context before the AI can help"
3. "The AI hallucinates about our codebase because it doesn't have real context"

---

## Our Differentiation

| Dimension | Generic AI Tools | Our Platform |
|-----------|------------------|--------------|
| **Context** | Code snippets | Business rules + workflows |
| **Understanding** | Syntax | Semantics + domain |
| **Scope** | Single file | Full codebase graph |
| **Validation** | None | Quality metrics |
| **Target** | General coding | Enterprise modernization |

---

## Related

- [[01-Vision|Product Vision]]
- [[02-Capabilities|Platform Capabilities]]
- [[Target-Codebases/|Validation Targets]]

---

*Last Updated: 2026-01-13*
