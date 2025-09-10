# Quick Start Guide

## 🚀 Your First Day Checklist

Welcome! Follow this checklist to get started quickly.

## 🎯 Day 1 Setup

### ✅ Essential Tasks

#### 1. Access and Accounts
- [ ] Check email for welcome message
- [ ] Join MS Teams with provided credentials
- [ ] Request GitHub access from Abhi
- [ ] Set up 2FA for all accounts
- [ ] Test all login credentials

#### 2. Communication Setup
- [ ] Join assigned team channel
- [ ] Join Internship channel
- [ ] Join Support channel
- [ ] Join DevOps channel
- [ ] Introduce yourself in team channel

#### 3. Development Environment
```bash
# Essential tools installation

# Node.js and npm
node --version  # Should be 18.x or higher
npm --version   # Should be 8.x or higher

# Git
git --version   # Should be 2.x or higher
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Code Editor (VS Code recommended)
code --version  # Install from https://code.visualstudio.com
```

#### 4. Project Setup

##### Backend Developers
```bash
# Install NestJS CLI
npm i -g @nestjs/cli

# Create project
nest new project-name
cd project-name

# Install dependencies
npm install

# Start development server
npm run start:dev
```

##### Full Stack Developers
```bash
# Frontend setup
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install
npm run dev

# Backend setup (in new terminal)
nest new backend
cd backend
npm install
npm run start:dev
```

##### AI Interns
```bash
# Python setup
python --version  # Should be 3.8 or higher
pip --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install essential packages
pip install numpy pandas scikit-learn jupyter
```

#### 5. Database Setup

##### PostgreSQL Installation
```bash
# macOS
brew install postgresql
brew services start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/

# Linux
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

##### Create Database
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE internship_db;

-- Create user
CREATE USER intern_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE internship_db TO intern_user;
```

## 📅 Daily Routine

### Morning (10:00 AM - 12:00 PM)
1. **10:00 AM**: Join training session
2. **10:15 AM**: Daily standup in team channel
3. **10:30 AM**: Receive task assignments
4. **11:00 AM**: Start working on tasks

### Afternoon (12:00 PM - 3:00 PM)
1. **12:00 PM**: Continue task implementation
2. **1:00 PM**: Lunch break
3. **2:00 PM**: Resume work / pair programming

### Evening (3:00 PM - 6:00 PM)
1. **3:00 PM**: Code review and testing
2. **4:30 PM**: Prepare pull request
3. **5:00 PM**: Submit PR and daily update
4. **5:30 PM**: Document learnings

## 🔧 Essential Commands

### Git Workflow
```bash
# Clone repository
git clone [repository-url]
cd [repository-name]

# Create new branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push changes
git push origin feature/your-feature-name

# Create PR via GitHub UI
```

### Project Commands

#### NestJS
```bash
npm run start          # Start application
npm run start:dev      # Start with hot-reload
npm run test          # Run tests
npm run test:watch    # Run tests in watch mode
npm run build         # Build for production
```

#### Next.js
```bash
npm run dev           # Start development server
npm run build         # Build for production
npm run start         # Start production server
npm run lint          # Run linter
npm run test          # Run tests
```

## 📡 API Testing with Hoppscotch

### Setup
1. Go to [hoppscotch.io](https://hoppscotch.io)
2. Create new collection: "Internship APIs"
3. Set base URL: `http://localhost:3000`

### Example Requests

#### POST - User Registration
```json
{
  "url": "http://localhost:3000/api/v1/auth/signup",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }
}
```

## 📝 First PR Guidelines

### PR Title Format
```
[Type]: Brief description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style
- refactor: Code refactoring
- test: Tests
- chore: Maintenance
```

### Commit Message Format
```bash
# Good examples
git commit -m "feat: add user authentication endpoint"
git commit -m "fix: resolve database connection issue"
git commit -m "docs: update API documentation"

# Bad examples
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "work in progress"
```

## 🌐 Useful Resources

### Documentation
- [NestJS Docs](https://docs.nestjs.com)
- [Next.js Docs](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

### Learning Platforms
- [freeCodeCamp](https://www.freecodecamp.org)
- [MDN Web Docs](https://developer.mozilla.org)
- [Stack Overflow](https://stackoverflow.com)

### Tools
- [VS Code](https://code.visualstudio.com)
- [Postman](https://www.postman.com)
- [Git](https://git-scm.com)
- [Docker](https://www.docker.com)

## ⚠️ Common Issues & Solutions

### Issue: Cannot connect to database
```bash
# Solution
1. Check PostgreSQL is running
   sudo systemctl status postgresql
   
2. Verify credentials in .env file
   DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
   
3. Test connection
   psql -U username -d database_name
```

### Issue: Port already in use
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process
kill -9 [PID]  # macOS/Linux
taskkill /PID [PID] /F  # Windows
```

### Issue: Module not found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run start:dev
```

## 📞 Getting Help

### Priority Order
1. Check this documentation
2. Search in team channel
3. Ask teammates
4. Post in Support channel
5. Contact mentor during office hours
6. Email hr@pearlthoughts.com for admin issues

## 🏁 Success Tips

### Do's
- ✅ Ask questions early
- ✅ Document your learning
- ✅ Help teammates
- ✅ Test thoroughly
- ✅ Commit frequently

### Don'ts
- ❌ Don't skip training sessions
- ❌ Don't wait until deadline
- ❌ Don't ignore errors
- ❌ Don't copy without understanding
- ❌ Don't forget daily PR

---

*Remember: Everyone starts somewhere. Focus on learning and improving every day!*

---

*Last Updated: [[2025-09-10]]*
*Next: [[../Handbook/Welcome|Welcome Guide]] | [[../Programme-Structure/Weekly-Plans|Weekly Plans]]*