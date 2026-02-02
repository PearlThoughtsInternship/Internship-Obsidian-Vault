# Platform Security

> *"Security is always excessive until it's not enough."*
> — **Robbie Sinclair**

## Security-First Mindset

> *Security isn't a feature you add later. It's a design constraint that shapes every decision. A breach can end a startup overnight.*

---

## Zero-Trust Architecture

```mermaid
flowchart TB
    subgraph External["External"]
        User["User"]
        Attacker["Attacker"]
    end

    subgraph Edge["Edge Layer"]
        CF["Cloudflare<br/>WAF + DDoS"]
    end

    subgraph Cluster["Kubernetes Cluster"]
        subgraph Network["Network Policies"]
            direction TB
            NP["Default: Deny All"]
        end

        subgraph Services["Services (mTLS)"]
            API["API Gateway"]
            Auth["Auth Service"]
            User2["User Service"]
            DB["Database"]
        end

        subgraph Identity["Identity Layer"]
            OIDC["OIDC Provider"]
            RBAC["RBAC"]
        end
    end

    User --> CF
    Attacker -.->|"Blocked"| CF
    CF --> API
    API <-->|"mTLS"| Auth
    API <-->|"mTLS"| User2
    User2 <-->|"mTLS"| DB
    Auth --> OIDC
    OIDC --> RBAC

    style Attacker fill:#FF5252
    style NP fill:#4CAF50
    style CF fill:#F48120
```

### Zero-Trust Principles

```mermaid
mindmap
  root((Zero Trust))
    Never Trust
      No implicit trust
      Verify every request
      Assume breach
    Always Verify
      Identity verification
      Device posture
      Context analysis
    Least Privilege
      Minimal permissions
      Time-bound access
      Just-in-time access
    Micro-segmentation
      Network policies
      Service mesh
      Pod-to-pod isolation
```

---

## Defense in Depth

```mermaid
flowchart TB
    subgraph L1["Layer 1: Edge Security"]
        WAF["WAF (Cloudflare)"]
        DDoS["DDoS Protection"]
        GeoBlock["Geo-blocking"]
    end

    subgraph L2["Layer 2: Network Security"]
        FW["Firewall"]
        NP["Network Policies"]
        mTLS["Service Mesh mTLS"]
    end

    subgraph L3["Layer 3: Application Security"]
        AuthN["Authentication"]
        AuthZ["Authorization"]
        Input["Input Validation"]
    end

    subgraph L4["Layer 4: Data Security"]
        Encrypt["Encryption at Rest"]
        TLS["Encryption in Transit"]
        Secrets["Secret Management"]
    end

    subgraph L5["Layer 5: Runtime Security"]
        Scan["Image Scanning"]
        Runtime["Runtime Protection"]
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

## Network Policies

### Default Deny Policy

```yaml
# network-policies/default-deny.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}  # Applies to all pods
  policyTypes:
    - Ingress
    - Egress
  # No ingress/egress rules = deny all
```

### Allow Specific Traffic

```yaml
# network-policies/allow-api-to-db.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-database
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 5432
```

### Network Policy Flow

```mermaid
flowchart LR
    subgraph Namespace["production namespace"]
        subgraph Allowed["Allowed Traffic"]
            API["api-gateway"] -->|"5432"| DB["database"]
            API -->|"80"| User["user-service"]
            User -->|"5432"| DB
        end

        subgraph Blocked["Blocked Traffic"]
            External["external-service"] -.->|"❌"| DB
            Other["other-pod"] -.->|"❌"| DB
        end
    end

    Internet["Internet"] -->|"443"| Ingress["Ingress"]
    Ingress -->|"80"| API

    style DB fill:#4CAF50
    style External fill:#FF5252
    style Other fill:#FF5252
```

### Complete Network Policy Example

```yaml
# network-policies/api-gateway.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Allow from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

  egress:
    # Allow to auth service
    - to:
        - podSelector:
            matchLabels:
              app: auth-service
      ports:
        - protocol: TCP
          port: 8080

    # Allow to user service
    - to:
        - podSelector:
            matchLabels:
              app: user-service
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

---

## Secrets Management

### Secret Hierarchy

```mermaid
flowchart TB
    subgraph External["External Secrets Store"]
        Vault["HashiCorp Vault"]
        AWS_SM["AWS Secrets Manager"]
        Azure_KV["Azure Key Vault"]
    end

    subgraph Kubernetes["Kubernetes Cluster"]
        ESO["External Secrets<br/>Operator"]
        Secret["Kubernetes<br/>Secret"]
        Pod["Application Pod"]
    end

    Vault --> ESO
    AWS_SM --> ESO
    Azure_KV --> ESO
    ESO -->|"Sync"| Secret
    Secret -->|"Mount"| Pod

    style Vault fill:#000000,color:#FFFFFF
    style ESO fill:#326CE5
```

### External Secrets Operator

```yaml
# external-secrets/secret-store.yaml

apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production-role"
          serviceAccountRef:
            name: "vault-auth"

---
# external-secrets/database-credentials.yaml

apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: production/database
        property: username
    - secretKey: password
      remoteRef:
        key: production/database
        property: password
```

### Sealed Secrets for GitOps

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as kubeseal CLI
    participant Git as Git Repository
    participant Ctrl as Sealed Secrets Controller
    participant K8s as Kubernetes

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

```bash
# Create sealed secret
kubectl create secret generic my-secret \
  --from-literal=api-key=supersecret \
  --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-secret.yaml

# Apply sealed secret
kubectl apply -f sealed-secret.yaml
```

```yaml
# sealed-secrets/database.yaml

apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  encryptedData:
    username: AgBy3i4O...encrypted...
    password: AgBy3i4O...encrypted...
  template:
    type: Opaque
    metadata:
      name: database-credentials
      namespace: production
```

---

## RBAC Configuration

### Role-Based Access Control

```mermaid
flowchart TB
    subgraph Users["Users & Service Accounts"]
        Dev["Developer"]
        Deploy["CI/CD Pipeline"]
        Admin["Cluster Admin"]
    end

    subgraph Roles["Roles"]
        ViewRole["view-only"]
        DeployRole["deployer"]
        AdminRole["admin"]
    end

    subgraph Permissions["Permissions"]
        Read["Read pods, services,<br/>configmaps"]
        Deploy2["Create/update<br/>deployments"]
        Full["Full cluster<br/>access"]
    end

    Dev --> ViewRole --> Read
    Deploy --> DeployRole --> Deploy2
    Admin --> AdminRole --> Full

    style ViewRole fill:#4CAF50
    style DeployRole fill:#FF9800
    style AdminRole fill:#F44336
```

### Developer Role

```yaml
# rbac/developer-role.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: development
rules:
  # Read-only for most resources
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "secrets"]
    verbs: ["get", "list", "watch"]

  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]

  # Can view logs
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]

  # Can exec into pods (for debugging)
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: development
subjects:
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

### CI/CD Service Account

```yaml
# rbac/cicd-role.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: cicd-deployer
  namespace: production

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployer
  namespace: production
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]

  - apiGroups: [""]
    resources: ["services", "configmaps"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]

  # Cannot access secrets directly
  # Cannot delete resources

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deployer-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: cicd-deployer
    namespace: production
roleRef:
  kind: Role
  name: deployer
  apiGroup: rbac.authorization.k8s.io
```

---

## Image Security

### Supply Chain Security

```mermaid
flowchart LR
    subgraph Build["Build Phase"]
        Code["Source Code"]
        Build2["Build Image"]
        Sign["Sign Image<br/>(Cosign)"]
    end

    subgraph Scan["Scan Phase"]
        Trivy["Trivy Scan"]
        SBOM["Generate SBOM"]
    end

    subgraph Registry["Registry"]
        GHCR["ghcr.io"]
    end

    subgraph Deploy["Deploy Phase"]
        Verify["Verify Signature"]
        Policy["Admission Policy"]
        K8s["Kubernetes"]
    end

    Code --> Build2 --> Sign --> GHCR
    Build2 --> Trivy --> SBOM
    GHCR --> Verify --> Policy --> K8s

    style Sign fill:#4CAF50
    style Trivy fill:#00BCD4
```

### Trivy Scanning

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

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on critical/high

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Image Signing with Cosign

```bash
# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key ghcr.io/org/app:v1.0.0

# Verify image
cosign verify --key cosign.pub ghcr.io/org/app:v1.0.0
```

### Admission Controller Policy

```yaml
# policies/require-signed-images.yaml

apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: verify-signature
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "ghcr.io/org/*"
          attestors:
            - entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      MFkwEwYHKoZI...
                      -----END PUBLIC KEY-----
```

---

## Pod Security Standards

### Restricted Security Context

```yaml
# deployments/secure-app.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
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
        - name: app
          image: ghcr.io/org/app:v1.0.0
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
            requests:
              memory: "128Mi"
              cpu: "100m"
          volumeMounts:
            - name: tmp
              mountPath: /tmp

      volumes:
        - name: tmp
          emptyDir: {}
```

### Pod Security Admission

```yaml
# namespaces/production.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
```

---

## Security Checklist

```mermaid
flowchart TB
    subgraph Checklist["Security Checklist"]
        subgraph Network["Network"]
            N1["✓ Network policies default deny"]
            N2["✓ mTLS between services"]
            N3["✓ WAF enabled"]
        end

        subgraph Access["Access Control"]
            A1["✓ RBAC configured"]
            A2["✓ Service accounts limited"]
            A3["✓ No cluster-admin users"]
        end

        subgraph Secrets["Secrets"]
            S1["✓ No secrets in Git"]
            S2["✓ External secrets synced"]
            S3["✓ Rotation policy active"]
        end

        subgraph Images["Images"]
            I1["✓ Signed images only"]
            I2["✓ No critical CVEs"]
            I3["✓ SBOM generated"]
        end

        subgraph Runtime["Runtime"]
            R1["✓ Read-only filesystem"]
            R2["✓ Non-root user"]
            R3["✓ Resource limits set"]
        end
    end

    style N1 fill:#4CAF50
    style N2 fill:#4CAF50
    style N3 fill:#4CAF50
    style A1 fill:#4CAF50
    style A2 fill:#4CAF50
    style A3 fill:#4CAF50
    style S1 fill:#4CAF50
    style S2 fill:#4CAF50
    style S3 fill:#4CAF50
    style I1 fill:#4CAF50
    style I2 fill:#4CAF50
    style I3 fill:#4CAF50
    style R1 fill:#4CAF50
    style R2 fill:#4CAF50
    style R3 fill:#4CAF50
```

---

## Related

- [Architecture](../02-Engineering/01-Architecture.md)
- [Networking](./04-Networking.md)
- [GitOps](../02-Engineering/05-GitOps.md)

---

*Last Updated: 2026-02-02*
