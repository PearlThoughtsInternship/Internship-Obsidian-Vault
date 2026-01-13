# AST vs Text Chunking

> **The fundamental trade-off**: Precision vs simplicity in code parsing

---

## The Problem

To build code intelligence, you need to break code into **chunks** that can be:
1. Embedded (converted to vectors)
2. Stored (in a database)
3. Retrieved (when answering queries)

But how do you chunk code? Two main approaches:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TWO APPROACHES TO CHUNKING                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TEXT-BASED CHUNKING                    AST-BASED CHUNKING              │
│  ───────────────────                    ────────────────────            │
│  Split by character/token count         Parse into syntax tree          │
│  Language-agnostic                      Language-specific               │
│  Simple to implement                    More complex                     │
│  May cut mid-function                   Respects code structure         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Text-Based Chunking

### How It Works

Split code into fixed-size pieces, like splitting a book into pages.

```python
def chunk_by_tokens(code: str, max_tokens: int = 500, overlap: int = 100):
    """Split code into overlapping chunks by token count."""
    tokens = tokenize(code)
    chunks = []

    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = tokens[i:i + max_tokens]
        chunks.append(detokenize(chunk))

    return chunks
```

### Example

**Input code:**
```python
class OrderService:
    def __init__(self, db):
        self.db = db

    def create_order(self, customer_id, items):
        order = Order(customer_id=customer_id)
        for item in items:
            order.add_line(item)
        return self.db.save(order)

    def cancel_order(self, order_id):
        order = self.db.find(order_id)
        if order.status == "shipped":
            raise ValueError("Cannot cancel shipped order")
        order.status = "cancelled"
        return self.db.save(order)
```

**Chunk 1** (tokens 0-200):
```python
class OrderService:
    def __init__(self, db):
        self.db = db

    def create_order(self, customer_id, items):
        order = Order(customer_id=customer_id)
        for item in items:
```

**Chunk 2** (tokens 100-300, overlapping):
```python
        for item in items:
            order.add_line(item)
        return self.db.save(order)

    def cancel_order(self, order_id):
        order = self.db.find(order_id)
```

**Problem**: Chunks cut across function boundaries. Chunk 2 starts mid-function.

### Pros and Cons

| Pros | Cons |
|------|------|
| Simple to implement | May cut mid-function |
| Works for any language | Loses structural context |
| No parsing required | May split related code |
| Fast | Duplicate code in overlaps |

---

## AST-Based Chunking

### How It Works

Parse code into an **Abstract Syntax Tree (AST)**, then extract chunks at meaningful boundaries (functions, classes, methods).

```python
import tree_sitter

def chunk_by_ast(code: str, language: str):
    """Extract chunks at syntax boundaries."""
    parser = get_parser(language)
    tree = parser.parse(code.encode())

    chunks = []
    for node in traverse(tree.root_node):
        if node.type in ['function_definition', 'class_definition', 'method_definition']:
            chunks.append({
                'type': node.type,
                'name': get_name(node),
                'code': code[node.start_byte:node.end_byte],
                'start_line': node.start_point[0],
                'end_line': node.end_point[0]
            })

    return chunks
```

### Example

**Same input code as above**

**Chunk 1** (class):
```python
class OrderService:
    def __init__(self, db):
        self.db = db

    def create_order(self, customer_id, items):
        order = Order(customer_id=customer_id)
        for item in items:
            order.add_line(item)
        return self.db.save(order)

    def cancel_order(self, order_id):
        order = self.db.find(order_id)
        if order.status == "shipped":
            raise ValueError("Cannot cancel shipped order")
        order.status = "cancelled"
        return self.db.save(order)
```

**OR more granular:**

**Chunk 1** (method):
```python
def __init__(self, db):
    self.db = db
```

**Chunk 2** (method):
```python
def create_order(self, customer_id, items):
    order = Order(customer_id=customer_id)
    for item in items:
        order.add_line(item)
    return self.db.save(order)
```

**Chunk 3** (method):
```python
def cancel_order(self, order_id):
    order = self.db.find(order_id)
    if order.status == "shipped":
        raise ValueError("Cannot cancel shipped order")
    order.status = "cancelled"
    return self.db.save(order)
```

**Benefit**: Each chunk is a complete, meaningful unit.

### Pros and Cons

| Pros | Cons |
|------|------|
| Respects code structure | Language-specific parsers needed |
| Complete functions/classes | More complex to implement |
| Can extract metadata (name, type) | Parser may fail on broken code |
| No mid-function cuts | Setup overhead |

---

## What Is tree-sitter?

**tree-sitter** is a parser generator that creates fast, incremental parsers for programming languages.

### Why tree-sitter?

1. **Fast**: Incremental parsing, handles large files
2. **Robust**: Works with incomplete/broken code
3. **Wide support**: 50+ languages
4. **Used in production**: VS Code, GitHub, Neovim

### Supported Languages

| Language | Grammar |
|----------|---------|
| Python | tree-sitter-python |
| Java | tree-sitter-java |
| JavaScript | tree-sitter-javascript |
| TypeScript | tree-sitter-typescript |
| PHP | tree-sitter-php |
| Ruby | tree-sitter-ruby |
| Go | tree-sitter-go |
| Rust | tree-sitter-rust |
| C/C++ | tree-sitter-c, tree-sitter-cpp |

### Basic Usage (Python)

```python
from tree_sitter import Language, Parser

# Load language
PY_LANGUAGE = Language('build/languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

# Parse code
code = b'''
def hello(name):
    return f"Hello, {name}"
'''
tree = parser.parse(code)

# Traverse AST
def traverse(node, depth=0):
    print("  " * depth + f"{node.type}: {node.text[:50] if node.text else ''}")
    for child in node.children:
        traverse(child, depth + 1)

traverse(tree.root_node)
```

**Output:**
```
module:
  function_definition: def hello(name):
    name: hello
    parameters: (name)
      identifier: name
    block:
      return_statement: return f"Hello, {name}"
        string: f"Hello, {name}"
```

### Basic Usage (TypeScript/JavaScript)

```typescript
import Parser from 'tree-sitter';
import Python from 'tree-sitter-python';

const parser = new Parser();
parser.setLanguage(Python);

const code = `
def hello(name):
    return f"Hello, {name}"
`;

const tree = parser.parse(code);

function traverse(node: Parser.SyntaxNode, depth = 0) {
  console.log('  '.repeat(depth) + `${node.type}`);
  for (const child of node.children) {
    traverse(child, depth + 1);
  }
}

traverse(tree.rootNode);
```

---

## Comparison Table

| Aspect | Text Chunking | AST Chunking |
|--------|--------------|--------------|
| **Implementation** | Simple | Complex |
| **Languages** | Any | Need parser per language |
| **Speed** | Fast | Fast (tree-sitter) |
| **Precision** | Low | High |
| **Metadata** | None | Names, types, lines |
| **Broken code** | Works | May fail |
| **Best for** | Quick prototype | Production systems |

---

## Hybrid Approach

Many production systems use **both**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HYBRID CHUNKING STRATEGY                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. AST CHUNKING (Primary)                                              │
│     └── Extract functions, classes, methods                             │
│     └── Preserve structure and metadata                                 │
│                                                                          │
│  2. TEXT CHUNKING (Fallback)                                            │
│     └── For unsupported languages                                       │
│     └── For comments/documentation                                      │
│     └── For very large functions                                        │
│                                                                          │
│  3. OVERLAP STRATEGY                                                    │
│     └── Small overlap for context continuity                            │
│     └── Include imports/headers in each chunk                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Recommendation for Week 1

### Start Simple (Text-Based)

If you're new to this, start with text chunking:

```python
def simple_chunk(code: str, lines_per_chunk: int = 50):
    """Dead simple chunking by line count."""
    lines = code.split('\n')
    chunks = []

    for i in range(0, len(lines), lines_per_chunk):
        chunk = '\n'.join(lines[i:i + lines_per_chunk])
        chunks.append(chunk)

    return chunks
```

### Then Upgrade (AST-Based)

Once working, upgrade to AST:

```python
def extract_functions(code: str, language: str):
    """Extract functions using tree-sitter."""
    parser = get_parser(language)
    tree = parser.parse(code.encode())

    functions = []
    for node in tree.root_node.children:
        if node.type in ['function_definition', 'method_definition']:
            functions.append({
                'name': get_function_name(node),
                'code': code[node.start_byte:node.end_byte],
                'line': node.start_point[0]
            })

    return functions
```

---

## Key Takeaways

1. **Text chunking** is simple but imprecise
2. **AST chunking** preserves code structure
3. **tree-sitter** is the standard for AST parsing
4. **Start simple**, upgrade later
5. **Hybrid approaches** combine the best of both

---

## Related

- [What Is Code Intelligence?](./01-What-Is-Code-Intelligence.md)
- [Indexing Strategies](./03-Indexing-Strategies.md)
- [Graph Extraction](./04-Graph-Extraction.md)
- [Week 1 Requirements](../08-Exercises/01-Pre-Internship-Requirements.md)
