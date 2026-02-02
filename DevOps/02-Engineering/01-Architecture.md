# Platform Architecture

> *"Design for failure. Anticipate and mitigate cascading failures. Build systems that fail fast and recover gracefully."*
> — **Release It!** (Michael Nygard)

## Beyond Traditional Infrastructure

> *Modern platform engineering is about building systems that enable developers to ship faster while maintaining enterprise-grade reliability.*

---

## The Architecture Layers

```mermaid
flowchart TB
    subgraph L5["LAYER 5: DEVELOPER EXPERIENCE"]
        DX1["Developer Portal"]
        DX2["Documentation"]
        DX3["Golden Paths"]
        DX4["Self-Service"]
    end

    subgraph L4["LAYER 4: DELIVERY PIPELINE"]
        DP1["CI/CD<br/>(GitHub Actions)"]
        DP2["GitOps<br/>(ArgoCD)"]
        DP3["Registry"]
        DP4["Scanning"]
    end

    subgraph L3["LAYER 3: APPLICATION PLATFORM"]
        AP1["Service Mesh"]
        AP2["Ingress"]
        AP3["Secrets"]
        AP4["Certificates"]
        AP5["DNS"]
    end

    subgraph L2["LAYER 2: CONTAINER ORCHESTRATION"]
        CO1["k3s Cluster"]
        CO2["Namespaces"]
        CO3["RBAC"]
        CO4["Storage<br/>(Longhorn)"]
        CO5["CNI<br/>(Cilium)"]
    end

    subgraph L1["LAYER 1: INFRASTRUCTURE"]
        IN1["Compute<br/>(Hetzner/AWS)"]
        IN2["Network<br/>(VPC)"]
        IN3["Storage"]
        IN4["DNS"]
        IN5["CDN"]
    end

    subgraph L0["LAYER 0: OBSERVABILITY (Cross-Cutting)"]
        OB1["Metrics<br/>(Prometheus)"]
        OB2["Logs<br/>(Loki)"]
        OB3["Traces<br/>(Tempo)"]
        OB4["Alerts"]
    end

    L5 --> L4 --> L3 --> L2 --> L1
    L0 -.-> L1
    L0 -.-> L2
    L0 -.-> L3
    L0 -.-> L4
    L0 -.-> L5
```

---

## Layer 1: Infrastructure (OpenTofu)

> *"Treat servers like cattle, not pets. If a server is misbehaving, shoot it in the head and create a new one."*
> — **Infrastructure as Code** (Kief Morris)

### Infrastructure-as-Code Philosophy

```mermaid
mindmap
  root((IaC<br/>Principles))
    Declarative
      Describe WHAT you want
      State file tracks reality
      Plan shows changes
    Versioned
      All infrastructure in Git
      Review changes via PR
      Audit trail
    Modular
      Reusable components
      Composition over inheritance
      DRY principle
    Tested
      Validate before apply
      Policy as code
      Integration tests
```

### Module Structure

```hcl
# modules/hetzner-k3s-cluster/main.tf

variable "cluster_name" {
  type        = string
  description = "Name of the k3s cluster"
}

variable "server_count" {
  type        = number
  default     = 3
  description = "Number of control plane nodes (odd number for HA)"
}

variable "agent_count" {
  type        = number
  default     = 3
  description = "Number of worker nodes"
}

variable "server_type" {
  type        = string
  default     = "cx31"
  description = "Hetzner server type"
}

# Create servers
resource "hetzner_server" "k3s_server" {
  count       = var.server_count
  name        = "${var.cluster_name}-server-${count.index}"
  image       = "ubuntu-22.04"
  server_type = var.server_type
  location    = "fsn1"

  labels = {
    cluster = var.cluster_name
    role    = "server"
  }
}

# Output for downstream modules
output "server_ips" {
  value = hetzner_server.k3s_server[*].ipv4_address
}
```

### Cloud Provider Comparison

| Resource | Hetzner | AWS | Notes |
|----------|---------|-----|-------|
| **Compute** | `hcloud_server` | `aws_instance` | Hetzner 80% cheaper |
| **Network** | `hcloud_network` | `aws_vpc` | Similar concepts |
| **Load Balancer** | `hcloud_load_balancer` | `aws_lb` | Hetzner included in price |
| **Storage** | `hcloud_volume` | `aws_ebs_volume` | Hetzner simpler |
| **Object Storage** | S3-compatible | `aws_s3_bucket` | Use MinIO for Hetzner |

---

## Layer 2: Container Orchestration (k3s)

### Why k3s?

| Feature | k3s | Full K8s | Impact |
|---------|-----|----------|--------|
| **Binary Size** | ~50MB | ~1GB | Faster installs |
| **Memory** | 512MB minimum | 2GB+ recommended | Lower cost |
| **Components** | Bundled (SQLite/etcd) | Separate | Simpler ops |
| **Certifications** | CNCF Certified | CNCF Certified | Same API |
| **Production Ready** | Yes | Yes | Equal capability |

### Cluster Topology

```mermaid
flowchart TB
    subgraph External["External Traffic"]
        LB["Load Balancer<br/>(Hetzner LB)"]
    end

    subgraph ControlPlane["Control Plane (HA)"]
        S1["Server 1<br/>(Primary)<br/>k3s server<br/>etcd member"]
        S2["Server 2<br/>(Secondary)<br/>k3s server<br/>etcd member"]
        S3["Server 3<br/>(Secondary)<br/>k3s server<br/>etcd member"]

        S1 <--> S2
        S2 <--> S3
        S3 <--> S1
    end

    subgraph Workers["Worker Nodes"]
        A1["Agent 1<br/>(Worker)<br/>Workloads"]
        A2["Agent 2<br/>(Worker)<br/>Workloads"]
        A3["Agent 3<br/>(GPU Node)<br/>ML/AI Jobs"]
    end

    LB --> S1
    LB --> S2
    LB --> S3

    S1 --> A1
    S2 --> A2
    S3 --> A3

    style S1 fill:#4CAF50
    style S2 fill:#2196F3
    style S3 fill:#2196F3
```

**Fault Tolerance**: Survives 1 server failure (n/2 + 1 quorum)
**Scaling**: Add agents with single command

### Installation Flow (Ansible)

```yaml
# playbooks/k3s-install.yml

- name: Install k3s cluster
  hosts: all
  become: yes

  tasks:
    - name: Install first server (initializes cluster)
      when: inventory_hostname == groups['servers'][0]
      shell: |
        curl -sfL https://get.k3s.io | sh -s - server \
          --cluster-init \
          --tls-san={{ loadbalancer_ip }} \
          --disable traefik \
          --flannel-backend=none \
          --disable-network-policy

    - name: Get join token
      when: inventory_hostname == groups['servers'][0]
      slurp:
        src: /var/lib/rancher/k3s/server/node-token
      register: k3s_token

    - name: Join additional servers
      when: inventory_hostname in groups['servers'][1:]
      shell: |
        curl -sfL https://get.k3s.io | sh -s - server \
          --server https://{{ groups['servers'][0] }}:6443 \
          --token {{ k3s_token.content | b64decode | trim }} \
          --tls-san={{ loadbalancer_ip }}

    - name: Join agents
      when: inventory_hostname in groups['agents']
      shell: |
        curl -sfL https://get.k3s.io | sh -s - agent \
          --server https://{{ loadbalancer_ip }}:6443 \
          --token {{ k3s_token.content | b64decode | trim }}
```

---

## Layer 3: Application Platform

### Core Platform Services

```mermaid
flowchart TB
    subgraph Ingress["INGRESS LAYER"]
        ING["Traefik / NGINX Ingress"]
        I1["TLS termination<br/>(Let's Encrypt)"]
        I2["Rate limiting"]
        I3["Path-based routing"]
        I4["Canary deployments"]
    end

    subgraph Mesh["SERVICE MESH (Optional)"]
        SM["Linkerd / Istio"]
        M1["mTLS between services"]
        M2["Traffic management"]
        M3["Automatic observability"]
        M4["Fault injection"]
    end

    subgraph Secrets["SECRETS & CONFIG"]
        SEC["External Secrets Operator"]
        S1["Sync from Vault/AWS SM"]
        S2["Auto-rotation"]
        S3["Sealed Secrets for GitOps"]
    end

    subgraph Storage["STORAGE"]
        STR["Longhorn / MinIO"]
        ST1["Replicated block storage"]
        ST2["Snapshots and backups"]
        ST3["S3-compatible objects"]
    end

    Ingress --> Mesh --> Secrets --> Storage
```

### Helm Charts vs Kustomize

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Helm** | Third-party apps | Templating, versioned releases | Complexity |
| **Kustomize** | Your apps | Native kubectl, overlays | Limited templating |
| **Both** | Best of both | Flexibility | Learning curve |

---

## Layer 4: Delivery Pipeline

### GitOps Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant AppRepo as Application Repo
    participant CI as CI Pipeline
    participant Registry as Container Registry
    participant InfraRepo as Infrastructure Repo
    participant Argo as ArgoCD
    participant K8s as k3s Cluster

    Dev->>AppRepo: Push code
    AppRepo->>CI: Trigger workflow
    CI->>CI: Build & Test
    CI->>Registry: Push image (ghcr.io)
    CI->>InfraRepo: Update image tag

    loop Every 3 minutes
        Argo->>InfraRepo: Poll for changes
    end

    Argo->>InfraRepo: Detect new tag
    Argo->>K8s: Sync to cluster
    K8s-->>Argo: Deployment complete

    Note over Dev,K8s: Git is the source of truth
    Note over Dev,K8s: Cluster converges to Git state
```

### ArgoCD Application Definition

```yaml
# argocd/applications/user-service.yaml

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/org/infra
    targetRevision: main
    path: k8s/overlays/prod/user-service

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

  # Health checks
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # Allow HPA to manage replicas
```

---

## Layer 0: Observability

> *"Hope is not a strategy. Without visibility into your systems, you're flying blind."*
> — **Site Reliability Engineering** (Google)

### Metrics Pipeline

```mermaid
flowchart LR
    subgraph Collection["COLLECTION"]
        App["Applications<br/>(metrics port)"]
        Node["Node Exporter"]
        KSM["kube-state-metrics"]
    end

    subgraph Storage["STORAGE"]
        Prom["Prometheus<br/>• TSDB<br/>• 15d retention<br/>• PromQL"]
    end

    subgraph Viz["VISUALIZATION"]
        Graf["Grafana<br/>• Dashboards<br/>• Explore<br/>• Alerting UI"]
    end

    subgraph Alerting["ALERTING"]
        AM["AlertManager<br/>• Deduplication<br/>• Grouping<br/>• Routing"]
        Slack["Slack/PagerDuty"]
    end

    App --> Prom
    Node --> Prom
    KSM --> Prom
    Prom --> Graf
    Prom --> AM
    AM --> Slack
```

### Golden Signals

| Signal | What It Measures | Example Metrics |
|--------|------------------|-----------------|
| **Latency** | Time to serve request | `http_request_duration_seconds` |
| **Traffic** | Demand on system | `http_requests_total` |
| **Errors** | Failed requests | `http_requests_total{status=~"5.."}` |
| **Saturation** | System capacity | `container_memory_usage_bytes` |

---

## Implementation Approach for Interns

### Week 1: Foundation

```mermaid
flowchart LR
    subgraph W1["Week 1: Foundation"]
        T1["Hetzner Account"] --> T2["OpenTofu Provider"]
        T2 --> T3["First VM Module"]
        T3 --> T4["Basic Ansible"]
    end
```

1. **Infrastructure Setup**
   - Create Hetzner account, configure OpenTofu provider
   - Write first module: single VM with SSH access
   - Learn: State management, plan/apply workflow

2. **Basic Ansible**
   - Inventory file with your VM
   - First playbook: install packages, configure firewall
   - Learn: Idempotency, roles, variables

### Week 2: Cluster

```mermaid
flowchart LR
    subgraph W2["Week 2: Cluster"]
        T5["k3s HA Cluster"] --> T6["Ansible Automation"]
        T6 --> T7["Ingress Controller"]
        T7 --> T8["First App Deployed"]
    end
```

3. **k3s Installation**
   - HA cluster (3 servers, 3 agents)
   - Ansible automation for reproducibility
   - Learn: Kubernetes fundamentals, kubectl

4. **Core Services**
   - Install ingress controller
   - Deploy first application
   - Learn: Services, ingress, namespaces

### Week 3: Platform

```mermaid
flowchart LR
    subgraph W3["Week 3: Platform"]
        T9["ArgoCD Setup"] --> T10["GitOps App"]
        T10 --> T11["Prometheus Stack"]
        T11 --> T12["First Dashboard"]
    end
```

5. **GitOps Setup**
   - Install ArgoCD
   - First GitOps-managed application
   - Learn: Declarative operations, self-healing

6. **Observability**
   - Deploy Prometheus stack
   - Create first dashboard
   - Learn: PromQL, alerting

### Week 4: Production Readiness

```mermaid
flowchart LR
    subgraph W4["Week 4: Production"]
        T13["Network Policies"] --> T14["Secrets Management"]
        T14 --> T15["Python CLI Tool"]
        T15 --> T16["Runbooks & Docs"]
    end
```

7. **Security Hardening**
   - Network policies
   - Secrets management
   - Learn: Zero-trust principles

8. **Documentation & Automation**
   - Python CLI tool for common operations
   - Runbooks for incidents
   - Learn: Toil elimination

---

## Related

- [Infrastructure-as-Code](./02-Infrastructure-as-Code.md)
- [Configuration Management](./03-Configuration-Management.md)
- [Container Orchestration](./04-Container-Orchestration.md)
- [GitOps](./05-GitOps.md)

---

*Last Updated: 2026-02-02*
