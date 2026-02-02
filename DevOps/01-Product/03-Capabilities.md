# Platform Capabilities

## Core Capabilities Overview

The platform provides these capabilities to development teams:

```mermaid
mindmap
  root((Platform<br/>Capabilities))
    Deploy
      Git push → production
      Rollback in seconds
      Preview environments
      Feature flags
    Build
      CI pipelines
      Container builds
      Security scans
      Artifact registry
    Run
      Auto-scaling
      Health checks
      Load balancing
      Service mesh
    Observe
      Metrics dashboards
      Log aggregation
      Distributed tracing
      Alerting & PagerDuty
    Secure
      TLS everywhere
      Secret management
      Network policies
      RBAC & SSO
    Manage
      DNS/Domains
      Backup/Restore
      Cost tracking
      Audit logs
```

---

## Service Level Objectives (SLOs)

### Platform SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Availability** | 99.9% (8.7h downtime/year) | Synthetic monitoring |
| **Deployment Success Rate** | 99% | GitOps pipeline metrics |
| **Deployment Time** | < 5 minutes | Pipeline duration |
| **Recovery Time (MTTR)** | < 15 minutes | Incident tracking |
| **API Latency (p99)** | < 200ms | Prometheus histograms |

### Developer Experience SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Deploy** | < 1 hour | Onboarding tracking |
| **Feedback Loop Time** | < 10 minutes | Push to preview |
| **Documentation Coverage** | 100% of features | Audit |
| **Self-Service Rate** | 80% of requests | Ticket analysis |

---

## Capability 1: Deployment Pipeline

### GitOps Workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as GitHub
    participant CI as CI/CD
    participant Reg as Registry
    participant Argo as ArgoCD
    participant K8s as Kubernetes

    Dev->>Git: Git Push
    Git->>CI: Trigger Build
    CI->>CI: Build & Test
    CI->>Reg: Push Image
    CI->>Git: Update Manifest
    Argo->>Git: Detect Change
    Argo->>K8s: Apply Deployment
    K8s-->>Argo: Sync Complete

    Note over Dev,K8s: Time: Push → Production: ~5 minutes
    Note over Dev,K8s: Rollback: Instant (Git revert)
```

### Deployment Features

| Feature | Implementation | Benefit |
|---------|----------------|---------|
| **Blue-Green** | ArgoCD rollouts | Zero-downtime deploys |
| **Canary** | Progressive delivery | Risk mitigation |
| **Rollback** | Git revert + sync | Instant recovery |
| **Preview Envs** | PR-triggered | Test before merge |

---

## Capability 2: Container Orchestration

### k3s Cluster Architecture

```mermaid
flowchart TB
    subgraph ControlPlane["Control Plane (HA)"]
        S1["Server 1<br/>(Leader)"]
        S2["Server 2<br/>(Follower)"]
        S3["Server 3<br/>(Follower)"]

        S1 <--> S2
        S2 <--> S3
        S3 <--> S1
    end

    subgraph Etcd["etcd (embedded)"]
        E["Distributed<br/>Consensus"]
    end

    subgraph Workers["Worker Nodes"]
        A1["Agent 1<br/>(16 vCPU)"]
        A2["Agent 2<br/>(16 vCPU)"]
        A3["Agent 3<br/>(GPU)"]
    end

    ControlPlane --> Etcd
    ControlPlane --> Workers

    style S1 fill:#4CAF50
    style S2 fill:#2196F3
    style S3 fill:#2196F3
```

**Scaling**: Add agents via Ansible, auto-join cluster
**HA**: 3 servers tolerate 1 failure, etcd consensus

### Workload Types

| Type | Use Case | Configuration |
|------|----------|---------------|
| **Deployment** | Stateless services | Replicas, rolling updates |
| **StatefulSet** | Databases, caches | Stable network, ordered |
| **DaemonSet** | Logging, monitoring | One per node |
| **CronJob** | Batch processing | Scheduled execution |
| **Job** | One-time tasks | Run to completion |

---

## Capability 3: Observability Stack

### Three Pillars

```mermaid
flowchart TB
    subgraph Metrics["METRICS"]
        Prom["Prometheus"]
        M1["CPU/Memory"]
        M2["Network"]
        M3["Custom"]
    end

    subgraph Logs["LOGS"]
        Loki["Loki"]
        L1["App logs"]
        L2["System logs"]
        L3["Audit logs"]
    end

    subgraph Traces["TRACES"]
        Tempo["Tempo"]
        T1["Spans"]
        T2["Context"]
        T3["Latency"]
    end

    Metrics --> Grafana
    Logs --> Grafana
    Traces --> Grafana

    subgraph Visualization["Visualization"]
        Grafana["Grafana<br/>Dashboards<br/>Alerting<br/>Explore"]
    end

    Grafana --> Alert["AlertManager"]
    Alert --> PagerDuty["PagerDuty/Slack"]
```

### Key Dashboards

| Dashboard | Purpose | Key Metrics |
|-----------|---------|-------------|
| **Cluster Overview** | Health at a glance | Node status, pod counts, resource usage |
| **Application** | Service health | Request rate, error rate, latency (RED) |
| **Infrastructure** | Resource usage | CPU, memory, disk, network (USE) |
| **Deployments** | Release tracking | Deploy frequency, rollback rate |
| **Costs** | Budget tracking | Resource costs by namespace |

---

## Capability 4: Security

### Zero-Trust Architecture

```mermaid
flowchart TB
    subgraph Network["NETWORK SECURITY"]
        N1["All traffic encrypted (mTLS)"]
        N2["Network policies (default deny)"]
        N3["Cloudflare DDoS protection"]
        N4["VPN for admin access"]
    end

    subgraph Identity["IDENTITY & ACCESS"]
        I1["SSO integration (OIDC)"]
        I2["RBAC for Kubernetes"]
        I3["Namespace isolation"]
        I4["Audit logging"]
    end

    subgraph Secrets["SECRETS MANAGEMENT"]
        S1["External Secrets Operator"]
        S2["Sealed Secrets for GitOps"]
        S3["Rotation policies"]
        S4["No secrets in Git (ever)"]
    end

    subgraph Supply["SUPPLY CHAIN"]
        SC1["Image scanning (Trivy)"]
        SC2["Signed images (Cosign)"]
        SC3["SBOM generation"]
        SC4["Vulnerability alerts"]
    end

    Network --> Identity --> Secrets --> Supply
```

### Security SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Critical CVE Response** | < 24 hours | Trivy alerts |
| **Secret Rotation** | 90 days max | Vault audit |
| **Compliance Drift** | 0 | Policy as code |
| **Access Reviews** | Quarterly | Audit trail |

---

## Capability 5: Developer Self-Service

### Golden Paths

Developers get self-service access to:

| Capability | Self-Service Method | Approval Needed |
|------------|---------------------|-----------------|
| **Deploy app** | Git push | No |
| **Create database** | Helm chart in GitOps | No |
| **Add domain** | Update ingress manifest | No |
| **View logs** | Grafana access | No |
| **SSH to pod** | kubectl exec | No |
| **Scale up** | Update manifest | No |
| **New namespace** | Terraform PR | Yes (automated) |
| **Production access** | RBAC request | Yes (manual) |

### Developer Portal

```mermaid
flowchart TB
    subgraph Portal["Developer Portal"]
        subgraph Services["MY SERVICES"]
            S1["api-gateway (prod) ✅ Healthy"]
            S2["user-service (prod) ✅ Healthy"]
            S3["ml-inference (prod) ⚠️ High latency"]
        end

        subgraph Actions["QUICK ACTIONS"]
            A1["Deploy"]
            A2["Rollback"]
            A3["Scale"]
            A4["Logs"]
            A5["Metrics"]
            A6["SSH"]
        end

        subgraph Deployments["RECENT DEPLOYMENTS"]
            D1["10:45 | api-gateway | v2.3.1 | ✅ | @alice"]
            D2["10:30 | user-service | v1.8.0 | ✅ | @bob"]
            D3["09:15 | ml-inference | v3.0.0 | ⚠️ | @carol"]
        end
    end
```

---

## Related

- [Product Vision](./01-Vision.md)
- [Market Context](./02-Market-Context.md)
- [Architecture Overview](../02-Engineering/01-Architecture.md)

---

*Last Updated: 2026-02-02*
