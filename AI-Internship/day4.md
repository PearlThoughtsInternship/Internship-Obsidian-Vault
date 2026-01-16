# Day 4 – Function Call Detection (Holiday – Light Progress)

## Context
Today was a festival holiday, so work was limited.  
I focused on consolidating my understanding of AST traversal and function-call detection.

## What I Worked On
- Extended the mini code analyzer to detect function calls
- Used `ast.walk` to scan function bodies
- Detected both:
  - Direct calls (e.g. `helper()`)
  - Method calls (e.g. `self.calculate_tax()`)
- Captured caller, callee, and line number

## Key Learnings
- Function calls are represented as `ast.Call` nodes
- `ast.Name` represents direct calls
- `ast.Attribute` represents method calls
- Traversing only within `FunctionDef` nodes prevents false positives

## Limitations Identified
- Caller context is function-level only (class context not fully tracked)
- Nested scopes and decorators are not handled yet

## Next Steps
- Refactor analyzer using `ast.NodeVisitor`
- Introduce scope stacks for class and function context
- Build a class-aware call graph
