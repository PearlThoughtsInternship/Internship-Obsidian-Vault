# Day 7 – Call Graph Structuring & Consolidation (Holiday)

## Context
Today was Sunday, so development time was limited.  
Instead of introducing new abstractions, I focused on **consolidating and strengthening** the existing mini code analyzer to make the extracted information more structured and meaningful.

## What I Worked On
- Refined the AST-based analyzer to produce a **structured call graph**
- Introduced **class-aware caller naming** (`Class.method`)
- Grouped function calls by caller instead of printing flat call lists
- Ensured duplicate calls are avoided in the call graph

## Technical Details
- Used `ast.walk` to traverse the AST
- Maintained a lightweight **class context tracker**
- Constructed a dictionary-based call graph:
  ```python
  {
      "Invoice.validate": ["Invoice.calculate_tax"]
  }
