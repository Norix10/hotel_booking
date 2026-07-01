# Hotel Booking API

A FastAPI-based hotel booking backend with JWT authentication, async SQLAlchemy, Alembic migrations, and background payment processing via Celery and Redis.

## 🚀 Overview

This project implements a hotel booking system with:
- user registration and authentication,
- JWT-protected endpoints,
- room and room-type management,
- booking creation, filtering, update, cancellation and confirmation,
- payment creation with asynchronous background confirmation,
- Docker-based local development with PostgreSQL, Redis and Celery workers.

## 🧩 Technologies

- Python 3.14+
- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- PostgreSQL / asyncpg
- Redis
- Celery
- PyJWT
- bcrypt
- pydantic v2
- Uvicorn
- Docker / Docker Compose

## 🏗️ Architecture

The project follows a layered architecture:

- Routers — HTTP endpoints and request validation
- Services — business logic and orchestration
- Repositories — database access and query composition
- Models — SQLAlchemy ORM entities and enums
- Schemas — Pydantic request/response models
- Core — configuration, dependencies, security, Celery setup

## 📁 Project Structure

- app/main.py — FastAPI app initialization
- app/routers/ — API routers
- app/services/ — business logic
- app/repositories/ — repository layer
- app/models/ — ORM models and enums
- app/schemas/ — request/response schemas
- app/tasks/ — Celery background tasks
- docker-compose.yml — local services stack
- Dockerfile — application image

## 📦 Installation

### Local

```bash
poetry install
```

### Docker

```bash
docker compose up --build
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- FastAPI app on port 8000
- Celery worker
- Celery beat

## 🔧 Environment Configuration

Create a `.env` file in the project root:

```env
DB_URL=postgresql+asyncpg://hotel_user:hotel_password@db:5432/hotel_db
SECRET_KEY=your-secret-key
ECHO=False
REDIS_URL=redis://redis_broker:6379/0
```

## ⚡ Running the App

### Locally

```bash
poetry run uvicorn app.main:app --reload
```

### With Docker

```bash
docker compose up
```

The application will be available at http://127.0.0.1:8000.

## 🩺 Health Check

```bash
GET /health
```

Returns database connectivity status.

## 📌 Available API Routes

All routes are available under the prefix `/api/v1`.

### Auth & Users

- `POST /api/v1/user` — register a user
- `POST /api/v1/user/signin` — sign in and receive a JWT
- `GET /api/v1/user/me` — get current user profile
- `PATCH /api/v1/user/` — update current user
- `DELETE /api/v1/user/` — delete current user
- `GET /api/v1/user/users` — list all users (admin only)

### Room Types

- `GET /api/v1/room-types/` — list room types
- `GET /api/v1/room-types/{room_type_id}` — get a room type by ID
- `POST /api/v1/room-types/` — create a room type (admin)
- `PATCH /api/v1/room-types/{room_type_id}` — update a room type (admin)
- `DELETE /api/v1/room-types/{room_type_id}` — delete a room type (admin)

### Rooms

- `GET /api/v1/room/` — list rooms
- `GET /api/v1/room/{room_id}` — get room by ID
- `POST /api/v1/room/` — create a room (admin)
- `PATCH /api/v1/room/{room_id}` — update a room (admin)
- `DELETE /api/v1/room/{room_id}` — delete a room (admin)

### Bookings

- `POST /api/v1/bookings/` — create a booking
- `POST /api/v1/bookings/with-payment` — create a booking and queue payment processing
- `GET /api/v1/bookings/` — list current user bookings, optionally filtered by status via `?status=pending`
- `GET /api/v1/bookings/{booking_id}` — get booking by ID
- `PATCH /api/v1/bookings/{booking_id}` — update a booking
- `PATCH /api/v1/bookings/{booking_id}/cancel` — cancel a booking

### Payments

- `POST /api/v1/payments/bookings/{booking_id}` — create a payment for a booking
- `GET /api/v1/payments/` — list payments for the current user
- `GET /api/v1/payments/{payment_id}` — get payment by ID
- `PATCH /api/v1/payments/{payment_id}` — update payment (admin)
- `DELETE /api/v1/payments/{payment_id}` — delete payment (admin)

### Admin

- `PATCH /api/v1/admin/bookings/{booking_id}` — admin booking update
- `DELETE /api/v1/admin/bookings/{booking_id}` — admin booking delete
- `PATCH /api/v1/admin/payments/{payment_id}` — admin payment update
- `DELETE /api/v1/admin/payments/{payment_id}` — admin payment delete

## 📚 Main Models

### User
- id — UUID
- email — unique email
- password hash — bcrypt hashed
- role — user/admin

### RoomType
- id — int
- name — string
- base_price — int
- capacity — int
- bed_type — enum
- bathroom_type — enum
- area_sq_m — int
- has_ac — bool
- has_wifi — bool

### Room
- id — int
- room_name — string
- room_type_id — int
- status — enum (`available`, `cleaning`, `occupied`)
- floor — int

### Booking
- id — UUID
- user_id — UUID
- room_id — int
- check_in — datetime (timezone-aware)
- check_out — datetime (timezone-aware)
- status — enum (`pending`, `confirmed`, `cancelled`)

### Payment
- id — UUID
- booking_id — UUID
- amount — int
- payment_method — enum
- payment_status — enum

## 📘 OpenAPI Docs

After starting the app, open:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## ⏰ Timezone Handling

Booking dates are stored as timezone-aware datetimes. Naive datetime values are converted to UTC automatically.

## 📄 Database Migrations

Run migrations with:

```bash
poetry run alembic upgrade head
```

## 🧪 Background Tasks

Payment processing is handled asynchronously with Celery. When a booking is created with payment, the system queues a background task that updates the booking status to confirmed.

## ✨ Contact

Author: Norix10
