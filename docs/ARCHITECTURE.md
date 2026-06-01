# Architecture

## Layer Map

```
┌──────────────────────────────────────────────────────────────────┐
│  API  ·  Spring MVC  ·  FastAPI router  ·  Django REST Framework │
├──────────────────────────────────────────────────────────────────┤
│  Services  ·  SignalIngestionService  ·  RiskScoringService      │
├──────────────────────────────────────────────────────────────────┤
│  Ports  ·  SignalWriter  ·  SignalReader  ·  Cache  (Protocols)  │
├──────────────────────────────────────────────────────────────────┤
│  Adapters  ·  PostgresSignalRepository  ·  DjangoSignalRepository│
│            ·  RedisCache  ·  FakeCache (tests)                   │
└──────────────────────────────────────────────────────────────────┘
           domain and ports are framework-zero — zero imports above them
```

> **Engineering note:** This is Hexagonal Architecture (Ports and Adapters). The rule: inner layers never import outer layers. The domain has no `import fastapi`, no `import django`, no `import sqlalchemy`. Swap the database by writing one new adapter class — nothing else changes.

---

## Write Path — POST /api/v1/signals

```mermaid
sequenceDiagram
    participant CI as Client (CI job / alertmanager)
    participant A as API layer
    participant I as SignalIngestionService
    participant W as SignalWriter (port)
    participant DB as PostgreSQL
    participant R as Redis

    CI->>+A: POST /api/v1/signals {X-API-Key}
    Note over A: 401 if key missing or wrong
    A->>+I: ingest(signal_dict)
    I->>+W: save(signal)
    Note over W: PostgresSignalRepository or DjangoSignalRepository
    W->>+DB: INSERT INTO signals
    DB-->>-W: row with generated id
    W-->>-I: saved dict
    I->>R: DEL risk:{service_name}
    Note over I,R: cache-aside eviction — next read recomputes fresh
    I-->>-A: saved dict
    A-->>-CI: 201 Created
```

> **Engineering note — cache-aside:** Evict-on-write guarantees consistency. The alternative (write-through) requires atomic DB+cache writes. Cache-aside is simpler and correct here because the miss cost (one SQL window query) is acceptable. Failure mode if Redis is down: every read falls back to a full DB scan — degraded latency, not an outage.

---

## Read Path — GET /api/v1/services/{name}/risk-summary

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API layer
    participant R as RiskScoringService
    participant Redis
    participant DB as PostgreSQL

    C->>+A: GET /services/{name}/risk-summary {X-API-Key}
    A->>+R: get_risk_summary(service_name)
    R->>Redis: GET risk:{name}

    alt cache hit (common path)
        Redis-->>R: JSON string
        R-->>A: summary dict (zero DB I/O)
        A-->>C: 200 OK  [fast path]
    else cache miss (first read or post-ingest)
        Redis-->>R: nil
        R->>+DB: SELECT * FROM signals WHERE service=name AND observed_at >= now()-lookback_hours
        DB-->>-R: signal rows
        R->>R: policy.compute_level(signals) → (score, level)
        Note over R: WeightedRiskPolicy or SpikeDetectionPolicy
        R->>Redis: SET risk:{name} {json} EX 60
        R-->>A: summary dict
        A-->>-C: 200 OK  [computed path]
    end
```

> **Engineering note — read path:** "Stateless" means the service holds no mutable state — it reads all needed data from the DB window query every miss. This makes horizontal scaling trivial. Multiple pods all share the same Redis cache, so cache warm-up is collective, not per-pod.

---

## Component Map

```mermaid
flowchart TD
    Client["CI job / alertmanager / dashboard"] -->|X-API-Key header| API

    subgraph API["API Layer — framework-swappable"]
        direction LR
        J["Spring MVC\nJava"]
        F["FastAPI router\npython/"]
        D["DRF APIView\ndjango/"]
    end

    API --> SIS["SignalIngestionService\n(SRP: writes + evicts only)"]
    API --> RSS["RiskScoringService\n(SRP: scores + caches only)"]

    SIS -->|"SignalWriter port"| Adapters
    SIS -->|"Cache port"| CacheAdapters
    RSS -->|"SignalReader port"| Adapters
    RSS -->|"Cache port"| CacheAdapters
    RSS -->|"RiskPolicy interface"| Policy

    subgraph Adapters["Storage Adapters"]
        PG["PostgresSignalRepository\nSQLAlchemy — FastAPI"]
        DJA["DjangoSignalRepository\nDjango ORM — django/"]
        JPA["JPA Repository\nSpring — Java"]
    end

    subgraph CacheAdapters["Cache Adapters"]
        RC["RedisCache\n(prod)"]
        FC["FakeCache\n(tests)"]
    end

    subgraph Policy["Scoring Strategy"]
        WP["WeightedRiskPolicy\nsum of severity weights"]
        SP["SpikeDetectionPolicy\namplified burst scoring"]
    end

    Adapters --> PDB[("PostgreSQL")]
    CacheAdapters --> RDB[("Redis")]
```

---

## Design Decisions

**Ingestion and scoring are separate services.** Signal writes and risk reads have different access patterns. Keeping them apart means each can scale, cache, and evolve independently.

> **Engineering note:** SRP at the service level. For write spikes, ingestion scales horizontally while the risk read path is unaffected. Cache-hit reads are Redis-only and don't touch the write path at all.

**Risk summaries are cached and evicted on write.** Scoring requires a full window query. Caching per service name keeps read latency low without serving stale data.

> **Engineering note:** For thundering-herd risk on cache miss, per-service keys mean a miss for `checkout` doesn't affect `payments`. Under extreme load, add a distributed lock (Redlock) around the miss computation to prevent duplicate window queries.

**Scoring policy is deterministic and stateless.** Score = sum of severity weights over a time window. No ML, no probabilistic logic — the output is fully auditable.

> **Engineering note:** Strategy pattern (OCP). Swapping `WeightedRiskPolicy` for `SpikeDetectionPolicy` requires changing exactly one line in the composition root (`main.py` or `apps.py`). The services and tests are unchanged.

**API key auth over OAuth.** A stateless header filter is enough for machine-to-machine callers (CI pipelines, alertmanager webhooks).

> **Engineering note:** Right-size the auth mechanism. OAuth adds complexity (token refresh, JWKS endpoints) that isn't needed for M2M. Upgrading is a new middleware — services and domain are untouched. This is DIP applied to auth.

**Tests run without Docker.** Spring uses H2. Python uses SQLite + `FakeCache`. Django uses SQLite + `FakeCache`.

> **Engineering note:** Ports make this possible. Tests inject `FakeCache` (a dict) and an in-memory DB that satisfy the same Protocol/interface. No mocks of internal classes — only fake infrastructure at the boundary. This is how you get fast, reliable tests without `docker compose up`.

**Port 80 in the image, TLS at the ingress.** Ingress terminates TLS on 443 and routes plain HTTP to the service on 80.

> **Engineering note:** Standard K8s ingress pattern. The application image stays certificate-free — certificate rotation is an infra concern, not a deploy.

---

## Python Hexagonal Architecture — FastAPI vs Django

Both Python ports share `domain/`, `ports/`, and `services/` unchanged. Only the adapter layer differs.

```
Shared across FastAPI and Django:
  domain/      zero-dependency scoring rules and enums
  ports/       Protocol definitions — the contracts services depend on
  services/    SignalIngestionService + RiskScoringService

FastAPI only (python/):
  adapters/    SQLAlchemy PostgresSignalRepository + RedisCache
  api/         FastAPI router, Pydantic schemas, Depends-based auth

Django only (django/):
  signals/     Django ORM DjangoSignalRepository + DRF APIViews
               + ApiKeyMiddleware + AppConfig composition root
```

> **Engineering note:** This is the strongest portability proof in the architecture. Two completely different web frameworks wire to the exact same service logic because services depend on `ports.SignalWriter`, not on `SQLAlchemy` or `Django ORM`. This is the clearest extension point for framework portability.
