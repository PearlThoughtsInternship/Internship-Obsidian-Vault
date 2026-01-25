Day 11 – Class-Aware Call Graph Resolution (AST)
Context

By Day 10, the mini code analyzer was capable of generating a multi-file call graph with fully-qualified function names.
However, method calls such as self.method() were still being resolved generically, without understanding class ownership.

Day 11 focused on improving semantic accuracy by making the analyzer class-aware.

Objective for Day 11

Resolve self.method() calls to the correct Class.method

Preserve full qualification: module.Class.method

Avoid runtime execution (pure static analysis)

Keep the analyzer scalable to multi-file projects

What I Worked On
1. Class Method Indexing

Introduced a class_methods registry

While visiting each ClassDef, collected all method names belonging to that class

Stored mappings like:

Invoice → { validate, calculate_tax }

2. Scope Stack Refinement

Used:

class_stack to track current class context

function_stack to track function scope

Built fully-qualified caller names dynamically:

module.Class.function

3. Class-Aware Call Resolution

Enhanced callee resolution logic:

helper() → module.helper

self.calculate_tax() → module.Invoice.calculate_tax

Validated method ownership using the class_methods registry

Prevented incorrect cross-class attribution

4. Global Call Graph Accuracy

Merged call graphs across files without duplications

Ensured semantic correctness of edges:

Invoice.validate → Invoice.calculate_tax

Example Output
sample.Invoice.validate
  └── sample.Invoice.calculate_tax


This confirms correct resolution of class-bound method calls.

Key Learnings

AST does not provide semantic resolution automatically

Accurate call graphs require:

Scope tracking

Context awareness

Explicit ownership mapping

Class-aware resolution is foundational for:

Impact analysis

Refactoring safety

Business logic extraction

Limitations Identified

Inheritance (super() calls) not yet handled

External imports resolved only at module level

Dynamic dispatch cannot be resolved statically

Next Steps

Add inheritance-aware resolution (super().method)

Resolve imported functions across modules

Export graph in DOT / Mermaid format for visualization

Begin rule-based business logic extraction

Reflection

This day marked a shift from syntactic parsing to semantic understanding.
The analyzer now understands who owns a method, not just who calls what — a critical step toward real-world code intelligence.