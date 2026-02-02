# Observability

> *"Monitoring tells you whether a system is working. Observability lets you ask why it's not."*
> — **Distributed Systems Observability** (Cindy Sridharan)

## The Three Pillars

> *You can't fix what you can't see. Observability transforms "the system is broken" into "the API latency increased at 14:32 when the database connection pool exhausted."*

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
        subgraph Metrics["METRICS"]
            Prom["Prometheus<br/>TSDB, PromQL"]
            NE["Node Exporter"]
            KSM["kube-state-metrics"]
        end

        subgraph Logs["LOGS"]
            Loki["Loki<br/>Log Aggregation"]
            Promtail["Promtail<br/>Agent"]
        end

        subgraph Traces["TRACES"]
            Tempo["Tempo<br/>Distributed Tracing"]
            OTel["OpenTelemetry<br/>Collector"]
        end
    end

    subgraph Storage["Long-term Storage"]
        S3["S3-Compatible<br/>(MinIO/Hetzner)"]
    end

    subgraph Visualization["Visualization & Alerting"]
        Graf["Grafana<br/>Dashboards"]
        AM["AlertManager"]
        Slack["Slack/PagerDuty"]
    end

    App1 & App2 & App3 -->|"/metrics"| Prom
    App1 & App2 & App3 -->|"stdout/stderr"| Promtail --> Loki
    App1 & App2 & App3 -->|"traces"| OTel --> Tempo

    NE & KSM --> Prom
    Prom & Loki & Tempo --> Graf
    Prom --> AM --> Slack
    Prom & Loki & Tempo -.-> S3

    style Prom fill:#E6522C
    style Loki fill:#F2C811
    style Tempo fill:#26BBD1
    style Graf fill:#F46800
```

---

## The Three Pillars Explained

```mermaid
mindmap
  root((Observability))
    Metrics
      What: Numeric measurements over time
      Tools: Prometheus, VictoriaMetrics
      Use: Alerting, dashboards, SLOs
      Example: request_count, latency_p99
    Logs
      What: Timestamped event records
      Tools: Loki, Elasticsearch
      Use: Debugging, audit trails
      Example: Error stack traces
    Traces
      What: Request flow across services
      Tools: Tempo, Jaeger, Zipkin
      Use: Performance analysis
      Example: API call through 5 services
```

### When to Use Each

| Question | Pillar | Example |
|----------|--------|---------|
| "How many requests per second?" | **Metrics** | `rate(http_requests_total[5m])` |
| "What error did user X see?" | **Logs** | Search for user ID in Loki |
| "Why is this API slow?" | **Traces** | Follow request through services |
| "Is the system healthy?" | **Metrics** | Dashboard with uptime, error rates |
| "What happened at 2:45 AM?" | **Logs** | Time-range query in Grafana |

---

## Prometheus Deep Dive

### How Prometheus Works

```mermaid
sequenceDiagram
    participant App as Application
    participant Prom as Prometheus
    participant AM as AlertManager
    participant Graf as Grafana

    loop Every 15 seconds
        Prom->>App: GET /metrics
        App-->>Prom: Counter, Gauge, Histogram data
        Prom->>Prom: Store in TSDB
    end

    Prom->>Prom: Evaluate alert rules
    alt Alert firing
        Prom->>AM: Send alert
        AM->>AM: Dedupe, group, route
        AM->>Slack: Notify on-call
    end

    Graf->>Prom: PromQL query
    Prom-->>Graf: Time series data
    Graf->>Graf: Render dashboard
```

### Metric Types

| Type | Description | Example |
|------|-------------|---------|
| **Counter** | Monotonically increasing | `http_requests_total` |
| **Gauge** | Can go up or down | `temperature_celsius` |
| **Histogram** | Distribution of values | `http_request_duration_seconds` |
| **Summary** | Similar to histogram, calculates quantiles | `request_duration_summary` |

### PromQL Essentials

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m])) * 100

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/
node_memory_MemTotal_bytes * 100

# Pod restarts in last hour
increase(kube_pod_container_status_restarts_total[1h])

# Top 5 pods by CPU
topk(5, sum by (pod) (rate(container_cpu_usage_seconds_total[5m])))
```

### Prometheus Configuration

```yaml
# prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Kubernetes service discovery
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)

  # Node exporter
  - job_name: 'node-exporter'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: replace
        target_label: __address__
        replacement: node-exporter.monitoring.svc:9100
```

---

## Grafana Loki for Logs

### Loki Architecture

```mermaid
flowchart LR
    subgraph Sources["Log Sources"]
        Pod1["Pod A"]
        Pod2["Pod B"]
        Pod3["Pod C"]
    end

    subgraph Collection["Collection"]
        PT["Promtail<br/>(DaemonSet)"]
    end

    subgraph Loki["Loki Cluster"]
        Dist["Distributor"]
        Ing["Ingester"]
        QF["Query Frontend"]
        Querier["Querier"]
    end

    subgraph Storage["Storage"]
        Chunks["Chunks<br/>(S3/MinIO)"]
        Index["Index<br/>(BoltDB/Cassandra)"]
    end

    Pod1 & Pod2 & Pod3 --> PT
    PT --> Dist --> Ing
    Ing --> Chunks & Index
    QF --> Querier --> Chunks & Index

    Graf["Grafana"] --> QF

    style Dist fill:#F2C811
    style Ing fill:#F2C811
```

### LogQL Examples

```logql
# All logs from a specific app
{app="user-service"}

# Errors only
{app="user-service"} |= "error"

# JSON parsing
{app="api-gateway"} | json | status >= 500

# Rate of errors
rate({app="user-service"} |= "error" [5m])

# Top error messages
{app="user-service"} |= "error" | pattern "<_> error: <msg>" | topk(5, msg)

# Logs with specific trace ID
{app=~".+"} |= "trace_id=abc123"
```

### Promtail Configuration

```yaml
# promtail.yml

server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - docker: {}
      - json:
          expressions:
            level: level
            msg: msg
      - labels:
          level:
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

---

## Grafana Tempo for Traces

### Distributed Tracing Concept

```mermaid
sequenceDiagram
    participant User
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant User as User Service
    participant DB as Database

    User->>Gateway: POST /api/orders
    Note over Gateway: trace_id: abc123<br/>span_id: span1

    Gateway->>Auth: Validate token
    Note over Auth: trace_id: abc123<br/>span_id: span2<br/>parent: span1

    Auth-->>Gateway: Token valid

    Gateway->>User: Get user details
    Note over User: trace_id: abc123<br/>span_id: span3<br/>parent: span1

    User->>DB: SELECT * FROM users
    Note over DB: trace_id: abc123<br/>span_id: span4<br/>parent: span3

    DB-->>User: User data
    User-->>Gateway: User details

    Gateway-->>User: Order created
```

### OpenTelemetry Configuration

```yaml
# otel-collector-config.yaml

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_percentage: 80

exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

  prometheus:
    endpoint: 0.0.0.0:8889

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/tempo]

    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
```

---

## Alert Rules

### Critical Alerts

```yaml
# alerts/critical.yml

groups:
  - name: critical
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Pod crash looping
      - alert: PodCrashLooping
        expr: |
          increase(kube_pod_container_status_restarts_total[1h]) > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"
          description: "{{ $value }} restarts in the last hour"

      # Node not ready
      - alert: NodeNotReady
        expr: |
          kube_node_status_condition{condition="Ready", status="true"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Node {{ $labels.node }} is not ready"

      # Disk space critical
      - alert: DiskSpaceCritical
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space critical on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} free"
```

### Warning Alerts

```yaml
# alerts/warning.yml

groups:
  - name: warning
    rules:
      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "p95 latency is {{ $value }}s"

      # Memory usage high
      - alert: HighMemoryUsage
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
          /
          node_memory_MemTotal_bytes > 0.85
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"

      # Certificate expiring soon
      - alert: CertificateExpiringSoon
        expr: |
          (cert_exporter_cert_not_after - time()) / 86400 < 30
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Certificate expiring in {{ $value }} days"
```

---

## AlertManager Configuration

```yaml
# alertmanager.yml

global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/xxx'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack-notifications'

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true

    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-low'
        title: '{{ .GroupLabels.alertname }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
        severity: critical

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname']
```

---

## Golden Signals Dashboard

```mermaid
flowchart TB
    subgraph Dashboard["Golden Signals Dashboard"]
        subgraph Latency["LATENCY"]
            L1["p50: 45ms"]
            L2["p95: 120ms"]
            L3["p99: 350ms"]
        end

        subgraph Traffic["TRAFFIC"]
            T1["Requests/sec: 1,234"]
            T2["Active connections: 456"]
        end

        subgraph Errors["ERRORS"]
            E1["Error rate: 0.3%"]
            E2["5xx count: 12"]
            E3["4xx count: 89"]
        end

        subgraph Saturation["SATURATION"]
            S1["CPU: 45%"]
            S2["Memory: 62%"]
            S3["Disk: 34%"]
        end
    end

    style L1 fill:#4CAF50
    style L2 fill:#FFC107
    style L3 fill:#FF5722
    style E1 fill:#4CAF50
```

### Grafana Dashboard JSON

```json
{
  "title": "Golden Signals",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m]))",
          "legendFormat": "Requests/s"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100",
          "legendFormat": "Error %"
        }
      ],
      "thresholds": {
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 1},
          {"color": "red", "value": 5}
        ]
      }
    },
    {
      "title": "Latency (p95)",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
          "legendFormat": "p95"
        }
      ]
    }
  ]
}
```

---

## Helm Installation

### kube-prometheus-stack

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install with custom values
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f prometheus-values.yaml
```

```yaml
# prometheus-values.yaml

prometheus:
  prometheusSpec:
    retention: 15d
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: longhorn
          resources:
            requests:
              storage: 50Gi

grafana:
  adminPassword: "changeme"
  persistence:
    enabled: true
    size: 10Gi

alertmanager:
  config:
    global:
      slack_api_url: "https://hooks.slack.com/..."
```

### Loki Stack

```bash
helm repo add grafana https://grafana.github.io/helm-charts

helm install loki grafana/loki-stack \
  --namespace monitoring \
  -f loki-values.yaml
```

```yaml
# loki-values.yaml

loki:
  persistence:
    enabled: true
    size: 50Gi

promtail:
  enabled: true
```

---

## Related

- [Architecture](../02-Engineering/01-Architecture.md)
- [Security](./03-Security.md)
- [GitOps](../02-Engineering/05-GitOps.md)

---

*Last Updated: 2026-02-02*
