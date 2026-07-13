# Hotel Booking API

A FastAPI-based hotel booking backend with JWT authentication, role-based admin access, room and booking management, payments, background jobs, and Docker support.

## 🚀 Overview

This project provides a complete backend for a hotel booking system with:

- user registration and sign-in with JWT,
- protected user and admin endpoints,
- room and room-type management,
- booking creation, updates, cancellation, and filtering,
- payment creation with background confirmation processing,
- health checks, Alembic migrations, and Docker-based local development.

## 🧩 Tech Stack

- Python 3.14+
- FastAPI
- Pydantic v2
- SQLAlchemy 2 (async)
- Alembic
- PostgreSQL + asyncpg
- Redis + Celery
- JWT + bcrypt
- Uvicorn
- Docker / Docker Compose

## 🏗️ Architecture

The application follows a layered structure:

- app/routers/ — HTTP endpoints and route registration
- app/services/ — business logic
- app/repositories/ — database access layer
- app/models/ — SQLAlchemy models and enums
- app/schemas/ — request/response validation models
- app/core/ — configuration, dependencies, and security helpers
- app/tasks/ — background Celery tasks

## 📁 Project Structure

- app/main.py — FastAPI app bootstrap and router inclusion
- app/routers/api.py — main API router
- app/routers/v1/ — user, room, booking, payment, and admin endpoints
- app/services/ — service layer for all business workflows
- app/repositories/ — repository layer for database operations
- app/alembic/ — database migrations
- tests/ — API, service, and repository tests

## 📦 Prerequisites

- Python 3.14+
- Poetry
- Docker and Docker Compose (recommended)
- PostgreSQL and Redis (if running outside Docker)

## ⚙️ Environment Configuration

Create a .env file in the project root:

```env
DB_URL=postgresql+asyncpg://hotel_user:hotel_password@localhost:5432/hotel_db
SYNC_DB_URL=postgresql+psycopg://hotel_user:hotel_password@localhost:5432/hotel_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ECHO=False
```

### Variables

- DB_URL — async SQLAlchemy connection string
- SYNC_DB_URL — synchronous DB URL used for Celery/sync operations
- REDIS_URL — Redis connection string for Celery
- SECRET_KEY — secret key for JWT signing
- ECHO — enable SQLAlchemy query logging

## ▶️ Running the Project

### Local development

```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

The API will be available at:
- http://3.123.132.252:8000/
- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Docker Compose

```bash
docker compose up --build
```

This starts:

- web — FastAPI application on port 8000
- db — PostgreSQL on port 5432
- test_db — PostgreSQL test database on port 5000
- redis_broker — Redis on port 6379
- celery_worker — background task worker
- celery_beat — Celery beat scheduler

## 🔐 API Highlights

All API routes are mounted under /api/v1.

### Auth and users

- POST /api/v1/user — register a user
- POST /api/v1/user/signin — sign in and receive JWT tokens
- GET /api/v1/user/me — get current user profile
- PATCH /api/v1/user/ — update current user
- DELETE /api/v1/user/ — delete current user account

### Rooms and room types

- GET /api/v1/room-types/ — list room types
- GET /api/v1/room-types/{room_type_id} — get room type by id
- GET /api/v1/room/ — list rooms
- GET /api/v1/room/available — list available rooms
- GET /api/v1/room/{room_id} — get room by id

### Bookings

- POST /api/v1/bookings/ — create a booking
- POST /api/v1/bookings/with-payment — create a booking and payment together
- GET /api/v1/bookings/ — list current user bookings
- GET /api/v1/bookings/{booking_id} — get booking by id
- PATCH /api/v1/bookings/{booking_id} — update booking
- PATCH /api/v1/bookings/{booking_id}/cancel — cancel booking

### Payments

- POST /api/v1/payments/{booking_id} — create a payment for a booking
- GET /api/v1/payments/ — list current user payments

### Admin

- GET /api/v1/admin/users/ — list users
- DELETE /api/v1/admin/users/{user_id} — delete a user
- POST /api/v1/admin/room-types/ — create a room type
- PATCH /api/v1/admin/room-types/{room_type_id} — update a room type
- POST /api/v1/admin/room/ — create a room
- PATCH /api/v1/admin/room/{room_id} — update a room
- GET /api/v1/admin/bookings/ — list bookings with filters
- PATCH /api/v1/admin/bookings/{booking_id} — update booking status/admin fields
- GET /api/v1/admin/payments/ — list payments

### Health

- GET /api/v1/health — database connectivity health check

## 🕒 Timezone Handling

Booking dates are stored as timezone-aware UTC timestamps. If a request contains naive datetimes, the API normalizes them to UTC before saving them.

## 🧠 Background Tasks

Payments can trigger a Celery task that updates the related booking status after processing. The worker and beat services are configured in Docker Compose.

## 🗄️ Database Migrations

This project uses Alembic for schema changes:

```bash
poetry run alembic upgrade head
```

To create a new migration:

```bash
poetry run alembic revision --autogenerate -m "your message"
```

## ✅ Testing

Run the test suite with:

```bash
poetry run pytest
```

## ✨ Maintainer

Norix10
