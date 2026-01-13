# Indexing Strategies

> **The foundation**: How to turn raw code into searchable, queryable knowledge

---

## What Is Indexing?

Indexing transforms raw source code into structured, searchable data.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INDEXING PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Source Code ───► Parser ───► Chunks ───► Embeddings ───► Storage       │
│       │              │           │             │              │          │
│       │              │           │             │              │          │
│       ▼              ▼           ▼             ▼              ▼          │
│  .py, .java     AST/Text    Functions,    Vectors      Vector DB        │
│  .ts files      parsing     Classes       [0.2, -0.5]  Graph DB         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: File Discovery

Find all relevant source files.

### Simple Approach

```python
import os
from pathlib import Path

def find_source_files(root_dir: str, extensions: list[str]) -> list[Path]:
    """Find all source files with given extensions."""
    files = []
    for ext in extensions:
        files.extend(Path(root_dir).rglob(f"*{ext}"))
    return files

# Usage
python_files = find_source_files("./erpnext", [".py"])
java_files = find_source_files("./bahmni-core", [".java"])
```

### With Ignore Patterns

```python
IGNORE_PATTERNS = [
    "**/node_modules/**",
    "**/__pycache__/**",
    "**/test_*.py",
    "**/tests/**",
    "**/*.min.js",
    "**/vendor/**",
    "**/.git/**",
]

def should_ignore(path: Path) -> bool:
    for pattern in IGNORE_PATTERNS:
        if path.match(pattern):
            return True
    return False

def find_source_files(root_dir: str, extensions: list[str]) -> list[Path]:
    files = []
    for ext in extensions:
        for f in Path(root_dir).rglob(f"*{ext}"):
            if not should_ignore(f):
                files.append(f)
    return files
```

---

## Step 2: Parsing

Extract structure from code.

### Option A: Regex (Simple, Fast Start)

```python
import re

def extract_python_functions(code: str) -> list[dict]:
    """Extract function definitions using regex."""
    pattern = r'def\s+(\w+)\s*\((.*?)\):'
    matches = re.finditer(pattern, code)

    functions = []
    for match in matches:
        functions.append({
            'name': match.group(1),
            'params': match.group(2),
            'start_pos': match.start()
        })
    return functions

# Usage
code = """
def hello(name):
    return f"Hello, {name}"

def add(a, b):
    return a + b
"""

functions = extract_python_functions(code)
# [{'name': 'hello', 'params': 'name', 'start_pos': 1},
#  {'name': 'add', 'params': 'a, b', 'start_pos': 48}]
```

### Option B: tree-sitter (Production Quality)

```python
from tree_sitter import Language, Parser

# Setup (one-time)
PY_LANGUAGE = Language('build/languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

def extract_functions_ast(code: str) -> list[dict]:
    """Extract functions using AST."""
    tree = parser.parse(code.encode())
    functions = []

    def traverse(node):
        if node.type == 'function_definition':
            name_node = node.child_by_field_name('name')
            functions.append({
                'name': name_node.text.decode() if name_node else 'unknown',
                'start_line': node.start_point[0],
                'end_line': node.end_point[0],
                'code': code[node.start_byte:node.end_byte]
            })
        for child in node.children:
            traverse(child)

    traverse(tree.root_node)
    return functions
```

---

## Step 3: Chunking Strategies

### Strategy 1: File-Level

Each file is one chunk.

```python
def chunk_by_file(files: list[Path]) -> list[dict]:
    chunks = []
    for f in files:
        content = f.read_text()
        chunks.append({
            'path': str(f),
            'content': content,
            'type': 'file'
        })
    return chunks
```

**Pros**: Simple, preserves context
**Cons**: Large files exceed embedding limits

### Strategy 2: Function-Level

Each function/method is one chunk.

```python
def chunk_by_function(files: list[Path]) -> list[dict]:
    chunks = []
    for f in files:
        content = f.read_text()
        functions = extract_functions_ast(content)
        for func in functions:
            chunks.append({
                'path': str(f),
                'name': func['name'],
                'content': func['code'],
                'type': 'function',
                'start_line': func['start_line']
            })
    return chunks
```

**Pros**: Clean boundaries, good for search
**Cons**: Loses file-level context

### Strategy 3: Sliding Window

Fixed-size overlapping chunks.

```python
def chunk_sliding_window(content: str, size: int = 500, overlap: int = 100) -> list[str]:
    lines = content.split('\n')
    chunks = []

    for i in range(0, len(lines), size - overlap):
        chunk = '\n'.join(lines[i:i + size])
        chunks.append(chunk)

    return chunks
```

**Pros**: Works for any content
**Cons**: May cut mid-function

### Strategy 4: Hybrid (Recommended)

```python
def chunk_hybrid(files: list[Path], max_tokens: int = 1000) -> list[dict]:
    """Function-level when possible, sliding window for large functions."""
    chunks = []

    for f in files:
        content = f.read_text()
        functions = extract_functions_ast(content)

        for func in functions:
            if len(func['code']) < max_tokens * 4:  # Rough token estimate
                # Function fits, use as-is
                chunks.append({
                    'path': str(f),
                    'name': func['name'],
                    'content': func['code'],
                    'type': 'function'
                })
            else:
                # Function too large, use sliding window
                sub_chunks = chunk_sliding_window(func['code'])
                for i, sub in enumerate(sub_chunks):
                    chunks.append({
                        'path': str(f),
                        'name': f"{func['name']}_part{i}",
                        'content': sub,
                        'type': 'function_part'
                    })

    return chunks
```

---

## Step 4: Embedding

Convert chunks to vectors.

### Using Ollama (Local)

```python
import requests

def embed_text(text: str, model: str = "mxbai-embed-large") -> list[float]:
    """Generate embedding using Ollama."""
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return response.json()["embedding"]

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Add embeddings to chunks."""
    for chunk in chunks:
        chunk['embedding'] = embed_text(chunk['content'])
    return chunks
```

### Using sentence-transformers (Python)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks: list[dict]) -> list[dict]:
    texts = [c['content'] for c in chunks]
    embeddings = model.encode(texts)

    for chunk, emb in zip(chunks, embeddings):
        chunk['embedding'] = emb.tolist()

    return chunks
```

---

## Step 5: Storage

### Option A: JSON File (Simplest)

```python
import json

def save_index(chunks: list[dict], path: str):
    with open(path, 'w') as f:
        json.dump(chunks, f)

def load_index(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)
```

### Option B: SQLite (Better for Metadata)

```python
import sqlite3

def create_index_db(path: str):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            path TEXT,
            name TEXT,
            content TEXT,
            type TEXT,
            start_line INTEGER,
            embedding BLOB
        )
    """)
    return conn

def insert_chunk(conn, chunk: dict):
    conn.execute("""
        INSERT INTO chunks (path, name, content, type, start_line, embedding)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        chunk['path'],
        chunk['name'],
        chunk['content'],
        chunk['type'],
        chunk.get('start_line'),
        json.dumps(chunk.get('embedding'))
    ))
```

### Option C: LanceDB (Vector-Native)

```python
import lancedb

def create_vector_db(path: str):
    db = lancedb.connect(path)
    return db

def insert_chunks(db, chunks: list[dict]):
    db.create_table("chunks", chunks)

def search_similar(db, query_embedding: list[float], k: int = 5):
    table = db.open_table("chunks")
    results = table.search(query_embedding).limit(k).to_list()
    return results
```

---

## Complete Indexing Pipeline

```python
def index_codebase(root_dir: str, output_path: str):
    """Complete indexing pipeline."""

    # Step 1: Find files
    print("Finding files...")
    files = find_source_files(root_dir, [".py", ".java"])
    print(f"Found {len(files)} files")

    # Step 2: Parse and chunk
    print("Parsing and chunking...")
    chunks = chunk_hybrid(files)
    print(f"Created {len(chunks)} chunks")

    # Step 3: Generate embeddings
    print("Generating embeddings...")
    chunks = embed_chunks(chunks)

    # Step 4: Store
    print("Saving index...")
    save_index(chunks, output_path)

    print(f"Done! Index saved to {output_path}")
    return chunks

# Usage
chunks = index_codebase("./erpnext", "erpnext_index.json")
```

---

## Performance Considerations

| Factor | Impact | Mitigation |
|--------|--------|------------|
| **Large codebases** | Slow indexing | Incremental updates |
| **Embedding API** | Rate limits | Local models (Ollama) |
| **Memory** | OOM on large files | Streaming, batching |
| **Storage** | Large indexes | Compression |

### Incremental Indexing

```python
import hashlib

def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()

def needs_reindex(path: Path, cached_hashes: dict) -> bool:
    current_hash = file_hash(path)
    return cached_hashes.get(str(path)) != current_hash
```

---

## Key Takeaways

1. **Start simple** - JSON files, regex parsing
2. **Upgrade incrementally** - Add AST, vectors, graph
3. **Ignore junk** - Tests, vendors, generated code
4. **Chunk smartly** - Function-level is usually best
5. **Store metadata** - Path, name, line numbers matter

---

## Related

- [What Is Code Intelligence?](./01-What-Is-Code-Intelligence.md)
- [AST vs Text Chunking](./02-AST-vs-Text-Chunking.md)
- [Graph Extraction](./04-Graph-Extraction.md)
- [CodeCompass Learnings](./06-CodeCompass-Learnings.md)
