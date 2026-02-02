# Week-by-Week Guide

## Your Mission (4 Weeks)

> *Design, build, deploy, and operate a production-grade infrastructure platform for an AI-native startup.*

---

## End-to-End Ownership

Unlike typical internships where you support an existing team, **you own everything end-to-end**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        YOUR OWNERSHIP SCOPE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WEEK 1: FOUNDATION                                                      │
│  └── Design infrastructure architecture                                 │
│  └── Set up cloud accounts and access                                   │
│  └── Build first OpenTofu modules                                       │
│  └── Write first Ansible playbooks                                      │
│                                                                          │
│  WEEK 2: ORCHESTRATION                                                   │
│  └── Deploy k3s cluster (HA configuration)                              │
│  └── Install core platform services                                     │
│  └── Configure networking and storage                                   │
│  └── Deploy first workload                                              │
│                                                                          │
│  WEEK 3: AUTOMATION                                                      │
│  └── Implement GitOps with ArgoCD                                       │
│  └── Set up CI/CD pipelines                                             │
│  └── Build observability stack                                          │
│  └── Create Python automation tools                                     │
│                                                                          │
│  WEEK 4: PRODUCTION READINESS                                           │
│  └── Security hardening                                                 │
│  └── Disaster recovery testing                                          │
│  └── Documentation and runbooks                                         │
│  └── Demo and presentation                                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Week 1: Foundation Phase

### Goal: Cloud Infrastructure & Configuration Management

Before you can orchestrate containers, you need infrastructure. This week you build the foundation.

### Day 1-2: Environment Setup

| Task | Deliverable | Time |
|------|-------------|------|
| Set up Hetzner account | API token generated | 1h |
| Install local tools | OpenTofu, Ansible, kubectl working | 2h |
| Create GitHub repo | `infra` repository with structure | 1h |
| First VM via OpenTofu | Single VM accessible via SSH | 4h |

### Day 3-4: OpenTofu Mastery

| Task | Deliverable | Time |
|------|-------------|------|
| Module for VMs | Reusable `hetzner-server` module | 4h |
| Network configuration | Private network for cluster | 2h |
| Load balancer setup | LB pointing to server group | 2h |
| State management | Remote state in Hetzner S3 | 2h |

### Day 5: Ansible Foundation

| Task | Deliverable | Time |
|------|-------------|------|
| Inventory from Terraform | Dynamic inventory plugin | 2h |
| Base hardening playbook | SSH, firewall, updates | 4h |
| Role structure | Reusable roles directory | 2h |

### Week 1 Checkpoint

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEEK 1 SUCCESS CRITERIA                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ✓ OpenTofu provisions 6 VMs (3 servers + 3 agents)                     │
│  ✓ Private network connects all VMs                                     │
│  ✓ Load balancer distributes to servers                                 │
│  ✓ Ansible can reach all nodes (SSH key auth)                           │
│  ✓ Base hardening applied to all nodes                                  │
│  ✓ Infrastructure can be destroyed and recreated in < 10 minutes        │
│                                                                          │
│  Deliverable: Infrastructure code in Git, working environment            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Week 2: Orchestration Phase

### Goal: Production k3s Cluster with Core Services

Now you have infrastructure. Time to run containers at scale.

### Day 1-2: k3s Installation

| Task | Deliverable | Time |
|------|-------------|------|
| k3s server installation | 3-node HA control plane | 4h |
| k3s agent joining | 3 worker nodes joined | 2h |
| Kubeconfig setup | Local kubectl access | 1h |
| Basic verification | Nodes healthy, pods running | 1h |

### Day 3: Networking

| Task | Deliverable | Time |
|------|-------------|------|
| CNI configuration | Cilium or Flannel working | 3h |
| Ingress controller | Traefik or NGINX installed | 2h |
| Cert-manager | Let's Encrypt certificates | 3h |

### Day 4: Storage

| Task | Deliverable | Time |
|------|-------------|------|
| Longhorn installation | Distributed block storage | 3h |
| Storage classes | Default SC configured | 1h |
| Test PVC | StatefulSet with persistent data | 2h |
| Backup configuration | Longhorn backup target | 2h |

### Day 5: First Application

| Task | Deliverable | Time |
|------|-------------|------|
| Deploy sample app | Nginx or httpbin | 2h |
| Expose via ingress | Public HTTPS endpoint | 2h |
| Horizontal scaling | HPA configured | 2h |
| Health checks | Liveness/readiness probes | 2h |

### Week 2 Checkpoint

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEEK 2 SUCCESS CRITERIA                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ✓ k3s cluster operational (3 servers + 3 agents)                       │
│  ✓ All nodes show Ready status                                          │
│  ✓ Ingress routes traffic with TLS termination                          │
│  ✓ Let's Encrypt certificates auto-renew                                │
│  ✓ Longhorn provides persistent storage                                 │
│  ✓ Sample app accessible at https://your-domain.com                     │
│  ✓ Cluster survives single node failure                                 │
│                                                                          │
│  Deliverable: Working Kubernetes cluster, application deployed           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Week 3: Automation Phase

### Goal: GitOps, CI/CD, and Observability

Manual deployments don't scale. This week you automate everything.

### Day 1-2: GitOps

| Task | Deliverable | Time |
|------|-------------|------|
| ArgoCD installation | ArgoCD running in cluster | 3h |
| First application | GitOps-managed deployment | 2h |
| App of Apps pattern | Multi-app management | 3h |
| Sync policies | Auto-sync, self-heal | 2h |

### Day 3: CI/CD Pipeline

| Task | Deliverable | Time |
|------|-------------|------|
| GitHub Actions workflow | Build → Test → Push image | 4h |
| Image versioning | Semantic versioning or SHA | 2h |
| Automated promotion | Dev → Staging → Prod | 2h |

### Day 4: Observability

| Task | Deliverable | Time |
|------|-------------|------|
| Prometheus installation | Metrics collection working | 3h |
| Grafana dashboards | Cluster overview dashboard | 3h |
| Loki for logs | Log aggregation working | 2h |

### Day 5: Alerting & Python Tools

| Task | Deliverable | Time |
|------|-------------|------|
| AlertManager | Critical alerts to Slack | 2h |
| Alert rules | CPU, memory, pod failures | 2h |
| Python CLI tool | `platform-cli` for common tasks | 4h |

### Week 3 Checkpoint

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEEK 3 SUCCESS CRITERIA                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ✓ ArgoCD manages all applications                                      │
│  ✓ Git push triggers automatic deployment                               │
│  ✓ Prometheus collects metrics from all services                        │
│  ✓ Grafana shows cluster health dashboards                              │
│  ✓ Logs searchable in Grafana/Loki                                      │
│  ✓ Critical alerts fire to Slack/Discord                                │
│  ✓ Python CLI automates common tasks                                    │
│                                                                          │
│  Deliverable: Fully automated platform, self-service deployments         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Week 4: Production Readiness Phase

### Goal: Security, DR, Documentation

A platform isn't production-ready until it's secure, recoverable, and documented.

### Day 1-2: Security Hardening

| Task | Deliverable | Time |
|------|-------------|------|
| Network policies | Default deny, explicit allow | 3h |
| RBAC configuration | Least privilege access | 2h |
| Secrets management | External Secrets or Sealed | 3h |
| Security scanning | Trivy for images | 2h |

### Day 3: Disaster Recovery

| Task | Deliverable | Time |
|------|-------------|------|
| Backup verification | Longhorn backups tested | 2h |
| Cluster restore test | Full cluster recovery | 4h |
| Runbook creation | Step-by-step recovery docs | 2h |

### Day 4: Documentation

| Task | Deliverable | Time |
|------|-------------|------|
| Architecture docs | Diagrams, decision records | 4h |
| Operational runbooks | Incident response guides | 2h |
| Onboarding guide | New developer setup | 2h |

### Day 5: Demo & Presentation

| Task | Deliverable | Time |
|------|-------------|------|
| Demo preparation | Walkthrough script | 2h |
| Demo recording | Video demonstrating platform | 3h |
| Retrospective | Lessons learned document | 2h |
| Next steps | Recommendations for improvement | 1h |

### Week 4 Checkpoint

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEEK 4 SUCCESS CRITERIA                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ✓ Network policies enforce least privilege                             │
│  ✓ Secrets never stored in Git                                          │
│  ✓ Image scanning prevents vulnerable deploys                           │
│  ✓ Cluster can be fully restored from backup                            │
│  ✓ Documentation complete and accurate                                  │
│  ✓ Demo video showcases platform capabilities                           │
│  ✓ Post-mortem/retrospective complete                                   │
│                                                                          │
│  Deliverable: Production-ready platform, comprehensive documentation     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Daily Rhythm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        RECOMMENDED DAILY SCHEDULE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  09:00 - 09:30  │  Plan: Review yesterday, set today's goals            │
│  09:30 - 12:00  │  Build: Deep work on infrastructure                   │
│  12:00 - 13:00  │  Break: Step away from the screen                     │
│  13:00 - 15:00  │  Build: Continue implementation                       │
│  15:00 - 15:30  │  Document: Write down what you learned                │
│  15:30 - 16:30  │  Research: Read docs, watch tutorials                 │
│  16:30 - 17:00  │  Review: Test what you built, prepare questions       │
│                                                                          │
│  Live Session (when scheduled): 10:00 AM                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria Summary

### Minimum Bar (Pass)

- [ ] Infrastructure provisioned via OpenTofu
- [ ] k3s cluster operational
- [ ] At least one application deployed
- [ ] Basic monitoring in place
- [ ] Documentation exists

### Exceeds Expectations

- [ ] HA configuration for all components
- [ ] GitOps fully implemented
- [ ] Comprehensive observability
- [ ] Security hardening complete
- [ ] Python automation tools

### Outstanding

- [ ] Multi-environment (dev/staging/prod)
- [ ] Disaster recovery tested and documented
- [ ] Novel optimizations or improvements
- [ ] Contribution to open source tools
- [ ] Research-quality documentation

---

## Related

- [Before You Begin](./01-Before-You-Begin.md)
- [What You Build](./03-What-You-Build.md)
- [Your Role](./04-Your-Role.md)
- [Exercises](./Exercises/)

---

*Last Updated: 2026-02-02*
