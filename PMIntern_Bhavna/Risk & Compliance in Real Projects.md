Date - 23 Feb
**Goal:** Interns understand how security, privacy, uptime, and SLAs impact scope, cost, and timelines in a product like Schedula.

1 . Session Overview

This session focuses on understanding how “non-functional” requirements such as security, privacy, uptime, and SLAs significantly impact project planning and delivery.

Even simple applications like Schedula (a salon booking app) handle sensitive data and business-critical workflows. Therefore, Project Managers must think beyond features.

2 . Warm-up Activity 

### Question to Interns:

“If Schedula is just a salon calendar app, what could really go wrong?”

### Discussion Points:

- Customer phone numbers leaked
    
- Appointment history exposed
    
- Salon revenue data leaked
    
- App down during peak traffic (festival/weekends)
    

### Key Learning:

Even simple applications carry sensitive data. PMs must think about risks, not just features.

3 . Security & Privacy Basics for PMs 

Core Concepts Explained Simply:

| Concept         | Meaning                              | Schedula Example                                |
| --------------- | ------------------------------------ | ----------------------------------------------- |
| Confidentiality | Only authorized people see the data  | Receptionist cannot see financial reports       |
| Integrity       | Data remains accurate and untampered | Past appointments cannot be edited without logs |
| Availability    | System is accessible when needed     | App should not crash on weekends                |

### Security vs Privacy

- **Security** = Lock on the door
    
- **Privacy** = Deciding who enters and what is stored inside
    

### Data Protection Principles (Schedula Context)

- Store only necessary data (data minimization)
    
- Avoid storing sensitive IDs unnecessarily
    
- Hide full phone numbers in public displays
    
- Clear retention policy for customer data
    

4 . Uptime & SLAs – Service Promises 

### What is an SLA?

An SLA (Service Level Agreement) is a promise about service performance.

### Common SLA Elements:

- **Uptime:** e.g., 99.5% or 99.9% availability per month
    
- **Response Time:** Critical issues responded within 1 hour
    
- **Resolution Time:** Critical issues fixed within 4 hours
    
- **Penalties:** Credits if commitments are not met
    

### Discussion Question:

“If we increase uptime from 98% to 99.9%, what changes?”

### Expected Impact:

- Need better cloud infrastructure
    
- Backup systems
    
- Monitoring tools
    
- On-call engineers
    
- Increased cost
    
- Extended timelines
    

### Key Insight:

Stronger SLA commitments increase scope, budget, and team requirements

5 . How Risk & Compliance Change Scope 

### Story 1: View Appointments

**Basic Version:** Show list of appointments  
**Secure Version:**

- Role-based access
    
- Access logs
    
- IP restrictions
    

### Story 2: Customer Data Deletion

Requires:

- Data deletion workflows
    
- Legal retention rules
    
- Data export functionality
    

### Story 3: Always Available on Weekends

Requires:

- Monitoring systems
    
- Alerts
    
- Backup infrastructure
    

### Learning:

Security and compliance requirements increase complexity and delivery time.

6 . Exercise: Data Protection in Schedula

Schedula stores:

- Customer name
    
- Phone
    
- Email
    
- Appointment details
    
- Notes (VIP client, allergic to product)
    

### Questions:

1. Which fields are most sensitive and why?
    
2. Suggest one improvement to protect this data.
    

### Expected Ideas:

- Encrypt sensitive fields
    
- Restrict notes visibility
    
- Allow customer data access and deletion
    
- Mask phone numbers


7 . Session Conclusion

Good Project Managers do not just ship features.  
They protect data, business continuity, and customer trust.

# Personal Productivity for PMs

**Goal:** Teach interns how to manage workload effectively using Kanban, calendar blocking, and decision logs.

1 . Why PMs Burn Out 

PMs receive inputs from:

- Developers
    
- Clients
    
- QA
    
- Sales
    

Without personal organization, effectiveness drops.

### Key Message:

“If you cannot manage yourself, you cannot manage a project.”

2 . Personal Kanban – Visualizing Work 

### Two Rules:

1. Visualize all tasks
    
2. Limit Work In Progress (WIP)
    

### Simple Board:

| Backlog | Doing (Max 3) | Done |

### Example Tasks:

- Review change request
    
- Prepare demo questions
    
- Summarize standup notes
    

### Mini Exercise:

- Write 5–7 tasks
    
- Choose only 3 for “Doing”
    
- Justify prioritization
    

### Benefit:

Improves focus and prevents overload.

3 . Calendar Blocking 

### Key Principle:

“If you don’t control your calendar, others will.”

### Types of Blocks:

- Focus Block (60–90 mins)
    
- Admin Block (30 mins)
    
- Buffer Block (15 mins)
    

### Example:

10:00–11:00 → Draft sprint change request  
3:00–3:30 → Respond to Jira comments

### Discussion:

What task deserves your daily deep-work block?

4 . Decision Logs 

### Why Needed?

PM memory is unreliable. Decisions must be documented.

### Simple Format:

| Date | Decision | Who | Why | Impact |

### Example:

“Feb 10 – WhatsApp moved to Phase 2 – To maintain MVP timeline.”

### Benefits:

- Prevents repeated debates
    
- Useful for documentation and portfolio
    
- Improves transparency

5 . Avoiding Burnout

### Common Issues:

- Saying yes to everything
    
- Always available online
    
- No focus time
    
- No boundaries
    

### Practical Boundaries:

- Fixed Slack checking times
    
- End-of-day shutdown ritual
    
- No-meeting focus hour
    
- Escalate major issues instead of absorbing all pressure
    

### Reflection Exercise:

Write one boundary to start this week.

## Final Takeaway

A strong PM:

- Understands risk and compliance
    
- Protects user data and uptime
    
- Manages personal workload effectively
    
- Builds systems instead of reacting emotionally