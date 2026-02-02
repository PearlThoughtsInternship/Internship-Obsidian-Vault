# Your Role: Platform Engineer

> *"A Platform team enables stream-aligned teams to deliver work with substantial autonomy."*
> — **Team Topologies** (Skelton & Pais)

## What Platform Engineers Do

> *Platform engineers build the roads that let developers drive fast without crashing. We create leverage—one hour of platform work saves hundreds of developer hours.*

---

## Platform Engineer vs DevOps vs SRE

```mermaid
flowchart TB
    subgraph Roles["Role Comparison"]
        subgraph DevOps["DevOps Engineer"]
            D1["Focus: Pipeline automation"]
            D2["Build CI/CD workflows"]
            D3["Bridge dev and ops teams"]
            D4["Tool-centric"]
        end

        subgraph SRE["Site Reliability Engineer"]
            S1["Focus: System reliability"]
            S2["Error budgets and SLOs"]
            S3["Incident response"]
            S4["Toil reduction"]
        end

        subgraph PE["Platform Engineer"]
            P1["Focus: Developer experience"]
            P2["Build internal platforms"]
            P3["Enable self-service"]
            P4["Product mindset"]
        end
    end

    DevOps -->|"Evolved into"| PE
    SRE -->|"Practices inform"| PE

    style PE fill:#4CAF50
```

### Role Characteristics

| Aspect | DevOps | SRE | Platform Engineering |
|--------|--------|-----|----------------------|
| **Primary Focus** | Process automation | Reliability | Developer productivity |
| **Customers** | Development teams | End users | Developers (internal) |
| **Metrics** | Deployment frequency | SLOs, error budgets | DORA metrics, adoption |
| **Output** | Pipelines, scripts | Runbooks, incident response | Self-service platforms |
| **Mindset** | Tool-centric | Operations-centric | Product-centric |

---

## The Platform Engineer Mindset

> *"The Three Ways: Flow (left to right), Feedback (right to left), and Continual Learning and Experimentation."*
> — **The Phoenix Project** (Kim, Behr, Spafford)

```mermaid
mindmap
  root((Platform<br/>Engineer))
    Product Thinking
      Developers are customers
      Platform is a product
      Measure adoption, satisfaction
      Iterate based on feedback
    Systems Thinking
      See connections
      Anticipate failure modes
      Design for resilience
      Understand trade-offs
    Automation First
      If you do it twice, automate
      Code over click
      GitOps everything
      Self-service > tickets
    Security Mindset
      Zero trust by default
      Defense in depth
      Shift left
      Least privilege
```

---

## Daily Responsibilities

```mermaid
flowchart LR
    subgraph Morning["Morning"]
        M1["Check alerts, dashboards"]
        M2["Review PRs"]
        M3["Triage issues"]
    end

    subgraph Build["Build Time"]
        B1["Design infrastructure"]
        B2["Write IaC code"]
        B3["Build automation"]
        B4["Create documentation"]
    end

    subgraph Support["Support"]
        S1["Unblock developers"]
        S2["Investigate issues"]
        S3["Improve golden paths"]
    end

    subgraph Learn["Continuous Learning"]
        L1["Research new tools"]
        L2["Evaluate trade-offs"]
        L3["Share knowledge"]
    end

    Morning --> Build --> Support --> Learn
```

### Typical Day Breakdown

| Activity | Time | Examples |
|----------|------|----------|
| **Observability Review** | 30 min | Check Grafana, review overnight alerts |
| **Deep Work: Building** | 4 hours | OpenTofu modules, Ansible playbooks, CLI tools |
| **Code Review** | 1 hour | Review infrastructure PRs, provide feedback |
| **Developer Support** | 1 hour | Unblock teams, answer questions, debug issues |
| **Documentation** | 1 hour | Update runbooks, write ADRs, improve guides |
| **Learning** | 30 min | Read docs, try new tools, attend talks |

---

## Core Skills

> *"Toil is the kind of work that tends to be manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows."*
> — **Site Reliability Engineering** (Google)

### Technical Skills

```mermaid
flowchart TB
    subgraph Core["Core Skills"]
        direction TB
        IaC["Infrastructure as Code<br/>(OpenTofu, Terraform)"]
        K8s["Container Orchestration<br/>(Kubernetes, k3s)"]
        CM["Configuration Management<br/>(Ansible)"]
        CI["CI/CD<br/>(GitHub Actions, ArgoCD)"]
    end

    subgraph Advanced["Advanced Skills"]
        direction TB
        Obs["Observability<br/>(Prometheus, Grafana)"]
        Sec["Security<br/>(Network Policies, RBAC)"]
        Net["Networking<br/>(Service Mesh, DNS)"]
        Auto["Automation<br/>(Python, Go)"]
    end

    subgraph Soft["Soft Skills"]
        direction TB
        Comm["Communication"]
        Doc["Documentation"]
        Debug["Debugging"]
        Teach["Teaching"]
    end

    Core --> Advanced --> Soft

    style IaC fill:#326CE5
    style K8s fill:#326CE5
```

### Skill Progression

| Level | Skills | Outcomes |
|-------|--------|----------|
| **Junior** | Linux, Git, Docker, basic Ansible | Deploy single apps, follow runbooks |
| **Mid** | OpenTofu, Kubernetes, CI/CD, monitoring | Design modules, build pipelines |
| **Senior** | Architecture, security, automation, strategy | Lead platform initiatives, mentor |
| **Staff** | Org-wide impact, vendor evaluation, culture | Shape technical direction |

---

## Your Internship Journey

```mermaid
gantt
    title Platform Engineering Internship
    dateFormat  YYYY-MM-DD
    section Week 1
    Foundation & IaC           :w1, 2026-02-03, 5d
    section Week 2
    Kubernetes & Orchestration :w2, after w1, 5d
    section Week 3
    GitOps & Automation        :w3, after w2, 5d
    section Week 4
    Production Readiness       :w4, after w3, 5d
```

### Week-by-Week Growth

| Week | You Start As | You End As |
|------|--------------|------------|
| **Week 1** | "I can SSH into a server" | "I provision infrastructure with code" |
| **Week 2** | "I can run kubectl commands" | "I manage a HA Kubernetes cluster" |
| **Week 3** | "I manually deploy apps" | "I have GitOps automating everything" |
| **Week 4** | "I hope it doesn't break" | "I have monitoring, alerting, and runbooks" |

---

## The Builder's Checklist

### Before You Build

```mermaid
flowchart TD
    A["Have an idea"] --> B{"Exists already?"}
    B -->|"Yes"| C["Use/extend existing"]
    B -->|"No"| D{"Documented need?"}
    D -->|"No"| E["Document the problem first"]
    D -->|"Yes"| F{"Multiple solutions?"}
    F -->|"Yes"| G["Evaluate trade-offs"]
    F -->|"No"| H["Build it"]
    G --> H
    C --> I["Done"]
    H --> I

    style E fill:#FFC107
    style G fill:#FFC107
```

### Building Checklist

- [ ] **Problem documented** — What am I solving? Why does it matter?
- [ ] **Alternatives evaluated** — Is there an existing solution?
- [ ] **Design reviewed** — Did I get feedback before building?
- [ ] **Tests written** — How will I know it works?
- [ ] **Documentation updated** — Can someone else use this?
- [ ] **Monitoring added** — How will I know if it breaks?

---

## Communication Patterns

### How to Ask for Help

```mermaid
flowchart TD
    Stuck["Stuck on problem"] --> Research["1. Research first<br/>(30 min minimum)"]
    Research --> Document["2. Document what you tried"]
    Document --> Question["3. Form specific question"]
    Question --> Ask["4. Ask with context"]

    subgraph Good["Good Question Anatomy"]
        G1["What I'm trying to do"]
        G2["What I tried"]
        G3["What happened"]
        G4["What I expected"]
        G5["Relevant code/config"]
    end

    Ask --> Good
```

### Question Template

```markdown
## Context
I'm working on [task] in [project].

## Goal
I'm trying to [specific goal].

## What I Tried
1. [First approach] — [what happened]
2. [Second approach] — [what happened]

## Error/Behavior
```
[paste error message or unexpected behavior]
```

## Expected
I expected [specific expected behavior].

## Question
[Specific question about the blocker]
```

---

## Career Path

```mermaid
flowchart LR
    subgraph Entry["Entry Level"]
        J1["Junior Platform<br/>Engineer"]
    end

    subgraph Mid["Mid Level"]
        M1["Platform<br/>Engineer"]
        M2["DevOps<br/>Engineer"]
    end

    subgraph Senior["Senior Level"]
        S1["Senior Platform<br/>Engineer"]
        S2["Platform<br/>Architect"]
    end

    subgraph Staff["Staff+ Level"]
        ST1["Staff Platform<br/>Engineer"]
        ST2["Principal<br/>Engineer"]
        ST3["Engineering<br/>Manager"]
    end

    J1 --> M1 & M2
    M1 --> S1 --> ST1 --> ST2
    M1 --> S2 --> ST2
    S1 --> ST3

    style J1 fill:#81C784
    style ST1 fill:#4CAF50
    style ST2 fill:#2E7D32
```

### What Gets You Promoted

| From → To | What Demonstrates Readiness |
|-----------|----------------------------|
| **Junior → Mid** | Owns features end-to-end, unblocks self |
| **Mid → Senior** | Designs systems, mentors juniors, handles ambiguity |
| **Senior → Staff** | Org-wide impact, technical strategy, grows others |

---

## Resources for Growth

### Books

| Book | Focus |
|------|-------|
| *Site Reliability Engineering* (Google) | SRE principles |
| *The Phoenix Project* | DevOps culture |
| *Infrastructure as Code* (Kief Morris) | IaC patterns |
| *Kubernetes Up & Running* | Container orchestration |
| *Team Topologies* | Platform team design |

### Certifications (Optional)

| Certification | Value |
|---------------|-------|
| CKA (Certified Kubernetes Administrator) | Validates K8s skills |
| AWS Solutions Architect | Cloud architecture |
| HashiCorp Terraform Associate | IaC fundamentals |

### Communities

- **CNCF Slack** — Cloud-native discussions
- **r/devops, r/kubernetes** — Peer learning
- **Platform Engineering Slack** — Platform-specific
- **Local meetups** — Networking

---

## Your Success Metrics

### During Internship

| Metric | Target | How |
|--------|--------|-----|
| **Infrastructure deployed** | Full cluster | Week 2 |
| **Automation coverage** | 80%+ GitOps | Week 3 |
| **Documentation** | Complete | Week 4 |
| **Demo quality** | Production-grade | Week 4 |

### After Internship

| Metric | Sign of Success |
|--------|-----------------|
| **Portfolio** | Can demonstrate what you built |
| **Knowledge** | Can explain architectural decisions |
| **Network** | Have references for future opportunities |
| **Skills** | Can interview for platform roles |

---

## Related

- [Week by Week](./02-Week-by-Week.md)
- [What You Build](./03-What-You-Build.md)
- [Architecture](../02-Engineering/01-Architecture.md)

---

*Last Updated: 2026-02-02*
