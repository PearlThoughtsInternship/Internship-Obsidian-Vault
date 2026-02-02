# Before You Begin

> **Read this first.** It sets the context for everything that follows.

---

## First: Set Up Your Communication Tools

Before diving into the technical content, ensure you can participate in the program:

| Step | Guide |
|------|-------|
| 1. Set up Microsoft Teams | [Teams Setup](../../How-We-Communicate/01-Teams-Getting-Started.md) |
| 2. Understand communication channels | [Communication Protocol](../../How-We-Communicate/02-Communication-Protocol.md) |
| 3. Know the live session format | [Live Sessions](../../How-We-Communicate/03-Live-Sessions.md) |
| 4. Get your tools ready (Git, SSH keys) | [Tools & Workflows](../../How-We-Communicate/04-Tools-and-Workflows.md) |

---

## The Reality of This Internship

We're a **small organization** with limited time and resources. We offered this internship **without any fee** because we believe in growing the next generation of platform engineers. But we need you to understand something important:

**You're not joining an Ops team. You're founding the infrastructure of a startup.**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE PLATFORM ENGINEERING MINDSET                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Traditional Ops:                                                        │
│  ├── "Wait for tickets"                                                 │
│  ├── "Run the same scripts"                                             │
│  ├── "Watch dashboards"                                                 │
│  └── "React to incidents"                                               │
│                                                                          │
│  Platform Engineering (This Program):                                   │
│  ├── "Build systems that prevent tickets"                               │
│  ├── "Automate everything"                                              │
│  ├── "Create dashboards that matter"                                    │
│  └── "Design for resilience"                                            │
│                                                                          │
│  You're not maintaining infrastructure.                                  │
│  You're BUILDING the platform that could run the next OpenClaw.         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## What This Means for You

### We Understand

- **Infrastructure is complex** — networking, Kubernetes, IaC have steep learning curves
- **Remote work is hard** — no one sitting next to you to debug SSH issues
- **Cloud providers are overwhelming** — AWS has 200+ services
- **Security is non-obvious** — what feels secure often isn't

### We Commit To

- **Sharing real-world patterns** we use in production
- **Reviewing your infrastructure code** and giving feedback
- **Answering architecture questions** when you're truly stuck

### We Expect You To

- **Research first, ask second** — Google the error, read the docs, try things
- **Show working systems** — not just "I read about Kubernetes"
- **Document your decisions** — "I chose X because Y, trade-off is Z"
- **Break things and learn** — this is a sandbox, experiment boldly

---

## The Startup Test

Your performance this week determines whether we continue together. We have limited mentorship capacity — we invest it in people who demonstrate they can:

1. **Debug independently** — when Terraform fails, what do you do?
2. **Learn from documentation** — can you figure out a new tool from its docs?
3. **Ship working infrastructure** — can you stand up a real VM, not just read about it?
4. **Communicate clearly** — can you explain what you built and why?

This is not about being harsh. It's about being honest: startups need people who ship.

---

## How to Ask Good Questions

When you're stuck, don't just say "Terraform doesn't work."

**Bad question:**
> "How do I deploy a Kubernetes cluster?"

**Good question:**
> "I'm trying to deploy k3s on Hetzner using Ansible. I followed the quickstart guide and modified the inventory for my VMs. When I run the playbook, I get 'SSH connection refused' for the second node. I've verified:
> - SSH key is on the node (can connect manually)
> - Firewall allows port 22
> - Ansible inventory has correct IP
> Here's my inventory file: [code]. What am I missing?"

The difference:
- Shows you tried
- Shows what you learned
- Shows specific blockers
- Includes relevant details
- Respects our time

---

## Required Tools Setup

Before Week 1 starts, you need:

### Local Development

| Tool | Purpose | Install |
|------|---------|---------|
| **Git** | Version control | `brew install git` |
| **OpenTofu** | Infrastructure-as-Code | `brew install opentofu` |
| **Ansible** | Configuration management | `pip install ansible` |
| **kubectl** | Kubernetes CLI | `brew install kubectl` |
| **k9s** | Kubernetes TUI | `brew install k9s` |
| **Helm** | Package manager | `brew install helm` |

### Cloud Access

| Provider | What You Need | How to Get It |
|----------|---------------|---------------|
| **Hetzner** | API token | Create account, generate in Console |
| **GitHub** | SSH key, PAT | Settings → SSH keys, Developer settings |
| **Container Registry** | ghcr.io access | Automatic with GitHub |

### Knowledge Prerequisites

| Topic | Minimum Level | Resources |
|-------|---------------|-----------|
| **Linux CLI** | Navigate, edit files, SSH | Linux Journey |
| **Git** | Commit, branch, merge, PR | Git docs |
| **YAML** | Read and write | Learn X in Y minutes |
| **Networking** | IP, ports, DNS, HTTP | Computer Networking basics |
| **Containers** | Build and run Docker | Docker Get Started |

---

## Your Opportunity

If you pass this week:
- You get **3 more weeks** of building real infrastructure
- You work on **production-grade patterns**
- You build **portfolio-worthy projects**
- You get **references** for future opportunities

If you demonstrate exceptional initiative:
- Extended internship opportunities
- Potential project collaboration
- Direct mentorship on advanced topics

---

## The Builder's Manifesto

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      PLATFORM ENGINEER'S CREED                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  I build systems that enable others to ship faster.                      │
│                                                                          │
│  I automate toil so humans can focus on what matters.                   │
│                                                                          │
│  I design for failure because failures are inevitable.                  │
│                                                                          │
│  I document because future-me is a stranger who deserves context.       │
│                                                                          │
│  I measure because hope is not a strategy.                              │
│                                                                          │
│  I secure by default because breaches are catastrophic.                 │
│                                                                          │
│  I test in production because staging is a lie.                         │
│  (But I have feature flags and rollback strategies.)                    │
│                                                                          │
│  I own my mistakes publicly and fix them faster.                        │
│                                                                          │
│  I ship.                                                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ready?

Now proceed to:
1. [Week by Week Guide](./02-Week-by-Week.md) — the 4-week plan
2. [What You Build](./03-What-You-Build.md) — technical deliverables
3. [Your Role](./04-Your-Role.md) — understand platform engineering

Then jump to [Environment Setup](./Exercises/01-Environment-Setup.md) for your Week 1 tasks.

---

*We're rooting for you. Now show us what you can build.*
