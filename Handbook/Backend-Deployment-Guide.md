# Backend Deployment & Repository Sync Guide

This document explains how to deploy the backend to **Render** and how to keep the **organization repository** and **personal repository** in sync for automatic redeployment.

---

## Step 1: Deploy Backend to Render

### Login to Render
- Login to Render
- Go to your **Dashboard**

---

### Create a PostgreSQL Database

1. Click **New** → **PostgreSQL**
2. Choose the **same region** you’ll use for your backend service
3. Copy the **External Database URL**
   - This will be used in backend environment variables

---

### Create a Web Service for Backend

1. Click **New** → **Web Service**
2. Connect it to the **GitHub repository** you just pushed
3. Select the correct branch (usually `main` or `master`)
4. Choose the **same region** as your database

---

### Configure the Web Service

#### Build Command
Use according to your setup:
- `npm install`
- `yarn install`
- `pip install -r requirements.txt`

#### Start Command
Use according to your setup:
- `npm start`
- `yarn start`
- `python app.py`

---

### Environment Variables

Add the following environment variables in Render:

- `DATABASE_URL` → Paste the PostgreSQL **External Database URL**
- Add any other required `.env` variables

---

### Deploy the Service

- Click **Deploy**
- Render will automatically:
  - Build your application
  - Deploy the backend service

---

## Step 2: Verify Deployment

- Visit the **Render-provided URL**
- Confirm the backend service is running
- Test API endpoints:
  - Using **Postman**
  - Or via browser (if applicable)
- Verify database connectivity

---

## How to Keep the Org Repo and Local Repo in Sync

### General Scenario

- Working in the **organization repository branch** (example: `1308harshit`)
- Deploying from the **main branch of your personal GitHub repository**
- Render is connected to your **personal GitHub repo**
- Goal: Sync org repo changes → personal main branch → auto redeploy

---

### One-Time Setup (Add Upstream Remote)

In your **local clone of your personal GitHub repository**:

```bash
git remote add upstream https://github.com/org-name/org-repo.git
