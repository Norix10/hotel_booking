FROM python:3.14-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.0.1

WORKDIR /hotel_booking

RUN pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock* /hotel_booking/

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --no-ansi

FROM python:3.14-slim-bookworm AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /hotel_booking

COPY --from=builder /hotel_booking/.venv /hotel_booking/.venv
COPY ./app /hotel_booking/app

COPY ./app/alembic.ini /hotel_booking/alembic.ini

ENV PATH="/hotel_booking/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]