import ast
import sys
from pathlib import Path

def analyze_file(file_path):
    code = Path(file_path).read_text()
    tree = ast.parse(code)

    functions = []
    classes = []
    calls = []

    for node in ast.walk(tree):

        # Track classes
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

        # Track functions and calls INSIDE them
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

            for inner_node in ast.walk(node):
                if isinstance(inner_node, ast.Call):

                    called_function = None

                    # helper()
                    if isinstance(inner_node.func, ast.Name):
                        called_function = inner_node.func.id

                    # self.calculate_tax()
                    elif isinstance(inner_node.func, ast.Attribute):
                        called_function = inner_node.func.attr

                    if called_function:
                        calls.append({
                            "caller": node.name,
                            "callee": called_function,
                            "line": inner_node.lineno
                        })

    print("\n📄 File analyzed:", file_path)
    print("📦 Classes found:", classes)
    print("🔧 Functions found:", functions)

    print("\n🔗 Function Calls:")
    for call in calls:
        print(f"  {call['caller']} -> {call['callee']} (line {call['line']})")

    print(f"\n📊 Summary: {len(classes)} classes, {len(functions)} functions, {len(calls)} calls\n")


if __name__ == "__main__":
    analyze_file(sys.argv[1])


