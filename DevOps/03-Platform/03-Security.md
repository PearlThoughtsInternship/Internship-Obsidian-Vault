# Platform Security: Protecting Autograph's Kingdom

> *"Security is always excessive until it's not enough."*
> — **Robbie Sinclair**

## The Purpose: Why Security for Autograph?

**Why are we doing this?** To protect Autograph and its users from attackers.

A breach doesn't just expose data — it destroys trust. Users share their content, their ideas, their business through Autograph. **One breach, and they never come back.**

```mermaid
flowchart TB
    subgraph Threats["🔓 THREATS TO AUTOGRAPH"]
        T1["Data theft\n(user content)"]
        T2["Service disruption\n(DDoS)"]
        T3["Unauthorized access\n(API abuse)"]
        T4["Supply chain\n(compromised images)"]
    end

    subgraph Protections["🛡️ YOUR DEFENSES"]
        P1["Network policies\n(isolation)"]
        P2["WAF + DDoS\n(Cloudflare)"]
        P3["RBAC\n(least privilege)"]
        P4["Image scanning\n(Trivy)"]
    end

    subgraph Result["✅ AUTOGRAPH SECURE"]
        R["Users trust their content is safe\nStrapi serves requests safely\nAI Service protected"]
    end

    Threats -.->|"Blocked by"| Protections
    Protections --> Result

    style Result fill:#4CAF50
```

---

## Who Needs to Understand Security?

| Stakeholder | Why Security Matters |
|-------------|---------------------|
| **DevOps** | "Is the platform protected from attacks?" |
| **Developers** | "How do I securely store API keys?" |
| **AI Service** | "How do I protect Claude API credentials?" |
| **Business** | "Can we promise customers their content is safe?" |
| **Customers** | "Is my unpublished content protected?" |

---

## Zero-Trust for Autograph

> *"Never trust, always verify."*

```mermaid
flowchart TB
    subgraph External["External"]
        User["Autograph User"]
        Attacker["Attacker"]
    end

    subgraph Edge["Edge Layer"]
        CF["Cloudflare\nWAF + DDoS Protection"]
    end

    subgraph Cluster["autograph namespace"]
        subgraph Network["Network Policies"]
            direction TB
            NP["Default: Deny All"]
        end

        subgraph Services["Services (mTLS)"]
            Strapi["Strapi CMS"]
            AI["AI Service"]
            PG["PostgreSQL"]
            Redis["Redis"]
            Meili["Meilisearch"]
        end

        subgraph Identity["Identity"]
            OIDC["OIDC Provider"]
            RBAC["RBAC"]
        end
    end

    User --> CF
    Attacker -.->|"Blocked"| CF
    CF --> Strapi
    Strapi <-->|"mTLS"| AI
    Strapi <-->|"mTLS"| PG
    Strapi <-->|"mTLS"| Redis
    Strapi <-->|"mTLS"| Meili
    OIDC --> RBAC

    style Attacker fill:#FF5252
    style NP fill:#4CAF50
    style CF fill:#F48120
```

---

## Defense in Depth for Autograph

```mermaid
flowchart TB
    subgraph L1["Layer 1: Edge Security"]
        WAF["WAF (Cloudflare)"]
        DDoS["DDoS Protection"]
        GeoBlock["Geo-blocking"]
    end

    subgraph L2["Layer 2: Network Security"]
        FW["Hetzner Firewall"]
        NP["Network Policies"]
        mTLS["Service Mesh mTLS"]
    end

    subgraph L3["Layer 3: Application Security"]
        Auth["Strapi Authentication"]
        JWT["JWT Validation"]
        Input["Input Validation"]
    end

    subgraph L4["Layer 4: Data Security"]
        Encrypt["PostgreSQL Encryption"]
        TLS["TLS Everywhere"]
        Secrets["Sealed Secrets"]
    end

    subgraph L5["Layer 5: Runtime Security"]
        Scan["Trivy Image Scanning"]
        PSS["Pod Security Standards"]
        Audit["Audit Logging"]
    end

    L1 --> L2 --> L3 --> L4 --> L5

    style L1 fill:#E91E63
    style L2 fill:#9C27B0
    style L3 fill:#3F51B5
    style L4 fill:#00BCD4
    style L5 fill:#4CAF50
```

---

## Network Policies for Autograph

### Default Deny All

```yaml
# network-policies/default-deny.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: autograph
spec:
  podSelector: {}  # Applies to ALL pods in autograph namespace
  policyTypes:
    - Ingress
    - Egress
  # No rules = deny all traffic by default
```

### Strapi Network Policy

Strapi needs to talk to PostgreSQL, Redis, Meilisearch, and AI Service:

```yaml
# network-policies/strapi.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: strapi-policy
  namespace: autograph
spec:
  podSelector:
    matchLabels:
      app: strapi
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Allow from ingress controller (public traffic)
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 1337  # Strapi port

  egress:
    # Allow to PostgreSQL
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432

    # Allow to Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379

    # Allow to Meilisearch
    - to:
        - podSelector:
            matchLabels:
              app: meilisearch
      ports:
        - protocol: TCP
          port: 7700

    # Allow to AI Service
    - to:
        - podSelector:
            matchLabels:
              app: ai-service
      ports:
        - protocol: TCP
          port: 8080

    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### AI Service Network Policy

AI Service needs to call external APIs (Claude, OpenAI):

```yaml
# network-policies/ai-service.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ai-service-policy
  namespace: autograph
spec:
  podSelector:
    matchLabels:
      app: ai-service
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Only Strapi can call AI Service
    - from:
        - podSelector:
            matchLabels:
              app: strapi
      ports:
        - protocol: TCP
          port: 8080

  egress:
    # Allow external HTTPS (Claude/OpenAI APIs)
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
      ports:
        - protocol: TCP
          port: 443

    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### Network Policy Visualization

```mermaid
flowchart LR
    subgraph Namespace["autograph namespace"]
        subgraph Allowed["✅ Allowed Traffic"]
            Internet["Internet"] -->|"443"| Ingress["Ingress"]
            Ingress -->|"1337"| Strapi["Strapi"]
            Strapi -->|"5432"| PG["PostgreSQL"]
            Strapi -->|"6379"| Redis["Redis"]
            Strapi -->|"7700"| Meili["Meilisearch"]
            Strapi -->|"8080"| AI["AI Service"]
            AI -->|"443"| Claude["Claude API"]
        end

        subgraph Blocked["❌ Blocked Traffic"]
            Direct["Direct"] -.->|"❌"| PG
            External["External"] -.->|"❌"| AI
        end
    end

    style PG fill:#4CAF50
    style Direct fill:#FF5252
    style External fill:#FF5252
```

---

## Secrets Management for Autograph

### What Secrets Autograph Needs

| Secret | Where Used | Sensitivity |
|--------|-----------|-------------|
| `DATABASE_URL` | Strapi → PostgreSQL | High |
| `CLAUDE_API_KEY` | AI Service → Claude | Critical |
| `OPENAI_API_KEY` | AI Service → OpenAI | Critical |
| `REDIS_PASSWORD` | Strapi → Redis | Medium |
| `MEILISEARCH_KEY` | Strapi → Meilisearch | Medium |
| `JWT_SECRET` | Strapi auth | High |
| `ADMIN_JWT_SECRET` | Strapi admin | Critical |

### Sealed Secrets for GitOps

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as kubeseal CLI
    participant Git as Git Repository
    participant Ctrl as Sealed Secrets Controller
    participant K8s as autograph namespace

    Dev->>Dev: Create plain Secret YAML
    Dev->>CLI: kubeseal < secret.yaml
    CLI->>CLI: Encrypt with cluster public key
    CLI-->>Dev: sealed-secret.yaml

    Dev->>Git: Commit sealed-secret.yaml
    Note over Git: Safe to store in Git!

    Git->>Ctrl: ArgoCD syncs
    Ctrl->>Ctrl: Decrypt using private key
    Ctrl->>K8s: Create Kubernetes Secret

    Note over K8s: Only controller can decrypt
```

### Creating Sealed Secrets for Autograph

```bash
# Create Strapi secrets
kubectl create secret generic strapi-secrets \
  --namespace autograph \
  --from-literal=DATABASE_URL="postgresql://strapi:password@postgres:5432/autograph" \
  --from-literal=JWT_SECRET="your-jwt-secret" \
  --from-literal=ADMIN_JWT_SECRET="your-admin-jwt-secret" \
  --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-strapi-secrets.yaml

# Create AI Service secrets
kubectl create secret generic ai-service-secrets \
  --namespace autograph \
  --from-literal=CLAUDE_API_KEY="sk-ant-..." \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-ai-secrets.yaml
```

### Sealed Secret Example

```yaml
# sealed-secrets/ai-service.yaml

apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: ai-service-secrets
  namespace: autograph
spec:
  encryptedData:
    CLAUDE_API_KEY: AgBy3i4O...encrypted...
    OPENAI_API_KEY: AgBy3i4O...encrypted...
  template:
    type: Opaque
    metadata:
      name: ai-service-secrets
      namespace: autograph
      labels:
        app: ai-service
```

---

## RBAC for Autograph

### Who Can Do What

```mermaid
flowchart TB
    subgraph Users["Users & Service Accounts"]
        Intern["Intern"]
        CI["GitHub Actions"]
        Admin["Platform Admin"]
    end

    subgraph Roles["Roles"]
        ViewRole["autograph-viewer"]
        DeployRole["autograph-deployer"]
        AdminRole["autograph-admin"]
    end

    subgraph Permissions["Permissions"]
        Read["Read pods, services,\nlogs in autograph"]
        Deploy["Create/update\ndeployments, configmaps"]
        Full["Full access to\nautograph namespace"]
    end

    Intern --> ViewRole --> Read
    CI --> DeployRole --> Deploy
    Admin --> AdminRole --> Full

    style ViewRole fill:#4CAF50
    style DeployRole fill:#FF9800
    style AdminRole fill:#F44336
```

### Intern Role (View Only)

```yaml
# rbac/intern-role.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: autograph-viewer
  namespace: autograph
rules:
  # Can view all resources
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "endpoints"]
    verbs: ["get", "list", "watch"]

  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "statefulsets"]
    verbs: ["get", "list", "watch"]

  # Can view logs (for debugging)
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]

  # Can exec into pods (for debugging)
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create"]

  # CANNOT view secrets (no access to API keys)
  # CANNOT modify anything

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: intern-viewer-binding
  namespace: autograph
subjects:
  - kind: User
    name: intern@example.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: autograph-viewer
  apiGroup: rbac.authorization.k8s.io
```

### CI/CD Deployer Role

```yaml
# rbac/cicd-role.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: github-actions
  namespace: autograph

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: autograph-deployer
  namespace: autograph
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]

  - apiGroups: [""]
    resources: ["services", "configmaps"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]

  # Can create Jobs (for migrations)
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["get", "list", "create"]

  # CANNOT delete anything
  # CANNOT access secrets directly

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-deployer-binding
  namespace: autograph
subjects:
  - kind: ServiceAccount
    name: github-actions
    namespace: autograph
roleRef:
  kind: Role
  name: autograph-deployer
  apiGroup: rbac.authorization.k8s.io
```

---

## Image Security

### Supply Chain for Autograph

```mermaid
flowchart LR
    subgraph Build["Build Phase"]
        Code["Source Code"]
        Build2["Build Image"]
        Sign["Sign (Cosign)"]
    end

    subgraph Scan["Scan Phase"]
        Trivy["Trivy Scan"]
        SBOM["Generate SBOM"]
    end

    subgraph Registry["Registry"]
        GHCR["ghcr.io/autograph"]
    end

    subgraph Deploy["Deploy Phase"]
        Verify["Verify Signature"]
        Policy["Kyverno Policy"]
        K8s["autograph namespace"]
    end

    Code --> Build2 --> Sign --> GHCR
    Build2 --> Trivy --> SBOM
    GHCR --> Verify --> Policy --> K8s

    style Sign fill:#4CAF50
    style Trivy fill:#00BCD4
```

### Trivy Scanning in CI

```yaml
# .github/workflows/security-scan.yaml

name: Security Scan

on:
  push:
    branches: [main]
  pull_request:

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Strapi image
        run: docker build -t ghcr.io/autograph/strapi:${{ github.sha }} ./strapi

      - name: Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/autograph/strapi:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on critical/high

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## Pod Security for Autograph

### Secure Strapi Deployment

```yaml
# deployments/strapi.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: strapi
  namespace: autograph
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
        - name: strapi
          image: ghcr.io/autograph/strapi:v1.0.0
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
            requests:
              memory: "256Mi"
              cpu: "100m"
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: uploads
              mountPath: /app/public/uploads

      volumes:
        - name: tmp
          emptyDir: {}
        - name: uploads
          persistentVolumeClaim:
            claimName: strapi-uploads
```

### Namespace Security Label

```yaml
# namespaces/autograph.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: autograph
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

---

## Security Checklist for Autograph

```mermaid
flowchart TB
    subgraph Checklist["Autograph Security Checklist"]
        subgraph Network["Network"]
            N1["✓ Default deny in autograph namespace"]
            N2["✓ Strapi → DB only via policy"]
            N3["✓ AI Service → external HTTPS only"]
            N4["✓ Cloudflare WAF enabled"]
        end

        subgraph Access["Access Control"]
            A1["✓ Intern: view-only RBAC"]
            A2["✓ CI/CD: deploy-only RBAC"]
            A3["✓ No direct secret access"]
        end

        subgraph Secrets["Secrets"]
            S1["✓ API keys in Sealed Secrets"]
            S2["✓ No secrets in Git history"]
            S3["✓ Rotation policy defined"]
        end

        subgraph Images["Images"]
            I1["✓ Trivy scan in CI"]
            I2["✓ No critical CVEs"]
            I3["✓ Images signed"]
        end

        subgraph Runtime["Runtime"]
            R1["✓ Non-root containers"]
            R2["✓ Read-only filesystem"]
            R3["✓ Resource limits set"]
        end
    end

    style N1 fill:#4CAF50
    style A1 fill:#4CAF50
    style S1 fill:#4CAF50
    style I1 fill:#4CAF50
    style R1 fill:#4CAF50
```

---

## What's Next

Once you've secured Autograph:

1. **[Networking](./04-Networking.md)** — Ingress, DNS, service mesh
2. **[Exercise: Security Hardening](../04-Internship/Exercises/09-Security-Hardening.md)** — Hands-on practice
3. **[Observability](./02-Observability.md)** — Monitor security events

---

## Related

- [Architecture](../02-Engineering/01-Architecture.md) — System design overview
- [GitOps](../02-Engineering/05-GitOps.md) — How Sealed Secrets flow through ArgoCD
- [Observability](./02-Observability.md) — Security monitoring and alerts

---

*Last Updated: 2026-02-02*
