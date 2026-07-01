import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("hotel_tasks", broker=REDIS_URL, backend=REDIS_URL)

celery_app.autodiscover_tasks(["app"], force=True)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Kyiv",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "cancel_expired_bookings_every_10_mins": {
        "task": "app.tasks.bookings.cancel_expired_bookings",
        "schedule": 600.0,
    }
}
celery_app.conf.timezone = "Europe/Kyiv"
