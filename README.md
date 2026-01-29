# LLM Engineering & Deployment - Week 10 Code Examples

**Week 10: Reliability, Monitoring & LLM Ops**  
Part of the LLM Engineering & Deployment Certification Program

This repository contains code examples for monitoring, observability, cost management, and security of LLM systems in production. The module covers:

- **LangFuse** - Open-source LLM tracing and observability
- **LangSmith** - LangChain's tracing and debugging platform
- **LiteLLM** - Unified proxy for cost tracking, alerting, and multi-provider routing
- **Bifrost** - LLM gateway for model switching and load balancing

---

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- OpenAI API key
- Anthropic API key (optional)
- LangFuse account (free self-hosted or cloud)
- LangSmith account (free tier available)

---

## Setup

### 1. Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 2. Dependency Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```bash
# LLM Providers
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# LangFuse (self-hosted or cloud)
LANGFUSE_SECRET_KEY=sk-lf-xxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxx
LANGFUSE_BASE_URL=http://localhost:3000  # or https://cloud.langfuse.com

# LangSmith
LANGSMITH_API_KEY=lsv2_pt_xxxxx
LANGSMITH_PROJECT=your-project-name
LANGSMITH_TRACING=true
```

---

## Running the Code Examples

### LangFuse Tracing

Demonstrates LLM observability with the `@observe()` decorator for automatic tracing.

**Run the examples:**

```bash
python code/langfuse_tracing.py
```

**What it demonstrates:**

| Example | Description |
|---------|-------------|
| Simple Question | Single LLM call with automatic tracing |
| Extract Keywords | LLM call + Python post-processing |
| Content Pipeline | Multi-step chain (Draft → Critique → Refine) |

**View traces:** Open your LangFuse dashboard to see the traces with latency, token usage, and nested spans.

---

### LangSmith Tracing

Demonstrates LLM tracing with the `@traceable()` decorator and `wrap_openai()` for the OpenAI SDK.

**Run the examples:**

```bash
python code/langsmith_tracing.py
```

**What it demonstrates:**

| Example | Description |
|---------|-------------|
| Simple Question | Single LLM call with automatic tracing |
| Extract Keywords | LLM call + Python post-processing |
| Content Pipeline | Multi-step chain with metadata |

**View traces:** Open the [LangSmith dashboard](https://smith.langchain.com) to see traces, latency, and token usage.

---

### LiteLLM Proxy

Unified LLM gateway with cost tracking, budget enforcement, and multi-provider support.

**Start the proxy:**

```bash
cd code/litellm
docker compose up -d
```

**Access the UI:** Open [http://localhost:4000/ui](http://localhost:4000/ui)

**Test with client:**

```bash
python code/litellm/client.py
```

**Key features:**

| Feature | Description |
|---------|-------------|
| Unified API | One endpoint for OpenAI, Anthropic, local models |
| Cost Tracking | Automatic token counting and spend logging |
| Budget Enforcement | Set spending limits per virtual key |
| Custom Pricing | Define per-token costs for self-hosted models |
| Alerting | Slack/email alerts for budget thresholds |

**Configuration:** Edit `code/litellm/litellm_config.yaml` to add models:

```yaml
model_list:
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY
```

**Cleanup:**

```bash
cd code/litellm
docker compose down
```

---

### Bifrost Gateway

LLM gateway with model switching and OpenAI-compatible API.

**Start the gateway:**

```bash
docker run -p 8080:8080 maximhq/bifrost
```

This starts Bifrost on port 8080. Configure providers via the web UI at [http://localhost:8080](http://localhost:8080).

**Run the interactive client:**

```bash
python code/bifrost/client.py
```

**Client commands:**

| Command | Description |
|---------|-------------|
| `/model` or `/switch` | Switch to a different model mid-conversation |
| `/models` or `/list` | List all available models |
| `/current` | Show the current model |
| `/help` | Show available commands |
| `quit` or `exit` | Exit the chat |

**Stop the gateway:**

```bash
docker stop $(docker ps -q --filter ancestor=maximhq/bifrost)
```

---

## Lessons Overview

| # | Lesson | Topic | Key Concepts |
|---|--------|-------|--------------|
| - | Overview | Unit Introduction | LLMOps feedback loop, unit structure |
| 1 | Monitoring Fundamentals | Core Metrics | TTFT, TPS, latency percentiles, throughput |
| 2 | Observability & Tracing | Structured Logging | Logs, metrics, traces, spans, PII handling |
| 3 | LangFuse | Hands-On Tool | `@observe()` decorator, nested traces, metadata |
| 4 | LangSmith | Hands-On Tool | `@traceable()`, `wrap_openai()`, Playground |
| 5 | CloudWatch | AWS Monitoring | Custom metrics, dashboards, alarms |
| 6 | Alerting & Incident Response | Operations | Thresholds, runbooks, on-call, post-mortems |
| 7 | Cost Monitoring | Optimization | LLM cascading, caching, speculative decoding |
| 8 | LiteLLM | Hands-On Tool | Proxy setup, cost tracking, budget enforcement |
| 9 | Bifrost | Hands-On Tool | Model gateway, routing, load balancing |
| 10 | Drift Detection | Quality Monitoring | Data drift, LLM-as-Judge, semantic monitoring |
| 11 | Security | Protection | Prompt injection, guardrails, PII redaction |

---

## Project Structure

```
rt-llm-eng-cert-week10/
├── code/
│   ├── langfuse_tracing.py      # LangFuse tracing examples
│   ├── langsmith_tracing.py     # LangSmith tracing examples
│   ├── litellm/
│   │   ├── docker-compose.yaml  # LiteLLM + PostgreSQL setup
│   │   ├── litellm_config.yaml  # Model configuration
│   │   └── client.py            # Interactive client
│   └── bifrost/
│       ├── docker-compose.yaml  # Bifrost gateway setup
│       ├── config.json          # Provider configuration
│       └── client.py            # Interactive client with model switching
├── lessons/
│   ├── overview.md              # Unit overview
│   ├── lesson1-monitoring-fundamentals.md
│   ├── lesson2-observability-tracing.md
│   ├── lesson3-langfuse.md
│   ├── lesson4-langsmith.md
│   ├── lesson6-alerting-incident-response.md
│   ├── lesson7-cost-monitoring.md
│   ├── lesson8-litellm.md
│   ├── lesson10-drift-detection.md
│   ├── lesson11-security.md
│   └── diagrams/
│       ├── guardrails-workflow.svg
│       └── two-llm-pattern.svg
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md
```

---

## Tool Comparison

| Tool | Purpose | Self-Hosted | Cost Tracking | Tracing |
|------|---------|-------------|---------------|---------|
| **LangFuse** | LLM Observability | ✅ Yes | ✅ Yes | ✅ Yes |
| **LangSmith** | LLM Debugging | ❌ No (cloud only) | ✅ Yes | ✅ Yes |
| **LiteLLM** | Unified Proxy | ✅ Yes | ✅ Yes (custom pricing) | Via integrations |
| **Bifrost** | LLM Gateway | ✅ Yes | ✅ Yes (built-in catalog) | ❌ Limited |

---

## Decision Framework

**Choose LangFuse if:**
- You want full control with self-hosting
- You need open-source with no vendor lock-in
- You want to build evaluation datasets from production traces

**Choose LangSmith if:**
- You're already using LangChain
- You want a polished UI with Playground features
- You prefer a managed cloud solution

**Choose LiteLLM if:**
- You need a unified API for multiple providers
- Custom token pricing for self-hosted models is important
- You want budget enforcement and alerting

**Choose Bifrost if:**
- You need high-performance routing (< 100µs overhead)
- You want request-type restrictions per provider
- You're building a Go-based infrastructure

---

## Key Concepts Covered

### Monitoring Metrics
- **TTFT** (Time to First Token) - User-perceived latency
- **TPS** (Tokens per Second) - Generation speed
- **Throughput** - Requests per second capacity
- **Queue Depth** - Pending request backlog

### Cost Optimization Strategies
- **LLM Cascading** - Cheap model first, escalate on low confidence
- **Prompt Caching** - Exact match, semantic, and prefix caching
- **Speculative Decoding** - Draft model + verification
- **Quantization** - INT4/INT8 for reduced GPU requirements

### Security Patterns
- **Two-LLM Pattern** - Gatekeeper model for intent detection
- **Guardrails** - Input/output validation and filtering
- **PII Redaction** - Strip sensitive data before API calls
- **Agent Security** - Deterministic tool contracts, allowlists

---

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**

- Share and adapt this material for non-commercial purposes
- Must give appropriate credit and indicate changes made
- Must distribute adaptations under the same license

See [LICENSE](LICENSE) for full terms.

---

## Contact

For questions or issues related to this repository, please refer to the course materials or contact your instructor.
