# Pull Request (PR) Workflow – Mandatory

You must follow the below guidelines while creating branches, working on tasks, and raising Pull Requests.  
These rules are **mandatory** and will be used for evaluation.

---

### References

- [NestJS Official Website](https://nestjs.com/)  
--------------- XX -------------  
- [TypeORM Getting Started](https://typeorm.io/docs/getting-started)  
--------------- XX -------------

---

### Backend Details

- **Framework:** Nest.js  
- **Language:** TypeScript  
- **Database:** PostgreSQL (managed via TypeORM)

---

## Pair Programming – Mandatory

You must form pairs with people within your respective team.

Pair programming means **two people working together on the same piece of code**.

### How Pair Programming Works

- 👨‍💻 **Driver**
  - Writes the code
  - Focuses on implementation

- 🧠 **Navigator**
  - Reviews each line of code
  - Thinks about the bigger picture
  - Suggests improvements and identifies issues

Roles **must be switched regularly** to ensure collaboration and shared ownership.

### PR & Loom Recording Requirement

- Raise a **Pull Request** for the task worked on during pair programming
- Record a **Loom video** explaining **your individual contribution**
- Share the **Loom recording link in the Pull Request description**
- Clearly explain:
  - What you worked on
  - Decisions you contributed
  - Challenges you solved

---

## Step 1: Create Your Own Main Branch (One-Time Setup)

If you haven’t created your intern main branch yet:

git checkout -b intern/your-name-main  
git push origin intern/your-name-main

---

## Step 2: Create Your First Feature Branch (Base: Intern Main Branch)

git checkout intern/your-name-main  
git add .  
git commit -m "commit-message"  
git checkout -b feature1/feature-name  
git push origin feature1/feature-name

---

## Step 3: Raise Pull Request

Raise a PR from:

feature1/feature-name → intern/your-name-main

- Add your respective **reviewer / mentor**
- **Do NOT wait** for the reviewer
- Immediately start working on the next feature

---

## Step 4: Create Next Feature Branch (Avoid Merge Conflicts)

To avoid merge conflicts, work on the next feature using the **previous feature branch as base**:

git checkout feature1/feature-name  
git add .  
git commit -m "commit-message"  
git checkout -b feature2/feature-name  
git push origin feature2/feature-name

---

## Step 5: Raise PR for the New Feature

Raise PR from:

feature2/feature-name → feature1/feature-name

### What This Does

- PR shows **only new changes** in feature2
- Changes from feature1 are excluded
- Reviewer focuses only on what’s different

---

## Step 6: Update PR Base After Merge

Once feature1/feature-name is merged into intern/your-name-main:

- Edit the open PR of feature2
- Change the base branch to:

intern/your-name-main

---

## Step 7: Repeat for Every New Feature

- Create each new feature from the **latest feature branch**
- Raise PR against the **previous feature**
- Update PR base after merge

---

### Quick Reference

- **Main Branch:** intern/<your-name>-main  
- **Feature Branch:** feature<number>/<feature-name>  
- **PR Frequency:** Daily  
- **Reviewer:** Mandatory  
- **Loom Recording:** Mandatory for pair programming  
- **Direct Main Commits:** Not allowed  

---

*Last Updated: [[2025-09-10]]*
