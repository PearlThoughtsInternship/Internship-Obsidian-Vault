# Tactical Patterns

> **Inside the boundary**: How to model domain concepts in code

---

## What Are Tactical Patterns?

Tactical patterns are **coding patterns** for implementing domain models.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE BUILDING BLOCKS                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ENTITIES          → Things with identity that change over time         │
│  VALUE OBJECTS     → Things defined by their attributes, immutable      │
│  AGGREGATES        → Cluster of entities with a root                    │
│  DOMAIN EVENTS     → Something that happened in the domain              │
│  REPOSITORIES      → How you get/store aggregates                       │
│  DOMAIN SERVICES   → Operations that don't belong to one entity         │
│  FACTORIES         → Complex object creation                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Entities

Things with **identity** that persist through time.

### Characteristics

- Has a unique ID
- Can change attributes but stays "the same thing"
- Two entities with same ID are the same entity
- Two entities with same attributes but different IDs are different

### Example

```typescript
// Entity: Order
class Order {
  readonly id: OrderId;        // Identity - never changes
  private status: OrderStatus; // Can change
  private items: OrderItem[];  // Can change
  private total: Money;        // Can change

  constructor(id: OrderId) {
    this.id = id;
    this.status = OrderStatus.Draft;
    this.items = [];
    this.total = Money.zero();
  }

  addItem(item: OrderItem): void {
    this.items.push(item);
    this.recalculateTotal();
  }

  submit(): void {
    if (this.items.length === 0) {
      throw new Error("Cannot submit empty order");
    }
    this.status = OrderStatus.Submitted;
  }

  // Identity comparison
  equals(other: Order): boolean {
    return this.id.equals(other.id);
  }
}
```

### How to Recognize Entities in Legacy Code

| Clue | Example |
|------|---------|
| Has ID field | `order_id`, `customer_id` |
| Stored in database with primary key | `orders` table |
| Referenced by ID | `customer_id` foreign key |
| Has lifecycle | Created → Updated → Deleted |
| Business talks about "the same X" | "the same order" |

---

## 2. Value Objects

Things defined **only by their attributes**. No identity.

### Characteristics

- Defined entirely by attributes
- Immutable (never changes)
- Two value objects with same attributes are equal
- Replaceable — you don't update, you replace

### Example

```typescript
// Value Object: Money
class Money {
  readonly amount: number;
  readonly currency: string;

  constructor(amount: number, currency: string) {
    this.amount = amount;
    this.currency = currency;
    Object.freeze(this); // Immutable
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error("Cannot add different currencies");
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  // Attribute comparison
  equals(other: Money): boolean {
    return this.amount === other.amount &&
           this.currency === other.currency;
  }

  static zero(): Money {
    return new Money(0, 'USD');
  }
}

// Value Object: Address
class Address {
  readonly street: string;
  readonly city: string;
  readonly country: string;
  readonly postalCode: string;

  constructor(street: string, city: string, country: string, postalCode: string) {
    this.street = street;
    this.city = city;
    this.country = country;
    this.postalCode = postalCode;
    Object.freeze(this);
  }

  equals(other: Address): boolean {
    return this.street === other.street &&
           this.city === other.city &&
           this.country === other.country &&
           this.postalCode === other.postalCode;
  }
}
```

### How to Recognize Value Objects in Legacy Code

| Clue | Example |
|------|---------|
| No ID field | Just `amount`, `currency` |
| Embedded in entity | `order.billing_address` |
| Compared by value | "same address" = same values |
| Business doesn't track individually | "a $50 payment" not "payment #123" |

---

## 3. Aggregates

A cluster of entities and value objects treated as a **single unit**.

### Characteristics

- Has a **root entity** (the Aggregate Root)
- External code only references the root
- All changes go through the root
- Consistency boundary — everything inside is consistent

### Example

```typescript
// Aggregate: Order (root) + OrderLines (children)
class Order {  // Aggregate Root
  readonly id: OrderId;
  private lines: OrderLine[] = [];  // Children
  private status: OrderStatus;

  // External code adds lines through the root
  addLine(productId: ProductId, quantity: number, price: Money): void {
    const line = new OrderLine(
      OrderLineId.generate(),
      productId,
      quantity,
      price
    );
    this.lines.push(line);
  }

  // Can't access lines directly — go through root
  getLines(): readonly OrderLine[] {
    return [...this.lines];  // Return copy
  }

  // Business rules enforced at aggregate level
  submit(): void {
    if (this.lines.length === 0) {
      throw new Error("Order must have at least one line");
    }
    if (this.total().amount > 10000) {
      throw new Error("Orders over $10,000 require approval");
    }
    this.status = OrderStatus.Submitted;
  }

  total(): Money {
    return this.lines.reduce(
      (sum, line) => sum.add(line.subtotal()),
      Money.zero()
    );
  }
}

class OrderLine {  // Not an Aggregate Root — accessed via Order
  readonly id: OrderLineId;
  readonly productId: ProductId;
  readonly quantity: number;
  readonly price: Money;

  subtotal(): Money {
    return new Money(this.price.amount * this.quantity, this.price.currency);
  }
}
```

### Aggregate Design Rules

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGGREGATE RULES                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Reference other aggregates by ID only                               │
│     ✓ order.customerId = customer.id                                    │
│     ✗ order.customer = customer (object reference)                      │
│                                                                          │
│  2. One aggregate = one transaction                                     │
│     ✓ Save entire Order with all lines in one transaction               │
│     ✗ Save Order and Customer in same transaction                       │
│                                                                          │
│  3. Keep aggregates small                                               │
│     ✓ Order with lines                                                  │
│     ✗ Customer with orders with lines with products...                  │
│                                                                          │
│  4. External changes through root only                                  │
│     ✓ order.addLine(...)                                                │
│     ✗ order.lines.push(...)                                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### How to Identify Aggregates in Legacy Code

| Pattern | Likely Aggregate |
|---------|------------------|
| Parent-child tables | Parent is root, children are inside |
| Cascade delete | Everything deleted together is one aggregate |
| Loaded together | What's always fetched together |
| Validated together | What must be consistent together |

---

## 4. Domain Events

Something that **happened** in the domain.

### Characteristics

- Past tense name (OrderPlaced, PaymentReceived)
- Immutable record of what happened
- Contains all data needed to understand what happened
- Used for communication between aggregates/contexts

### Example

```typescript
// Domain Event
class OrderPlaced {
  readonly eventId: string;
  readonly occurredAt: Date;
  readonly orderId: OrderId;
  readonly customerId: CustomerId;
  readonly total: Money;
  readonly items: ReadonlyArray<{
    productId: ProductId;
    quantity: number;
  }>;

  constructor(order: Order) {
    this.eventId = generateId();
    this.occurredAt = new Date();
    this.orderId = order.id;
    this.customerId = order.customerId;
    this.total = order.total();
    this.items = order.getLines().map(l => ({
      productId: l.productId,
      quantity: l.quantity
    }));
    Object.freeze(this);
  }
}

// Using events
class Order {
  private events: DomainEvent[] = [];

  submit(): void {
    // ... validation ...
    this.status = OrderStatus.Submitted;
    this.events.push(new OrderPlaced(this));
  }

  pullEvents(): DomainEvent[] {
    const events = [...this.events];
    this.events = [];
    return events;
  }
}
```

### Why Events Matter for Modernization

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EVENTS IN MODERNIZATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LEGACY (Direct Coupling):                                              │
│  OrderService.submit() {                                                │
│    save(order);                                                         │
│    inventoryService.reserve(order);    // Direct call                   │
│    emailService.sendConfirmation();    // Direct call                   │
│    analyticsService.track(order);      // Direct call                   │
│  }                                                                       │
│                                                                          │
│  MODERN (Event-Driven):                                                 │
│  OrderService.submit() {                                                │
│    save(order);                                                         │
│    publish(new OrderPlaced(order));    // Just publish                  │
│  }                                                                       │
│                                                                          │
│  // Other services listen independently                                 │
│  InventoryService.on(OrderPlaced, e => reserve(e.items));              │
│  EmailService.on(OrderPlaced, e => sendConfirmation(e.customerId));    │
│                                                                          │
│  Benefits: Decoupling, easier testing, can add listeners without        │
│  changing the order service.                                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Repositories

How you **retrieve and store** aggregates.

### Characteristics

- One repository per aggregate type
- Looks like an in-memory collection
- Hides persistence details
- Only loads aggregate roots

### Example

```typescript
// Repository Interface (Domain layer)
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  save(order: Order): Promise<void>;
  delete(order: Order): Promise<void>;
}

// Implementation (Infrastructure layer)
class PostgresOrderRepository implements OrderRepository {
  constructor(private db: Database) {}

  async findById(id: OrderId): Promise<Order | null> {
    const row = await this.db.query(
      'SELECT * FROM orders WHERE id = $1',
      [id.value]
    );
    if (!row) return null;

    const lines = await this.db.query(
      'SELECT * FROM order_lines WHERE order_id = $1',
      [id.value]
    );

    return this.toOrder(row, lines);
  }

  async save(order: Order): Promise<void> {
    await this.db.transaction(async (tx) => {
      await tx.query(
        'INSERT INTO orders (id, customer_id, status, total) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET ...',
        [order.id.value, order.customerId.value, order.status, order.total().amount]
      );

      for (const line of order.getLines()) {
        await tx.query(
          'INSERT INTO order_lines (id, order_id, product_id, quantity, price) VALUES ...',
          [line.id.value, order.id.value, line.productId.value, line.quantity, line.price.amount]
        );
      }
    });
  }

  private toOrder(row: any, lines: any[]): Order {
    // Reconstitute the aggregate from database rows
    const order = new Order(new OrderId(row.id));
    // ... populate from row and lines ...
    return order;
  }
}
```

---

## 6. Domain Services

Operations that don't belong to a single entity.

### When to Use

- Operation involves multiple aggregates
- Operation doesn't naturally fit in any entity
- Complex business logic that spans entities

### Example

```typescript
// Domain Service: Pricing
class PricingService {
  calculateOrderTotal(
    order: Order,
    customer: Customer,
    promotions: Promotion[]
  ): Money {
    let total = order.subtotal();

    // Apply customer discount
    if (customer.tier === 'GOLD') {
      total = total.multiply(0.9);  // 10% off
    }

    // Apply promotions
    for (const promo of promotions) {
      if (promo.appliesTo(order)) {
        total = promo.apply(total);
      }
    }

    return total;
  }
}

// Domain Service: Transfer
class MoneyTransferService {
  transfer(
    from: Account,
    to: Account,
    amount: Money
  ): TransferResult {
    if (from.balance.lessThan(amount)) {
      return TransferResult.insufficientFunds();
    }

    from.debit(amount);
    to.credit(amount);

    return TransferResult.success(from, to, amount);
  }
}
```

---

## Pattern Summary

| Pattern | What | When | Example |
|---------|------|------|---------|
| **Entity** | Has identity | Track over time | Order, Customer |
| **Value Object** | No identity, immutable | Describe attributes | Money, Address |
| **Aggregate** | Cluster with root | Consistency boundary | Order + Lines |
| **Domain Event** | Something happened | Decouple, audit | OrderPlaced |
| **Repository** | Get/store aggregates | Persistence | OrderRepository |
| **Domain Service** | Cross-entity logic | Doesn't fit one entity | PricingService |

---

## Recognizing Patterns in Legacy Code

### Entity Clues

```python
# Likely an Entity
class Order:
    def __init__(self, id):
        self.id = id  # Has ID
        self.created_at = datetime.now()
        self.status = 'draft'

    def update_status(self, new_status):  # Changes over time
        self.status = new_status
```

### Value Object Clues

```python
# Likely a Value Object (but not implemented as one)
class Address:
    def __init__(self, street, city, state, zip):
        self.street = street  # No ID
        self.city = city
        self.state = state
        self.zip = zip
        # Often mutable in legacy code (should be immutable)
```

### Aggregate Clues

```python
# Likely an Aggregate
class Invoice:
    def __init__(self, id):
        self.id = id
        self.lines = []  # Children

    def add_line(self, product, qty, price):
        self.lines.append(InvoiceLine(product, qty, price))
        self._recalculate_total()  # Maintains consistency

    def save(self, db):
        db.save_invoice(self)
        for line in self.lines:
            db.save_invoice_line(line)  # Saved together
```

### Domain Event Clues

```python
# Hidden events in legacy code
class OrderService:
    def submit_order(self, order):
        order.status = 'submitted'
        self.db.save(order)

        # These are really reactions to OrderSubmitted event
        self.inventory.reserve(order.items)
        self.email.send_confirmation(order.customer)
        self.analytics.track('order_submitted', order)
```

---

## Applying to Modernization

### Step 1: Identify What Exists

Look at legacy code and label:
- "This looks like an Entity"
- "This should be a Value Object"
- "These are always saved together — Aggregate"
- "This direct call should be an event"

### Step 2: Design Clean Model

Using proper DDD patterns:

```typescript
// Clean design for extracted domain
interface OrderAggregate {
  // Aggregate Root
  id: OrderId;
  customerId: CustomerId;  // Reference by ID
  lines: OrderLine[];      // Children inside
  status: OrderStatus;

  // Behavior
  addLine(item: OrderItem): void;
  removeLine(lineId: OrderLineId): void;
  submit(): OrderPlaced;  // Returns event
}
```

### Step 3: Build ACL

Translate between legacy and clean:

```typescript
class LegacyOrderAdapter {
  toDomain(legacy: LegacyOrder): Order {
    const order = new Order(new OrderId(legacy.order_num));

    for (const line of legacy.lines) {
      order.addLine(
        new ProductId(line.item_code),
        line.qty,
        new Money(line.unit_price, 'USD')
      );
    }

    return order;
  }
}
```

---

## Key Takeaways

1. **Entities** have identity — track them over time
2. **Value Objects** have no identity — compare by attributes
3. **Aggregates** are consistency boundaries — save together
4. **Domain Events** decouple — publish what happened
5. **Repositories** hide persistence — look like collections
6. **Look for patterns** in legacy code — they're there, just messy

---

## Related

- [Strategic Design](./03-Strategic-Design.md)
- [Bounded Contexts](./02-Bounded-Contexts.md)
- [Applied to Target Projects](./05-Applied-To-Projects.md)
- [Why DDD Matters](./01-Why-DDD-Matters.md)
