# Target Architecture

## Multi-Region, Multi-Tenant Platform

This document describes the production architecture you'll build incrementally over 4 weeks.

---

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Internet["Internet"]
        Users[("Users")]
        Agents[("AI Agents")]
    end

    subgraph Edge["Edge Layer"]
        CF["Cloudflare CDN\n+ DDoS Protection"]
    end

    subgraph Platform["Platform (Hetzner)"]
        subgraph LB["Load Balancer"]
            HLB["Hetzner LB"]
        end

        subgraph Cluster["k3s Cluster"]
            subgraph CP["Control Plane (HA)"]
                S1["Server 1"]
                S2["Server 2"]
                S3["Server 3"]
            end

            subgraph Workers["Worker Nodes"]
                W1["Agent 1\n(General)"]
                W2["Agent 2\n(General)"]
                W3["Agent 3\n(GPU)"]
            end
        end

        subgraph Storage["Storage"]
            LH["Longhorn\n(Block)"]
            MINIO["MinIO\n(Object)"]
        end

        subgraph DB["Databases"]
            PG["PostgreSQL"]
            REDIS["Redis"]
        end
    end

    subgraph Observability["Observability"]
        PROM["Prometheus"]
        GRAF["Grafana"]
        LOKI["Loki"]
    end

    Users --> CF
    Agents --> CF
    CF --> HLB
    HLB --> CP
    CP <--> Workers
    Workers --> LH
    Workers --> MINIO
    Workers --> PG
    Workers --> REDIS
    Workers --> PROM
    PROM --> GRAF
    LOKI --> GRAF
```

---

## Network Architecture

```mermaid
flowchart LR
    subgraph Public["Public Internet"]
        User["User/Agent"]
    end

    subgraph DMZ["DMZ Network"]
        LB["Load Balancer\n10.0.0.1"]
    end

    subgraph Private["Private Network (10.1.0.0/16)"]
        subgraph Servers["Server Subnet (10.1.1.0/24)"]
            S1["Server 1\n10.1.1.1"]
            S2["Server 2\n10.1.1.2"]
            S3["Server 3\n10.1.1.3"]
        end

        subgraph Agents["Agent Subnet (10.1.2.0/24)"]
            A1["Agent 1\n10.1.2.1"]
            A2["Agent 2\n10.1.2.2"]
            A3["Agent 3\n10.1.2.3"]
        end

        subgraph Data["Data Subnet (10.1.3.0/24)"]
            DB1["PostgreSQL\n10.1.3.1"]
            DB2["Redis\n10.1.3.2"]
        end
    end

    User --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    S1 <--> A1
    S2 <--> A2
    S3 <--> A3
    A1 --> DB1
    A2 --> DB2
```

---

## Deployment Pipeline

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant REG as Container Registry
    participant ARGO as ArgoCD
    participant K8S as k3s Cluster

    Dev->>GH: git push
    GH->>CI: Trigger workflow
    CI->>CI: Run tests
    CI->>CI: Build container
    CI->>CI: Security scan
    CI->>REG: Push image
    CI->>GH: Update manifest (image tag)

    loop Every 3 minutes
        ARGO->>GH: Poll for changes
    end

    ARGO->>GH: Detect new manifest
    ARGO->>K8S: Apply changes
    K8S->>K8S: Rolling deployment
    K8S-->>ARGO: Sync complete
```

---

## Observability Architecture

```mermaid
flowchart TB
    subgraph Apps["Applications"]
        App1["Service A"]
        App2["Service B"]
        App3["Service C"]
    end

    subgraph Collection["Data Collection"]
        PM["Prometheus\n(Metrics)"]
        OT["OpenTelemetry\n(Traces)"]
        FL["Fluent Bit\n(Logs)"]
    end

    subgraph Storage["Time Series Storage"]
        PROM["Prometheus TSDB"]
        TEMPO["Tempo"]
        LOKI["Loki"]
    end

    subgraph Viz["Visualization"]
        GRAF["Grafana"]
    end

    subgraph Alert["Alerting"]
        AM["AlertManager"]
        SLACK["Slack"]
        PD["PagerDuty"]
    end

    App1 --> PM
    App2 --> PM
    App3 --> PM
    App1 --> OT
    App2 --> OT
    App3 --> OT
    App1 --> FL
    App2 --> FL
    App3 --> FL

    PM --> PROM
    OT --> TEMPO
    FL --> LOKI

    PROM --> GRAF
    TEMPO --> GRAF
    LOKI --> GRAF

    PROM --> AM
    AM --> SLACK
    AM --> PD
```

---

## GitOps Repository Structure

```mermaid
flowchart TB
    subgraph Repos["Git Repositories"]
        subgraph Infra["infra-repo"]
            TF["terraform/"]
            AN["ansible/"]
            K8S["k8s/"]
        end

        subgraph Apps["app-repos"]
            App1["user-service/"]
            App2["api-gateway/"]
            App3["ml-service/"]
        end
    end

    subgraph ArgoCD["ArgoCD"]
        AOA["App of Apps"]
        A1["user-service app"]
        A2["api-gateway app"]
        A3["ml-service app"]
        Platform["platform-services"]
    end

    subgraph Cluster["k3s Cluster"]
        NS1["production namespace"]
        NS2["staging namespace"]
        NS3["platform namespace"]
    end

    Infra --> AOA
    AOA --> A1
    AOA --> A2
    AOA --> A3
    AOA --> Platform

    A1 --> NS1
    A2 --> NS1
    A3 --> NS1
    Platform --> NS3
```

---

## Security Architecture

```mermaid
flowchart TB
    subgraph External["External Traffic"]
        User["User"]
    end

    subgraph Edge["Edge Security"]
        CF["Cloudflare\n• WAF\n• DDoS\n• Rate Limiting"]
    end

    subgraph Cluster["Cluster Security"]
        ING["Ingress\n• TLS Termination\n• Auth Headers"]

        subgraph Mesh["Service Mesh (Linkerd)"]
            SVC1["Service A"]
            SVC2["Service B"]
        end

        subgraph Secrets["Secrets Management"]
            ESO["External Secrets\nOperator"]
            VAULT["HashiCorp Vault\nor AWS SM"]
        end

        subgraph Policies["Policy Enforcement"]
            NP["Network Policies\n(Default Deny)"]
            RBAC["RBAC\n(Least Privilege)"]
            OPA["OPA Gatekeeper\n(Policy as Code)"]
        end
    end

    User --> CF
    CF --> ING
    ING --> SVC1
    SVC1 <-->|mTLS| SVC2
    SVC1 --> ESO
    ESO --> VAULT
    NP --> Mesh
    RBAC --> Mesh
    OPA --> Mesh
```

---

## Disaster Recovery Architecture

```mermaid
flowchart LR
    subgraph Primary["Primary Region (FSN1)"]
        subgraph K8S1["k3s Cluster"]
            App["Applications"]
            LH1["Longhorn"]
        end
        DB1["PostgreSQL\n(Primary)"]
    end

    subgraph Backup["Backup Storage"]
        S3["S3-Compatible\nObject Storage"]
    end

    subgraph DR["DR Region (NBG1)"]
        subgraph K8S2["k3s Cluster (Standby)"]
            App2["Applications\n(Scaled to 0)"]
            LH2["Longhorn"]
        end
        DB2["PostgreSQL\n(Replica)"]
    end

    LH1 -->|"Backup (hourly)"| S3
    DB1 -->|"WAL Streaming"| DB2
    S3 -->|"Restore"| LH2

    style DR fill:#f5f5f5
```

---

## Scaling Strategy

```mermaid
flowchart TB
    subgraph Triggers["Scale Triggers"]
        CPU["CPU > 70%"]
        MEM["Memory > 80%"]
        QUEUE["Queue Depth > 100"]
        LATENCY["P99 > 500ms"]
    end

    subgraph HPA["Horizontal Pod Autoscaler"]
        METRICS["Custom Metrics API"]
        SCALE["Scale Decision"]
    end

    subgraph Pods["Pod Scaling"]
        P1["Pod 1"]
        P2["Pod 2"]
        P3["Pod 3\n(new)"]
        P4["Pod N\n(new)"]
    end

    subgraph CA["Cluster Autoscaler"]
        PENDING["Pending Pods"]
        PROVISION["Provision Node"]
    end

    subgraph Nodes["Node Scaling"]
        N1["Node 1"]
        N2["Node 2"]
        N3["Node 3\n(new)"]
    end

    CPU --> METRICS
    MEM --> METRICS
    QUEUE --> METRICS
    LATENCY --> METRICS
    METRICS --> SCALE
    SCALE --> P1
    SCALE --> P2
    SCALE --> P3
    SCALE --> P4

    P4 -->|"No capacity"| PENDING
    PENDING --> CA
    CA --> PROVISION
    PROVISION --> N3
```

---

## Cost Optimization

| Component | Hetzner Spec | Monthly Cost | AWS Equivalent |
|-----------|--------------|--------------|----------------|
| **3x Server (CX31)** | 4 vCPU, 8GB RAM | €30 (€10 each) | $180+ |
| **3x Agent (CX41)** | 8 vCPU, 16GB RAM | €60 (€20 each) | $360+ |
| **1x GPU (CCX33)** | RTX 4000, 32GB | €180 | $1,200+ |
| **Load Balancer** | Standard | €6 | $20+ |
| **Storage (100GB)** | SSD | €5 | $10+ |
| **Bandwidth** | 20TB included | €0 | $1,800 |
| **Total** | | **€281** | **$3,570+** |

*Annual savings: ~$39,000*

---

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Cloud Provider** | Hetzner | 90% cost savings, EU sovereignty |
| **Kubernetes** | k3s | Lightweight, production-ready, HA |
| **IaC** | OpenTofu | Open source Terraform fork |
| **Config Mgmt** | Ansible | Agentless, Python-based |
| **GitOps** | ArgoCD | UI, multi-cluster, mature |
| **CNI** | Cilium | eBPF, network policies, observability |
| **Storage** | Longhorn | Distributed, built for k8s |
| **Ingress** | Traefik | k3s native, middleware support |
| **Monitoring** | Prometheus + Grafana | Industry standard |
| **Logging** | Loki | Lightweight, Grafana native |

---

## Related

- [Product Vision](./01-Vision.md)
- [Market Context](./02-Market-Context.md)
- [Capabilities](./03-Capabilities.md)
- [Architecture Overview](../02-Engineering/01-Architecture.md)

---

*Last Updated: 2026-02-02*
