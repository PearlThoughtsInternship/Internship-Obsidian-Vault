# Day 9 – Multi-File Call Graph Merge

## Context
Until now, the mini code analyzer worked on a **single Python file**.  
Today’s goal was to move closer to real-world static analysis by enabling **multi-file analysis**.

Enterprise codebases are never single-file — so the analyzer must:
- Scan directories
- Analyze multiple `.py` files
- Merge results into one unified call graph

---

## Objective for Day 9
- Analyze **multiple Python files** from a directory
- Generate a **single merged call graph**
- Avoid duplicate nodes and edges
- Preserve **fully-qualified function names**

---

## What I Worked On

### 1. Directory Traversal
- Extended the analyzer to accept:
  - A single `.py` file
  - A directory containing multiple `.py` files
- Used `Path.rglob("*.py")` to recursively discover Python files

---

### 2. Per-File AST Analysis
- Each Python file is parsed independently using Python’s `ast` module
- Extracted:
  - Class definitions
  - Function definitions
  - Local call relationships
- Generated a **per-file call graph fragment**

---

### 3. Global Call Graph Merge Strategy
- Introduced a global `call_graph` data structure
- Merged per-file call graph fragments into a unified graph
- Ensured:
  - No duplicate caller nodes
  - No duplicate callee edges
- Maintained normalized, fully-qualified naming:
  - `module.Class.method`
  - `module.function`

---

## Example Usage

```bash
python analyzer.py project/

