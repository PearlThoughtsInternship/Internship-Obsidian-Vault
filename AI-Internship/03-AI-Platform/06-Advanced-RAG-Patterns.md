# Advanced RAG Patterns

Synthesized from Keith Bourne's "Unlocking Data with Generative AI and RAG" applied to code intelligence for legacy modernization.

---

## Overview

This document captures advanced RAG techniques from Keith Bourne's comprehensive guide and applies them to our ERPNext → Go modernization context. The patterns here extend beyond naive RAG to address real-world challenges in code understanding.

---

## RAG Evolution: From Naive to Advanced

### The Progression

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  RAG EVOLUTION                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  NAIVE RAG (Baseline)                                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Query → Embed → Vector Search → Top-K → LLM                                │
│  Problems: Context gaps, irrelevant results, no semantic understanding      │
│                                                                              │
│  HYBRID RAG (Better)                                                         │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Query → [BM25 + Dense] → RRF Fusion → Top-K → LLM                          │
│  Improvement: Catches keyword matches naive RAG misses                       │
│                                                                              │
│  ADVANCED RAG (Production)                                                   │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Query → Expand/Decompose → Hybrid Search → Rerank → Context Build → LLM    │
│  Improvement: Handles complex queries, prioritizes relevance                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why Naive RAG Falls Short for Code

| Problem | Naive RAG Behavior | Impact on Code Intelligence |
|---------|-------------------|----------------------------|
| **Vocabulary mismatch** | "payment processing" ≠ "make_gl_entries" | Misses relevant business logic |
| **Context fragmentation** | Returns random code snippets | Loses function-to-function relationships |
| **No semantic understanding** | Treats code as text | Ignores AST structure, call graphs |
| **Single-hop retrieval** | One search, done | Can't follow import chains |

---

## Query Enhancement Techniques

### 1. Query Expansion

Expand the original query to capture related concepts:

```python
# Applied to Code Intelligence

class QueryExpander:
    """Expands developer queries to catch ERPNext-specific terminology."""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.domain_mappings = {
            # Business term → ERPNext implementation
            "invoice": ["SalesInvoice", "make_gl_entries", "on_submit"],
            "payment": ["PaymentEntry", "get_outstanding_invoices"],
            "discount": ["apply_pricing_rule", "PricingRule", "discount_percentage"],
            "stock": ["StockEntry", "update_stock_ledger", "get_stock_balance"],
            "customer": ["Customer", "get_party_account", "customer_group"],
        }

    def expand(self, query: str) -> list[str]:
        """Generate expanded queries for better recall."""
        expansions = [query]  # Original always included

        # 1. Domain-specific expansion
        for term, mappings in self.domain_mappings.items():
            if term.lower() in query.lower():
                for mapping in mappings:
                    expansions.append(f"{query} {mapping}")

        # 2. LLM-based expansion (for complex queries)
        if self._is_complex_query(query):
            llm_expansions = self._llm_expand(query)
            expansions.extend(llm_expansions)

        return list(set(expansions))[:5]  # Dedupe, limit to 5

    def _llm_expand(self, query: str) -> list[str]:
        """Use LLM to generate semantically related queries."""
        prompt = f"""Given this code search query about ERPNext:
        "{query}"

        Generate 3 alternative phrasings that might help find relevant code.
        Focus on:
        - ERPNext/Frappe specific terminology
        - Python method naming conventions
        - Business domain terminology

        Return only the queries, one per line."""

        response = self.llm.complete(prompt)
        return [q.strip() for q in response.split('\n') if q.strip()]

    def _is_complex_query(self, query: str) -> bool:
        """Detect queries that benefit from LLM expansion."""
        complex_indicators = [
            "how does", "where is", "what happens when",
            "relationship between", "flow of", "process for"
        ]
        return any(ind in query.lower() for ind in complex_indicators)
```

### 2. Query Decomposition

Break complex questions into sub-queries:

```python
class QueryDecomposer:
    """Breaks complex code questions into searchable sub-queries."""

    def decompose(self, query: str) -> list[str]:
        """
        Example:
        Input: "How does submitting a Sales Invoice update stock and create accounting entries?"

        Output: [
            "SalesInvoice on_submit hook implementation",
            "make_gl_entries function in SalesInvoice",
            "update_stock method in SalesInvoice",
            "StockLedgerEntry creation from SalesInvoice"
        ]
        """
        # Detect multi-part questions
        if not self._is_compound(query):
            return [query]

        # Use LLM to decompose
        prompt = f"""Break this code question into specific, searchable sub-queries:

        Question: {query}

        Context: ERPNext/Frappe codebase (Python)

        Generate 2-4 focused sub-queries that together answer the full question.
        Each sub-query should target a specific function, class, or code path.

        Return one sub-query per line."""

        response = self.llm.complete(prompt)
        sub_queries = [q.strip() for q in response.split('\n') if q.strip()]

        return sub_queries[:4]  # Limit to avoid over-retrieval

    def _is_compound(self, query: str) -> bool:
        """Detect queries with multiple parts."""
        compound_markers = [" and ", " then ", " after ", " also ", " both "]
        return any(marker in query.lower() for marker in compound_markers)
```

### 3. Step-Back Prompting

For specific questions, first retrieve broader context:

```python
class StepBackRetriever:
    """
    Step-back prompting: Before answering specific questions,
    retrieve the broader context first.
    """

    def retrieve_with_stepback(self, specific_query: str) -> dict:
        """
        Example:
        Specific: "What validation runs on item_code in SalesInvoiceItem?"
        Step-back: "SalesInvoiceItem validation methods"

        Returns both specific and contextual results.
        """
        # Generate step-back query
        stepback_query = self._generate_stepback(specific_query)

        # Retrieve both
        specific_results = self.retriever.search(specific_query, k=5)
        context_results = self.retriever.search(stepback_query, k=3)

        # Combine with context first
        return {
            "context": context_results,  # Broader understanding
            "specific": specific_results,  # Direct answer
            "queries": {
                "original": specific_query,
                "stepback": stepback_query
            }
        }

    def _generate_stepback(self, query: str) -> str:
        """Generate a broader version of the query."""
        prompt = f"""Given this specific code question:
        "{query}"

        Generate a broader question that provides context for understanding the answer.
        The broader question should be about the containing class, module, or concept.

        Return only the broader question."""

        return self.llm.complete(prompt).strip()
```

---

## Reranking Strategies

### Cross-Encoder Reranking

Initial retrieval optimizes for recall; reranking optimizes for precision:

```python
from sentence_transformers import CrossEncoder

class CodeReranker:
    """
    Two-stage retrieval:
    1. Fast bi-encoder retrieval (recall)
    2. Slow cross-encoder reranking (precision)
    """

    def __init__(self):
        # Cross-encoder sees query AND document together
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.code_reranker = CrossEncoder('Salesforce/codet5p-110m-embedding')

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        top_k: int = 10
    ) -> list[dict]:
        """
        Rerank candidates using cross-encoder scoring.

        Args:
            query: Original search query
            candidates: Initial retrieval results (20-50 items)
            top_k: Number of results after reranking

        Returns:
            Top-k most relevant results
        """
        if not candidates:
            return []

        # Prepare pairs for cross-encoder
        pairs = []
        for candidate in candidates:
            # Combine code with docstring for better matching
            text = self._prepare_text(candidate)
            pairs.append([query, text])

        # Score all pairs
        scores = self.reranker.predict(pairs)

        # Attach scores and sort
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(scores[i])

        reranked = sorted(
            candidates,
            key=lambda x: x['rerank_score'],
            reverse=True
        )

        return reranked[:top_k]

    def _prepare_text(self, candidate: dict) -> str:
        """Prepare candidate text for reranking."""
        parts = []

        if candidate.get('docstring'):
            parts.append(candidate['docstring'])

        if candidate.get('signature'):
            parts.append(candidate['signature'])

        # Include first few lines of code body
        if candidate.get('code'):
            code_preview = '\n'.join(candidate['code'].split('\n')[:10])
            parts.append(code_preview)

        return '\n'.join(parts)
```

### Domain-Aware Reranking

Boost results that match ERPNext patterns:

```python
class DomainAwareReranker:
    """Reranking with ERPNext domain knowledge."""

    def __init__(self, cross_encoder):
        self.cross_encoder = cross_encoder

        # ERPNext-specific boosting rules
        self.boost_patterns = {
            # DocType lifecycle methods are highly relevant
            'on_submit': 1.3,
            'validate': 1.3,
            'before_save': 1.2,
            'on_cancel': 1.2,

            # Core business logic
            'make_gl_entries': 1.4,
            'update_stock': 1.4,
            'apply_pricing_rule': 1.3,

            # WhiteList APIs (entry points)
            '@frappe.whitelist': 1.2,
        }

    def rerank_with_domain_boost(
        self,
        query: str,
        candidates: list[dict]
    ) -> list[dict]:
        """Apply cross-encoder scores with domain boosting."""

        # Get base cross-encoder scores
        reranked = self.cross_encoder.rerank(query, candidates, top_k=len(candidates))

        # Apply domain boosts
        for candidate in reranked:
            boost = self._calculate_boost(candidate)
            candidate['final_score'] = candidate['rerank_score'] * boost
            candidate['domain_boost'] = boost

        # Re-sort by final score
        return sorted(reranked, key=lambda x: x['final_score'], reverse=True)

    def _calculate_boost(self, candidate: dict) -> float:
        """Calculate domain-specific boost factor."""
        boost = 1.0
        code = candidate.get('code', '') + candidate.get('name', '')

        for pattern, factor in self.boost_patterns.items():
            if pattern in code:
                boost = max(boost, factor)  # Take highest boost, don't multiply

        return boost
```

---

## Chunking Strategies for Code

### Strategy Comparison

| Strategy | Best For | Limitations |
|----------|----------|-------------|
| **Fixed-size** | Text documents | Breaks code mid-function |
| **Recursive character** | General text | Ignores code structure |
| **AST-based** | Source code | Requires language parser |
| **Semantic** | Concept grouping | Computationally expensive |

### AST-Based Chunking (Recommended for Code)

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

class ASTChunker:
    """
    AST-aware chunking that respects code boundaries.
    Each chunk is a complete syntactic unit.
    """

    def __init__(self):
        self.parser = Parser()
        self.parser.set_language(Language(tspython.language()))

        # Node types that form natural chunk boundaries
        self.chunk_types = {
            'function_definition',
            'class_definition',
            'decorated_definition',
        }

    def chunk_file(self, source_code: str, file_path: str) -> list[dict]:
        """
        Extract semantic chunks from Python source.

        Returns chunks with:
        - type: function/class/method
        - name: symbol name
        - code: full source
        - docstring: extracted docstring
        - start_line, end_line: location
        - parent: containing class (for methods)
        """
        tree = self.parser.parse(bytes(source_code, 'utf8'))
        chunks = []

        self._extract_chunks(tree.root_node, source_code, file_path, chunks)

        return chunks

    def _extract_chunks(
        self,
        node,
        source: str,
        file_path: str,
        chunks: list,
        parent_class: str = None
    ):
        """Recursively extract chunks from AST."""

        if node.type in self.chunk_types:
            chunk = self._node_to_chunk(node, source, file_path, parent_class)
            if chunk:
                chunks.append(chunk)

            # If this is a class, extract methods with class context
            if node.type == 'class_definition':
                class_name = self._get_name(node)
                for child in node.children:
                    if child.type == 'block':
                        for stmt in child.children:
                            self._extract_chunks(
                                stmt, source, file_path, chunks,
                                parent_class=class_name
                            )
                return  # Don't recurse further into class

        # Recurse into children
        for child in node.children:
            self._extract_chunks(child, source, file_path, chunks, parent_class)

    def _node_to_chunk(
        self,
        node,
        source: str,
        file_path: str,
        parent_class: str
    ) -> dict:
        """Convert AST node to chunk dict."""
        name = self._get_name(node)
        if not name:
            return None

        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        code = source[node.start_byte:node.end_byte]

        # Determine type
        if node.type == 'class_definition':
            chunk_type = 'class'
        elif parent_class:
            chunk_type = 'method'
        else:
            chunk_type = 'function'

        return {
            'type': chunk_type,
            'name': name,
            'qualified_name': f"{parent_class}.{name}" if parent_class else name,
            'code': code,
            'docstring': self._extract_docstring(node, source),
            'signature': self._extract_signature(node, source),
            'file_path': file_path,
            'start_line': start_line,
            'end_line': end_line,
            'parent_class': parent_class,
            'line_count': end_line - start_line + 1,
        }

    def _get_name(self, node) -> str:
        """Extract name from function/class definition."""
        for child in node.children:
            if child.type == 'identifier':
                return child.text.decode('utf8')
        return None

    def _extract_docstring(self, node, source: str) -> str:
        """Extract docstring if present."""
        for child in node.children:
            if child.type == 'block':
                for stmt in child.children:
                    if stmt.type == 'expression_statement':
                        expr = stmt.children[0] if stmt.children else None
                        if expr and expr.type == 'string':
                            return expr.text.decode('utf8').strip('"""\'\'\'')
        return None

    def _extract_signature(self, node, source: str) -> str:
        """Extract function/method signature."""
        # Find the colon that ends the signature
        for i, child in enumerate(node.children):
            if child.type == ':':
                sig_end = child.start_byte
                sig_start = node.start_byte
                return source[sig_start:sig_end].strip()
        return None
```

### Semantic Chunking with Overlap

For cases where AST boundaries are too rigid:

```python
class SemanticChunker:
    """
    Groups related code based on semantic similarity.
    Useful for documentation and comments.
    """

    def __init__(self, embedder, similarity_threshold: float = 0.7):
        self.embedder = embedder
        self.threshold = similarity_threshold

    def chunk_with_context(
        self,
        chunks: list[dict],
        context_lines: int = 5
    ) -> list[dict]:
        """
        Add overlapping context to AST chunks.
        Helps with code that references nearby definitions.
        """
        enhanced_chunks = []

        for i, chunk in enumerate(chunks):
            enhanced = chunk.copy()

            # Add context from surrounding chunks in same file
            same_file = [c for c in chunks if c['file_path'] == chunk['file_path']]

            # Find chunks that are semantically related
            related = self._find_related(chunk, same_file)

            if related:
                enhanced['related_context'] = [
                    {
                        'name': r['name'],
                        'signature': r.get('signature', ''),
                        'docstring': r.get('docstring', '')[:100]
                    }
                    for r in related[:3]  # Top 3 related
                ]

            enhanced_chunks.append(enhanced)

        return enhanced_chunks

    def _find_related(self, target: dict, candidates: list[dict]) -> list[dict]:
        """Find semantically related chunks."""
        if not candidates:
            return []

        # Embed target
        target_text = f"{target['name']} {target.get('docstring', '')}"
        target_emb = self.embedder.embed(target_text)

        # Score candidates
        scored = []
        for candidate in candidates:
            if candidate['name'] == target['name']:
                continue  # Skip self

            cand_text = f"{candidate['name']} {candidate.get('docstring', '')}"
            cand_emb = self.embedder.embed(cand_text)

            similarity = self._cosine_similarity(target_emb, cand_emb)
            if similarity > self.threshold:
                scored.append((similarity, candidate))

        # Sort by similarity
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored]
```

---

## RAG Evaluation Framework

### RAGAs Metrics Explained

From Keith Bourne's evaluation framework, applied to code intelligence:

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

class CodeRAGEvaluator:
    """
    RAGAs-based evaluation for code intelligence.

    Key metrics:
    - Faithfulness: Is the generated code grounded in retrieved context?
    - Answer Relevancy: Does the output address the query?
    - Context Precision: Is retrieved context relevant? (not noise)
    - Context Recall: Did we retrieve all needed context?
    """

    def __init__(self, llm_client):
        self.llm = llm_client
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

    def evaluate_retrieval(self, test_cases: list[dict]) -> dict:
        """
        Evaluate RAG pipeline on test cases.

        Each test case:
        {
            "question": "How does SalesInvoice calculate taxes?",
            "contexts": ["def calculate_taxes(self):...", ...],
            "answer": "Generated explanation or code",
            "ground_truth": "Expected relevant code/explanation"
        }
        """
        from datasets import Dataset

        dataset = Dataset.from_list(test_cases)
        results = evaluate(dataset, metrics=self.metrics)

        return {
            'faithfulness': results['faithfulness'],
            'answer_relevancy': results['answer_relevancy'],
            'context_precision': results['context_precision'],
            'context_recall': results['context_recall'],
            'overall': self._calculate_overall(results),
        }

    def _calculate_overall(self, results: dict) -> float:
        """Weighted overall score."""
        weights = {
            'faithfulness': 0.3,      # Critical: don't hallucinate
            'context_precision': 0.3,  # Important: don't waste context
            'context_recall': 0.25,    # Important: get all relevant
            'answer_relevancy': 0.15,  # Nice to have: address query
        }

        return sum(
            results[metric] * weight
            for metric, weight in weights.items()
        )
```

### Code-Specific Metrics

Beyond RAGAs, evaluate code-specific quality:

```python
class CodeQualityMetrics:
    """Metrics specific to code generation from RAG."""

    def evaluate_generated_code(
        self,
        generated: str,
        reference: str,
        query: str
    ) -> dict:
        """
        Evaluate generated Go code against reference.

        Returns:
        - syntax_valid: Does it parse?
        - type_correct: Do types match?
        - logic_preserved: Same business logic?
        - idiomatic: Follows Go conventions?
        """
        return {
            'syntax_valid': self._check_syntax(generated),
            'type_alignment': self._check_types(generated, reference),
            'logic_coverage': self._check_logic(generated, reference),
            'idiom_score': self._check_idioms(generated),
        }

    def _check_syntax(self, code: str) -> bool:
        """Verify Go code parses."""
        import subprocess
        result = subprocess.run(
            ['go', 'fmt'],
            input=code.encode(),
            capture_output=True
        )
        return result.returncode == 0

    def _check_types(self, generated: str, reference: str) -> float:
        """
        Check type alignment between generated and reference.
        Uses AST comparison of type signatures.
        """
        # Extract type signatures from both
        gen_types = self._extract_type_signatures(generated)
        ref_types = self._extract_type_signatures(reference)

        if not ref_types:
            return 1.0  # No types to compare

        matches = sum(1 for t in gen_types if t in ref_types)
        return matches / len(ref_types)

    def _check_logic(self, generated: str, reference: str) -> float:
        """
        Check if business logic patterns are preserved.
        Uses semantic similarity of function bodies.
        """
        # This would use embeddings to compare logic similarity
        pass

    def _check_idioms(self, code: str) -> float:
        """
        Check adherence to Go idioms.
        - Error handling patterns
        - Naming conventions
        - Package organization
        """
        score = 1.0

        # Check error handling
        if 'if err != nil' not in code and 'error' in code.lower():
            score -= 0.2  # Missing idiomatic error handling

        # Check naming (camelCase for exports, lowercase internal)
        # ...additional checks

        return max(0, score)
```

### Evaluation Dataset Creation

```python
class EvaluationDatasetBuilder:
    """Build golden test sets for RAG evaluation."""

    def create_test_case(
        self,
        question: str,
        relevant_files: list[str],
        expected_answer: str,
        difficulty: str = "medium"
    ) -> dict:
        """
        Create a single test case.

        Example:
        {
            "question": "How does SalesInvoice handle partial payments?",
            "relevant_files": [
                "erpnext/accounts/doctype/sales_invoice/sales_invoice.py",
                "erpnext/accounts/doctype/payment_entry/payment_entry.py"
            ],
            "expected_answer": "SalesInvoice tracks outstanding_amount...",
            "difficulty": "hard",
            "tags": ["accounting", "payments", "multi-file"]
        }
        """
        return {
            "question": question,
            "relevant_files": relevant_files,
            "expected_answer": expected_answer,
            "difficulty": difficulty,
            "ground_truth_context": self._load_contexts(relevant_files),
        }

    def generate_test_suite(self, module: str) -> list[dict]:
        """
        Generate comprehensive test suite for a module.

        Categories:
        - Single-function lookup
        - Multi-file traversal
        - Business logic explanation
        - Migration pattern matching
        """
        test_cases = []

        # Category 1: Direct lookup (easy)
        test_cases.extend(self._generate_lookup_tests(module))

        # Category 2: Cross-reference (medium)
        test_cases.extend(self._generate_cross_ref_tests(module))

        # Category 3: Business logic (hard)
        test_cases.extend(self._generate_logic_tests(module))

        return test_cases
```

---

## Multi-Modal RAG (MM-RAG)

For codebases with diagrams, UI screenshots, or documentation images:

```python
class MultiModalCodeRAG:
    """
    Handle multiple modalities in code intelligence:
    - Source code (text)
    - Architecture diagrams (image)
    - ERPNext UI screenshots (image)
    - API documentation (text + diagrams)
    """

    def __init__(self, text_embedder, vision_encoder):
        self.text_embedder = text_embedder
        self.vision_encoder = vision_encoder

    def index_multimodal(self, artifacts: list[dict]) -> None:
        """
        Index artifacts of different types.

        Artifacts:
        - {"type": "code", "path": "...", "content": "..."}
        - {"type": "diagram", "path": "...", "description": "..."}
        - {"type": "screenshot", "path": "...", "ui_element": "..."}
        """
        for artifact in artifacts:
            if artifact['type'] == 'code':
                embedding = self.text_embedder.embed(artifact['content'])
            elif artifact['type'] in ('diagram', 'screenshot'):
                embedding = self.vision_encoder.encode(artifact['path'])

            self._store(artifact, embedding)

    def search_multimodal(self, query: str, modalities: list[str] = None) -> list[dict]:
        """
        Search across modalities.

        Example query: "SalesInvoice form layout"
        - Returns: Code for form definition + UI screenshot
        """
        modalities = modalities or ['code', 'diagram', 'screenshot']

        results = []
        query_embedding = self.text_embedder.embed(query)

        for modality in modalities:
            modal_results = self._search_modality(query_embedding, modality)
            results.extend(modal_results)

        # Rank by relevance across modalities
        return self._cross_modal_rank(results, query)
```

---

## Context Window Optimization

### Efficient Context Construction

```python
class ContextOptimizer:
    """
    Optimize retrieved context for LLM consumption.
    Goal: Maximum information in minimum tokens.
    """

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.tokenizer = None  # Use appropriate tokenizer

    def build_context(
        self,
        retrieved: list[dict],
        query: str
    ) -> str:
        """
        Build optimized context string.

        Strategy:
        1. Prioritize most relevant chunks
        2. Include signatures over full code when space-limited
        3. Add relationship context (imports, calls)
        4. Reserve tokens for query-specific details
        """
        context_parts = []
        tokens_used = 0

        # Reserve 20% for relationships
        main_budget = int(self.max_tokens * 0.8)
        relationship_budget = self.max_tokens - main_budget

        # Add main content
        for chunk in retrieved:
            chunk_text = self._format_chunk(chunk)
            chunk_tokens = self._count_tokens(chunk_text)

            if tokens_used + chunk_tokens <= main_budget:
                context_parts.append(chunk_text)
                tokens_used += chunk_tokens
            else:
                # Add compressed version
                compressed = self._compress_chunk(chunk)
                comp_tokens = self._count_tokens(compressed)
                if tokens_used + comp_tokens <= main_budget:
                    context_parts.append(compressed)
                    tokens_used += comp_tokens

        # Add relationship context
        relationships = self._extract_relationships(retrieved)
        rel_text = self._format_relationships(relationships, relationship_budget)
        context_parts.append(rel_text)

        return '\n\n'.join(context_parts)

    def _compress_chunk(self, chunk: dict) -> str:
        """Compress chunk to essential information."""
        parts = [
            f"# {chunk['qualified_name']} ({chunk['file_path']}:{chunk['start_line']})"
        ]

        if chunk.get('signature'):
            parts.append(chunk['signature'])

        if chunk.get('docstring'):
            parts.append(f'"""{chunk["docstring"][:200]}..."""')

        return '\n'.join(parts)

    def _format_chunk(self, chunk: dict) -> str:
        """Format chunk for context."""
        return f"""### {chunk['qualified_name']}
File: {chunk['file_path']}:{chunk['start_line']}-{chunk['end_line']}

```python
{chunk['code']}
```"""

    def _extract_relationships(self, chunks: list[dict]) -> dict:
        """Extract relationships between chunks."""
        relationships = {
            'imports': set(),
            'calls': set(),
            'inherits': set(),
        }

        for chunk in chunks:
            if 'imports' in chunk:
                relationships['imports'].update(chunk['imports'])
            if 'calls' in chunk:
                relationships['calls'].update(chunk['calls'])
            if 'parent_class' in chunk and chunk['parent_class']:
                relationships['inherits'].add(chunk['parent_class'])

        return relationships
```

---

## Integration with Existing Pipeline

### Where These Patterns Fit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  UPDATED PIPELINE WITH ADVANCED PATTERNS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  QUERY PHASE                                                                 │
│  ───────────────────────────────────────────────────────────────────────── │
│  User Query                                                                  │
│       ↓                                                                      │
│  Query Expansion (domain mappings + LLM)           ← NEW                     │
│       ↓                                                                      │
│  Query Decomposition (for complex queries)         ← NEW                     │
│       ↓                                                                      │
│  Multiple Sub-Queries                                                        │
│                                                                              │
│  RETRIEVAL PHASE                                                             │
│  ───────────────────────────────────────────────────────────────────────── │
│  Each Sub-Query                                                              │
│       ↓                                                                      │
│  Hybrid Search (BM25 + Dense)                      ← EXISTING                │
│       ↓                                                                      │
│  RRF Fusion                                        ← EXISTING                │
│       ↓                                                                      │
│  Cross-Encoder Reranking                           ← NEW                     │
│       ↓                                                                      │
│  Domain Boost                                      ← NEW                     │
│       ↓                                                                      │
│  Top-K Results                                                               │
│                                                                              │
│  CONTEXT PHASE                                                               │
│  ───────────────────────────────────────────────────────────────────────── │
│  Retrieved Chunks                                                            │
│       ↓                                                                      │
│  Graph Expansion (imports, calls)                  ← EXISTING                │
│       ↓                                                                      │
│  Context Optimization (token budget)               ← NEW                     │
│       ↓                                                                      │
│  Formatted Context                                                           │
│                                                                              │
│  GENERATION PHASE                                                            │
│  ───────────────────────────────────────────────────────────────────────── │
│  Context + Query                                                             │
│       ↓                                                                      │
│  LLM Generation                                    ← EXISTING                │
│       ↓                                                                      │
│  Response                                                                    │
│                                                                              │
│  EVALUATION PHASE                                                            │
│  ───────────────────────────────────────────────────────────────────────── │
│  RAGAs Metrics                                     ← EXISTING                │
│  Code Quality Metrics                              ← NEW                     │
│  Developer Feedback                                ← EXISTING                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Priority

For the internship, implement in this order:

### Week 5-6: Core Enhancements

| Pattern | Priority | Effort | Impact |
|---------|----------|--------|--------|
| AST-based chunking | P0 | Medium | High |
| Hybrid search (BM25 + dense) | P0 | Low | High |
| Basic reranking | P1 | Low | Medium |

### Week 7-8: Advanced Retrieval

| Pattern | Priority | Effort | Impact |
|---------|----------|--------|--------|
| Query expansion | P1 | Medium | High |
| Domain-aware boosting | P1 | Low | Medium |
| Context optimization | P2 | Medium | Medium |

### Week 9-10: Evaluation & Polish

| Pattern | Priority | Effort | Impact |
|---------|----------|--------|--------|
| RAGAs integration | P0 | Low | High |
| Code quality metrics | P1 | Medium | High |
| Query decomposition | P2 | Medium | Medium |

---

## References

- Keith Bourne, "Unlocking Data with Generative AI and RAG" (2024)
- [01-Sales-Invoice-Case-Study](../05-Worked-Examples/01-Sales-Invoice-Case-Study.md) - Applied example
- [05-Enterprise-Tooling](./05-Enterprise-Tooling.md) - Evaluation tools
- [05-Development-Workflow](../04-Internship/05-Development-Workflow.md) - End-to-end process

---

*Last Updated: 2026-01-14*
