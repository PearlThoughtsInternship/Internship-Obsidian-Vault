# Exercise 11: ContentAI — AI Service Integration

> *"AI is not going to replace managers, but managers who use AI will replace managers who don't."*
> — Adapted from business wisdom

## Objective

Integrate AI content generation into ContentAI using Claude/OpenAI APIs, turning Strapi into a true AI-powered content platform.

**This is what makes ContentAI special.**

---

## Prerequisites

- [ ] Completed Exercise 10 (Strapi running)
- [ ] Claude API key or OpenAI API key
- [ ] kubectl configured and connected
- [ ] Strapi admin access

---

## Learning Outcomes

By the end of this exercise, you will:
- Deploy an AI service that integrates with Strapi
- Configure API keys securely
- Implement content generation endpoints
- Monitor AI API costs and latency
- Understand rate limiting and error handling

---

## Part 1: AI Service Architecture

### How ContentAI Uses AI

```mermaid
flowchart LR
    subgraph ContentAI["ContentAI Platform"]
        Strapi["Strapi CMS"]
        AI["AI Service"]
    end

    subgraph External["External APIs"]
        Claude["Claude API"]
        OpenAI["OpenAI API"]
    end

    User["Content Creator"] -->|"Generate blog post"| Strapi
    Strapi -->|"Generate request"| AI
    AI -->|"Prompt"| Claude
    AI -.->|"Fallback"| OpenAI
    Claude -->|"Generated text"| AI
    AI -->|"Content"| Strapi
    Strapi -->|"Draft ready"| User

    style AI fill:#4CAF50
```

### AI Service Responsibilities

| Feature | Description |
|---------|-------------|
| **Content Generation** | Generate blog posts, descriptions from prompts |
| **Summarization** | Condense long documents |
| **Translation** | Translate content to multiple languages |
| **SEO Optimization** | Suggest titles, meta descriptions |
| **Rate Limiting** | Protect API budget |
| **Fallback** | Switch providers if one fails |

---

## Part 2: AI Service Deployment

### Create AI Service Secret

```yaml
# ai-service/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ai-service-secret
  namespace: contentai
type: Opaque
stringData:
  # Claude API (Primary)
  ANTHROPIC_API_KEY: "sk-ant-api03-YOUR_KEY"

  # OpenAI API (Fallback)
  OPENAI_API_KEY: "sk-YOUR_KEY"

  # Service authentication
  API_SECRET: "your-internal-api-secret"
```

### AI Service ConfigMap

```yaml
# ai-service/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-service-config
  namespace: contentai
data:
  # Server config
  PORT: "3001"
  HOST: "0.0.0.0"
  NODE_ENV: production

  # AI Provider config
  PRIMARY_PROVIDER: claude
  FALLBACK_PROVIDER: openai

  # Claude settings
  CLAUDE_MODEL: claude-3-5-sonnet-20241022
  CLAUDE_MAX_TOKENS: "4096"

  # OpenAI settings (fallback)
  OPENAI_MODEL: gpt-4-turbo-preview
  OPENAI_MAX_TOKENS: "4096"

  # Rate limiting
  RATE_LIMIT_REQUESTS: "100"
  RATE_LIMIT_WINDOW_MS: "60000"

  # Strapi integration
  STRAPI_URL: "http://strapi:1337"
```

### AI Service Deployment

```yaml
# ai-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
  namespace: contentai
  labels:
    app: ai-service
    product: contentai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-service
  template:
    metadata:
      labels:
        app: ai-service
        product: contentai
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3001"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: ai-service
          image: node:20-alpine
          command:
            - node
            - /app/server.js
          ports:
            - containerPort: 3001
              name: http
          envFrom:
            - configMapRef:
                name: ai-service-config
            - secretRef:
                name: ai-service-secret
          volumeMounts:
            - name: ai-service-code
              mountPath: /app
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3001
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 3001
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: ai-service-code
          configMap:
            name: ai-service-code
```

### AI Service Code (ConfigMap)

```yaml
# ai-service/code-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-service-code
  namespace: contentai
data:
  server.js: |
    const http = require('http');
    const https = require('https');

    const PORT = process.env.PORT || 3001;

    // Metrics storage
    const metrics = {
      requests: 0,
      errors: 0,
      claudeRequests: 0,
      openaiRequests: 0,
      totalTokens: 0,
      latencySum: 0
    };

    // Rate limiting
    const rateLimiter = {
      requests: [],
      maxRequests: parseInt(process.env.RATE_LIMIT_REQUESTS || '100'),
      windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000')
    };

    function checkRateLimit() {
      const now = Date.now();
      rateLimiter.requests = rateLimiter.requests.filter(
        t => now - t < rateLimiter.windowMs
      );
      if (rateLimiter.requests.length >= rateLimiter.maxRequests) {
        return false;
      }
      rateLimiter.requests.push(now);
      return true;
    }

    // Claude API call
    async function callClaude(prompt, maxTokens = 4096) {
      return new Promise((resolve, reject) => {
        const data = JSON.stringify({
          model: process.env.CLAUDE_MODEL || 'claude-3-5-sonnet-20241022',
          max_tokens: maxTokens,
          messages: [{ role: 'user', content: prompt }]
        });

        const options = {
          hostname: 'api.anthropic.com',
          port: 443,
          path: '/v1/messages',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': process.env.ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01'
          }
        };

        const req = https.request(options, (res) => {
          let body = '';
          res.on('data', chunk => body += chunk);
          res.on('end', () => {
            if (res.statusCode === 200) {
              const parsed = JSON.parse(body);
              metrics.claudeRequests++;
              metrics.totalTokens += parsed.usage?.input_tokens || 0;
              metrics.totalTokens += parsed.usage?.output_tokens || 0;
              resolve(parsed.content[0].text);
            } else {
              reject(new Error(`Claude API error: ${res.statusCode} - ${body}`));
            }
          });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
      });
    }

    // OpenAI API call (fallback)
    async function callOpenAI(prompt, maxTokens = 4096) {
      return new Promise((resolve, reject) => {
        const data = JSON.stringify({
          model: process.env.OPENAI_MODEL || 'gpt-4-turbo-preview',
          max_tokens: maxTokens,
          messages: [{ role: 'user', content: prompt }]
        });

        const options = {
          hostname: 'api.openai.com',
          port: 443,
          path: '/v1/chat/completions',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
          }
        };

        const req = https.request(options, (res) => {
          let body = '';
          res.on('data', chunk => body += chunk);
          res.on('end', () => {
            if (res.statusCode === 200) {
              const parsed = JSON.parse(body);
              metrics.openaiRequests++;
              metrics.totalTokens += parsed.usage?.total_tokens || 0;
              resolve(parsed.choices[0].message.content);
            } else {
              reject(new Error(`OpenAI API error: ${res.statusCode} - ${body}`));
            }
          });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
      });
    }

    // Generate content with fallback
    async function generateContent(prompt, options = {}) {
      const startTime = Date.now();

      try {
        // Try primary provider (Claude)
        const result = await callClaude(prompt, options.maxTokens);
        metrics.latencySum += Date.now() - startTime;
        return { content: result, provider: 'claude' };
      } catch (claudeError) {
        console.error('Claude failed, trying OpenAI:', claudeError.message);

        try {
          // Fallback to OpenAI
          const result = await callOpenAI(prompt, options.maxTokens);
          metrics.latencySum += Date.now() - startTime;
          return { content: result, provider: 'openai' };
        } catch (openaiError) {
          metrics.errors++;
          throw new Error(`All providers failed: ${openaiError.message}`);
        }
      }
    }

    // HTTP Server
    const server = http.createServer(async (req, res) => {
      const url = new URL(req.url, `http://${req.headers.host}`);

      // CORS
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

      if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
      }

      // Health check
      if (url.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
        return;
      }

      // Metrics endpoint (Prometheus format)
      if (url.pathname === '/metrics') {
        const avgLatency = metrics.requests > 0
          ? metrics.latencySum / metrics.requests
          : 0;

        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end(`
    # HELP ai_requests_total Total AI generation requests
    # TYPE ai_requests_total counter
    ai_requests_total ${metrics.requests}

    # HELP ai_errors_total Total AI generation errors
    # TYPE ai_errors_total counter
    ai_errors_total ${metrics.errors}

    # HELP ai_claude_requests_total Claude API requests
    # TYPE ai_claude_requests_total counter
    ai_claude_requests_total ${metrics.claudeRequests}

    # HELP ai_openai_requests_total OpenAI API requests
    # TYPE ai_openai_requests_total counter
    ai_openai_requests_total ${metrics.openaiRequests}

    # HELP ai_tokens_total Total tokens used
    # TYPE ai_tokens_total counter
    ai_tokens_total ${metrics.totalTokens}

    # HELP ai_latency_avg_ms Average latency in milliseconds
    # TYPE ai_latency_avg_ms gauge
    ai_latency_avg_ms ${avgLatency.toFixed(2)}
        `);
        return;
      }

      // Generate content endpoint
      if (url.pathname === '/api/generate' && req.method === 'POST') {
        metrics.requests++;

        // Check auth
        const authHeader = req.headers.authorization;
        if (!authHeader || authHeader !== `Bearer ${process.env.API_SECRET}`) {
          res.writeHead(401, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Unauthorized' }));
          return;
        }

        // Check rate limit
        if (!checkRateLimit()) {
          res.writeHead(429, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Rate limit exceeded' }));
          return;
        }

        // Parse body
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', async () => {
          try {
            const { prompt, type, maxTokens } = JSON.parse(body);

            if (!prompt) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Prompt is required' }));
              return;
            }

            // Build prompt based on type
            let fullPrompt = prompt;
            if (type === 'blog') {
              fullPrompt = `Write a professional blog post about: ${prompt}\n\nFormat with markdown headers and paragraphs.`;
            } else if (type === 'summary') {
              fullPrompt = `Summarize the following text concisely:\n\n${prompt}`;
            } else if (type === 'seo') {
              fullPrompt = `Generate SEO metadata for: ${prompt}\n\nProvide: title (60 chars), description (160 chars), and 5 keywords.`;
            }

            const result = await generateContent(fullPrompt, { maxTokens });

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
              success: true,
              content: result.content,
              provider: result.provider,
              type: type || 'custom'
            }));
          } catch (error) {
            console.error('Generation error:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: error.message }));
          }
        });
        return;
      }

      // 404
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not found' }));
    });

    server.listen(PORT, () => {
      console.log(`AI Service running on port ${PORT}`);
    });
```

### AI Service

```yaml
# ai-service/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-service
  namespace: contentai
  labels:
    app: ai-service
spec:
  type: ClusterIP
  ports:
    - port: 3001
      targetPort: 3001
      name: http
  selector:
    app: ai-service
```

### Deploy AI Service

```bash
kubectl apply -f ai-service/

# Wait for deployment
kubectl wait --for=condition=ready pod -l app=ai-service -n contentai --timeout=60s
```

---

## Part 3: Test AI Generation

### Test from Command Line

```bash
# Get AI service pod name
AI_POD=$(kubectl get pod -n contentai -l app=ai-service -o jsonpath='{.items[0].metadata.name}')

# Test health
kubectl exec -n contentai $AI_POD -- curl -s http://localhost:3001/health | jq .

# Test generation (from within cluster)
kubectl run test-curl --rm -it --restart=Never --image=curlimages/curl -- \
  curl -X POST http://ai-service.contentai:3001/api/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-internal-api-secret" \
  -d '{"prompt": "Write a paragraph about Kubernetes", "type": "blog"}'
```

### Test Metrics

```bash
kubectl exec -n contentai $AI_POD -- curl -s http://localhost:3001/metrics
```

---

## Part 4: Strapi Integration

### Create AI Plugin in Strapi

You can integrate the AI service with Strapi by:

1. **Custom API Route** — Add a route in Strapi that calls the AI service
2. **Lifecycle Hooks** — Auto-generate content on create
3. **Admin UI Plugin** — Add "Generate" button to content editor

### Example: Custom Controller

Create `src/api/ai/controllers/generate.js` in your Strapi project:

```javascript
// Strapi custom controller for AI generation
module.exports = {
  async generate(ctx) {
    const { prompt, type } = ctx.request.body;

    try {
      const response = await fetch('http://ai-service:3001/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.AI_SERVICE_SECRET}`
        },
        body: JSON.stringify({ prompt, type })
      });

      const data = await response.json();

      if (!response.ok) {
        return ctx.badRequest(data.error);
      }

      return ctx.send(data);
    } catch (error) {
      return ctx.internalServerError(error.message);
    }
  }
};
```

---

## Part 5: Monitoring AI Costs

### Grafana Dashboard

Create a dashboard for AI service metrics:

```yaml
# monitoring/ai-dashboard-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-ai
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  ai-service.json: |
    {
      "title": "ContentAI - AI Service",
      "panels": [
        {
          "title": "Requests per Minute",
          "type": "graph",
          "targets": [
            {
              "expr": "rate(ai_requests_total[1m]) * 60",
              "legendFormat": "Requests/min"
            }
          ]
        },
        {
          "title": "Provider Distribution",
          "type": "piechart",
          "targets": [
            {
              "expr": "ai_claude_requests_total",
              "legendFormat": "Claude"
            },
            {
              "expr": "ai_openai_requests_total",
              "legendFormat": "OpenAI"
            }
          ]
        },
        {
          "title": "Total Tokens Used",
          "type": "stat",
          "targets": [
            {
              "expr": "ai_tokens_total",
              "legendFormat": "Tokens"
            }
          ]
        },
        {
          "title": "Error Rate",
          "type": "graph",
          "targets": [
            {
              "expr": "rate(ai_errors_total[5m]) / rate(ai_requests_total[5m]) * 100",
              "legendFormat": "Error %"
            }
          ]
        },
        {
          "title": "Average Latency",
          "type": "gauge",
          "targets": [
            {
              "expr": "ai_latency_avg_ms",
              "legendFormat": "ms"
            }
          ]
        }
      ]
    }
```

### Cost Estimation

| Provider | Model | Cost per 1K tokens |
|----------|-------|-------------------|
| Claude | claude-3-5-sonnet | ~$0.003 input / $0.015 output |
| OpenAI | gpt-4-turbo | ~$0.01 input / $0.03 output |

Monitor with: `ai_tokens_total` metric × cost per token

---

## Success Criteria

| Criteria | Check |
|----------|-------|
| AI service running (2 replicas) | `kubectl get pods -n contentai -l app=ai-service` |
| Health endpoint responding | `curl http://ai-service.contentai:3001/health` |
| Content generation working | POST to `/api/generate` returns content |
| Metrics exposed | `/metrics` returns Prometheus format |
| Fallback working | Claude failure triggers OpenAI |
| Rate limiting active | 429 on excessive requests |

---

## What You've Built

```mermaid
flowchart TB
    subgraph ContentAI["ContentAI Platform - Now with AI!"]
        Strapi["Strapi CMS"]
        AI["AI Service"]
        PG["PostgreSQL"]
        Redis["Redis"]
    end

    subgraph External["AI Providers"]
        Claude["Claude API"]
        OpenAI["OpenAI API"]
    end

    User["Content Creator"] --> Strapi
    Strapi -->|"Generate"| AI
    AI -->|"Primary"| Claude
    AI -.->|"Fallback"| OpenAI

    style AI fill:#4CAF50
    style Claude fill:#2196F3
```

**ContentAI now generates content with AI!** 🚀

---

## Architecture Diagram

```mermaid
sequenceDiagram
    participant User as Content Creator
    participant Strapi as Strapi CMS
    participant AI as AI Service
    participant Claude as Claude API
    participant OpenAI as OpenAI API

    User->>Strapi: "Generate blog about K8s"
    Strapi->>AI: POST /api/generate
    AI->>Claude: API Request
    alt Claude succeeds
        Claude->>AI: Generated content
    else Claude fails
        AI->>OpenAI: Fallback request
        OpenAI->>AI: Generated content
    end
    AI->>Strapi: { content, provider }
    Strapi->>User: Draft ready for review
```

---

## Next Steps

- [[06-GitOps-ArgoCD]] — Manage AI service with GitOps
- [[07-Observability-Stack]] — Monitor AI costs and latency
- [[09-Security-Hardening]] — Secure API keys

---

## Troubleshooting

### API Key Issues

```bash
# Check if secret is mounted
kubectl exec -n contentai deploy/ai-service -- env | grep API_KEY

# Verify Claude API works
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
```

### Rate Limiting

```bash
# Check current rate limit status
kubectl exec -n contentai deploy/ai-service -- curl -s http://localhost:3001/metrics | grep rate
```

### Fallback Not Working

Check both API keys are configured and valid:

```bash
kubectl get secret ai-service-secret -n contentai -o jsonpath='{.data.ANTHROPIC_API_KEY}' | base64 -d
kubectl get secret ai-service-secret -n contentai -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d
```

---

## Cost Control Tips

1. **Set token limits** — `maxTokens` in requests
2. **Cache responses** — Redis for repeated prompts
3. **Rate limit** — Prevent runaway costs
4. **Monitor daily** — Alert on cost thresholds
5. **Use summaries** — Shorter prompts = fewer tokens

---

*Last Updated: 2026-02-02*
