Change Request Document – CR-012

Project: Schedula
Internship: Project Management Internship – PearlThoughts
Date: 19 February 2026
Prepared By: Dhiraj Roy

1. Request Details

Requestor: Salon Owner (Client)
Priority (Client Mentioned): High

Request Summary:
The client has requested the addition of a WhatsApp booking feature so customers can schedule appointments directly through WhatsApp. The expectation is that customers will be able to book appointments, receive confirmation messages, and get reminders using WhatsApp notifications.

Purpose of Request:
The salon mainly receives customers through social media and walk-ins. Adding WhatsApp booking is expected to make scheduling easier, improve customer response time, and increase engagement with existing clients.

2. Impact Assessment
Overview

This request introduces functionality that was not included in the original MVP scope. It requires backend integration, UI updates, and dependency on an external WhatsApp Business API.

Scope Impact
Area	Existing Plan	After Change	Impact
Story Points	18 SP	23 SP	+5 SP
Features	Standard booking	WhatsApp booking added	New module
UI Changes	Minimal	New booking & confirmation flow	Additional work
External Integration	None	WhatsApp API required	New dependency

Observation:
The scope increases by nearly 28%, which is higher than the recommended safe sprint change limit.

Time Impact
Task	Estimated Duration
API setup & configuration	3 days
Backend development	2 days
Frontend changes	2 days
Testing & QA	3 days
Buffer / issue handling	2 days
Total Estimated Impact	~12 days

Timeline Effect:

Original Launch: 28 Feb 2026

Revised Launch (if added now): Around 7–10 March 2026

Expected Delay: Approximately 1 week+

Cost Impact
Cost Component	Estimate
Development effort	₹25,000
WhatsApp API setup	₹5,000
QA & testing	₹3,000
Recurring API charges	₹2,000–₹4,000/month

Total Immediate Cost: ₹30,000–₹35,000 (approx.)

Risk Analysis
Risk	Level	Reason
Third-party approval delays	High	WhatsApp API dependency
Launch postponement	Medium	Marketing schedule affected
Technical complexity	Medium	New integration area
Team workload	High	Team already fully utilized
3. Available Options
Option A – Implement Immediately

Add WhatsApp integration in the current sprint.

Advantages

Feature available at launch

Strong customer convenience

Competitive advantage

Disadvantages

Launch delayed by 1–2 weeks

Increased budget requirement

Higher pressure on development team

Option B – Move to Phase 2 (Recommended)

Launch MVP as planned and introduce WhatsApp booking in the next release cycle.

Advantages

Launch date remains unchanged

Budget stays controlled

Lower execution risk

Feature can be marketed as “Coming Soon”

Disadvantages

Feature unavailable at initial launch

Client waits a few weeks

Option C – Scope Trade-Off

Introduce WhatsApp booking but remove the Monthly Reports feature from MVP.

Advantages

Launch timeline maintained

Budget remains similar

WhatsApp available immediately

Disadvantages

Reporting and analytics temporarily unavailable

Operational insights delayed

4. Recommendation

Recommended Approach: Option B – Defer to Phase 2

Reasoning:

Meeting the planned launch date is critical due to the upcoming wedding season business demand.

External API approvals may introduce uncertainty and risk to delivery timelines.

Deferring the feature prevents additional cost escalation during MVP delivery.

The team can maintain focus on delivering a stable and high-quality initial release.

Proposed Timeline (Phase 2):

Planning: Early March

Development & Testing: 1 week

Release Target: Mid-March update

5. Communication Plan
Client Communication

Arrange a short review meeting with the client.

Present impact analysis clearly using scope, time, and cost trade-offs.

Explain available options and request client preference based on priorities.

Internal Communication

Update Jira roadmap and backlog.

Create a Phase-2 Epic: WhatsApp Booking Integration.

Inform development team during sprint stand-up.

Update risk and status reports.

Project Adjustment

Move WhatsApp feature to upcoming release roadmap.

Reflect decision in stakeholder status update.

Align marketing messaging with “Feature Coming Soon”
