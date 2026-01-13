# Internship Goals & Expectations

## Your Mission (4 Weeks)

> *Research, build, validate, and execute a real legacy modernization using AI-powered tools you create.*

---

## End-to-End Ownership

Unlike typical internships where you support a delivery team, **you own everything end-to-end**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR OWNERSHIP SCOPE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WEEK 1: RESEARCH                                               │
│  └── Study existing AI modernization tools                      │
│  └── Understand enterprise modernization patterns               │
│  └── Select target module from validation project               │
│                                                                  │
│  WEEK 2: BUILD                                                  │
│  └── Build your AI-powered modernization tooling                │
│  └── Index and analyze target legacy module                     │
│  └── Generate domain understanding artifacts                    │
│                                                                  │
│  WEEK 3: MIGRATE                                                │
│  └── Use your tools + Cursor AI to perform actual migration     │
│  └── Translate code (Java/Python → TypeScript/Go)               │
│  └── Preserve business behavior and feature parity              │
│                                                                  │
│  WEEK 4: VERIFY & DOCUMENT                                      │
│  └── Migrate and run tests                                      │
│  └── Verify functional parity                                   │
│  └── Document findings, write blog post                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Week 1: Research Phase

### Goal: Understand the Landscape

Before building, you must understand what exists and what's missing.

### Task 1.1: Study Existing AI Modernization Tools

Research and document capabilities/limitations of:

#### Commercial Tools

| Tool | Vendor | Focus | Research Questions |
|------|--------|-------|-------------------|
| **GitHub Copilot Agents** | Microsoft | .NET, Java upgrades | How do agents work? What can they automate? Limitations? |
| **Amazon Q Developer** | AWS | Cloud migration, COBOL | What languages supported? How does it handle business logic? |
| **Azure Migrate + Copilot** | Microsoft | End-to-end migration | How do tools integrate? What's automated vs manual? |
| **CAST Highlight/Imaging** | CAST | Portfolio analysis | How does it visualize dependencies? What metrics? |
| **OpenLegacy** | OpenLegacy | Mainframe API generation | How does it bridge legacy to modern? |

#### Open Source Tools

| Tool | Repository | Focus | Research Questions |
|------|------------|-------|-------------------|
| **GPT-Migrate** | [github.com/joshpxyne/gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Framework migration | How does it work? Success rate? Limitations? |
| **Konveyor** | CNCF Project | Kubernetes migration | What analysis does it provide? How does it guide refactoring? |
| **Red Hat MTA** | Red Hat | Containerization | How does it identify migration issues? |
| **TransCoder** | Meta AI | Cross-language translation | What accuracy? Which languages? |

#### Research Tools/Papers

| Tool | Source | Focus |
|------|--------|-------|
| **LLMLift** | Code Metal | Formal verification of LLM outputs |
| **TransCoder** | Meta AI Research | Unsupervised code translation |

### Task 1.2: Try Tools Against Target Project

**Hands-on requirement**: Don't just read about tools—try them!

```bash
# Example: Try GPT-Migrate on a small Odoo module
git clone https://github.com/joshpxyne/gpt-migrate
cd gpt-migrate

# Attempt to migrate odoo/addons/sale/models/sale_order.py
# Document: What worked? What failed? Why?
```

**Deliverable**: Research report with:
- Tool capabilities matrix
- Hands-on experience notes
- Identified gaps (what's missing in existing tools?)

### Task 1.3: Study Enterprise Modernization Patterns

These patterns remain true regardless of AI involvement. AI accelerates them, doesn't replace them.

#### Strangler Fig Pattern

```
┌────────────────────────────────────────────────────────────────┐
│                    STRANGLER FIG PATTERN                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LEGACY MONOLITH          FAÇADE/PROXY          MODERN SERVICES│
│  ┌───────────────┐       ┌──────────┐       ┌────────────────┐ │
│  │               │       │          │       │                │ │
│  │  Module A     │◄──────│  Routes  │───────►  New Service A │ │
│  │  Module B     │◄──────│  Traffic │       │                │ │
│  │  Module C     │       │          │       │  (Replaces A)  │ │
│  │               │       └──────────┘       └────────────────┘ │
│  └───────────────┘                                              │
│                                                                 │
│  Over time: Route more traffic to new services until           │
│  legacy is fully replaced ("strangled")                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Key Resources**:
- [Martin Fowler's Original Article](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)

#### Domain-Driven Design (DDD)

DDD helps identify **bounded contexts** - natural boundaries for migration:

```
LEGACY MONOLITH
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Sales     │  │  Inventory  │  │  Accounting │         │
│  │  Context    │  │   Context   │  │   Context   │         │
│  │             │  │             │  │             │         │
│  │ • Orders    │  │ • Products  │  │ • Invoices  │         │
│  │ • Quotes    │  │ • Stock     │  │ • Payments  │         │
│  │ • Customers │  │ • Warehouse │  │ • Ledger    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  DDD helps identify these contexts for incremental migration │
└─────────────────────────────────────────────────────────────┘
```

**Key Resources**:
- [DDD Practitioners Guide](https://ddd-practitioners.com/)
- Eric Evans' "Domain-Driven Design" book
- [Event Storming](https://www.eventstorming.com/) for domain discovery

#### Anti-Corruption Layer (ACL)

When old and new systems must coexist:

```
NEW SERVICE                ACL                    LEGACY SYSTEM
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│              │    │                 │    │                  │
│  Modern      │───►│  Translates     │───►│  Legacy          │
│  Domain      │    │  Models/APIs    │    │  Database/API    │
│  Model       │◄───│  Between        │◄───│                  │
│              │    │  Worlds         │    │                  │
└──────────────┘    └─────────────────┘    └──────────────────┘
```

---

## Week 2: Build Phase

### Goal: Create Your AI-Powered Modernization Tools

### Task 2.1: Build the Indexing Pipeline

Create tools that understand your target codebase:

```
YOUR TOOL SHOULD PRODUCE:
├── Symbol Index (functions, classes, methods)
├── Call Graph (who calls whom)
├── Dependency Graph (imports, dependencies)
├── Business Rule Catalog (validations, calculations)
├── Domain Boundary Map (bounded contexts)
└── Embedding Store (for semantic search)
```

### Task 2.2: Index Target Module

Select ONE module from your validation project:

| Project | Suggested Module | Size | Complexity |
|---------|-----------------|------|------------|
| **Bahmni** | Clinical Service | ~5K LOC | Medium |
| **ERPNext** | Sales Invoice | ~8K LOC | Medium-High |
| **Odoo** | Sale Module | ~10K LOC | Medium |

### Task 2.3: Generate Understanding Artifacts

Your tools should output:

1. **Domain Overview**: What does this module do?
2. **Entity Map**: Key models and relationships
3. **Workflow Documentation**: How data flows
4. **Business Rules**: Extracted validation/calculation logic
5. **Dependency Report**: What this module depends on

**Deliverable**: Working indexing tool + generated artifacts for target module

---

## Week 3: Migrate Phase

### Goal: Actually Migrate Code Using Your Tools + Cursor AI

### Task 3.1: Plan Migration

Using your understanding artifacts:

```
MIGRATION PLAN TEMPLATE:

Target: [Module name] from [Source language] to [Target language]

Files to migrate:
├── models/sale_order.py → src/models/sale-order.ts
├── models/sale_order_line.py → src/models/sale-order-line.ts
└── ...

Business logic to preserve:
├── Discount calculation (lines 45-89)
├── Tax computation (lines 102-156)
└── Validation rules (lines 200-245)

Test coverage:
├── Existing tests to migrate: 23
├── New tests needed: 12
└── Integration tests: 5
```

### Task 3.2: Migrate with Cursor AI + Your Tools

**Workflow**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUGMENTED MIGRATION WORKFLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. QUERY YOUR TOOLS                                            │
│     "Show me all business rules in SaleOrder.calculate_total()" │
│     → Returns: Discount logic, tax rules, rounding behavior     │
│                                                                  │
│  2. FEED CONTEXT TO CURSOR AI                                   │
│     Paste the extracted business rules into Cursor context      │
│     "Migrate this Python method to TypeScript, preserving       │
│      all business rules documented above"                       │
│                                                                  │
│  3. VERIFY WITH YOUR TOOLS                                      │
│     Run migrated code against test cases                        │
│     Compare behavior with original                              │
│                                                                  │
│  4. ITERATE                                                     │
│     If parity fails, query tools for more context               │
│     Feed additional context to Cursor                           │
│     Repeat until parity achieved                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Task 3.3: Preserve Feature Parity

**Critical requirements**:

| Aspect | Requirement |
|--------|-------------|
| **Business Logic** | All calculations produce identical results |
| **Validation** | Same rules enforced, same error messages |
| **Data Model** | Same fields, relationships preserved |
| **API Surface** | Same inputs/outputs (if applicable) |
| **Edge Cases** | Same behavior for null, empty, boundary values |

### Target Stack

| From | To | Notes |
|------|-----|-------|
| Java | TypeScript | NestJS for services |
| Python | TypeScript | or Go for performance-critical |
| PHP | TypeScript | NestJS ecosystem |

---

## Week 4: Verify & Document Phase

### Goal: Prove It Works and Share Learnings

### Task 4.1: Migrate Tests

```bash
# Original test (Python/pytest)
def test_calculate_total_with_discount():
    order = SaleOrder(customer_id=1)
    order.add_line(product_id=1, quantity=2, unit_price=100)
    order.apply_discount(10)  # 10%
    assert order.total == 180.0

# Migrated test (TypeScript/Vitest)
test('calculate total with discount', () => {
    const order = new SaleOrder({ customerId: 1 });
    order.addLine({ productId: 1, quantity: 2, unitPrice: 100 });
    order.applyDiscount(10);  // 10%
    expect(order.total).toBe(180.0);
});
```

### Task 4.2: Verify Functional Parity

Create parity verification report:

```
PARITY VERIFICATION REPORT
═══════════════════════════════════════════════════════════════

Module: Odoo Sale Order → TypeScript SaleOrder
Date: 2025-01-15
Intern: [Your Name]

TEST RESULTS:
├── Unit Tests: 45/47 passing (95.7%)
├── Integration Tests: 12/12 passing (100%)
└── Edge Cases: 8/10 passing (80%)

FAILING TESTS:
├── test_currency_rounding: Floating point precision issue
│   └── Fix: Use decimal.js library
└── test_multi_company: Not implemented (out of scope)

BUSINESS LOGIC VERIFICATION:
├── Discount Calculation: ✅ Identical
├── Tax Computation: ✅ Identical
├── Line Total: ✅ Identical
├── Order Total: ✅ Identical
└── Stock Reservation: ⚠️ Not migrated (dependency)

PERFORMANCE:
├── Original (Python): 45ms avg
└── Migrated (TypeScript): 12ms avg (73% faster)
```

### Task 4.3: Document & Share

**Deliverables**:

1. **Technical Report**: What you built, how it works, results
2. **Blog Post**: Shareable article about your approach
3. **Demo Video**: 5-10 minute walkthrough
4. **Code Repository**: Clean, documented, tested code

---

## Success Criteria

### Minimum Bar (Pass)

- [ ] Researched 5+ existing tools with documented findings
- [ ] Built working indexing/analysis tool
- [ ] Migrated 1 module (at least 50% of files)
- [ ] 70%+ test pass rate on migrated code
- [ ] Basic documentation complete

### Exceeds Expectations

- [ ] Comprehensive tool comparison report
- [ ] Full module migration with 90%+ test pass rate
- [ ] Published blog post
- [ ] Demo presentation delivered
- [ ] Novel insight or technique documented

### Outstanding

- [ ] Tool demonstrates capability beyond existing solutions
- [ ] Migration completed with no known defects
- [ ] Contribution upstream (PR to open source project)
- [ ] Research-quality findings

---

## AI Accelerates, Doesn't Replace

Remember: **AI tools accelerate developer learning and execution**. They don't replace:

| AI Accelerates | Human Still Required |
|---------------|---------------------|
| Code analysis | Architectural decisions |
| Pattern detection | Business prioritization |
| Documentation generation | Stakeholder communication |
| Test generation | Edge case identification |
| Translation suggestions | Verification of correctness |

Enterprise modernization patterns (DDD, Strangler Fig, ACL) remain essential. AI helps you execute faster and with more confidence.

---

## Related

- [AI Internship Overview](../README.md)
- [Existing Tools Landscape](../03-Market-Research/01-Existing-Tools-Research.md)
- [Target Projects](../04-Target-Projects/05-Validation-Projects.md)
- [Your Role in PearlThoughts](./01-Organizational-Context.md)

---

*Last Updated: 2025-01-12*
