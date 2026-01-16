# Mini Code Analyzer (AST-based)

This is a **minimal Python code analyzer** built to understand the fundamentals of **code intelligence** using Python’s built-in `ast` module.

The goal of this mini project is **learning**, not completeness.

---

## 🎯 Purpose

- Understand how source code can be analyzed **structurally**, not as plain text
- Learn how Python converts code into an **Abstract Syntax Tree (AST)**
- Practice extracting useful information from code:
  - Classes
  - Functions

This serves as a **stepping stone** toward a larger code analysis tool.

---

## 📂 Project Structure

mini-code-analyzer/
├── analyzer.py # Minimal AST-based analyzer
├── sample.py # Example Python file to analyze
└── README.md # This file

## ✅ Current Capabilities

- Detects class definitions
- Detects function definitions
- Identifies function → function call relationships
- Tracks caller, callee, and line number

## ▶️ How to Run

```bash
python analyzer.py sample.py
