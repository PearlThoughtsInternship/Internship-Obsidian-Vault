# Backend Java - Out Patient Appointment Scheduling System

## Project Purpose

This service is the Java backend implementation of the **Out Patient Appointment Scheduling System**.  
The goal of this project is to build a backend that allows patients and doctors to interact with an OPD appointment platform in a structured and secure way.

### Main Objectives
- Patient registration and authentication
- Doctor registration and profile setup
- Appointment booking and cancellation
- Appointment rescheduling
- Notifications and re-engagement features
- Scalable backend design using clean module structure

This implementation is being built as a **modular monolith** using **Java + Spring Boot**, so that it remains simple for initial development and can later evolve cleanly.

---

## Tech Stack

### Backend
- Java 21
- Spring Boot 3.5.x
- Spring Web
- Spring Data JPA
- Spring Security
- Spring Validation

### Database
- PostgreSQL
- Flyway Migration

### API Documentation
- Springdoc OpenAPI
- Swagger UI

### Authentication
- BCrypt Password Encoder
- JWT (planned next phase)
- Google OAuth (planned as per internship flow)

### Build Tool
- Maven

### Development Tools
- IntelliJ IDEA / VS Code
- Postman / Hoppscotch
- Git & GitHub

---

## Current Project Scope

At the current stage, this backend includes the base setup required for Week 1 development:
- Spring Boot project initialization
- PostgreSQL connection
- Flyway migration setup
- Health check API
- Authentication base structure
- User entity and role model
- Signup API base
- Signin / Signout API stubs
- Swagger/OpenAPI setup

---

## Project Structure

```text
apps/backend-java/
├── README.md
├── pom.xml
├── docs/
├── src/
│   ├── main/
│   │   ├── java/com/appointment/backendjava/
│   │   │   ├── config/
│   │   │   ├── common/
│   │   │   ├── health/
│   │   │   ├── auth/
│   │   │   └── user/
│   │   └── resources/
│   │       ├── application.properties
│   │       └── db/migration/
│   └── test/
