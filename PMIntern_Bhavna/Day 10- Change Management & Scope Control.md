
**Project Management Internship – PearlThoughts**  
**Date:** February 19, 2026  
**Focus:** Managing Change Requests & Preventing Scope Creep

1 . Request Details
**Requestor:** Salon Owner (Client)  
**Priority (Client Stated):** High  
**Request Description:**  
Client has requested integration of **WhatsApp booking functionality** allowing customers to:

- Book appointments via WhatsApp
    
- Receive booking confirmations
    
- Receive reminders via WhatsApp
    

The request is intended to increase customer engagement and simplify booking for walk-in and social media customers.

2 . Impact Assessment

## Overview of Change

This change introduces new backend API integrations, frontend UI modifications, and third-party WhatsApp Business API configuration.

Scope Impact

| Item            | Current Plan    | With Change                           | Impact         |
| --------------- | --------------- | ------------------------------------- | -------------- |
| Story Points    | 18 SP           | 23 SP                                 | +5 SP (+28%)   |
| New Features    | None            | WhatsApp Booking + Messaging Logic    | New module     |
| New Screens     | 0               | 2 (WhatsApp flow + Confirmation view) | Added UI       |
| API Integration | No external API | WhatsApp Business API                 | New dependency |
**Scope Increase:** 28%  
This exceeds safe sprint change threshold (15%).

Time Impact

| Activity                  | Estimated Time           |
| ------------------------- | ------------------------ |
| WhatsApp API Integration  | 3 days                   |
| Backend Logic Development | 2 days                   |
| Frontend UI Changes       | 2 days                   |
| Testing & QA              | 3 days                   |
| Buffer for Issues         | 2 days                   |
| Total Impact              | **~12 days (1.5 weeks)** |

### Timeline Effect:

- Original Launch: **28 Feb 2026**
    
- New Launch (if added now): **7–10 March 2026**
    
- Delay: +7–10 days


Cost Impact

| Cost Item                     | Estimated Cost          |
| ----------------------------- | ----------------------- |
| Developer Effort (10–12 days) | ₹25,000                 |
| WhatsApp API Setup            | ₹5,000                  |
| Monthly API Cost              | ₹2,000–₹4,000 recurring |
| QA Effort                     | ₹3,000                  |
| Total Immediate Cost          | **₹30,000 – ₹35,000**   |
Risk Impact

| Risk                   | Impact Level | Explanation                     |
| ---------------------- | ------------ | ------------------------------- |
| Third-party API issues | High         | Dependency on WhatsApp approval |
| Launch delay           | Medium       | Marketing campaign impact       |
| Technical complexity   | Medium       | New integration area            |
| Team Overload          | High         | Team already at 100% capacity   |
Three Options for Decision

Option A: Approve Now & Delay Launch

### Description:

Implement WhatsApp integration immediately in current sprint.

### Pros:

- Client gets full functionality at launch
    
- Competitive feature advantage
    
- Strong customer engagement
    

### Cons:

- Launch delayed by 1–2 weeks
    
- Marketing campaign rescheduling required
    
- Increased cost (+₹30,000+)
    
- Higher stress on team
    

### Impact:

- Launch moves to March 7–10
    
- Budget increases
    
- Risk level increases


Option B: Defer to Phase 2 (Recommended)

### Description:

Launch MVP as planned. Add WhatsApp integration in Phase 2 (March Update).

### Pros:

- Launch on time (28 Feb)
    
- Budget remains stable
    
- Reduced technical risk
    
- Can market as “WhatsApp Coming Soon”
    
- Better planning & structured integration
    

### Cons:

- WhatsApp not available at launch
    
- Client must wait 2–3 weeks
    

### Impact:

- No launch delay
    
- No immediate cost increase
    
- Lower risk
    
- Cleaner sprint execution


Option C: Swap Feature (Scope Trade-off)

### Description:

Add WhatsApp but remove “Monthly Reports” feature from MVP.

### Pros:

- Launch on time
    
- Budget neutral
    
- WhatsApp available at launch
    

### Cons:

- Analytics/reporting not available initially
    
- Loss of management insights
    
- Client may miss operational tracking
    

### Impact:

- Same total story points (swap)
    
- No cost increase
    
- Functional trade-off


4 . Recommendation

## Recommended Option: **Option B – Defer to Phase 2**

### Reason 1: Protect Launch Deadline

Wedding season is critical for salon business. Timely launch is strategically more important than one feature.

### Reason 2: Risk Reduction

WhatsApp API approval delays can create unpredictable launch blockers.

### Reason 3: Controlled Budget

Avoids immediate ₹30,000–₹35,000 cost increase.

### Implementation Timeline if Approved:

- Add to Phase 2 Roadmap (March Sprint 1)
    
- Planning: 1 March
    
- Development: 3–10 March
    
- Release: Mid-March Update

5 . Communication Plan

## Client Communication

- Schedule 30-minute review call
    
- Present impact assessment table
    
- Show Iron Triangle trade-offs:
    
    - Scope
        
    - Time
        
    - Cost
        
- Present 3 options clearly
    
- Ask: “Which constraint is most flexible for you?”

## Internal Team Communication

If Option B selected:

1. Update product roadmap
    
2. Create Phase 2 Epic in Jira
    
3. Adjust sprint board
    
4. Inform developers in standup
    
5. Update risk log

## Project Plan Adjustment

- Move WhatsApp to Q2 Roadmap
    
- Add as Epic: “WhatsApp Booking Integration”
    
- Update stakeholder status report