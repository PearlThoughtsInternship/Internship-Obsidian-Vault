# Before You Begin

> *"The most dangerous phrase in the language is, 'We've always done it this way.'"*
> — **Rear Admiral Grace Hopper**

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

```mermaid
flowchart TB
    subgraph Traditional["Traditional Ops"]
        T1["Wait for tickets"]
        T2["Run the same scripts"]
        T3["Watch dashboards"]
        T4["React to incidents"]
    end

    subgraph Platform["Platform Engineering (This Program)"]
        P1["Build systems that prevent tickets"]
        P2["Automate everything"]
        P3["Create dashboards that matter"]
        P4["Design for resilience"]
    end

    Traditional -.->|"NOT this"| X["❌"]
    Platform -.->|"THIS"| Y["✅"]

    Result["You're BUILDING the platform<br/>that could run the next OpenClaw"]

    Platform --> Result
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

```mermaid
flowchart LR
    subgraph Skills["Skills We're Looking For"]
        S1["Debug independently"]
        S2["Learn from documentation"]
        S3["Ship working infrastructure"]
        S4["Communicate clearly"]
    end

    subgraph Questions["The Questions"]
        Q1["When Terraform fails,<br/>what do you do?"]
        Q2["Can you figure out a new tool<br/>from its docs?"]
        Q3["Can you stand up a real VM,<br/>not just read about it?"]
        Q4["Can you explain what you built<br/>and why?"]
    end

    S1 --> Q1
    S2 --> Q2
    S3 --> Q3
    S4 --> Q4
```

This is not about being harsh. It's about being honest: **startups need people who ship**.

---

## How to Ask Good Questions

When you're stuck, don't just say "Terraform doesn't work."

### Bad Question

> "How do I deploy a Kubernetes cluster?"

### Good Question

> "I'm trying to deploy k3s on Hetzner using Ansible. I followed the quickstart guide and modified the inventory for my VMs. When I run the playbook, I get 'SSH connection refused' for the second node. I've verified:
> - SSH key is on the node (can connect manually)
> - Firewall allows port 22
> - Ansible inventory has correct IP
> Here's my inventory file: [code]. What am I missing?"

```mermaid
flowchart LR
    subgraph Good["Good Question Anatomy"]
        G1["Shows you tried"]
        G2["Shows what you learned"]
        G3["Shows specific blockers"]
        G4["Includes relevant details"]
        G5["Respects our time"]
    end
```

---

## Required Tools Setup

Before Week 1 starts, you need:

### Local Development

| Tool | Purpose | Install |
|------|---------|---------||
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
|-------|---------------|-----------||
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

> *"If it hurts, do it more frequently, and bring the pain forward."*
> — **Continuous Delivery** (Humble & Farley)

```mermaid
mindmap
  root((Platform<br/>Engineer's<br/>Creed))
    Build
      Enable others to ship faster
      Automate toil
    Design
      Design for failure
      Measure everything
    Secure
      Secure by default
      Breaches are catastrophic
    Test
      Test in production
      Feature flags + rollback
    Own
      Own mistakes publicly
      Fix them faster
    Ship
      I SHIP
```

### The Principles

1. **I build systems that enable others to ship faster.**
2. **I automate toil so humans can focus on what matters.**
3. **I design for failure because failures are inevitable.**
4. **I document because future-me is a stranger who deserves context.**
5. **I measure because hope is not a strategy.**
6. **I secure by default because breaches are catastrophic.**
7. **I test in production because staging is a lie.** (But I have feature flags and rollback strategies.)
8. **I own my mistakes publicly and fix them faster.**
9. **I ship.**

---

## Ready?

Now proceed to:
1. [Week by Week Guide](./02-Week-by-Week.md) — the 4-week plan
2. [What You Build](./03-What-You-Build.md) — technical deliverables
3. [Your Role](./04-Your-Role.md) — understand platform engineering

Then jump to [Environment Setup](./Exercises/01-Environment-Setup.md) for your Week 1 tasks.

---

*We're rooting for you. Now show us what you can build.*
