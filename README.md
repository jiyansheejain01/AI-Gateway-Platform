# AI Gateway Platform

An enterprise-grade, high-performance, FastAPI-based AI Gateway Platform designed to route, secure, cache, and monitor LLM requests across multiple providers.

## Overview

The AI Gateway Platform provides a central entrypoint for orchestrating language model requests, ensuring consistent authentication, rate limiting, caching, monitoring, and routing across multiple LLM backends.

## Key Features

- FastAPI-based microservice gateway
- JWT authentication and RBAC support
- Redis and semantic cache integration
- Vector search with Qdrant
- Kafka event publishing and worker processing
- OpenTelemetry tracing and Prometheus metrics
- PostgreSQL-backed user management
- Modular service architecture for extensibility

## Architecture

The platform is organized into separate services and packages for clarity:

- `gateway/` - main API gateway, routing, auth, and middleware
- `services/` - domain-specific services such as cache, embeddings, memory, monitoring, routing, usage, and user management
- `kafka_service/` - Kafka producer configuration and topic definitions
- `docker/` - container orchestration and observability config

## Getting Started

1. Create a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Configure environment variables for Redis, PostgreSQL, Kafka, Qdrant, Tempo, and JWT settings.
4. Start dependent services using `docker-compose.yml`.
5. Launch the FastAPI gateway.

## Configuration

This project should use a centralized configuration module and environment variables to manage service endpoints and secrets consistently. Do not hard-code credentials or connection strings in source files.

## Contributing

Contributions are welcome. Follow best practices for structured logging, dependency pinning, and consistent configuration management.

