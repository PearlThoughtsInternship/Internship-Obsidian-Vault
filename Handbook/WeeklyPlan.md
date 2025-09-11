# Weekly Plan – Patient & Doctor Experience

## Table of Contents
1. [Patient Experience](#patient-experience)  
2. [Doctor Experience](#doctor-experience)  

---

## Patient Experience

### Week 1: Registration & Onboarding
**Objectives:** Help patients locate the app, register, verify, and complete onboarding.

**Experience Flow:**  
- Locate the app.  
- Register via email/phone/social login.  
- Verify identity via OTP/email.  
- Complete onboarding walkthrough.

**Technical Implementation:**  
- **Entities:** Patient, Profile, VerificationToken, OnboardingStatus  
- **Relationships:**  
  - Patient ↔ Profile (1:1)  
  - Patient ↔ VerificationToken (1:N)  
  - Patient ↔ OnboardingStatus (1:1)  

**Tasks:**  
- Backend APIs: registration, verification, onboarding status  
- Database tables: patients, profiles, verification_tokens  
- Frontend: registration form, OTP input, onboarding slides  

---

### Week 2: Appointment Making
**Objectives:** Allow patients to book appointments easily.

**Experience Flow:**  
- Locate doctor by specialty/ratings/availability  
- Select available slot and preferred time  
- Confirm appointment  
- View appointment summary and reminders

**Technical Implementation:**  
- **Entities:** Appointment, Doctor, Patient, Slot, Time  
- **Relationships:**  
  - Appointment ↔ Patient (N:1)  
  - Appointment ↔ Doctor (N:1)  
  - Doctor ↔ Slot (1:N)  
  - Slot ↔ Time (1:N)  

**Tasks:**  
- Backend: APIs for doctor listing, slot selection, time booking, confirmation  
- Frontend: appointment booking UI  

---

### Week 3: Reschedule Experience
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

---

### Week 4: Re-engagement Experience
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
- Setup profile: specialization, experience, consultation hours, profile pic

**Technical Implementation:**  
- **Entities:** Doctor, Profile, VerificationToken, Specialization  
- **Relationships:**  
  - Doctor ↔ Profile (1:1)  
  - Doctor ↔ VerificationToken (1:N)  
  - Doctor ↔ Specialization (1:N)  

**Tasks:**  
- Backend APIs: registration, verification, profile update  
- Database: doctors, profiles, verification_tokens, specializations  
- Frontend: registration form, credential upload, profile editor  

---

### Week 2: Appointment Management
**Objectives:** Allow doctors to view, confirm, and manage appointments.

**Experience Flow:**  
- View scheduled appointments 
- Update appointment status (Completed/Cancelled)  
- Send confirmation/reminder to patients

**Technical Implementation:**  
- **Entities:** Appointment, Doctor, Patient, Slot, Time  
- **Relationships:**  
  - Doctor ↔ Appointment (1:N)  
  - Appointment ↔ Patient (N:1)  
  - Doctor ↔ Slot (1:N)  
  - Slot ↔ Time (1:N)  

**Tasks:**  
- Backend: APIs for fetching appointments, updating status, sending notifications  
- Frontend: dashboard with appointments, status updates, patient details  

---

### Week 3: Reschedule Experience
**Objectives:** Allow doctors to reschedule appointments efficiently.

**Experience Flow:**  
- Access upcoming appointments  
- Select new slot/time  
- Confirm reschedule and notify patient  
- Track reschedule history

**Technical Implementation:**  
- **Entities:** Appointment, RescheduleHistory, Doctor  
- **Relationships:**  
  - Appointment ↔ RescheduleHistory (1:N)  
  - Doctor ↔ RescheduleHistory (1:N)  

**Tasks:**  
- Backend: APIs for rescheduling, updating status, notifying patients  
- Frontend: UI for selecting new slots, confirming reschedule  

---

### Week 4: Patient Engagement Experience
**Objectives:** Keep doctors engaged with patients and practice management.

**Experience Flow:**  
- Review patient feedback  
- Track patient reports and follow-ups  
- Send reminders for appointments/lab results  
- Access dashboard/analytics for performance

**Technical Implementation:**  
- **Entities:** Doctor, Patient, Feedback, Notification, EngagementHistory  
- **Relationships:**  
  - Doctor ↔ Patient (1:N)  
  - Doctor ↔ Feedback (1:N)  
  - Doctor ↔ Notification (1:N)  

**Tasks:**  
- Backend: APIs for feedback, notifications, analytics  
- Frontend: dashboard showing feedback, patient history, notifications, analytics  
