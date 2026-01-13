# Strategic Design

> **The big picture**: How to divide a system into manageable pieces

---

## What Is Strategic Design?

Strategic design is about **boundaries** and **relationships** at the macro level.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    STRATEGIC vs TACTICAL                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STRATEGIC DESIGN (This note)                                           │
│  └── Where to draw boundaries                                           │
│  └── How bounded contexts relate                                        │
│  └── Which parts to modernize first                                     │
│  └── Team organization                                                  │
│                                                                          │
│  TACTICAL DESIGN (Next note)                                            │
│  └── How to model inside a boundary                                     │
│  └── Entities, Value Objects, Aggregates                                │
│  └── Domain Events, Repositories                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### 1. Bounded Contexts

A boundary within which a model is consistent.

```mermaid
graph TB
    subgraph "Sales Context"
        SC_Customer[Customer]
        SC_Order[Order]
        SC_Product[Product]
    end

    subgraph "Shipping Context"
        SH_Shipment[Shipment]
        SH_Address[Address]
        SH_Package[Package]
    end

    subgraph "Billing Context"
        B_Invoice[Invoice]
        B_Payment[Payment]
        B_Customer[Customer]
    end

    SC_Order -.->|"Order Placed"| SH_Shipment
    SC_Order -.->|"Order Placed"| B_Invoice
```

**Key insight**: `Customer` means different things in different contexts:
- **Sales**: Contact info, preferences, purchase history
- **Billing**: Payment methods, credit limit, billing address
- **Shipping**: Delivery address, delivery preferences

### 2. Ubiquitous Language

Each context has its own vocabulary.

| Term | Sales Context | Shipping Context | Billing Context |
|------|---------------|------------------|-----------------|
| **Customer** | Person who buys | Recipient | Account holder |
| **Address** | Contact address | Delivery location | Billing address |
| **Order** | Purchase request | Shipment source | Invoice basis |
| **Item** | Product selected | Package contents | Line item |

**Why this matters for modernization**: When you see `Customer` in legacy code, you need to know WHICH customer concept it represents.

### 3. Context Mapping

How bounded contexts relate to each other.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONTEXT RELATIONSHIPS                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PARTNERSHIP                                                            │
│  └── Two teams coordinate, mutual dependency                            │
│  └── Example: Sales and Inventory coordinate on stock levels            │
│                                                                          │
│  CUSTOMER-SUPPLIER                                                      │
│  └── Upstream (supplier) provides, downstream (customer) consumes       │
│  └── Example: Product Catalog (upstream) → Sales (downstream)           │
│                                                                          │
│  CONFORMIST                                                             │
│  └── Downstream conforms to upstream's model, no negotiation            │
│  └── Example: Your system conforms to Stripe's payment API              │
│                                                                          │
│  ANTI-CORRUPTION LAYER (ACL)                                            │
│  └── Downstream translates upstream's model to protect itself           │
│  └── Example: Translate legacy ERP data to clean domain model           │
│                                                                          │
│  OPEN HOST SERVICE                                                      │
│  └── Upstream provides a well-defined protocol for many consumers       │
│  └── Example: REST API that multiple systems consume                    │
│                                                                          │
│  PUBLISHED LANGUAGE                                                     │
│  └── Shared language for exchange (JSON schemas, protobuf)              │
│  └── Example: FHIR for healthcare data exchange                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Context Map Patterns

### Partnership

```mermaid
graph LR
    subgraph "Sales Team"
        Sales[Sales Context]
    end

    subgraph "Inventory Team"
        Inv[Inventory Context]
    end

    Sales <-->|"Coordinate"| Inv
```

Both teams must coordinate changes. Neither can change without the other.

### Customer-Supplier

```mermaid
graph LR
    subgraph "Upstream (Supplier)"
        Cat[Product Catalog]
    end

    subgraph "Downstream (Customer)"
        Sales[Sales Context]
    end

    Cat -->|"Provides Products"| Sales
```

Catalog team provides data. Sales team requests features but catalog team decides.

### Anti-Corruption Layer

```mermaid
graph LR
    subgraph "Legacy System"
        Legacy[Old ERP]
    end

    subgraph "Your System"
        ACL[Anti-Corruption Layer]
        Domain[Clean Domain Model]
    end

    Legacy -->|"Messy Data"| ACL
    ACL -->|"Clean Model"| Domain
```

**This is critical for modernization!** The ACL translates legacy concepts to clean ones.

---

## Identifying Bounded Contexts

### Clues in Legacy Code

| Clue | What It Suggests |
|------|------------------|
| **Separate databases/schemas** | Likely separate contexts |
| **Different teams own different code** | Team boundaries often match contexts |
| **Same term, different meaning** | Context boundary |
| **Separate deployment units** | Likely separate contexts |
| **Integration points** | Boundaries between contexts |

### Process for Discovery

```
Step 1: List all the "nouns" in the system
        Customer, Order, Product, Invoice, Shipment, etc.

Step 2: Group nouns that are always used together
        {Order, OrderLine, Cart} — always together
        {Invoice, Payment, Receipt} — always together

Step 3: Find nouns that appear in multiple groups with different meanings
        Customer in {Sales} vs Customer in {Billing}
        → These are different contexts

Step 4: Draw boundaries around groups
        → Each group is a candidate bounded context

Step 5: Validate with business stakeholders
        → Do these boundaries make sense?
```

### Example: ERPNext Discovery

```mermaid
graph TB
    subgraph "Accounts Context"
        GL[General Ledger]
        JE[Journal Entry]
        Account[Account]
    end

    subgraph "Sales Context"
        SO[Sales Order]
        SI[Sales Invoice]
        Customer[Customer]
    end

    subgraph "Inventory Context"
        Item[Item]
        Stock[Stock Entry]
        Warehouse[Warehouse]
    end

    subgraph "HR Context"
        Employee[Employee]
        Payroll[Payroll Entry]
        Leave[Leave Application]
    end

    SI -->|"Creates"| JE
    SO -->|"Reserves"| Stock
```

---

## Subdomains

Not all parts of a system are equally important.

### Types of Subdomains

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SUBDOMAIN TYPES                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CORE DOMAIN                                                            │
│  └── What makes the business unique                                     │
│  └── Competitive advantage                                              │
│  └── Worth investing heavily in                                         │
│  └── Example: Lab testing workflow in OpenElis                          │
│                                                                          │
│  SUPPORTING SUBDOMAIN                                                   │
│  └── Necessary but not unique                                           │
│  └── Custom to business but not differentiating                         │
│  └── Worth building, but don't over-engineer                            │
│  └── Example: Sample tracking in OpenElis                               │
│                                                                          │
│  GENERIC SUBDOMAIN                                                      │
│  └── Same for everyone                                                  │
│  └── Buy or use open source                                             │
│  └── Don't build yourself                                               │
│  └── Example: User authentication, email sending                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Why This Matters for Modernization

| Subdomain Type | Modernization Priority | Approach |
|----------------|------------------------|----------|
| **Core** | HIGH | Careful, incremental, test heavily |
| **Supporting** | MEDIUM | Can be more aggressive |
| **Generic** | LOW | Replace with off-the-shelf |

---

## Context Mapping Diagram

A complete view of how contexts relate.

```mermaid
graph TB
    subgraph "Core Domain"
        Lab[Lab Testing]
    end

    subgraph "Supporting"
        Sample[Sample Tracking]
        Report[Reporting]
    end

    subgraph "Generic"
        Auth[Authentication]
        Audit[Audit Log]
    end

    subgraph "External"
        FHIR[FHIR API]
        Printer[Label Printer]
    end

    Lab -->|"ACL"| FHIR
    Lab -->|"Partnership"| Sample
    Lab -->|"Customer-Supplier"| Report
    Sample -->|"Conformist"| Printer
    Auth -.->|"Generic"| Lab
    Auth -.->|"Generic"| Sample
```

---

## Applying to Legacy Modernization

### Step 1: Draw the Current State

Before modernizing, understand what exists:

```mermaid
graph TB
    subgraph "Legacy Monolith"
        Everything[All Code Together]
        DB[(Single Database)]
    end

    Everything --> DB
```

### Step 2: Identify Hidden Contexts

Look for natural seams in the monolith:

```mermaid
graph TB
    subgraph "Legacy Monolith"
        subgraph "Hidden: Sales"
            S1[order_*.py]
            S2[customer_*.py]
        end
        subgraph "Hidden: Inventory"
            I1[stock_*.py]
            I2[warehouse_*.py]
        end
        subgraph "Hidden: Accounts"
            A1[invoice_*.py]
            A2[payment_*.py]
        end
    end
```

### Step 3: Plan Target State

Design where you want to end up:

```mermaid
graph TB
    subgraph "Sales Service"
        Sales[Sales API]
        SalesDB[(Sales DB)]
    end

    subgraph "Inventory Service"
        Inv[Inventory API]
        InvDB[(Inventory DB)]
    end

    subgraph "Accounts Service"
        Acc[Accounts API]
        AccDB[(Accounts DB)]
    end

    Sales --> SalesDB
    Inv --> InvDB
    Acc --> AccDB

    Sales -.->|"Events"| Inv
    Sales -.->|"Events"| Acc
```

### Step 4: Define the ACL

The translation layer between old and new:

```python
# Anti-Corruption Layer Example

class LegacyOrderAdapter:
    """Translates legacy order data to clean domain model."""

    def to_domain(self, legacy_order: dict) -> Order:
        """Convert legacy format to domain model."""
        return Order(
            id=OrderId(legacy_order['ORDER_NUM']),  # Legacy uses ORDER_NUM
            customer=self._map_customer(legacy_order['CUST_CODE']),
            items=self._map_items(legacy_order['LINES']),
            status=self._map_status(legacy_order['STAT'])  # Legacy uses codes
        )

    def _map_status(self, legacy_code: str) -> OrderStatus:
        """Translate legacy status codes to domain status."""
        mapping = {
            'N': OrderStatus.NEW,
            'P': OrderStatus.PROCESSING,
            'S': OrderStatus.SHIPPED,
            'C': OrderStatus.COMPLETED,
            'X': OrderStatus.CANCELLED,
        }
        return mapping.get(legacy_code, OrderStatus.UNKNOWN)
```

---

## Key Takeaways

1. **Bounded Contexts** define where models are consistent
2. **Ubiquitous Language** differs between contexts
3. **Context Mapping** shows how contexts relate
4. **Subdomains** tell you where to invest effort
5. **ACL** protects new code from legacy mess
6. **Discovery** before design — understand what exists

---

## For Your Week-1 Project

When analyzing your target codebase:

1. **List the major "nouns"** (entities) you find
2. **Group them** by which ones are used together
3. **Identify where terms have different meanings**
4. **Draw a rough context map**
5. **Classify each area** as Core/Supporting/Generic

---

## Related

- [Bounded Contexts Deep Dive](./02-Bounded-Contexts.md)
- [Tactical Patterns](./04-Tactical-Patterns.md)
- [Applied to ERPNext/Bahmni/OpenElis](./05-Applied-To-Projects.md)
- [Why DDD Matters](./01-Why-DDD-Matters.md)
