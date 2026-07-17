import uvicorn
from fastapi import FastAPI
from app.routers.api import api_router

import app.models

app = FastAPI(title="Hotel Booking API")

app.include_router(api_router)
