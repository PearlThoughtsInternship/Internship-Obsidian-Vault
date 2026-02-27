# PM Internship Program — Complete Summary Report

**Organization:** PearlThoughts
**Program:** Project Management Internship
**Duration Covered:** February 19–26, 2026 (Days 10–13, Week 2 late → Week 3 start)
**Primary Project Context:** *Schedula* — a salon appointment booking web application
**Session Format:** 60-minute daily sessions (trainer-led, interactive)

---

## Program Overview

The PM Internship at PearlThoughts is a structured, hands-on training program teaching real-world project management skills. Unlike theory-heavy courses, every session uses a single running project — **Schedula** — as the practical sandbox. Interns act as PMs, facing real decisions around scope, timelines, clients, and teams.

The GitHub vault also reveals 3 parallel internship tracks at PearlThoughts:

| Track | Duration | Focus |
|---|---|---|
| PM Internship | ~3 weeks (implied) | Project management skills |
| Backend Dev | 4 weeks | NestJS, TypeScript, PostgreSQL |
| Full Stack Dev | 6 weeks | Next.js + NestJS (Schedula project) |
| AI Internship | 4 weeks | AI Engineering, Legacy Modernization |

---

## Session-by-Session Breakdown

### Day 10 — Change Management & Scope Control
**Dates:** Feb 19 (advanced guide) + Feb 20 (simplified guide)
**Two versions exist** — a detailed 5-part academic guide and a leaner practitioner script

**Core Concepts:**
- **Scope Creep** — the #2 reason projects fail; uncontrolled expansion without adjusting time/cost/resources
- **Iron Triangle** — Scope ↔ Time ↔ Cost: changing one forces adjustment in others; "there's no such thing as a free feature addition"
- **5-Step Change Control Process:**
  1. **Log/Receive** — don't say Yes or No immediately; buy time to assess
  2. **Impact Assessment** — quantify scope (story points), time (days), cost (₹), and risk
  3. **Generate Options** — always present 3 options, never just Yes/No
  4. **Present Trade-offs** — use the Iron Triangle; frame it as "which constraint are you flexible on?"
  5. **Decide & Document** — written record, update Jira, notify team

**Schedula Example Used:** Client requests WhatsApp booking integration (6 days before launch)
- Option A: Accept → launch delayed 2 weeks (+₹1.2–1.5L)
- Option B: Swap features (remove SMS reminders, add WhatsApp)
- Option C: Defer to Phase 2 (April update, cheaper at ₹80K)

**Assignment:** SCH-60 — Draft a formal Change Request document for the WhatsApp integration request

**Key Mindset Shift:** "Your job is NOT to say yes to everything. Your job is to make trade-offs visible."

---

### Day 11 (Feb 23) — Daily Standups & Sprint Ceremonies
*Note: This session was dated/labelled "Day 11" but delivered Feb 23 (Week 3 Monday)*

**Core Concepts:**
- **Daily Standup — 3 Questions:**
  1. What did I complete yesterday?
  2. What will I work on today?
  3. What blockers do I have?
- **Standup Rules:** Stand up, start on time, walk the board right-to-left, park side discussions, end in ≤15 min
- **4 Sprint Ceremonies:**
  - Sprint Planning (Day 1): Pick stories, estimate, commit to goal
  - Daily Standup (every day): 15 min sync, surface blockers
  - Sprint Review/Demo (last day): Show working software to stakeholders
  - Sprint Retrospective (last day): Start/Stop/Continue → 1–2 concrete action items
- **PM's Role:** Facilitator, not boss; solve blockers *after* standup

**Practice:** Interns rotated facilitating live standups with feedback checklist

**Assignment:** SCH-90 — Write a Start/Stop/Continue retrospective board for Schedula Sprint 2 with 1 action item

**Key Quote:** "Ceremonies aren't bureaucracy. They're the rhythm that keeps teams synchronized."

---

### Day X (Feb 23 file also includes) — Risk, Compliance & Personal Productivity

*(Two additional sessions were embedded in the Feb 23 file)*

**Risk & Compliance for PMs:**
- **CIA Triad applied to Schedula:** Confidentiality, Integrity, Availability
- **Security vs Privacy:** Security = lock on the door; Privacy = deciding what goes in the room
- **SLAs:** Uptime %, response time, resolution time, penalties — tighter SLAs = more scope + cost
- **PM's responsibility:** Not to design infrastructure, but to understand that security/compliance *adds* scope, budget, and timeline

**Personal Productivity (PM Workflow):**
- **Personal Kanban:** Visualize all work; limit WIP to max 2–3 items
- **Calendar Blocking:** Focus blocks (60–90 min), admin blocks (30 min), buffer blocks (15 min)
- **Decision Log:** Date | Decision | Who | Why | Impact — prevents re-arguing old decisions
- **Burnout Prevention:** Response windows, end-of-day shutdown routine, no-meeting blocks, escalation (not absorption)

---

### Day 11/Advanced (Feb 24) — Client Mastery & Meeting Facilitation
*Labelled "Day 11 Advanced" — delivered Feb 24*

**Core Concepts:**

**4 Types of Difficult Clients:**

| Type | Behavior | PM Strategy |
|---|---|---|
| The Demander | "I need this YESTERDAY!" | Slow down, gather facts |
| The Scope Creep | "Just one more thing..." | Iron Triangle + options |
| The Radio Silent | Never replies | Escalation + alternatives |
| The Micromanager | Questions every decision | Pre-emptive communication |

**De-escalation Language:**
- Use: "I understand this is urgent...", "Here are 3 options...", "What outcome are you trying to achieve?"
- Avoid: "Calm down", "That's impossible", "We'll try our best", "That's not in scope"

**Escalation Rule:**
- Own decisions up to ₹50K / 2-day delay
- Escalate anything bigger using structured template: Background → Impact → What I've Done → Next Steps Needed

**7-Minute Meeting Framework:**
- 1 min: Agenda + objective
- 2 min: Discussion (time-boxed, 30 sec/person)
- 2 min: Options
- 2 min: Decision with clear owner

**4 Facilitation Techniques:** Silent brainstorming, Dot voting, 5-5-5 prioritization, Parking lot

**Assignment:** SCH-90 — Client Escalation Pack (escalation email + de-escalation script + 7-min meeting agenda)

---

### Day 12 (Feb 25) — Workshop & Meeting Facilitation Deep Dive

**Core Concepts:**
- **Why workshops beat email chains:** 1 async email chain = 5 days of back-and-forth with no alignment; 1-hour workshop = clear priority list + team aligned
- **3 Situations for Workshops:** Project kickoff, mid-project scope review, problem-solving
- **60-Minute Workshop Agenda Template:**
  - 0–5 min: Welcome + ground rules
  - 5–15 min: Context setting
  - 15–25 min: Silent brainstorm (individual writing)
  - 25–35 min: Group share (round-robin)
  - 35–50 min: Prioritization/voting
  - 50–60 min: Decisions + action items

**Schedula Example:** Week 2 workshop that produced the MoSCoW-aligned feature list:
- Must: Booking, Calendar, SMS
- Should: Staff scheduling
- Could: Monthly reports
- Won't (Phase 2): Payments, Google sync

**Key Insight:** "Great PMs don't just react to problems; they prevent confusion through structured conversations."

---

### Day 13 (Feb 26) — Influencing Without Authority

**Core Concepts:**
- PMs have **no direct power** over developers, designers, or clients
- PM role = **Translator** between 5 concurrent stakeholders (Dev, Client, Marketing, Support, Sales)

**4-Step Agreement Method:**
1. Ask what each party actually wants
2. Explain limits using numbers (not vague language)
3. Give 3 concrete choices
4. Let them pick (restore their sense of control)

**Schedula Launch-Week Scenario:** Simultaneous crises from 4 teams — PM response is one clear priority list with specific instructions per person, not firefighting each separately

**Assignment:** SCH-95 — Post a ranked priority list for Schedula Sprint 3's top 5 tasks in Slack (who owns each, when done)

**Key Insight:** "PMs spend 50% of their time getting agreement on what matters most."

---

## Running Project: Schedula

All sessions are grounded in a single consistent project:

| Attribute | Detail |
|---|---|
| Product | Salon appointment booking web app |
| Client | Salon owner (SMB) |
| Budget | ₹8,00,000 |
| Timeline | 10 weeks MVP |
| Target launch | March 1, 2026 |
| Tech | Web-only for MVP |
| Phase 2 | Payments, WhatsApp, Google sync, mobile app |

Schedula serves as the PM intern's "sandbox" — every concept (scope creep, change requests, standups, client escalation) is applied to the same project, building continuity.

---

## Skills Progression Map

```
Week 1–2 (Days 1–9, not in vault):
  → Planning, prioritization, estimation, problem-solving

Week 2 (Days 10):
  → Scope control, change management, Iron Triangle

Week 3 (Days 11–13):
  → Execution: Standups, sprint ceremonies, client handling,
    facilitation, influencing without authority

Implied Week 3+ (Days 14+):
  → Burndown charts, status reports, stakeholder updates (referenced)
```

---

## Recurring Frameworks & Tools

| Framework | Used In |
|---|---|
| Iron Triangle (Scope/Time/Cost) | Days 10, 11, 12, 13 |
| 5-Step Change Control | Days 10 (both versions) |
| 3-Options Rule | Every client scenario |
| MoSCoW Prioritization | Referenced across days |
| Start/Stop/Continue | Day 11 retrospective |
| 7-Minute Meeting | Day 11 Advanced |
| Personal Kanban | Day 23 session |
| Jira + Confluence | Every assignment |
| PERT Estimation | Referenced (Day 5) |
| 5 Whys | Referenced (Day 9) |

---

## Assignment Pattern

Every session ends with a **Jira-tracked deliverable** with a clear rubric:

| Day | Jira Task | Deliverable |
|---|---|---|
| Day 10 | SCH-60 | Change Request Document (WhatsApp integration) |
| Day 11 | SCH-90 | Sprint Retrospective board (Start/Stop/Continue) |
| Day 11 Adv | SCH-90 | Client Escalation Pack |
| Day 13 | SCH-95 | Sprint 3 Priority List posted to Slack |

---

## Key Pedagogical Observations

1. **Single project throughout** — Schedula creates narrative continuity; interns see the same problems evolve across days
2. **Script-first delivery** — Presenters are given exact words to say, reducing variability across facilitators
3. **Model answers included** — Every practice scenario has a "good PM response" to calibrate against
4. **Anti-patterns explicitly taught** — "What NOT to say/do" sections in every session
5. **Jira/Confluence as real tools** — Assignments submitted to actual project management tools, not just docs
6. **Escalation thresholds defined** — Interns learn concrete rules (₹50K / 2-day limit) not vague judgment
7. **Numbers over vagueness** — Every impact is quantified (hours, days, rupees) — a core PM skill reinforced daily

---

## Summary

The PearlThoughts PM Internship is a tightly structured, execution-focused program. In the 6 documented sessions (Days 10–13 of an implied 3-week program), interns cover:

- **Scope defense** — how to protect a project from feature bloat
- **Agile ceremonies** — how to run standups, retros, and sprint demos effectively
- **Client management** — de-escalation, escalation paths, and professional "no"
- **Facilitation** — running workshops and structured decisions
- **Influence** — coordinating across teams without formal authority
- **Personal effectiveness** — Kanban, calendar blocking, decision logs

The program is deliberately practical: every concept is taught through Schedula scenarios, every session ends with a portfolio-worthy Jira assignment, and interns leave each day with skills they can use the next morning.
