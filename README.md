# 🎬 Cinema Microservice Backend (FastAPI)

A **production‑ready FastAPI microservice backend** for a cinema / movie
catalog platform.\
This project demonstrates real-world backend architecture with
PostgreSQL, Redis, Elasticsearch, S3 storage, async SQLAlchemy, Alembic
migrations, observability, and clean DDD-like layering.

> Designed as a scalable template for modern Python backend engineering.

------------------------------------------------------------------------

## 🚀 Features

### Core

-   **FastAPI** async REST API
-   **PostgreSQL + SQLAlchemy Async ORM**
-   **Alembic migrations**
-   **Repository + Unit of Work pattern**
-   **Service layer abstraction**
-   **Domain models for movies, genres, countries, persons, shots**
-   **Many-to-many relations with association tables**
-   **Database constraints & validation**

### Performance & Infrastructure

-   **Redis caching with invalidation system**
-   **Elasticsearch full‑text search**
-   **Async Task Queue (Taskiq)**
-   **S3-compatible file storage**
-   **Gunicorn + Uvicorn production config**
-   **Docker & Docker Compose**

### Observability

-   **OpenTelemetry tracing**
-   **Prometheus metrics**
-   **Grafana Loki logging**
-   **Tempo tracing backend**
-   **Sentry integration**

### Dev Experience

-   **Poetry dependency management**
-   **Typed schemas (Pydantic v2)**
-   **Structured settings via env**
-   **Clean architecture folder structure**
-   **Signal/event system**
-   **Elastic sync workers**
-   **Background tasks**

------------------------------------------------------------------------

## 🏗️ Architecture Overview

    app/
     ├── api/              # FastAPI routers
     ├── core/             # config, models, db helper, gunicorn
     ├── repositories/     # data access layer
     ├── services/          # business logic layer
     ├── schemas/            # Pydantic models
     ├── cache/              # Redis cache logic
     ├── elastic/             # Elasticsearch documents & sync
     ├── storage/             # S3 abstraction layer
     ├── tasks/               # background jobs
     ├── telemetry/           # OpenTelemetry setup
     ├── metrics/             # Prometheus metrics
     ├── sentry/               # error monitoring
     ├── signals/              # domain events
     ├── db_integrity_handler/ # DB constraint handling
     └── alembic/              # migrations

This structure follows **clean architecture / DDD-inspired layering**:

-   API Layer → Services → Repositories → Database
-   Cross‑cutting concerns isolated (cache, elastic, telemetry, storage)

------------------------------------------------------------------------

## 🧩 Domain Models

Entities implemented:

-   **Movie**
-   **Genre**
-   **Country**
-   **Person**
-   **MovieShot**
-   **MoviePersonAssociation (roles: actor, director, writer,
    producer)**
-   **MovieGenreAssociation**
-   **MovieCountryAssociation**

All relations are normalized and enforced with foreign keys &
constraints.

------------------------------------------------------------------------

## ⚙️ Tech Stack

  Category           Tech
  ------------------ -------------------------------------------------
  Backend            FastAPI, Python 3.12
  ORM                SQLAlchemy Async
  DB                 PostgreSQL
  Cache              Redis
  Search             Elasticsearch
  Migrations         Alembic
  Queue              Taskiq
  Storage            S3-compatible (MinIO, AWS S3)
  Observability      OpenTelemetry, Prometheus, Grafana, Loki, Tempo
  Packaging          Poetry
  Containerization   Docker, Docker Compose

------------------------------------------------------------------------

## 🐳 Running with Docker

### 1️⃣ Clone repo

``` bash
git clone <your-repo-url>
cd project
```

### 2️⃣ Create `.env`

``` bash
cp app/.env.template app/.env
```

### 3️⃣ Run services

``` bash
docker compose up --build
```

------------------------------------------------------------------------

## 🧪 Local Development (without Docker)

### Install dependencies

``` bash
poetry install
```

### Run DB migrations

``` bash
alembic upgrade head
```

### Run API

``` bash
python app/run.py
```

------------------------------------------------------------------------

## 🔎 API Example Endpoints

    GET    /api/v1/movies
    POST   /api/v1/movies
    GET    /api/v1/genres
    GET    /api/v1/persons
    GET    /api/v1/countries
    GET    /api/v1/search?q=...

------------------------------------------------------------------------

## ⚡ Caching Strategy

-   Redis used for **read-heavy endpoints**
-   Automatic invalidation via signals & event handlers
-   Cache DTO schemas defined in `schemas/cache.py`

------------------------------------------------------------------------

## 🔍 Elasticsearch Search

-   Separate documents for movies, genres, persons, countries
-   Sync workers in `elastic/syncer.py`
-   Adapter layer for DB → Elastic models

------------------------------------------------------------------------

## 📂 File Storage

-   Abstract storage interface
-   S3 implementation included
-   Path builder & URL resolver logic
-   Background upload tasks

------------------------------------------------------------------------

## 📊 Observability

### Metrics

-   Prometheus exporter

### Tracing

-   OpenTelemetry integration

### Logging

-   Loki + Promtail config

### Errors

-   Sentry integration

------------------------------------------------------------------------

## 🧠 Design Patterns Used

-   Repository Pattern
-   Unit of Work
-   Service Layer
-   Domain Events / Signals
-   Dependency Injection
-   Clean Architecture layering
-   Async IO everywhere

------------------------------------------------------------------------

## 🛠️ Migrations

Alembic async migrations configured with timestamped filenames:

    2026_01_11_2130-add_movie_model.py
    2026_01_14_1604-add_movie_country_assoc_model.py
    ...

------------------------------------------------------------------------

## 🧑‍💻 Project Purpose

This project is:

-   A **production-level FastAPI backend template**
-   A **portfolio project demonstrating senior backend patterns**
-   A **reference architecture for scalable Python microservices**
-   A **training ground for distributed system components**

------------------------------------------------------------------------

## 📌 Roadmap Ideas

-   Authentication (JWT / OAuth2)
-   Rate limiting
-   GraphQL API
-   Kafka / NATS event bus
-   Admin panel
-   CI/CD pipelines
-   Kubernetes deployment
-   Python 3.14 no-GIL performance benchmark

------------------------------------------------------------------------

## 🤝 Contributing

Pull requests are welcome.\
For major changes, please open an issue first.

------------------------------------------------------------------------

## 📄 License

MIT License (or specify your own).

------------------------------------------------------------------------

## 👤 Author

**Dmytro Chemin**\
Backend Python Engineer\
FastAPI • PostgreSQL • Redis • Elasticsearch • Distributed Systems
