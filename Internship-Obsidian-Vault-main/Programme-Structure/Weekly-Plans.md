# Weekly Plan – Patient & Doctor Experience

## Table of Contents
1. [Patient Experience](#patient-experience)  
2. [Doctor Experience](#doctor-experience)  

---
## Patient Experience

Week 1: Registration & Onboarding

Theme: Project Initialization and Authentication

🎯 Objectives

-Set up the foundational backend project structure using NestJS.
-Help patients locate the app, register, verify, and complete onboarding.
-Implement secure authentication using Google OAuth with role-based access (Doctor / Patient).

🧭 Experience Flow

-Locate the app.
-Register via email / phone / Google OAuth (social login).
-Verify identity via OTP or email verification.
-Choose role (Doctor / Patient) during Google login or registration.
-Complete onboarding walkthrough.

🧩 Tasks
Project Setup

-Initialize the backend project using NestJS framework.
-Set up API testing using Hoppscotch workspace.
-Design an ER Diagram to visualize database relationships.

Authentication Endpoints

-POST /api/v1/auth/signup → User registration (email/phone or Google OAuth).
-POST /api/v1/auth/signin → User login.
-POST /api/v1/auth/signout → User logout.
 
### Week 2: Appointment Making
**Objectives:** Allow patients to book appointments easily.
 
**Experience Flow:**  
- Locate doctor by specialty/ratings/availability  
- Select available slot and preferred time  
- Confirm appointment →
System triggers notification to patient:
 
“Your appointment with Dr. XYZ on DD/MM/YYYY at HH:MM is confirmed.”
 
- View appointment summary and reminders
- Cancel appointment if needed
 
**Technical Implementation:**  
- **Entities:** Appointment, Doctor, Patient, Slot, Time  
- **Relationships:**  
  - Appointment ↔ Patient (N:1)  
  - Appointment ↔ Doctor (N:1)  
  - Doctor ↔ Slot (1:N)  
  - Slot ↔ Time (1:N)  
 
**Tasks:**  
Backend:
 
API for doctor listing
 
One API for appointment booking
 
API for patient to cancel appointment
 
API for fetching patient’s appointment
 
 
## Week 3: Reschedule Experience
**Objectives:** Allow patients to reschedule appointments.
 
**Experience Flow:**  
- Access existing appointment  
- Select new slot/time  
- Confirm reschedule  
- Receive updated appointment notification
 
**Technical Implementation:**  
- **Entities:** Appointment, RescheduleHistory  
- **Relationships:**  
  - Appointment ↔ RescheduleHistory (1:N)  
 
**Tasks:**  
- Backend: APIs for fetching appointments, rescheduling  
- Frontend: UI for selecting new slots, showing updated appointment details  
 
 
## Week 4: Re-engagement Experience
**Objectives:** Keep patients engaged with reminders and follow-ups.
 
**Experience Flow:**  
- Notifications for upcoming appointments  
- Share health tips, reports, reminders  
- Encourage follow-up appointments  
- Personalized recommendations
 
**Technical Implementation:**  
- **Entities:** Notification, Patient, EngagementHistory  
- **Relationships:**  
  - Patient ↔ Notification (1:N)  
  - Patient ↔ EngagementHistory (1:N)  
 
**Tasks:**  
- Backend: scheduled jobs for reminders, notifications system  
- Frontend: notification center, email/SMS alerts  
 
---
 
## Doctor Experience
 
### Week 1: Onboarding & Profile Setup
**Objectives:** Help doctors register, verify credentials, and setup profile.
 
**Experience Flow:**  
- Locate app  
- Register with professional credentials  
- Verify credentials/approval  
- Setup profile: specialization, experience, consultation hours
 
**Technical Implementation:**  
- **Entities:** Doctor, Profile, VerificationToken, Specialization  
- **Relationships:**  
  - Doctor ↔ Profile (1:1)  
  - Doctor ↔ VerificationToken (1:N)  
  - Doctor ↔ Specialization (1:N)  
 
**Tasks:**  
- Backend APIs: registration, verification, profile update , to set availability 
- Database: doctors, profiles, verification_tokens, specializations  
 
---
 
### Week 2: Appointment Management
**Objectives:** Allow doctors to view, confirm, and manage appointments.
 
**Experience Flow:**  
- View scheduled appointments   
- Doctor can cancel appointment and patients should get notification for the same
 
**Technical Implementation:**  
- **Entities:** Appointment, Doctor, Patient, Slot, Time  
- **Relationships:**  
  - Doctor ↔ Appointment (1:N)  
  - Appointment ↔ Patient (N:1)  
  - Doctor ↔ Slot (1:N)  
  - Slot ↔ Time (1:N)  
 
**Tasks:**  
- Backend: APIs for fetching appointments, cancel appointments
 
---
 
### Week 3: Elastic Scheduling
**Objectives:** Implement elastic scheduling for doctors to manage dynamic appointments.
 
**Experience Flow:**  
- View flexible slots based on doctor availability   
- allow doctors to expand the consulting hours and capacity (max number of appointments)
 
**Technical Implementation:**  
- **Entities:** Doctor, Appointment, ElasticSlot, SlotAllocation  
- **Relationships:**  
  - Doctor ↔ ElasticSlot (1:N)  
  - Appointment ↔ ElasticSlot (N:1)  
 
**Tasks:**  
- Backend: APIs for elastic slot management, update appointment allocations  
- Database: ElasticSlot, SlotAllocation tables  
 
---
 
### Week 4: Re-engagement Experience
**Objectives:**  Keep doctors informed about important appointment changes and help them analyze slot utilization for better decision-making.
**Experience Flow:**  
- Monitor dynamic slot changes  
- Doctor will receive notifications when:
    - A patient cancels an appointment → So doctor knows the slot is now free.  
    - An appointment is rescheduled → So doctor is aware of new timing.  - Analyze slot utilization and patient engagement 
- Analyze slot utilization and patient engagement   
 
**Technical Implementation:**  
- **Entities:** Doctor, Appointment, Notification, Analytics, ElasticSlot  
- **Relationships:**  
  - Doctor ↔ Notification (1:N)  
  - Appointment ↔ Analytics (1:1)  
 
**Tasks:**  
- Backend: APIs for notifications, analytics, dynamic slot updates  
- Database: logging changes and tracking utilization  

## Daily Schedule Template

### Morning (10:00 AM - 12:30 PM)
- [ ] Training session
- [ ] Task assignment
- [ ] Q&A with mentors

### Afternoon (12:30 PM - 3:30 PM)
- [ ] Independent work on tasks
- [ ] Code implementation
- [ ] Testing and debugging

### Late Afternoon (3:30 PM - 6:00 PM)
- [ ] Code review preparation
- [ ] Documentation updates
- [ ] Pull request submission
- [ ] Team channel update

---

## Evaluation Checkpoints

### Week 1 Review
- Project setup completion
- Basic functionality implementation
- Code quality assessment

### Week 2 Review
- Feature completion rate
- API endpoint testing
- Documentation quality

### Week 3-4 Review
- Complex feature implementation
- Performance optimization
- Team collaboration

### Final Evaluation
- Project completeness
- Code quality and best practices
- Professional conduct
- Learning progression

---

*Last Updated: [[2025-09-10]]*
*Navigate: [[Index|Programme Home]] | [[../Handbook/Index|Handbook]] | [[../Support/Index|Support]]*
