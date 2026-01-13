# Tools and Workflows

> How we share work, demonstrate progress, and collaborate on code.

---

## Required Tools Overview

| Tool | Purpose | Why We Use It |
|------|---------|---------------|
| **Git + GitHub** | Version control, code sharing | Public repos enable review without access management |
| **Loom** (or similar) | Screencasts | Async demos, explaining your work |
| **Cloud Hosting** | Live demos | Show working apps, not just code |
| **Microsoft Teams** | Communication | See [[01-Teams-Getting-Started]] |

---

## Git and GitHub

### Public Repositories Required

All intern work should be in **public GitHub repositories**.

**Why public?**
- Mentors can review without managing access permissions
- Builds your portfolio
- Enables community learning
- No confidential data is involved (we work with open-source codebases)

### Repository Setup

1. Create a GitHub account (if you don't have one)
2. Create a new public repository for your internship project
3. Use a clear naming convention: `[project-name]-[your-name]` or similar
4. Include a README explaining your project

### What Belongs in Your Repo

| Include | Don't Include |
|---------|---------------|
| Your code and scripts | API keys or secrets |
| README with setup instructions | Personal data |
| Documentation of your approach | Large binary files |
| Test files | Node modules / build artifacts (use .gitignore) |

### Commit Practices

- Commit regularly (at least daily when working)
- Write meaningful commit messages
- Your commit history tells the story of your learning

**Good commit message:**
```
feat: add tree-sitter parsing for Python files

- Implemented AST extraction using tree-sitter-python
- Handles function and class definitions
- Added unit tests for basic parsing
```

**Bad commit message:**
```
fixed stuff
```

---

## Screencasting with Loom

### Why Screencasts?

We're a remote-only program. Screencasts let you:
- Explain your work asynchronously
- Demonstrate understanding (not just code)
- Build presentation skills
- Share with the community for feedback

### Getting Started with Loom

1. Sign up at [loom.com](https://www.loom.com) (free tier is sufficient)
2. Install the browser extension or desktop app
3. Record yourself explaining + showing your screen

### Alternatives to Loom

| Tool | Notes |
|------|-------|
| Loom | Recommended, easy sharing |
| OBS Studio | Free, more features, steeper learning curve |
| Screen recording (OS built-in) | macOS: Cmd+Shift+5, Windows: Xbox Game Bar |
| CloudApp | Similar to Loom |

### What Makes a Good Screencast

| Good | Not Good |
|------|----------|
| 3-7 minutes focused | 30+ minute rambling |
| Clear audio | Background noise, mumbling |
| Shows the work AND explains the thinking | Just clicking through silently |
| Prepared structure | "Um, let me find that file..." |

### Recording Tips

1. **Prepare**: Know what you'll show before recording
2. **Audio**: Use a decent microphone, minimize background noise
3. **Screen**: Clean up your desktop, close unrelated tabs
4. **Pace**: Speak clearly, pause at key points
5. **Length**: Aim for 5 minutes, max 10 minutes

### Video-On Requirement

**Keep your camera ON during screencasts.**

| Requirement | Why |
|-------------|-----|
| Face visible in recording | Confirms you're the person presenting your work |
| Same face as profile picture | Identity verification |
| Natural lighting, clear view | Professionalism, recognizability |

This is required for:
- Weekly progress screencasts
- Pre-internship submission videos
- Demo recordings shared with mentors

**Why we ask for this:**
- Ensures the work is genuinely yours
- Builds trust and accountability
- Prepares you for professional presentations
- Creates a verifiable record of your contributions

### When to Create Screencasts

- Weekly progress updates
- Explaining a complex solution
- Pre-internship requirements submission
- Demo preparation (practice run)

---

## Cloud Hosting for Demos

### Why Host Your Apps?

"It works on my machine" doesn't demonstrate capability. A hosted demo:
- Proves it actually works
- Lets mentors test without setup
- Shows deployment skills
- Creates a shareable portfolio piece

### Free Hosting Options

| Platform | Best For | Free Tier |
|----------|----------|-----------|
| **Vercel** | Frontend, Next.js | Generous free tier |
| **Railway** | Backend, databases | 500 hours/month free |
| **Render** | Full stack | Free tier available |
| **Fly.io** | Containers | Free allowance |
| **GitHub Pages** | Static sites | Free for public repos |
| **Netlify** | Frontend, static | Free tier available |

### What to Host

| Project Type | Hosting Suggestion |
|--------------|-------------------|
| Static frontend | Vercel, Netlify, GitHub Pages |
| Node.js backend | Railway, Render, Fly.io |
| Python backend | Railway, Render |
| Full stack app | Railway (backend) + Vercel (frontend) |
| CLI tools | Provide clear install instructions instead |

### Deployment Checklist

- [ ] App runs without errors
- [ ] Environment variables configured (not hardcoded secrets)
- [ ] README includes the live URL
- [ ] Basic functionality works (test it!)
- [ ] Load time is reasonable

---

## Workflow: Submitting Your Work

### Weekly Submission Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WEEKLY SUBMISSION WORKFLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. CODE        Push your work to public GitHub repo                │
│                                                                      │
│  2. DOCUMENT    Update README with what you built this week         │
│                                                                      │
│  3. RECORD      Create a Loom explaining your progress              │
│                                                                      │
│  4. DEPLOY      Host the latest version (if applicable)             │
│                                                                      │
│  5. SHARE       Post links in your Teams channel                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### What Mentors Look For

| Area | We Evaluate |
|------|-------------|
| **Code** | Working functionality, clean structure, good practices |
| **Documentation** | Clear README, explained approach |
| **Communication** | Screencast clarity, ability to explain technical concepts |
| **Initiative** | Going beyond minimum, solving problems independently |
| **Progress** | Steady improvement, learning from feedback |

---

## Summary: Tool Setup Checklist

Before your first week:

- [ ] GitHub account created
- [ ] Public repo set up with README
- [ ] Loom (or alternative) account created
- [ ] Test recording done
- [ ] Cloud hosting account created (choose based on your project type)
- [ ] Microsoft Teams fully set up (see [[01-Teams-Getting-Started]])

---

## Getting Help with Tools

- **Git issues**: Post in Support channel with specific error messages
- **Hosting problems**: Include the platform, error logs, and what you tried
- **Recording questions**: Share a draft for feedback

Don't suffer in silence — ask for help after you've tried solving it yourself.

---

*Last Updated: 2026-01-13*
