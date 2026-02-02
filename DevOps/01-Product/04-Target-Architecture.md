# Autograph Target Architecture

> *"The best architectures are those that allow you to defer decisions about details."*
> — **Clean Architecture** (Robert C. Martin)

## This Is What You'll Build

By the end of your 4-week internship, you'll have built a production-ready AI content platform.

**Not a demo. Not a toy. A real product that could serve real users.**

---

## Full System Architecture

```mermaid
flowchart TB
    subgraph Users["👥 CONTENT CREATORS"]
        Creator[("Writers")]
        Marketer[("Marketers")]
        Dev[("Developers")]
    end

    subgraph Edge["🌍 EDGE LAYER"]
        CF["CloudFlare CDN\n+ DDoS Protection"]
        LB["Hetzner Load Balancer"]
    end

    subgraph Autograph["🚀 AUTOGRAPH PRODUCT"]
        subgraph App["Application Layer"]
            Strapi["Strapi CMS\n(Content Management)"]
            AI["AI Service\n(Claude/OpenAI)"]
            Search["Meilisearch\n(Content Search)"]
        end

        subgraph Data["Data Layer"]
            PG["PostgreSQL\n(Content Storage)"]
            Redis["Redis\n(Cache & Sessions)"]
            S3["S3/MinIO\n(Media Assets)"]
        end
    end

    subgraph Platform["⚙️ PLATFORM LAYER"]
        subgraph K8s["k3s Cluster"]
            subgraph CP["Control Plane (HA)"]
                S1["Server 1"]
                S2["Server 2"]
                S3["Server 3"]
            end
            subgraph Workers["Worker Nodes"]
                A1["Agent 1"]
                A2["Agent 2"]
                A3["Agent 3"]
            end
        end

        GitOps["ArgoCD\n(Deployment)"]
        Obs["Prometheus + Grafana\n(Observability)"]
    end

    subgraph Infra["🏗️ INFRASTRUCTURE"]
        VMs["Hetzner Cloud VMs"]
        Network["Private Network"]
        Storage["Block Storage\n(Longhorn)"]
    end

    Users --> CF --> LB --> Strapi
    Strapi --> AI
    Strapi --> Search
    Strapi --> PG
    Strapi --> Redis
    Strapi --> S3

    App --> K8s
    K8s --> VMs
    GitOps --> K8s
    Obs --> K8s

    style Strapi fill:#4CAF50
    style AI fill:#4CAF50
```

---

## Autograph Component Architecture

### Application Components

```mermaid
flowchart LR
    subgraph Strapi["STRAPI CMS (Port 1337)"]
        Admin["Admin Panel"]
        REST["REST API"]
        GQL["GraphQL API"]
        Plugins["AI Plugins"]
    end

    subgraph AIService["AI SERVICE (Port 3001)"]
        Gen["Content Generation"]
        Sum["Summarization"]
        Trans["Translation"]
        SEO["SEO Metadata"]
    end

    subgraph Search["MEILISEARCH (Port 7700)"]
        Index["Content Index"]
        Query["Search API"]
    end

    Admin --> REST
    REST --> AIService
    REST --> Search
    Plugins --> AIService

    style Strapi fill:#4CAF50
    style AIService fill:#4CAF50
```

### Data Flow

```mermaid
sequenceDiagram
    participant U as Content Creator
    participant S as Strapi
    participant AI as AI Service
    participant PG as PostgreSQL
    participant R as Redis
    participant MS as Meilisearch

    rect rgb(200, 230, 200)
    Note over U,MS: Content Creation Flow
    U->>S: Create article with AI assist
    S->>AI: Generate content
    AI-->>S: AI-generated draft
    S->>PG: Save content
    S->>MS: Index for search
    S->>R: Invalidate cache
    S-->>U: Article created!
    end

    rect rgb(200, 200, 230)
    Note over U,MS: Content Retrieval Flow
    U->>S: Request article
    S->>R: Check cache
    R-->>S: Cache hit (fast!)
    S-->>U: Article data
    end
```

---

## Network Architecture

```mermaid
flowchart TB
    subgraph Internet["PUBLIC INTERNET"]
        Users["Users"]
    end

    subgraph DMZ["DMZ (10.0.0.0/24)"]
        LB["Load Balancer\n10.0.0.1\n(Public IP: 1.2.3.4)"]
    end

    subgraph Private["PRIVATE NETWORK (10.1.0.0/16)"]
        subgraph Servers["Server Subnet (10.1.1.0/24)"]
            S1["Server 1\n10.1.1.1"]
            S2["Server 2\n10.1.1.2"]
            S3["Server 3\n10.1.1.3"]
        end

        subgraph Agents["Agent Subnet (10.1.2.0/24)"]
            A1["Agent 1\n10.1.2.1\nAutograph workloads"]
            A2["Agent 2\n10.1.2.2\nAutograph workloads"]
            A3["Agent 3\n10.1.2.3\nAutograph workloads"]
        end

        subgraph Data["Data Subnet (10.1.3.0/24)"]
            PG["PostgreSQL\n10.1.3.1"]
            Redis["Redis\n10.1.3.2"]
            Meili["Meilisearch\n10.1.3.3"]
        end
    end

    Users --> LB
    LB --> S1 & S2 & S3
    S1 & S2 & S3 --> A1 & A2 & A3
    A1 & A2 & A3 --> PG & Redis & Meili

    style A1 fill:#4CAF50
    style A2 fill:#4CAF50
    style A3 fill:#4CAF50
```

---

## Autograph Deployment Pipeline

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant REG as ghcr.io
    participant ARGO as ArgoCD
    participant K8S as k3s Cluster
    participant CAI as Autograph

    Dev->>GH: Push Autograph code
    GH->>CI: Trigger workflow

    rect rgb(200, 200, 230)
    Note over CI: Build Phase
    CI->>CI: Run tests
    CI->>CI: Build container
    CI->>CI: Security scan (Trivy)
    CI->>REG: Push image (ghcr.io/org/autograph:v1.2.3)
    end

    CI->>GH: Update k8s/autograph/deployment.yaml

    rect rgb(200, 230, 200)
    Note over ARGO,K8S: Deploy Phase
    ARGO->>GH: Detect manifest change
    ARGO->>K8S: Apply new deployment
    K8S->>CAI: Rolling update
    CAI-->>K8S: Health check passed
    end

    K8S-->>Dev: Autograph v1.2.3 deployed!

    Note over Dev,CAI: Total time: ~5 minutes
```

---

## Autograph Namespace Layout

```yaml
# How Autograph is organized in Kubernetes

autograph/
├── strapi/
│   ├── deployment.yaml        # 2+ replicas, rolling updates
│   ├── service.yaml           # ClusterIP for internal access
│   ├── ingress.yaml           # HTTPS endpoint
│   ├── configmap.yaml         # Environment configuration
│   ├── secret.yaml            # Credentials (sealed)
│   └── hpa.yaml               # Auto-scaling rules
│
├── ai-service/
│   ├── deployment.yaml        # 2+ replicas
│   ├── service.yaml           # Internal service
│   ├── configmap.yaml         # AI configuration
│   └── secret.yaml            # API keys (Claude, OpenAI)
│
├── database/
│   ├── postgresql/
│   │   ├── statefulset.yaml   # Persistent database
│   │   ├── service.yaml       # Stable network identity
│   │   ├── secret.yaml        # DB credentials
│   │   └── pvc.yaml           # 10Gi storage
│   └── redis/
│       ├── deployment.yaml    # Cache instance
│       ├── service.yaml
│       └── pvc.yaml           # 1Gi persistence
│
└── search/
    └── meilisearch/
        ├── statefulset.yaml   # Search engine
        ├── service.yaml
        └── pvc.yaml           # Index storage
```

---

## Observability Architecture

### Monitoring Autograph

```mermaid
flowchart TB
    subgraph Autograph["AUTOGRAPH METRICS"]
        Strapi["Strapi Metrics\n• requests/sec\n• error rate\n• latency"]
        AI["AI Service Metrics\n• tokens used\n• generation time\n• provider (Claude/OpenAI)"]
        Search["Search Metrics\n• query latency\n• index size"]
    end

    subgraph Collection["COLLECTION"]
        Prom["Prometheus"]
        Loki["Loki (Logs)"]
    end

    subgraph Visualization["VISUALIZATION"]
        Graf["Grafana"]
        Dash1["Autograph Dashboard"]
        Dash2["Infrastructure Dashboard"]
        Dash3["Cost Tracking Dashboard"]
    end

    subgraph Alerting["ALERTING"]
        AM["AlertManager"]
        Slack["Slack"]
    end

    Autograph --> Prom
    Autograph --> Loki
    Prom --> Graf
    Loki --> Graf
    Graf --> Dash1 & Dash2 & Dash3
    Prom --> AM --> Slack

    style Dash1 fill:#4CAF50
```

### Autograph-Specific Alerts

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| **High AI Cost** | tokens > 100K/hour | Warning | Review usage |
| **AI Provider Down** | Claude AND OpenAI failing | Critical | Check API keys |
| **Strapi Unhealthy** | Health check failed | Critical | Investigate pods |
| **Search Slow** | p99 > 500ms | Warning | Check index |
| **Content DB Full** | Storage > 80% | Warning | Expand storage |

---

## Security Architecture

```mermaid
flowchart TB
    subgraph External["EXTERNAL USERS"]
        User["Content Creator"]
    end

    subgraph Edge["EDGE SECURITY"]
        CF["CloudFlare\n• WAF rules\n• DDoS protection\n• Rate limiting\n• Bot protection"]
    end

    subgraph Cluster["K3S CLUSTER"]
        subgraph Ingress["INGRESS LAYER"]
            ING["NGINX Ingress\n• TLS termination\n• Auth headers"]
        end

        subgraph Autograph["AUTOGRAPH NAMESPACE"]
            subgraph NetPol["Network Policies"]
                NP1["Default: Deny All"]
                NP2["Allow: Strapi ↔ PostgreSQL"]
                NP3["Allow: Strapi ↔ AI Service"]
                NP4["Allow: Strapi ↔ Redis"]
                NP5["Allow: Prometheus scraping"]
            end

            Strapi["Strapi\n(JWT Auth)"]
            AI["AI Service"]
            PG["PostgreSQL"]
        end

        subgraph Secrets["SECRETS MANAGEMENT"]
            Sealed["Sealed Secrets\n(GitOps-safe)"]
            Keys["• DB password\n• AI API keys\n• JWT secrets"]
        end

        subgraph RBAC["RBAC"]
            R1["admin: Full access"]
            R2["developer: autograph namespace"]
            R3["ci-bot: Deploy only"]
        end
    end

    User --> CF --> ING --> Strapi
    Strapi --> AI --> Keys
    Strapi --> PG --> Keys
    NetPol --> Autograph
    RBAC --> Cluster

    style Strapi fill:#4CAF50
```

---

## Disaster Recovery

### Backup Strategy

```mermaid
flowchart LR
    subgraph Primary["PRIMARY (FSN1)"]
        subgraph Autograph["Autograph"]
            Strapi["Strapi"]
            PG["PostgreSQL"]
            Media["Media Files"]
        end
        LH1["Longhorn"]
    end

    subgraph Backup["BACKUP STORAGE"]
        S3["S3-Compatible\nObject Storage"]
    end

    subgraph DR["DR READY"]
        Restore["Can restore in < 30 min"]
    end

    PG -->|"Daily backup\n+ WAL streaming"| S3
    Media -->|"Hourly sync"| S3
    LH1 -->|"Hourly snapshots"| S3
    S3 -->|"Restore"| Restore

    style Autograph fill:#4CAF50
```

### Recovery Time Objectives

| Component | RPO (Data Loss) | RTO (Downtime) |
|-----------|-----------------|----------------|
| **PostgreSQL** | 5 minutes | 15 minutes |
| **Media Files** | 1 hour | 30 minutes |
| **Redis Cache** | Acceptable loss | 5 minutes |
| **Search Index** | Rebuilds from DB | 15 minutes |
| **Full Autograph** | 5 minutes | 30 minutes |

---

## Scaling Architecture

### Auto-Scaling Autograph

```mermaid
flowchart TB
    subgraph Triggers["SCALE TRIGGERS"]
        CPU["CPU > 70%"]
        MEM["Memory > 80%"]
        QUEUE["AI Queue > 100"]
        LATENCY["P99 > 500ms"]
    end

    subgraph HPA["HORIZONTAL POD AUTOSCALER"]
        Metrics["Custom Metrics API"]
        Decision["Scale Decision"]
    end

    subgraph Strapi["STRAPI PODS"]
        S1["Pod 1 ✓"]
        S2["Pod 2 ✓"]
        S3["Pod 3 (scaling)"]
    end

    subgraph AI["AI SERVICE PODS"]
        A1["Pod 1 ✓"]
        A2["Pod 2 ✓"]
    end

    Triggers --> Metrics --> Decision
    Decision --> Strapi
    Decision --> AI

    style S1 fill:#4CAF50
    style S2 fill:#4CAF50
    style A1 fill:#4CAF50
    style A2 fill:#4CAF50
```

### Scaling Limits

| Component | Min Replicas | Max Replicas | Scale On |
|-----------|--------------|--------------|----------|
| **Strapi** | 2 | 10 | CPU, Memory |
| **AI Service** | 2 | 5 | Queue depth |
| **Meilisearch** | 1 | 1 | Vertical only |
| **PostgreSQL** | 1 | 1 | Vertical only |
| **Redis** | 1 | 1 | Vertical only |

---

## Cost Architecture

### Hetzner vs AWS Comparison

| Component | Hetzner Spec | Monthly Cost | AWS Equivalent |
|-----------|--------------|--------------|----------------|
| **3x Server (CX31)** | 4 vCPU, 8GB RAM | €30 | $180+ |
| **3x Agent (CX41)** | 8 vCPU, 16GB RAM | €60 | $360+ |
| **Load Balancer** | Standard | €6 | $20+ |
| **Storage (100GB)** | SSD | €5 | $10+ |
| **Bandwidth** | 20TB included | €0 | $1,800 |
| **Total** | | **€101/mo** | **$2,370/mo** |

**Annual savings: ~$27,000** — That's 3 years of AI API costs!

### Autograph Operating Costs

| Cost Center | Monthly Budget | Notes |
|-------------|----------------|-------|
| **Infrastructure** | €101 | Hetzner VMs + Storage |
| **Claude API** | ~$200 | Primary AI provider |
| **OpenAI API** | ~$50 | Backup provider |
| **Domain/SSL** | ~$5 | CloudFlare |
| **Total** | **~$360/mo** | Production-ready AI platform |

---

## Technology Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| **CMS** | Strapi | Open source, API-first, extensible |
| **AI Primary** | Claude | Best content quality |
| **AI Fallback** | OpenAI | Reliability |
| **Database** | PostgreSQL | Strapi default, JSON support |
| **Cache** | Redis | Fast, sessions, rate limiting |
| **Search** | Meilisearch | Typo-tolerant, fast |
| **Orchestration** | k3s | Lightweight, production-ready |
| **GitOps** | ArgoCD | UI, sync status, rollback |
| **Observability** | Prometheus + Grafana | Industry standard |
| **Cloud** | Hetzner | 90% cost savings |

---

## Implementation Timeline

| Week | Focus | Autograph Milestone |
|------|-------|---------------------|
| **Week 1** | Infrastructure | VMs provisioned, hardened |
| **Week 2** | **Autograph** | **Strapi + AI live!** |
| **Week 3** | Automation | GitOps deploys Autograph |
| **Week 4** | Production | Secured, monitored, documented |

---

## Related

- [Product Vision](./01-Vision.md) — Why we're building Autograph
- [Market Context](./02-Market-Context.md) — The opportunity
- [Capabilities](./03-Capabilities.md) — What Autograph does
- [Architecture Overview](../02-Engineering/01-Architecture.md) — Deep dive

---

*Last Updated: 2026-02-02*
