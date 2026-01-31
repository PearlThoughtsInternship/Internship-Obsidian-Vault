🧠 Mini Code Analyzer

AST-based Static Code Intelligence Tool (Python)

A minimal yet powerful static analysis engine built using Python’s ast module to understand code structure, dependencies, and execution flow — without running the code.

This project focuses on learning how real code intelligence tools work internally.

🚀 Why This Project Exists

Modern AI systems (GraphRAG, Copilot-style tools, refactoring engines) cannot rely on raw text alone.
They need structured understanding of code:

Which functions call which?

How modules depend on each other?

Where are architectural risks like cyclic dependencies?

This project answers those questions using pure static analysis.

✨ Key Capabilities
1️⃣ Call Graph Extraction

Detects:

Functions

Class methods

Cross-module calls

Outputs a fully qualified call graph:

module.Class.method → module.function

2️⃣ Import Dependency Graph

Tracks import and from … import …

Builds a module dependency graph

Differentiates internal vs external structure

3️⃣ Multi-File Analysis

Analyze:

Single Python file

Entire directory (recursively)

Merges results into one global graph

4️⃣ Cycle Detection (Architecture Risk)

Detects cyclic dependencies using DFS

Outputs:

Human-readable cycles

Machine-readable cycles.json

Example:

a.func_a → b.func_b → c.func_c → a.func_a

5️⃣ Visual Graph Export (Mermaid)

Generates:

call_graph.mmd

import_graph.mmd

Features:

Module grouping

Red-highlighted cycle edges

Cycle labels

These diagrams render cleanly in:

Mermaid Live

GitHub

Documentation systems

📂 Project Structure
mini-code-analyzer/
├── analyzer.py          # AST analyzer (calls + imports)
├── cycle_detector.py    # Cycle detection engine
├── graph_exporter.py    # Mermaid graph generator
├── call_graph.json      # Structured graph output
├── diagrams/
│   ├── call_graph.mmd
│   └── import_graph.mmd
├── examples/
│   ├── multi_file_project/
│   └── cycle_project/
└── README.md

▶️ How to Run
Step 1: Analyze Code
python analyzer.py examples/multi_file_project


Generates:

call_graph.json

Step 2: Detect Cycles
python cycle_detector.py


Output:

Console cycle report

cycles.json

Step 3: Generate Diagrams
python graph_exporter.py


Creates:

diagrams/call_graph.mmd

diagrams/import_graph.mmd

🧪 Example Output
Call Graph (JSON)
{
  "a.func_a": ["b.func_b"],
  "b.func_b": ["c.func_c"],
  "c.func_c": ["a.func_a"]
}

Import Graph
{
  "a": ["b"],
  "b": ["c"],
  "c": ["a"]
}

🧠 How This Fits AI / GraphRAG Systems

This analyzer provides structured, machine-readable code context that can be fed into:

GraphRAG pipelines

LLM code assistants

Refactoring tools

Legacy modernization systems

Instead of raw text, an LLM receives:

Execution paths

Dependency boundaries

Risk hotspots (cycles)

This drastically improves reasoning quality.

⚠️ Known Limitations (By Design)

No runtime resolution (static only)

No dynamic dispatch inference

No type inference yet

These are intentional to keep the learning surface focused.

🔮 Future Enhancements

Severity ranking of cycles

Cross-repo analysis

Graph embeddings for LLM retrieval

CI integration for architecture checks

🎯 What This Project Demonstrates

Deep understanding of Python AST

Graph theory applied to real systems

Static analysis fundamentals

Tooling mindset (not just scripts)

Readiness for AI / platform engineering work

## 🔁 Cyclic Dependency Example

The analyzer can detect and visualize cyclic dependencies, which are common
architectural risks in large codebases.

```mermaid
graph TD
  subgraph a
    "a.func_a"
  end
  subgraph b
    "b.func_b"
  end
  subgraph c
    "c.func_c"
  end

  "a.func_a" -->|cycle| "b.func_b":::cycleEdge
  "b.func_b" -->|cycle| "c.func_c":::cycleEdge
  "c.func_c" -->|cycle| "a.func_a":::cycleEdge

  classDef cycleEdge stroke:red,stroke-width:3px;


📌 Author

Subhajit Das
AI / ML Engineer (in training)
Focus: Code Intelligence, AI Tooling, Graph-based Systems
