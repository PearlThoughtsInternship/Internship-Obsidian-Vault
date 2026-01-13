# LLM Integration

## Purpose

Expose platform capabilities to AI assistants through standardized interfaces.

---

## Integration Patterns

### Pattern 1: MCP Server (Recommended)

Model Context Protocol allows Claude Code and other AI assistants to call your tools directly.

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";

const server = new Server({
  name: "code-intelligence",
  version: "1.0.0"
});

// Tool: Search codebase
server.tool("search_code", {
  query: { type: "string", description: "Natural language query" },
  limit: { type: "number", default: 10 }
}, async ({ query, limit }) => {
  const results = await semanticSearch(query, limit);
  return formatForLLM(results);
});

// Tool: Trace workflow
server.tool("trace_workflow", {
  entry_point: { type: "string", description: "Function or method name" },
  depth: { type: "number", default: 5 }
}, async ({ entry_point, depth }) => {
  const graph = await buildCallGraph(entry_point, depth);
  return {
    context: formatForLLM(graph),
    diagram: toMermaid(graph)
  };
});

// Tool: Get business rules
server.tool("get_business_rules", {
  entity: { type: "string", description: "Entity name (e.g., SalesInvoice)" }
}, async ({ entity }) => {
  const rules = await extractBusinessRules(entity);
  return formatRulesForLLM(rules);
});
```

### Pattern 2: Context Injection

Prepare context and inject into prompts:

```python
def answer_with_context(question: str) -> str:
    # Generate relevant context
    context = generate_context(question)

    # Build prompt with context
    prompt = f"""
You are an expert on the ERPNext codebase. Use the following context to answer the question.

## Context
{context}

## Question
{question}

## Instructions
- Base your answer on the provided context
- Cite specific files and line numbers
- If the context doesn't contain the answer, say so
"""

    return llm.generate(prompt)
```

### Pattern 3: Agentic Workflow

Let the AI decide when to call tools:

```typescript
// Agent can call tools iteratively
const agent = new Agent({
  tools: [searchCode, traceWorkflow, getBusinessRules],
  maxIterations: 5
});

const result = await agent.run(
  "Explain the complete checkout flow, including all validations"
);
// Agent calls traceWorkflow, then getBusinessRules, then searchCode
// Synthesizes results into comprehensive answer
```

---

## Recommended AI Stack

### Embeddings (Local, Free)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull embedding model
ollama pull nomic-embed-text
```

```typescript
async function embed(text: string): Promise<number[]> {
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
```

### LLM (Groq - Free, Fast)

```typescript
async function generate(prompt: string): Promise<string> {
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
```

### Fallback (Ollama - Local)

```typescript
async function generateLocal(prompt: string): Promise<string> {
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
```

---

## Prompt Templates

### Code Explanation

```markdown
You are an expert on the {project_name} codebase.

## Context
{context}

## Question
Explain how {feature} works.

## Format
1. Start with a high-level summary (2-3 sentences)
2. Describe the main components involved
3. Explain the flow step by step
4. Note any important business rules or edge cases
5. Include a Mermaid diagram if helpful
```

### Business Rule Extraction

```markdown
Analyze the following code and extract business rules.

## Code
{code}

## Output Format
Return a JSON array of business rules:
```json
[
  {
    "rule": "description of the rule",
    "type": "validation|calculation|workflow",
    "location": "file:line",
    "confidence": 0.0-1.0
  }
]
```
```

### Impact Analysis

```markdown
Given this code change, analyze the impact.

## Changed Code
{diff}

## Codebase Context
{context}

## Analyze
1. What functions/classes are affected?
2. What tests might break?
3. What downstream systems are impacted?
4. What business processes are affected?
```

---

## Error Handling

```typescript
async function safeGenerate(prompt: string): Promise<string> {
  try {
    // Try primary (Groq)
    return await generateGroq(prompt);
  } catch (error) {
    if (error.status === 429) {
      // Rate limited, use fallback
      console.log("Rate limited, falling back to Ollama");
      return await generateLocal(prompt);
    }
    throw error;
  }
}
```

---

## Related

- [[01-Context-Generation|Context Generation]]
- [[03-Observability|Observability & Experiments]]
- [[../02-Engineering/01-Architecture|4-Mode Architecture]]

---

*Last Updated: 2026-01-13*
