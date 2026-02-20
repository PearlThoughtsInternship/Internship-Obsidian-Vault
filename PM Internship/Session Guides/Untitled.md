# Day 10 Session Plan: Change Management & Scope Control

**Project Management Internship – PearlThoughts**  
**Date:** February 20, 2026  
**Duration:** 60 minutes  
**Presenter:** [Your Name]  
**Focus:** Controlling Scope & Professional Change Management

---

## 1. Session Overview (3 minutes)

**Read aloud:**

"Welcome to Day 10. Today we tackle the #1 killer of projects: SCOPE CREEP.

Scope creep is when:

- Client asks for 'one small thing' that becomes 10 things
    
- Features keep getting added mid-sprint
    
- Project never actually finishes
    

You'll learn:

1. **How scope creep happens** (usually silently)
    
2. **The 5-step Change Control Process** (how professionals handle it)
    
3. **How to say 'No' using data** (not emotions)
    

We'll use **real Schedula scenarios** where client wants extra features."

---

## 2. Understanding Scope Creep (10 minutes)

## 2.1 What is Scope Creep?

**Simple definition:**

> "Scope creep = Work keeps growing without adjusting time, budget, or team size."

**Schedula Example:**

**Original Plan (Week 1):**

- Online booking
    
- Calendar view
    
- SMS reminders
    
- Budget: ₹8 lakhs | Timeline: 10 weeks
    

**After 4 weeks (scope creep):**

- Online booking
    
- Calendar view
    
- SMS reminders
    
- ✚ WhatsApp booking (client asked Week 2)
    
- ✚ Google Calendar sync (client asked Week 3)
    
- ✚ Payment gateway (client asked Week 4)
    
- ✚ Customer loyalty points (client asked yesterday)
    
- Budget: Still ₹8 lakhs | Timeline: Still 10 weeks ❌
    

**Result:** Project will fail. Team will burn out. Quality will suffer.

---

## 2.2 How Scope Creep Happens (The Pattern)

**Show this conversation pattern:**

text

`Client: "Can you just add WhatsApp booking? Should be easy, right?" Bad PM: "Sure, we'll try to fit it in." [2 days later] Client: "Since you're doing WhatsApp, can we add Instagram DMs too?" Bad PM: "Okay, I'll talk to the team." [3 days later] Client: "One more small thing - loyalty points for repeat customers?" Bad PM: "Um... okay..."`

**Why this happens:**

- PM wants to make client happy (good intention, bad execution)
    
- PM doesn't show the **trade-offs** clearly
    
- Client thinks additions are "small" because PM didn't explain impact
    

---

## 2.3 The Iron Triangle

**Draw or show this triangle:**

text

        `SCOPE         /\        /  \       /    \      /      \     /        \    /          \   /____________\ TIME          COST`

**The rule:** If you increase SCOPE, you must also increase TIME or COST (or both). You cannot add scope while keeping time and cost fixed.

**Schedula Example:**

- Client wants WhatsApp booking (increase SCOPE)
    
- Options:
    
    - Delay launch by 2 weeks (increase TIME)
        
    - Pay ₹1.5 lakh extra for contractor (increase COST)
        
    - Remove SMS reminders to make room (reduce SCOPE elsewhere)
        

**Key message:** "There's no such thing as a free feature addition."

---

## 3. The 5-Step Change Control Process (20 minutes)

**Explain:**

"When client asks for changes, professionals follow this 5-step process. Learn this and you'll handle scope creep better than 80% of PMs."

---

## STEP 1: RECEIVE the Request

**Don't say 'Yes' or 'No' immediately.**

**Good PM response:**

> "Thanks for this suggestion. Let me assess the impact and get back to you by tomorrow with options."

**Why this works:**

- Buys time to think
    
- Shows professionalism
    
- Avoids saying yes to impossible things
    

---

## STEP 2: ASSESS the Impact

**Use this simple template:**

text

`CHANGE REQUEST: [Feature name] IMPACT ANALYSIS: - Scope: [How many story points? How complex?] - Timeline: [How many days/weeks delay?] - Cost: [Extra money needed?] - Risk: [What could go wrong?] - Dependencies: [What else is affected?]`

**Schedula Example:**

text

`CHANGE REQUEST: Add WhatsApp Booking IMPACT ANALYSIS: - Scope: +8 story points (High complexity - need WhatsApp Business API) - Timeline: +2 weeks to launch date - Cost: +₹1.2 lakhs (WhatsApp API setup + 40 dev hours) - Risk: WhatsApp API approval can take 5-7 days (unpredictable) - Dependencies: Affects SMS reminder feature (both use similar logic)`

---

## STEP 3: GENERATE Options

**Always give client 3 options (not just 1):**

**Schedula WhatsApp Example:**

**Option A: Add now, delay launch**

- Add WhatsApp booking
    
- Move launch from March 1 to March 15 (+2 weeks)
    
- Extra cost: ₹1.2 lakhs
    
- ✅ Pro: Client gets everything
    
- ❌ Con: Delayed market entry, budget increase
    

**Option B: Add now, remove something else**

- Add WhatsApp booking
    
- Remove SMS reminders from MVP (move to Phase 2)
    
- Keep March 1 launch date
    
- No extra cost
    
- ✅ Pro: Timeline and budget maintained
    
- ❌ Con: Lose one planned feature
    

**Option C: Add in Phase 2 (after launch)**

- Keep current plan for March 1 launch
    
- Add WhatsApp booking in April update
    
- Extra cost: ₹80,000 (cheaper because we learn from MVP first)
    
- ✅ Pro: Get to market fast, add feature based on real user feedback
    
- ❌ Con: Feature not available at launch
    

---

## STEP 4: PRESENT Trade-offs

**Schedule meeting with client. Show the 3 options clearly.**

**Script to use:**

> "You asked about WhatsApp booking. Great idea - I can see why customers would want this.
> 
> I've analyzed the impact. Here are your 3 options with trade-offs:
> 
> [Show Option A, B, C with pros/cons]
> 
> My recommendation as PM: **Option C** - launch on time, add WhatsApp in Phase 2. Here's why: [explain reasoning]
> 
> But the decision is yours. Which option works best for your business?"

**Why this works:**

- Shows you took request seriously
    
- Uses data, not emotions
    
- Gives client control while showing consequences
    
- Demonstrates professional competence
    

---

## STEP 5: DECIDE & Document

**Once client chooses:**

1. **Update Jira** - Create new epic/story if approved, or mark as "Deferred"
    
2. **Update timeline** - Adjust sprint plan if needed
    
3. **Email confirmation** - Send written record of decision
    
4. **Inform team** - Update everyone on what changed
    

**Documentation template:**

text

`CHANGE REQUEST DECISION: WhatsApp Booking Decision: Option C - Add in Phase 2 Date: February 20, 2026 Decided by: Client (Salon Owner), PM Reason: Maintain March 1 launch to capture spring season bookings. WhatsApp feature will be added in April based on MVP user feedback. Action Items: - Create Epic "Phase 2 Enhancements" in Jira - Add WhatsApp story under Phase 2 (8 points) - Notify dev team: no scope change for current sprint - Schedule April planning meeting Signed off by: [Client Name]`

---

## 4. Live Practice: Handling Real Change Requests (15 minutes)

**Give them 3 mini-scenarios. They practice responding:**

---

## Scenario 1: "Just a Small Change"

**Client message:**

> "Hey! Can you change the calendar colors to match our brand? Should be quick - just update some colors. Can you have it done by tomorrow?"

**Your task (5 minutes):**  
Write a professional response using the 5-step process. Include:

1. Your immediate reply
    
2. Quick impact assessment
    
3. 2 options for client
    

**Model answer (show after they try):**

> "Thanks for the suggestion! Brand alignment is important.
> 
> Let me assess this properly and get back to you in 2 hours with options.
> 
> Quick question: Do you have your brand color codes (hex values) documented? That will help speed up the assessment."

_[After assessment]_

> "Color update impact:
> 
> - Scope: 4 hours (not just CSS - need to test contrast, accessibility)
>     
> - Timeline: Can complete by end of week (not tomorrow - we're in QA phase)
>     
> 
> Options:  
> A) Do now (Friday delivery): Pauses current QA work by 4 hours  
> B) Do next week: No impact to current sprint
> 
> Recommendation: Option B - keeps us on track for demo Thursday.
> 
> Which works for you?"

---

## Scenario 2: The "Since You're Already Building It" Trap

**Client message:**

> "Since you're already building the booking form, can you add a field for customer's birthday? And maybe their anniversary date too? We want to send them special offers."

**Your task (5 minutes):**

- Assess impact
    
- Give 3 options
    
- Make a recommendation
    

---

## Scenario 3: Major Feature Addition

**Client message:**

> "I just saw a competitor's app - they have a mobile check-in feature where customers can check in when they arrive at the salon. This is CRITICAL for us. Can we add this before launch?"

**Your task (5 minutes):**

- Full 5-step process
    
- Include risk assessment
    
- Document your recommendation
    

---

## 5. How to Say "No" Professionally (8 minutes)

**Key phrases to use:**

❌ **Never say:** "That's impossible" or "We can't do that"

✅ **Always say:** "We can do that if we adjust X or Y. Here are the options..."

---

**Formula for Professional "No":**

text

`1. Acknowledge the value ("I understand why this matters") 2. Show the constraint ("Given our timeline/budget/resources") 3. Offer alternatives ("Here's what we can do instead") 4. Give choice back to them ("Which approach works best?")`

**Schedula Example:**

Bad response:

> "No, we can't add video calls. It's too complicated."

Professional response:

> "Video calling would add great value - I can see customers wanting virtual consultations.
> 
> Given our current 10-week timeline and ₹8L budget, adding video calling would require:
> 
> - 3 additional weeks (licensing + infrastructure + testing)
>     
> - ₹2.5L extra cost (video API licenses + server upgrades)
>     
> 
> Two alternatives:
> 
> 1. Launch core booking features on time (March 1), add video calling in Phase 2 (May)
>     
> 2. Delay entire launch to April 1 to include video calling
>     
> 
> My recommendation: Option 1 - get booking features to market, then add video based on actual customer demand.
> 
> What makes most sense for your business timeline?"

---

## 6. Your Real Assignment (4 minutes)

**Jira Task: SCH-60 "Draft Change Request Document"**

**Scenario:**

Client just sent this email:

> "Hi Team,
> 
> Can we add these to the Schedula app before launch:
> 
> 1. Instagram integration for booking through DMs
>     
> 2. Automatic birthday discount coupons (10% off)
>     
> 3. Staff performance dashboard (which stylist gets most bookings)
>     
> 
> These will really differentiate us from competitors!
> 
> Thanks!"

**Your deliverable (due Monday EOD):**

Using the 5-step Change Control Process, create a professional response document that includes:

1. **Impact Assessment** for all 3 features (scope, time, cost, risk)
    
2. **Three Options** with clear trade-offs
    
3. **Your Recommendation** with reasoning
    
4. **Draft Email** to client presenting your analysis
    

**Template provided in Confluence: "Change Request Response Template"**

**Word limit:** 400 words max (client won't read more)

---

## 7. Wrap-Up (2 minutes)

**What you learned today:**

✅ **Scope creep** = #1 project killer (work grows without adjusting time/budget)  
✅ **Iron Triangle** = Scope-Time-Cost are connected (change one, must change another)  
✅ **5-Step Process** = Receive → Assess → Options → Present → Document  
✅ **Professional "No"** = Acknowledge + Constraint + Alternatives + Choice

**Key mindset shift:**

"Your job as PM is NOT to say yes to everything. Your job is to **show trade-offs clearly** so stakeholders can make informed decisions."

**Monday:** Daily standups & sprint ceremonies (Week 3 begins!)

---

## Presenter Notes

**This session is critical because:**

- Scope creep is the most common reason interns see projects fail
    
- Learning to say "no" professionally is a career-defining skill
    
- The 5-step process is immediately applicable to any project
    

**Make it interactive:**

- Let interns struggle with scenarios for 3-4 minutes before showing model answers
    
- Ask: "Has anyone seen scope creep in college projects or part-time work?"
    
- Emphasize: The goal isn't to block client ideas - it's to make consequences visible
    

**Common mistakes to watch for:**

- Interns saying "no" without offering alternatives
    
- Not quantifying impact (saying "it will take longer" instead of "adds 2 weeks")
    
- Forgetting to document decisions