# Validation Projects

## Proving Our Tools Work on Real Enterprise Systems

> *We don't just build tools - we validate them by modernizing actual open-source enterprise systems.*

---

## Why Validation Matters

Building AI tools for code intelligence is one thing. **Proving they work on real enterprise complexity** is another entirely. Our validation approach:

1. **Select challenging systems** - Not toy projects, but real enterprise software
2. **Apply our tools** - Index, analyze, and understand the codebase
3. **Measure outcomes** - Did we find what we expected? Did we miss anything?
4. **Actually modernize** - Migrate a subset to prove end-to-end value

---

## Project 1: Bahmni (Healthcare Platform)

### Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | [github.com/Bahmni/bahmni-core](https://github.com/Bahmni/bahmni-core) |
| **Stack** | Java, Spring, Hibernate, MySQL |
| **Base Platform** | OpenMRS (medical records system) |
| **Domain** | Hospital Management, Electronic Medical Records |
| **Size** | ~500K lines of code |
| **Active Users** | 40+ countries, primarily low-resource settings |

### Why Bahmni?

Bahmni represents **healthcare domain complexity** - one of the most challenging domains for modernization:

- **Regulatory compliance** - HIPAA-like requirements in various countries
- **Data sensitivity** - Patient records, clinical observations
- **Complex workflows** - Registration → Consultation → Diagnosis → Treatment → Billing
- **Integration heavy** - Lab systems, pharmacy, radiology, billing

### Domain Model Highlights

```
Patient
├── Person (demographics)
├── PatientIdentifier (MRN, national ID)
├── Encounter (visits)
│   ├── Observation (vitals, symptoms)
│   ├── Diagnosis
│   ├── Order (lab, medication, procedure)
│   └── Note
├── Program (HIV, TB, maternal health)
└── Appointment
```

### Validation Tasks

| Task | Description | Measure |
|------|-------------|---------|
| **Index Core Module** | Parse bahmni-core Java codebase | Symbol coverage, relationship accuracy |
| **Extract Patient Flow** | Trace patient registration to discharge | Path completeness |
| **Identify Business Rules** | Find validation and compliance logic | Rule count vs manual audit |
| **Map OpenMRS Extensions** | Understand customizations | Extension point coverage |
| **Migration Candidate** | Select one service for modernization | Feasibility assessment |

### Suggested Module for Migration

**Clinical Service** (`bahmni-clinical/`)
- Patient encounter management
- Observation recording
- Diagnosis capture
- Moderate complexity, well-bounded

---

## Project 2: ERPNext (Enterprise Resource Planning)

### Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | [github.com/frappe/erpnext](https://github.com/frappe/erpnext) |
| **Stack** | Python, Frappe Framework, MariaDB, JavaScript |
| **Domain** | Full ERP (Accounting, Inventory, HR, Manufacturing, CRM) |
| **Size** | ~1M lines of code |
| **Active Users** | Thousands of businesses worldwide |

### Why ERPNext?

ERPNext is a **complete business system** - it covers every aspect of running a company:

- **Financial complexity** - Double-entry accounting, multi-currency, tax compliance
- **Inventory management** - Stock levels, warehouses, batch/serial tracking
- **Manufacturing** - BOM, work orders, production planning
- **Human Resources** - Payroll, leave, recruitment, performance

### Domain Model Highlights

```
Company
├── Accounting
│   ├── Account (chart of accounts)
│   ├── Journal Entry
│   ├── Payment Entry
│   └── Tax Template
├── Stock
│   ├── Item (products, services)
│   ├── Warehouse
│   ├── Stock Entry
│   └── Stock Ledger Entry
├── Selling
│   ├── Customer
│   ├── Quotation
│   ├── Sales Order
│   └── Sales Invoice
├── Buying
│   ├── Supplier
│   ├── Purchase Order
│   └── Purchase Invoice
└── HR
    ├── Employee
    ├── Salary Structure
    └── Leave Application
```

### Validation Tasks

| Task | Description | Measure |
|------|-------------|---------|
| **Index Accounting Module** | Parse erpnext/accounts | Symbol extraction accuracy |
| **Trace Invoice Flow** | Quotation → Order → Invoice → Payment | Workflow completeness |
| **Extract Validation Rules** | Find all doctype validations | Rule count vs documented |
| **Discover Bounded Contexts** | Auto-identify module boundaries | Match vs actual structure |
| **Map Report Queries** | Understand reporting logic | Query coverage |

### Suggested Module for Migration

**Accounts Receivable** (`erpnext/accounts/doctype/sales_invoice/`)
- Customer invoicing workflow
- Payment matching
- Clear boundaries with other modules
- Well-documented business rules

---

## Project 3: Odoo Modules (Modular ERP)

### Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | [github.com/odoo/odoo](https://github.com/odoo/odoo/tree/19.0/addons) |
| **Stack** | Python, PostgreSQL, JavaScript (OWL framework) |
| **Domain** | Modular Business Applications |
| **Size** | ~2M lines across all modules |
| **Active Users** | 7M+ users, enterprise standard |

### Why Odoo?

Odoo demonstrates **modular architecture at scale** - how to organize a massive system:

- **Clear module boundaries** - Each app is a separate module
- **Inheritance patterns** - Models extend base with `_inherit`
- **Dependency management** - Explicit module dependencies
- **Plugin architecture** - Third-party modules extend core

### Module Structure

```
odoo/addons/
├── sale/                    # Sales Management
│   ├── models/
│   │   ├── sale_order.py
│   │   └── sale_order_line.py
│   ├── views/
│   └── data/
├── stock/                   # Inventory Management
│   ├── models/
│   │   ├── stock_move.py
│   │   └── stock_picking.py
│   └── ...
├── account/                 # Accounting
│   ├── models/
│   │   ├── account_move.py
│   │   └── account_payment.py
│   └── ...
├── hr/                      # Human Resources
├── mrp/                     # Manufacturing
└── crm/                     # Customer Relationship
```

### Validation Tasks

| Task | Description | Measure |
|------|-------------|---------|
| **Index Sale Module** | Parse sale/ completely | Model/method coverage |
| **Map Model Inheritance** | Track `_inherit` chains | Inheritance graph accuracy |
| **Extract ORM Relations** | Find One2many, Many2many | Relation completeness |
| **Discover Dependencies** | Build module dependency graph | Match vs `__manifest__.py` |
| **Trace Sale-to-Stock** | Follow sale order to delivery | Cross-module flow accuracy |

### Suggested Module for Migration

**Sale Module** (`addons/sale/`)
- Core sales order management
- Clear relationships (customer, product, invoice)
- Well-documented ORM patterns
- Good size for internship scope

---

## Validation Metrics

### Indexing Quality

| Metric | Target | How We Measure |
|--------|--------|----------------|
| **Symbol Coverage** | >95% | Functions, classes, methods indexed vs total |
| **Relationship Accuracy** | >90% | Call graph edges correct vs actual |
| **Chunk Quality** | >85% | Semantic boundaries preserved |

### Understanding Quality

| Metric | Target | How We Measure |
|--------|--------|----------------|
| **Query Precision** | >80% | Relevant results in top-5 |
| **Answer Accuracy** | >75% | LLM answers validated against docs |
| **Business Rule Recall** | >70% | Rules found vs manual audit |

### Migration Quality

| Metric | Target | How We Measure |
|--------|--------|----------------|
| **Feature Parity** | >90% | Migrated functionality matches original |
| **Test Pass Rate** | >85% | Original tests passing on new code |
| **Time Savings** | >50% | Compared to manual migration estimate |

---

## Getting Started

### Week 1: Setup & Familiarization

```bash
# Clone validation projects
git clone https://github.com/Bahmni/bahmni-core
git clone https://github.com/frappe/erpnext
git clone https://github.com/odoo/odoo --branch 19.0 --depth 1

# Explore structure
find bahmni-core -name "*.java" | wc -l
find erpnext -name "*.py" | wc -l
find odoo/addons/sale -name "*.py" | wc -l
```

### Week 2: Initial Indexing

Apply our tools to one module from your chosen project. Measure:
- How many symbols were extracted?
- How accurate is the call graph?
- Can we answer basic questions about the code?

### Week 3+: Deep Validation

Progress through the validation tasks for your chosen project. Document findings, measure metrics, identify gaps in our tools.

---

## Related

- [[Index|AI Internship Overview]]
- [[../Programme-Structure/Weekly-Plans|Weekly Plans]]
- [[../Support/Mentors|Mentors]]

---

*Last Updated: 2025-01-12*
