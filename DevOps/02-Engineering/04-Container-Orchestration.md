# Container Orchestration with k3s

## Why Kubernetes?

> *Containers are the unit of deployment. Kubernetes is the operating system for the cloud.*

---

## The Container Evolution

```mermaid
flowchart LR
    subgraph Era1["Era 1: Physical"]
        P1["Physical Server 1"]
        P2["Physical Server 2"]
    end

    subgraph Era2["Era 2: Virtual"]
        V1["VM 1"]
        V2["VM 2"]
        V3["VM 3"]
    end

    subgraph Era3["Era 3: Containers"]
        C1["Container 1"]
        C2["Container 2"]
        C3["Container 3"]
        C4["Container 4"]
    end

    subgraph Era4["Era 4: Orchestration"]
        K8S["Kubernetes"]
        K8S --> Pod1["Pod"]
        K8S --> Pod2["Pod"]
        K8S --> Pod3["Pod"]
    end

    Era1 --> Era2 --> Era3 --> Era4
```

---

## Why k3s?

| Feature | k3s | Full Kubernetes |
|---------|-----|-----------------|
| **Binary size** | ~60MB | ~1GB+ |
| **Memory footprint** | ~512MB | ~2GB+ |
| **Install time** | 30 seconds | Hours |
| **Complexity** | Low | High |
| **Production ready** | Yes | Yes |
| **CNCF certified** | Yes | Yes |
| **Built-in components** | SQLite, Traefik, CoreDNS | External deps |

**For this project:** k3s provides full Kubernetes API compatibility with 90% less overhead—perfect for cost-optimized Hetzner infrastructure.

---

## k3s Architecture

```mermaid
flowchart TB
    subgraph CP["Control Plane (HA)"]
        S1["Server 1\n• API Server\n• Scheduler\n• Controller"]
        S2["Server 2\n• API Server\n• Scheduler\n• Controller"]
        S3["Server 3\n• API Server\n• Scheduler\n• Controller"]

        S1 <--> S2 <--> S3
        S1 <--> S3
    end

    subgraph Datastore["Embedded etcd"]
        E1["etcd"]
        E2["etcd"]
        E3["etcd"]
    end

    subgraph Workers["Worker Nodes"]
        A1["Agent 1\n• kubelet\n• containerd"]
        A2["Agent 2\n• kubelet\n• containerd"]
        A3["Agent 3\n• kubelet\n• containerd"]
    end

    LB["Load Balancer\n(API: 6443)"]

    LB --> S1
    LB --> S2
    LB --> S3

    S1 --> E1
    S2 --> E2
    S3 --> E3

    A1 --> LB
    A2 --> LB
    A3 --> LB
```

---

## Core Concepts

### Pods

```mermaid
flowchart TB
    subgraph Pod["Pod: web-app"]
        C1["Container: nginx"]
        C2["Container: log-shipper"]
        Vol["Shared Volume"]
        Net["Shared Network\n(localhost)"]

        C1 --> Vol
        C2 --> Vol
        C1 --> Net
        C2 --> Net
    end
```

```yaml
# Pod definition
apiVersion: v1
kind: Pod
metadata:
  name: web-app
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:1.25
      ports:
        - containerPort: 80
      volumeMounts:
        - name: shared-logs
          mountPath: /var/log/nginx

    - name: log-shipper
      image: fluent/fluent-bit:2.1
      volumeMounts:
        - name: shared-logs
          mountPath: /logs
          readOnly: true

  volumes:
    - name: shared-logs
      emptyDir: {}
```

### Deployments

```mermaid
flowchart TB
    subgraph Deployment["Deployment: web-app"]
        RS["ReplicaSet\n(manages replicas)"]

        subgraph Pods["Pods (replicas=3)"]
            P1["Pod 1"]
            P2["Pod 2"]
            P3["Pod 3"]
        end

        RS --> P1
        RS --> P2
        RS --> P3
    end

    subgraph RollingUpdate["Rolling Update"]
        Old["v1.0"]
        New["v1.1"]
        Old -->|"gradual replacement"| New
    end
```

```yaml
# Deployment definition
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web
        version: v1.0.0
    spec:
      containers:
        - name: web
          image: ghcr.io/company/web-app:v1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 3
```

### Services

```mermaid
flowchart LR
    subgraph External["External Traffic"]
        User["User"]
    end

    subgraph Services["Service Types"]
        CIP["ClusterIP\n(internal only)"]
        NP["NodePort\n(port on node)"]
        LBSvc["LoadBalancer\n(cloud LB)"]
    end

    subgraph Pods["Backend Pods"]
        P1["Pod 1\n10.42.0.5"]
        P2["Pod 2\n10.42.0.6"]
        P3["Pod 3\n10.42.0.7"]
    end

    User --> LBSvc --> CIP
    CIP --> P1
    CIP --> P2
    CIP --> P3
```

```yaml
# Service definition
apiVersion: v1
kind: Service
metadata:
  name: web-app
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
# Headless service for StatefulSets
apiVersion: v1
kind: Service
metadata:
  name: database
  namespace: production
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
    - port: 5432
```

### Ingress

```mermaid
flowchart LR
    subgraph Internet["Internet"]
        User["User"]
    end

    subgraph Edge["Edge"]
        LB["Load Balancer"]
    end

    subgraph Cluster["Cluster"]
        ING["Ingress Controller\n(Traefik)"]

        subgraph Rules["Routing Rules"]
            R1["api.example.com"]
            R2["app.example.com"]
            R3["admin.example.com"]
        end

        subgraph Services["Services"]
            API["api-service"]
            APP["app-service"]
            ADMIN["admin-service"]
        end
    end

    User --> LB --> ING
    ING --> R1 --> API
    ING --> R2 --> APP
    ING --> R3 --> ADMIN
```

```yaml
# Ingress definition
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    traefik.ingress.kubernetes.io/router.middlewares: production-redirect-https@kubernetescrd
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app
                port:
                  number: 80
```

---

## Namespace Organization

```mermaid
flowchart TB
    subgraph Cluster["k3s Cluster"]
        subgraph System["kube-system"]
            DNS["CoreDNS"]
            CNI["Flannel/Cilium"]
            Metrics["Metrics Server"]
        end

        subgraph Platform["platform"]
            ING["Traefik"]
            CERT["cert-manager"]
            ARGO["ArgoCD"]
        end

        subgraph Monitoring["monitoring"]
            PROM["Prometheus"]
            GRAF["Grafana"]
            LOKI["Loki"]
        end

        subgraph Storage["storage"]
            LH["Longhorn"]
        end

        subgraph Production["production"]
            App1["App 1"]
            App2["App 2"]
            DB["Database"]
        end

        subgraph Staging["staging"]
            SApp1["App 1"]
            SApp2["App 2"]
        end
    end
```

```yaml
# Namespace definitions
---
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    istio-injection: enabled
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
---
apiVersion: v1
kind: Namespace
metadata:
  name: platform
  labels:
    purpose: platform-services
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
  labels:
    purpose: observability
```

---

## Storage with Longhorn

```mermaid
flowchart TB
    subgraph App["Application"]
        Pod["Pod"]
        PVC["PersistentVolumeClaim\n(10Gi)"]
        Pod --> PVC
    end

    subgraph Longhorn["Longhorn"]
        PV["PersistentVolume"]
        Vol["Longhorn Volume"]
        PVC --> PV --> Vol

        subgraph Replicas["Replicas (3x)"]
            R1["Replica 1\n(Node 1)"]
            R2["Replica 2\n(Node 2)"]
            R3["Replica 3\n(Node 3)"]
        end

        Vol --> R1
        Vol --> R2
        Vol --> R3
    end

    subgraph Backup["Backup"]
        S3["S3-Compatible\nObject Storage"]
        R1 -.-> S3
    end
```

```yaml
# StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: longhorn
provisioner: driver.longhorn.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
parameters:
  numberOfReplicas: "3"
  staleReplicaTimeout: "2880"
  fromBackup: ""
  fsType: ext4
---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 10Gi
```

---

## High Availability

```mermaid
flowchart TB
    subgraph HA["High Availability Design"]
        subgraph AntiAffinity["Pod Anti-Affinity"]
            N1["Node 1"]
            N2["Node 2"]
            N3["Node 3"]

            P1["Pod 1"] --> N1
            P2["Pod 2"] --> N2
            P3["Pod 3"] --> N3
        end

        subgraph PDB["Pod Disruption Budget"]
            MIN["minAvailable: 2"]
            PODS["3 Pods Running"]
            MIN --> PODS
        end

        subgraph HPA["Horizontal Pod Autoscaler"]
            METRIC["CPU > 70%"]
            SCALE["Scale 3 → 5"]
            METRIC --> SCALE
        end
    end
```

```yaml
# Deployment with HA features
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-app
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: critical-app
              topologyKey: kubernetes.io/hostname

      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: critical-app
---
# Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: critical-app
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: critical-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: critical-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## Health Checks

```mermaid
sequenceDiagram
    participant K as Kubelet
    participant C as Container
    participant S as Service

    Note over K,S: Startup Phase
    loop Every 5s until success
        K->>C: Startup Probe
        C-->>K: Still starting...
    end
    C-->>K: Ready!

    Note over K,S: Running Phase
    loop Every 10s
        K->>C: Liveness Probe
        C-->>K: I'm alive
    end

    loop Every 5s
        K->>C: Readiness Probe
        alt Ready
            C-->>K: Ready
            K->>S: Add to endpoints
        else Not Ready
            C-->>K: Not ready
            K->>S: Remove from endpoints
        end
    end

    Note over K,S: Failure Scenario
    K->>C: Liveness Probe
    C--xK: No response
    K->>C: Restart container
```

```yaml
# Probe configurations
spec:
  containers:
    - name: app
      # Startup probe: for slow-starting apps
      startupProbe:
        httpGet:
          path: /startup
          port: 8080
        failureThreshold: 30
        periodSeconds: 10

      # Liveness probe: is the app alive?
      livenessProbe:
        httpGet:
          path: /health
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3

      # Readiness probe: can the app serve traffic?
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
        timeoutSeconds: 3
        successThreshold: 1
        failureThreshold: 3
```

---

## kubectl Essentials

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes -o wide
kubectl top nodes

# Namespaces
kubectl get namespaces
kubectl config set-context --current --namespace=production

# Pods
kubectl get pods -A                     # All namespaces
kubectl get pods -o wide                # With node info
kubectl describe pod <name>             # Detailed info
kubectl logs <pod> -f                   # Stream logs
kubectl logs <pod> -c <container>       # Specific container
kubectl exec -it <pod> -- /bin/sh       # Shell access

# Deployments
kubectl get deployments
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl scale deployment/<name> --replicas=5

# Services & Ingress
kubectl get svc,ing
kubectl port-forward svc/<name> 8080:80

# Debug
kubectl get events --sort-by='.lastTimestamp'
kubectl describe node <name>
kubectl top pods --sort-by=memory
```

---

## k9s: Terminal UI

```
┌──────────────────────────────────────────────────────────────┐
│ k9s - Kubernetes CLI To Manage Your Clusters                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Navigation:                                                 │
│  :pod      - View pods                                       │
│  :deploy   - View deployments                                │
│  :svc      - View services                                   │
│  :ns       - View namespaces                                 │
│  :node     - View nodes                                      │
│                                                              │
│  Actions:                                                    │
│  l         - View logs                                       │
│  s         - Shell into container                            │
│  d         - Describe resource                               │
│  y         - View YAML                                       │
│  ctrl-d    - Delete resource                                 │
│  /         - Filter resources                                │
│                                                              │
│  Install: brew install k9s                                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Related

- [Infrastructure-as-Code](./02-Infrastructure-as-Code.md)
- [Configuration Management](./03-Configuration-Management.md)
- [GitOps](./05-GitOps.md)

---

*Last Updated: 2026-02-02*
