# AI Internship - Objectives & Key Results

## Program Objective

> Build and validate AI-powered tools that understand enterprise codebases and accelerate legacy modernization.

---

## OKR by Track

### Track A: Knowledge Extraction

**Objective**: Extract comprehensive knowledge from legacy codebases

| Key Result | Target | Measurement |
|------------|--------|-------------|
| Symbol extraction coverage | >95% | Functions/classes indexed vs total |
| Call graph accuracy | >90% | Edges validated against manual trace |
| Business rule extraction | >70% recall | Rules found vs manual audit |
| Framework pattern detection | >80% | ORM relations, validations identified |

**Deliverables**:
- [ ] Semantic chunking pipeline for Java/Python
- [ ] Graph extraction module (calls, dependencies)
- [ ] Business rule pattern extractors
- [ ] Validation report on Bahmni clinical module

---

### Track B: Intelligent Retrieval

**Objective**: Build retrieval systems that understand developer intent

| Key Result | Target | Measurement |
|------------|--------|-------------|
| Query precision@5 | >80% | Relevant results in top 5 |
| Cross-file understanding | >75% | Multi-file queries answered correctly |
| Answer accuracy | >75% | LLM answers validated against docs |
| Latency | <2s | Time to first result |

**Deliverables**:
- [ ] RAG pipeline for code understanding
- [ ] GraphRAG implementation (vector + graph)
- [ ] Multi-modal retrieval (code + docs + context)
- [ ] Validation report on ERPNext accounting queries

---

### Track C: Domain Discovery

**Objective**: Automatically identify bounded contexts in monolithic systems

| Key Result | Target | Measurement |
|------------|--------|-------------|
| Module boundary accuracy | >85% | Auto-detected vs actual |
| Coupling metrics | Calculated | Inter-module dependency scores |
| Visualization quality | Usable | Team can understand output |
| False positive rate | <20% | Incorrect boundary suggestions |

**Deliverables**:
- [ ] Clustering pipeline for domain detection
- [ ] Visualization for domain boundaries
- [ ] Validation tool comparing against known structure
- [ ] Validation report on Odoo module discovery

---

### Track D: Migration Automation

**Objective**: Accelerate actual code migration with AI assistance

| Key Result | Target | Measurement |
|------------|--------|-------------|
| Feature parity | >90% | Migrated features match original |
| Test pass rate | >85% | Original tests passing on new code |
| Time savings | >50% | vs manual migration estimate |
| Defect rate | <5% | Critical bugs in migrated code |

**Deliverables**:
- [ ] Parity tracking system (legacy↔modern mapping)
- [ ] AI migration agent for code transformation
- [ ] Test generation for migrated code
- [ ] Actual migration of one Bahmni service

---

## Cross-Cutting KRs

| Key Result | Target | All Tracks |
|------------|--------|------------|
| Documentation quality | Complete | README, ADRs, API docs |
| Code test coverage | >70% | Unit and integration tests |
| Blog post | Published | Technical write-up of approach |
| Demo presentation | Delivered | End-of-internship showcase |

---

## Weekly Milestones

| Week | Milestone |
|------|-----------|
| 1-2 | Environment setup, project familiarization |
| 3-4 | Core feature implementation (v0.1) |
| 5-6 | Validation on real project, iterate |
| 7-8 | Integration, polish, documentation |
| 9-10 | Final validation, metrics collection |
| 11-12 | Presentation, knowledge transfer, blog |

---

## Success Criteria

### Individual Success
- [ ] Completed assigned track deliverables
- [ ] Met >70% of Key Results
- [ ] Published blog post
- [ ] Delivered demo presentation

### Program Success
- [ ] Tools validated on all 3 projects
- [ ] At least one actual migration completed
- [ ] Metrics demonstrate tool effectiveness
- [ ] Knowledge captured for future cohorts

---

*Last Updated: 2025-01-12*
