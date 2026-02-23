
# Risk, Compliance & Personal Productivity for PMs

## Risk & Compliance in Real Projects (Why “simple apps” aren’t simple)

At first Schedula looks like **just a salon calendar**, but it actually handles **sensitive customer and business data**.  
So the PM’s job is not only delivering features — it is also protecting **data, trust, and reliability**.

### What can go wrong?

- Customer phone numbers leak
    
- Appointment history exposed
    
- Salon revenue data stolen
    
- App crashes during peak days (weekends/festivals)
    

So even a small app has **real-world consequences**.

---

## Three Core Concepts PMs Must Understand

### Confidentiality

Only the right people see the data  
- Example: receptionist can see bookings but not financial reports

### Integrity

Data should not be altered incorrectly  
- No one should secretly edit past appointments

### Availability

System must work when needed  
- If Schedula is down on Saturday evening - salon loses business

---

### Privacy vs Security

- **Security** = protecting the system (locks, permissions)
    
- **Privacy** = controlling what data you collect and who can access it
    

Example:

- Store only phone number, not Aadhaar
    
- Hide full numbers on public screens
    
- Allow customers to delete their data
    

PM learning: **Non-functional requirements (security, privacy, uptime) directly affect scope, time, and cost.**

---

## Uptime & SLA (Service Level Agreement)

**SLA = a promise to customers about service quality and speed.**

It includes:

- Uptime (e.g., 99.9%)
    
- Response time (how fast support replies)
    
- Resolution time (how fast issues are fixed)
    
- Penalties if broken
    

### Important PM understanding:

Higher SLA -> 
more monitoring + backups + support staff + cost + time.

So:  
**Better reliability always means larger scope and budget.**

---

##  How Risk & Compliance Change Development

A simple feature becomes complex when compliance is added:

| Feature           | Without Compliance | With Compliance               |
| ----------------- | ------------------ | ----------------------------- |
| View appointments | Just display list  | role permissions + logs       |
| Delete data       | Remove record      | retention rules + legal flow  |
| Always available  | normal hosting     | monitoring + failover servers |

 So, PM planning must include these from the start.

---

## Key Takeaway

A good PM does not just ship features.  
A good PM **protects user trust and business continuity.**

---

# Personal Productivity for PMs

PMs burn out because:

- constant messages
    
- meetings
    
- documentation
    
- coordination

## Personal Kanban (Your External Brain)

Simple board:

|Column|Meaning|
|---|---|
|Backlog|All tasks|
|Doing|Max 2–3 tasks only|
|Done|Completed work|

Rule: **Limit Work in Progress**

Why important?

- Prevents overload
    
- Helps prioritization
    
- Lets you communicate workload to manager
    

---

## Calendar Blocking

PMs must protect focus time.

Use:

- Focus block (deep work)
    
- Admin block (emails/messages)
    
- Buffer time (after meetings)
    

Example:  
10–11 AM → write change request  
3–3:30 PM → reply to Jira + Slack

---

## Decision Logs

PM memory is unreliable.

So PMs maintain a log:  
Date | Decision | Who | Why | Impact

Example:  
“WhatsApp moved to Phase 2 to meet launch deadline”

Benefits:

- avoids repeated arguments
    
- helps documentation
    
- useful for portfolio
    

---

## Avoiding Burnout

PM should set boundaries:

- fixed Slack checking times
    
- daily shutdown routine
    
- protected focus hours
    
- escalate major issues instead of handling alone