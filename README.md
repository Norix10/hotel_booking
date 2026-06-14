# Hotel Booking API

A lightweight FastAPI-based hotel booking backend with user authentication, async SQLAlchemy database access, and a modular repository-service architecture.

## 🚀 Overview

This project implements a basic backend for a hotel room booking system. It focuses on:
- user registration and authentication,
- JWT-protected endpoints,
- asynchronous database access using SQLAlchemy Async,
- separation of concerns across routers, services, and repositories.

## 🧩 Technologies

- Python 3.14+
- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- PostgreSQL / asyncpg
- PyJWT
- bcrypt
- pydantic v2
- Uvicorn

## 🏗️ Architecture

The project follows a **layered repository-service architecture**:

- **Routers** (`app/routers/v1/`) — HTTP endpoint handlers, dependency injection, request validation
- **Services** (`app/services/`) — business logic, orchestration, validation rules
- **Repositories** (`app/repositories/`) — data access layer, async query execution
- **Models** (`app/models/`) — SQLAlchemy ORM definitions with enums
- **Schemas** (`app/schemas/`) — Pydantic models for request/response validation with ORM support
- **Core** (`app/core/`) — configuration, dependencies, security utilities

This separation ensures testability, reusability, and maintainability.

## 📁 Project Structure

- `app/main.py` — FastAPI application and router registration.
- `app/routers/` — HTTP routes (API endpoints).
- `app/services/` — business logic.
- `app/repositories/` — database access layer.
- `app/models/` — SQLAlchemy ORM models.
- `app/schemas/` — Pydantic schemas for validation and serialization.
- `app/db/database.py` — async database session configuration.
- `app/core/dependencies.py` — FastAPI dependencies and DI for repositories and services.
- `app/core/config.py` — configuration via `.env`.

## 📦 Installation

```bash
poetry install
```

## 🔧 Environment Configuration

Create a `.env` file in the project root with the following values:

```env
DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ECHO=False
```

- `DB_URL` — database connection string.
- `SECRET_KEY` — secret key for signing JWT tokens.
- `ECHO` — enable SQL query logging (True/False).

## ⚡ Running the App

```bash
poetry run uvicorn app.main:app --reload
```

By default, the application will run at `http://127.0.0.1:8000`.

## 📌 Available API Routes

All routes are available under the prefix `/api/v1`.

### Auth & User

- `POST /api/v1/user` — register a new user
  - Request body:
    - `name` — user name
    - `email` — user email
    - `password` — password

- `POST /api/v1/user/signin` — sign in
  - Request body:
    - `email`
    - `password`
  - Response:
    - `access_token`
    - `token_type`

- `GET /api/v1/user/me` — get current user profile
  - Requires header `Authorization: Bearer <token>`

- `PATCH /api/v1/user/` — update current user
  - Requires token
  - You can update `name`, `email`, and `password`

- `DELETE /api/v1/user/` — delete current user account
  - Requires token

- `GET /api/v1/user/users` — list all users (admin only)
  - Requires admin token

### Room Types

- `GET /api/v1/room-types/all` — list all room types

- `GET /api/v1/room-types/{room_type_id}` — get room type by ID

- `POST /api/v1/room-types` — create new room type (admin only)
  - Request body:
    - `name` — room type name
    - `price_per_night` — price per night (float)
    - `bed_type` — bed type enum (single, double, queen, king, twin, sofa, bunk)

- `PATCH /api/v1/room-types/{room_type_id}` — update room type (admin only)

### Rooms

- `GET /api/v1/room/all` — list all rooms

- `GET /api/v1/room/{room_id}` — get room by ID

- `POST /api/v1/room` — create new room (admin only)
  - Request body:
    - `room_number` — room number (string)
    - `room_type_id` — room type ID (int)

- `PATCH /api/v1/room/{room_id}` — update room (admin only)

### Bookings

- `POST /api/v1/booking` — create new booking
  - Requires token
  - Request body:
    - `room_id` — room ID (int)
    - `check_in` — check-in datetime (ISO 8601, will be converted to UTC if naive)
    - `check_out` — check-out datetime (ISO 8601, will be converted to UTC if naive)

- `GET /api/v1/booking/{booking_id}` — get booking by ID
  - Requires token (user can only see their own booking)

- `GET /api/v1/booking/user/bookings` — list current user's bookings
  - Requires token

- `PATCH /api/v1/booking/{booking_id}` — update booking
  - Requires token (user can only update their own)

- `DELETE /api/v1/booking/{booking_id}` — cancel booking
  - Requires token (user can only delete their own)

### Payments

- `POST /api/v1/payments` — create payment for booking
  - Requires token
  - Request body:
    - `booking_id` — booking ID (UUID)
    - `payment_method` — payment method (card, bank_transfer, cash)

- `GET /api/v1/payments/{payment_id}` — get payment by ID

### Admin Routes

- `GET /api/v1/admin/users` — list all users (admin only)

- `PATCH /api/v1/admin/users/{user_id}` — update user (admin only)

## 📚 Supported Models

### User

- `id` — UUID (primary key)
- `name` — user name (string)
- `email` — unique user email
- `hashed_password` — bcrypt hashed password
- `role` — user role enum (user, admin)
- `active` — account active flag (boolean)

### RoomType

- `id` — primary key (int, auto-increment)
- `name` — room type name (string)
- `price_per_night` — price per night (float)
- `bed_type` — bed type enum (single, double, queen, king, twin, sofa, bunk)

### Room

- `id` — primary key (int, auto-increment)
- `room_number` — room number (string)
- `room_type_id` — foreign key to RoomType
- `status` — room status enum (available, occupied, maintenance)

### Booking

- `id` — UUID (primary key)
- `user_id` — foreign key to User
- `room_id` — foreign key to Room
- `check_in` — check-in datetime (timezone-aware, UTC)
- `check_out` — check-out datetime (timezone-aware, UTC)
- `status` — booking status enum (pending, confirmed, cancelled)

### Payment

- `id` — UUID (primary key)
- `booking_id` — foreign key to Booking
- `amount` — payment amount (float)
- `payment_method` — payment method enum (card, bank_transfer, cash)
- `status` — payment status enum (pending, completed, failed)

## 📘 OpenAPI Documentation

After running the app, open the automatic API docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## ⏰ Timezone Handling

Booking `check_in` and `check_out` datetime fields are **timezone-aware** and stored in UTC. When sending requests with naive datetimes (no timezone info), the API will automatically convert them to UTC. Responses will always include timezone information.

Example:
```bash
# Naive datetime (will be converted to UTC)
POST /api/v1/booking
{
  "room_id": 1,
  "check_in": "2026-07-15T10:00:00",
  "check_out": "2026-07-17T11:00:00"
}

# Response (UTC-aware)
{
  "check_in": "2026-07-15T10:00:00+00:00",
  "check_out": "2026-07-17T11:00:00+00:00"
}
```

## 📄 Database Migrations

This project uses Alembic for schema migrations. Run:

```bash
poetry run alembic upgrade head
```

Recent migrations include:
- **Migration 11**: Add `RoomBedTypeEnum` with values (single, double, queen, king, twin, sofa, bunk)
- **Migration 12**: Convert booking `check_in` and `check_out` columns to `TIMESTAMP(timezone=True)` for timezone-aware datetime storage

## ✨ Contact

Author: `Norix10`
