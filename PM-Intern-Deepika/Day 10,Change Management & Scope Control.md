# CHANGE REQUEST DOCUMENT

**Project:** Schedula Appointment System  
**Jira Task:** SCH-60  
**Change Request Title:** WhatsApp Reminder Integration

---

## 1. Request Details

**Date:** 18 Feb 2026  
**Requested By:** Schedula Client (Operations Manager)  
**Priority:** High (Customer Communication Improvement)

**Description:**  
The client has requested integration of WhatsApp messaging to send automated appointment reminders to customers after booking and before appointment time. The goal is to reduce no-shows and improve customer engagement.

---

## 2. Impact Assessment

### Scope Impact

New work required:

|Work Item|Effort|
|---|---|
|WhatsApp API integration|5 story points|
|Reminder scheduler logic|3 story points|
|Message template management|2 story points|
|Testing (QA scenarios)|3 story points|
|**Total**|**13 story points**|

New backend service + notification module required.

---

### Time Impact

- Estimated development: **5 working days**
    
- QA testing: **2 days**
    
- Total: **7 working days**
    
- Affects: **Current Sprint (Sprint 3) + 2 days spillover into Sprint 4**
    

---

### Cost Impact

|Item|Estimated Cost|
|---|---|
|Developer effort (7 days)|Included in contract|
|WhatsApp Business API setup|$50 setup fee|
|Messaging cost|~$0.005 per message|
|Monthly average (5,000 reminders)|~$25/month|

---

### Risk Impact

| Risk                       | Impact                     |
| -------------------------- | -------------------------- |
| Third-party API dependency | Integration delay possible |
| Message delivery failure   | Customer confusion         |
| Approval from WhatsApp     | May take 2–5 days          |
| Timeline risk              | Sprint delivery shift      |

---

## 3. Options

### Option A - Implement Immediately (Current Sprint)

**Description:** Start WhatsApp integration now and include in upcoming release.

**Pros**

- Client satisfied quickly
    
- Marketing advantage at launch
    
- Reduces no-shows immediately
    

**Cons**

- Current sprint commitments delayed
    
- High pressure on development team
    
- Increased risk of bugs before launch
    

---

### Option B - Next Sprint Implementation (Recommended)

**Description:** Complete current sprint scope first, implement WhatsApp in next sprint.

**Pros**

- No disruption to planned release
    
- Proper testing possible
    
- Lower technical risk
    

**Cons**

- Client waits 2 weeks
    
- No-show reduction delayed
    

---

### Option C - Phase-1 Basic SMS, Phase-2 WhatsApp

**Description:** Provide simple SMS reminder now, WhatsApp later.

**Pros**

- Immediate reminder feature
    
- Lower complexity
    
- Faster delivery (2–3 days)
    

**Cons**

- Additional integration later
    
- SMS cost higher long-term
    
- Not client’s preferred channel
    

---

## 4. Recommendation

**Recommended Option:** Option B - Next Sprint Implementation

### Reason:

1. Prevents disruption of current committed release.
    
2. Allows proper testing and reduces launch risk.
    
3. Avoids rushing third-party API integration.
    

### Implementation Timeline (If Approved)

- Sprint 3: No change
    
- Sprint 4: Development (5 days)
    
- Sprint 4 end: QA testing (2 days)
    
- Release: End of Sprint 4 (≈ 2 weeks)
    

---

## 5. Communication Plan

### Client Communication

- Send formal email explaining effort, risks, and recommended timeline.
    
- Share expected delivery date (end of Sprint 4).
    
- Provide demo preview once ready.
    

### Team Communication

- Announce approved change in daily standup.
    
- Create new Jira Epic: **WhatsApp Notification Integration**
    
- Break into stories and add to Sprint 4 backlog.
    

### Project Plan Adjustment

- Update roadmap
    
- Update sprint backlog
    
- Update release notes
    
- Track via new Epic