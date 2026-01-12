# Real-World Legacy Examples

> **Context matters**: Understanding why systems become legacy

---

## Famous Legacy Systems

### 1. COBOL in Banking

**The situation:**
- Written in 1960s-1980s
- Processes $3 trillion daily
- 95% of ATM transactions
- 80% of in-person transactions

**Why it's still running:**
- Works reliably for 40+ years
- Mission-critical (can't afford downtime)
- Nobody understands it well enough to replace safely
- Rewrite attempts have failed

**The challenge:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COBOL IN BANKING                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  • 220 billion lines of COBOL still in production                       │
│  • Average COBOL programmer age: 55+                                     │
│  • Average system age: 30+ years                                        │
│  • Failed modernization projects: Many                                   │
│                                                                          │
│  The code contains:                                                     │
│  • Decades of regulatory compliance logic                               │
│  • Thousands of edge cases discovered in production                     │
│  • Business rules that exist nowhere else                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Healthcare Systems

**The situation:**
- Many hospitals run 20+ year old systems
- HL7 v2 messages (1988 standard) still dominant
- Patient data across multiple incompatible systems
- Regulatory requirements (HIPAA) make changes risky

**Why modernization is hard:**
- Patient safety (bugs could kill people)
- Data migration risk (losing patient history)
- Regulatory compliance (every change needs validation)
- 24/7 availability requirements

**Real example: NHS (UK)**
```
2002: Started £12.7 billion NPfIT project
2011: Abandoned after £10 billion spent
Reason: Too complex, too many stakeholders,
        underestimated existing system complexity
```

---

### 3. Airlines Reservation Systems

**The situation:**
- SABRE (American Airlines) - started 1960
- Still processes 1 million+ transactions per second
- Powers most airline booking worldwide
- Written in assembly language, later TPF

**Why it persists:**
- Handles massive scale reliably
- Integration with thousands of partners
- Switching cost is enormous
- "If it ain't broke..."

**The complexity:**
```
Every booking touches:
• Seat inventory (real-time)
• Pricing rules (thousands)
• Frequent flyer calculations
• Interline agreements
• Regulatory requirements (per country)
• Partner airline integration
• Payment processing
• Refund/change rules

All in milliseconds. All reliable.
```

---

## What These Examples Teach Us

### 1. Legacy ≠ Bad

These systems:
- Process billions of dollars
- Serve millions of users
- Run 24/7 for decades
- Are incredibly reliable

The **code quality** may be poor by modern standards, but the **business value** is enormous.

### 2. The Knowledge Is Irreplaceable

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WHERE THE KNOWLEDGE LIVES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Documentation:  "Calculate tax per regulations"                        │
│                                                                          │
│  Code:           if (state == "CA" && product_type == "food" &&         │
│                      not(is_hot_prepared) && not(sold_with_utensils) && │
│                      not(sold_for_consumption_on_premises)) {           │
│                      tax_rate = 0;                                       │
│                  } else if (state == "CA" && product_type == "food") {  │
│                      tax_rate = sales_tax_rate;                         │
│                  }                                                       │
│                  // 500 more lines of state-specific rules...           │
│                                                                          │
│  The code IS the documentation.                                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Big Bang Rewrites Fail

| Company | Project | Outcome |
|---------|---------|---------|
| NHS (UK) | NPfIT | Abandoned after £10B |
| FBI | Virtual Case File | Scrapped after $170M |
| California | SACSS welfare system | $500M over budget |
| Many startups | "Rewrite v2" | Company died |

**Pattern**: Underestimate legacy complexity, overestimate new system timeline.

### 4. Incremental Works

| Company | Approach | Outcome |
|---------|----------|---------|
| Amazon | Strangler fig over 10+ years | Success |
| Netflix | Gradual cloud migration | Success |
| Spotify | Squad-based incremental | Success |

**Pattern**: Small changes, continuous delivery, feature flags.

---

## The Target Systems You'll Analyze

### ERPNext

**What it represents:**
- Modern open-source ERP
- Frappe framework patterns
- Well-documented business logic
- Clear module boundaries

**Learning opportunity:**
- How modern enterprise software is structured
- DocType patterns for business entities
- Event-driven business logic

### OpenElis / Bahmni

**What they represent:**
- Real healthcare systems in production
- Lab and clinical workflows
- Regulatory compliance requirements
- Integration challenges (HL7, FHIR)

**Learning opportunity:**
- Healthcare domain complexity
- Why some code is hard to change
- Technical debt patterns

---

## Patterns You'll Recognize

### The God Class

One class that does everything:

```java
// 5000+ lines, 200+ methods
public class OrderManager {
    public void createOrder() { ... }
    public void calculateTax() { ... }
    public void sendEmail() { ... }
    public void updateInventory() { ... }
    public void processPayment() { ... }
    public void generateReport() { ... }
    // ... 194 more methods
}
```

### The Distributed Monolith

Microservices that share a database:

```
Service A ─┐
Service B ─┼──► Shared Database ◄──┼─ Service D
Service C ─┘                       └─ Service E

"Microservices" that can't deploy independently
```

### The Integration Nightmare

Multiple systems connected with point-to-point integrations:

```
System A ───────► System B
    │                │
    ▼                ▼
System C ◄─────► System D ───► System E
    │                │              │
    └────────────────┴──────────────┘

Change one system = test all integrations
```

### The Documentation Lie

```
README: "See docs/ folder for API documentation"
docs/: Last updated 3 years ago
Code: Completely different from docs
```

---

## Why AI Tools Help

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE OPPORTUNITY                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WHAT HUMANS DO NOW:                                                    │
│  • Read code for days/weeks                                             │
│  • Ask colleagues (who may have left)                                   │
│  • Guess based on variable names                                        │
│  • Trial and error                                                      │
│                                                                          │
│  WHAT AI COULD DO:                                                      │
│  • Index codebase in minutes                                            │
│  • Answer "how does X work?" instantly                                  │
│  • Show impact of changes                                               │
│  • Extract business rules automatically                                 │
│  • Track what's been migrated                                           │
│                                                                          │
│  YOU'RE BUILDING TOOLS FOR THIS.                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Legacy systems run the world** - Banking, healthcare, airlines
2. **The value is in the knowledge** - Business rules in code
3. **Big rewrites fail** - Incremental is the way
4. **Complexity is underestimated** - Always
5. **AI can help** - That's why you're here

---

## Related

- [What Is Legacy Code?](./01-What-Is-Legacy.md)
- [Why Modernize?](./02-Why-Modernize.md)
- [Terminology Glossary](./04-Terminology-Glossary.md)
- [What Is Code Intelligence?](../06-Code-Intelligence/01-What-Is-Code-Intelligence.md)
