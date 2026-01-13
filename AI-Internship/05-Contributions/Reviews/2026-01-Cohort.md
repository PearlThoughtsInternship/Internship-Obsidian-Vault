# Submission Review - January 2026

## Purpose

This document reviews all intern submissions to help everyone learn together. Each submission has strengths others can learn from, and areas where the broader goals can guide improvement.

---

## What We're Building Toward

Before diving into submissions, here's the target outcome:

> **A tool that helps AI assistants (Claude Code, Cursor) give accurate answers about enterprise legacy codebases.**

The test: Ask Claude Code "How does discount calculation work in ERPNext?" Does your tool's output help it answer correctly?

---

## Submissions Overview

| Intern | Project | Repo | Key Approach |
|--------|---------|------|--------------|
| Harishlal M E | ERPNext | [python-code-analyzer](https://github.com/Harishlal-me/python-code-analyzer) | AST + multiple output formats |
| Bhagath | ERPNext | [Python-Code-Analyzer](https://github.com/BhagathUma/Python-Code-Analyzer) | AST + Gemini API suggestions |
| Sai Mahima Jilla | ERPNext | [python-ast-code-analyzer](https://github.com/Cloxy7/python-ast-code-analyzer) | AST + JSON output |
| GUGHAN S | ERPNext | *(repo URL needed)* | Sales Invoice on_submit workflow |
| Srilakshmi B | ERPNext | [ERPNext-Domain-Analyzer](https://github.com/srilakshmi-bheemshetty/ERPNext-Domain-Analyzer) | Domain mapping (JSON) |
| Lakshita Mishra | ERPNext | [ERP-Next](https://github.com/laxita05/ERP-Next) | Basic AST analyzer |
| Abhi Pandey | ERPNext | [ERPNext](https://github.com/Abhi4621/ERPNext) | Directory scanner + JSON |
| Nilesh Mehta | ERPNext | [code-analyzer-demo](https://github.com/iamnileshmehta/code-analyzer-demo) | AST + call relationships |
| Nikita Jaiswal | ERPNext | [code-analyzer-demo](https://github.com/NikitaJaiswal77/code-analyzer-demo) | Scanner + complexity rules |
| Neel Vadhiya | Bahmni | [Bahmni-test](https://github.com/Neeln11/Bahmni-test) | Multi-language indexer + artifacts |
| Ashish Rastogi | ERPNext | *(repo URL needed)* | AST + JSON structure |

---

## Detailed Review

### Harishlal M E - Multiple Output Formats

**Repo**: [python-code-analyzer](https://github.com/Harishlal-me/python-code-analyzer)

**What's Here**: AST-based analyzer with three output formats (colored console, JSON, text summary). Includes comparative analysis of two files.

**What Others Can Learn From This**:
- Multiple output formats serve different needs (console for quick checks, JSON for programmatic use)
- Comparative analysis is useful for understanding changes between code versions

**Opportunities**:
- Currently analyzes sample files. The next step is running against actual ERPNext source code
- Add relationship extraction - which functions call which others?
- Test: Does this JSON output help Claude Code answer questions about the code?

---

### Bhagath - LLM Integration

**Repo**: [Python-Code-Analyzer](https://github.com/BhagathUma/Python-Code-Analyzer)

**What's Here**: AST analysis combined with Gemini API to generate improvement suggestions. Detects unused imports/variables.

**What Others Can Learn From This**:
- LLM integration is the direction we're heading - Bhagath is the only submission with this
- The 5-stage workflow (parse → traverse → metrics → LLM → output) is well-structured

**Opportunities**:
- Current LLM use: "Here's code, suggest improvements" (like a linter)
- Target LLM use: "Here's context about the codebase, answer this question about it"

The shift:
```python
# Current
suggestions = llm("Suggest improvements for this code: {code}")

# Target
answer = llm("""
Given this context about ERPNext Sales Invoice:
{extracted_context}

How does discount calculation work?
""")
```

---

### Sai Mahima Jilla - Clean Implementation

**Repo**: [python-ast-code-analyzer](https://github.com/Cloxy7/python-ast-code-analyzer)

**What's Here**: Straightforward AST extraction with JSON output. 25 commits showing iteration.

**What Others Can Learn From This**:
- Clean, simple implementation that does one thing well
- Commit history shows learning progression

**Opportunities**:
- Apply to ERPNext source code (not just sample files)
- Add more structure to the JSON - entity relationships, call graphs
- Document what you learned in the README (this helps others and shows understanding)

---

### GUGHAN S - Business Logic Focus

**Repo**: *(Need URL)*

**What's Described**: Focuses on ERPNext Sales Invoice `on_submit` workflow. Identifies downstream calls like GL entries and Stock updates.

**What Others Can Learn From This**:
- This is the right problem framing: "Standard LLMs miss critical downstream calls"
- Targeting a specific workflow (on_submit) rather than generic "all functions"

**Opportunities**:
- Share the repo so others can see the approach
- Generate a visual flow diagram (Mermaid) of the on_submit cascade

---

### Srilakshmi B - Domain Understanding

**Repo**: [ERPNext-Domain-Analyzer](https://github.com/srilakshmi-bheemshetty/ERPNext-Domain-Analyzer)

**What's Here**: JSON mapping of ERPNext domains (Finance, HR, Manufacturing, CRM, Projects) with strengths and limitations.

**What Others Can Learn From This**:
- Understanding the business domains is valuable context
- Honest reflection: "ERP modules overlap (Finance ↔ Projects ↔ HR)"

**Opportunities**:
- Current: Hand-crafted JSON describing domains
- Target: Extract domain information programmatically from code

The question to answer: Can you derive the domain structure by analyzing the code itself?

---

### Lakshita Mishra - Getting Started

**Repo**: [ERP-Next](https://github.com/laxita05/ERP-Next)

**What's Here**: Basic AST analyzer following the reference repo pattern.

**What Others Can Learn From This**:
- Starting with the reference repo is a good learning approach

**Opportunities**:
- More iteration needed - single commit suggests early stage
- Look at Nilesh's repo for ideas on adding call relationship extraction
- Look at Bhagath's repo for ideas on LLM integration

---

### Abhi Pandey - ERPNext-Specific Tooling

**Repo**: [ERPNext](https://github.com/Abhi4621/ERPNext)

**What's Here**: CLI tool with directory scanner, designed specifically to help understand ERPNext. Video demo included.

**What Others Can Learn From This**:
- Clear problem statement: "ERPNext is very large and complex. For new developers, it is difficult to understand how the code works by reading files one by one."
- Video demo helps others understand the tool quickly

**Opportunities**:
- Add call graph extraction (see Nilesh's connector.py for ideas)
- Test on a specific ERPNext module and document findings
- Structure output to answer specific questions about the code

---

### Nilesh Mehta - Relationship Extraction

**Repo**: [code-analyzer-demo](https://github.com/iamnileshmehta/code-analyzer-demo)

**What's Here**: Separated architecture with extractor, connector, and output modules. The connector module maps function call relationships.

**What Others Can Learn From This**:
- Separating extraction from relationship-building from output is clean design
- Call relationship extraction is valuable - "who calls whom" helps trace workflows

**Opportunities**:
- Output relationships as Mermaid diagrams for visualization
- Apply to ERPNext and generate call graphs for specific workflows
- Test if the relationship data helps Claude Code answer "what happens when X is called?"

---

### Nikita Jaiswal - Rule-Based Analysis

**Repo**: [code-analyzer-demo](https://github.com/NikitaJaiswal77/code-analyzer-demo)

**What's Here**: Scanner with configurable rules for metrics and complexity.

**What Others Can Learn From This**:
- Config-driven approach allows customization
- Good mindset: "The goal is not perfection, but to understand how codebases can be analyzed"

**Opportunities**:
- Apply complexity rules to ERPNext - which files are most complex?
- Connect complexity metrics to modernization priorities
- Consider: What rules would identify "hard to modernize" code?

---

### Neel Vadhiya - Multi-Artifact Generation

**Repo**: [Bahmni-test](https://github.com/Neeln11/Bahmni-test)

**What's Here**: Dual-language indexer (Python AST + Java regex) generating five artifact types:
- Domain overview (all classes, functions, files)
- Entity maps (Mermaid class diagrams)
- Call graphs (workflow visualization)
- Business rules (extracted validation logic)
- Dependency reports

Tested on Bahmni Core (~800 files).

**What Others Can Learn From This**:
- Multiple artifact types serve different needs
- Testing on the actual target codebase validates the approach
- Extracting business rules ("Patient must have identifier") is exactly what modernization needs
- Java support opens up more legacy codebases

**Opportunities**:
- Add LLM integration to synthesize artifacts into natural language context
- Create an MCP server so Claude Code can query the artifacts
- Test: Do the artifacts help Claude Code answer questions about Bahmni?

---

### Ashish Rastogi

**Repo**: *(Need URL)*

**What's Described**: AST-based analyzer with JSON output for understanding large codebases.

**Opportunities**:
- Share the repo so we can provide specific feedback
- Look at other submissions for ideas to incorporate

---

## Cross-Pollination Ideas

Here's how different submissions can inspire each other:

| If You Built... | Look At... | To Learn About... |
|-----------------|------------|-------------------|
| Basic AST extraction | Nilesh's connector.py | Call relationship extraction |
| Single output format | Harishlal's repo | Multiple output formats |
| Sample file testing | Neel's repo | Testing on real codebase |
| Code-only analysis | Srilakshmi's repo | Domain/business context |
| Static analysis only | Bhagath's repo | LLM integration |
| Python only | Neel's repo | Multi-language support |
| Function extraction | GUGHAN's description | Workflow-specific analysis |

---

## Gaps from Original Goals

The internship goal is building tools for **enterprise legacy modernization with AI**. Here's where submissions diverge from this goal:

### Gap 1: Sample Files vs Real Codebases

Most submissions test on sample Python files. The target is ERPNext (Python) or Bahmni (Java) - real, complex codebases.

**Bridge**: Clone ERPNext, pick one module (Sales Invoice), run your tool, document what you find.

### Gap 2: Generic Analysis vs Modernization-Specific

Current: "Here are the functions in this file"
Target: "Here's what happens when a Sales Invoice is submitted, including all downstream effects"

**Bridge**: Focus on workflows and business logic, not just code structure.

### Gap 3: Tool Output vs AI-Ready Context

Current: JSON listing functions and classes
Target: Context that helps AI assistants answer questions accurately

**Bridge**: Run the context quality experiment (see [[03-Context-Quality-Experiment]])

### Gap 4: Building vs Validating

Most submissions build tools but don't validate if they work.

**Bridge**: Test your output. Does it help Claude Code answer questions about ERPNext/Bahmni?

---

## What Success Looks Like

At the end of this internship, we want tools that can:

1. **Index** a legacy codebase (ERPNext, Bahmni, or similar)
2. **Extract** meaningful context (workflows, business rules, relationships)
3. **Provide** that context to AI assistants
4. **Improve** AI responses about the codebase (measurably)

The validation question: "With my tool's context, did Claude Code give a better answer?"

---

## Next Steps for Everyone

### This Week

1. **Clone your target codebase** (ERPNext or Bahmni)
2. **Pick ONE module** to focus on
3. **Run your tool** on real code
4. **Document findings** - what worked? what broke?

### Next Week

1. **Run the context quality experiment**
2. **Compare notes** with other interns
3. **Iterate** based on what you learned

---

## Related

- [[03-Context-Quality-Experiment|How to Validate Context Quality]]
- [[04-ERPNext-Business-Context|Understanding ERPNext from Business Perspective]]
- [[../04-Target-Projects/02-ERPNext-Domain-Analysis|ERPNext Domain Analysis]]

---

*Last Updated: 2026-01-13*
