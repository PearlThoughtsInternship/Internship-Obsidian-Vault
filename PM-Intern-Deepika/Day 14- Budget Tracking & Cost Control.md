
## Budget Tracking & Cost Control — What I Understood

In this session I learned that a Project Manager does not only manage tasks and timelines, but also manages the **project budget**. Every project has a fixed amount of money, and the PM’s responsibility is to make sure the team completes the work **before the money finishes**.

### 1. Where project money goes

A project’s budget is mainly divided into three parts:

1. **People (largest cost – about 75%)**  
    Salaries of developers, designers, QA, and PM effort. Human resources are the most expensive part of any software project.
    
2. **Tools (around 10%)**  
    Cloud servers, SMS services (like Twilio), Jira, design tools, and other software subscriptions.
    
3. **Other costs (around 15%)**  
    Testing devices, meetings, travel, and a small buffer for unexpected expenses.
    

So the most important insight is:

> Software projects spend more money on people than on technology.

---

### 2. Planned vs Actual Spending

Every week the PM compares:

- **Planned spending** (how much money should have been used by this week)
    
- **Actual spending** (how much money has really been used)
    

This helps the PM detect problems early.

In the Schedula project:

- Planned by Week 7: 65% of budget
    
- Actual spent: 73% of budget
    

This means the project is spending money faster than expected, mainly due to high SMS testing costs.

---

### 3. Traffic Light System (Budget Health)

To simplify tracking, the PM uses a traffic light indicator:

- **Green:** under budget (safe)
    
- **Yellow:** on budget but needs monitoring
    
- **Red:** over budget and action required
    

Since more money is being spent while a lot of work is still left, the project status becomes **Yellow/Warning**, meaning the PM must watch costs carefully.

---

### 4. High-Risk Costs

Certain costs can suddenly increase and must be monitored:

- Cloud usage (servers scale up)
    
- Third-party APIs (Twilio, payment gateways)
    
- Overtime hours
    
- Scope creep (adding new features)
    

The Schedula issue happened because SMS API usage increased unexpectedly.

---

### 5. What a PM does when costs increase

A PM does not immediately stop the project. Instead, they take actions such as:

- **Defer** a feature to a later phase
    
- **Reduce** usage (limit testing or API calls)
    
- **Negotiate** with vendors for discounts
    

The goal is to protect both the project and client trust.

---

## Week 8 Budget Status Report

**People Cost:** ₹1.2L  
**Tools Cost:** ₹35K  
**Total Spend:** ₹5.9L / ₹6.2L planned  
**Status:** YELLOW

**Good:** Development is progressing according to schedule and core modules are stable.  
**Problem:** Twilio SMS usage is higher than expected and may risk the remaining budget if not controlled.

### Final Learning

The main learning is that a Project Manager tracks budget weekly to detect risks early and communicate them clearly.  
The PM’s job is not accounting — it is **financial awareness and decision-making**, ensuring the project finishes successfully without exceeding the client’s budget.

# Week 8 Budget Status Report (Completed Assignment)

### 1. Budget Details

- **Total Project Budget:** ₹8,00,000
    
- **Planned spend till Week 8:** ₹6,20,000
    
- **Actual estimated spend till Week 8:** ₹5,90,000
    

**Breakdown (Week 8):**

- **People Cost:** ₹1,20,000
    
- **Tools Cost:** ₹35,000
    
- **Total Spend:** ₹5,90,000
    

---

### 2. Budget Health Indicator

**Status: YELLOW (On budget but requires monitoring)**

Reason:  
The project is close to planned spending, but there is a risk because 35% of work is still pending while only about 25% of budget remains.

---

### 3. Positive Observation

Development progress is on schedule and core functionality is being completed as planned.

---

### 4. Identified Problem

SMS testing through Twilio is consuming more cost than expected and may cause budget overrun if usage continues at the same rate.

---

### 5. Recommended Actions

1. Limit SMS testing volume during development.
    
2. Use test or mock mode wherever possible instead of real SMS.
    
3. Move non-critical features (like additional notifications) to Phase-2 if needed.