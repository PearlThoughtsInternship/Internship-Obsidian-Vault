import ast
import sys
from pathlib import Path

def analyze_file(file_path):
    code = Path(file_path).read_text()
    tree = ast.parse(code)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    print("\n📄 File analyzed:", file_path)
    print("📦 Classes found:", classes)
    print("🔧 Functions found:", functions)
    print(f"\n📊 Summary: {len(classes)} classes, {len(functions)} functions\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <python_file>")
        sys.exit(1)

    analyze_file(sys.argv[1])
