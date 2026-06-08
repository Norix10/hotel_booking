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

- `POST /api/v1/user/singin` — sign in
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

## 📚 Supported Models

### User

- `id`
- `name`
- `email`
- `hashed_password`
- `role`
- `active`

### Room / RoomType / Booking / Payment

The project also includes models for rooms, room types, bookings, and payments. These are defined in `app/models/` and supported by repository classes in `app/repositories/`, even if some endpoints are not yet implemented.

## 📘 OpenAPI Documentation

After running the app, open the automatic API docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`


## 📄 Database Migrations

This project uses Alembic for schema migrations. Run:

```bash
poetry run alembic  upgrade head
```

## ✨ Contact

Author: `Norix10`
