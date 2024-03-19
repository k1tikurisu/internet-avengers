from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from database import get_db

from routers import status  # from app.routerにすると動きませんでした
from cruds import scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


app = FastAPI()
app.include_router(status.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://github.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/hc")
def read_root():
    return {"msg": "Health good"}


@app.on_event("startup")
async def patrol_dino():
    schedule = AsyncIOScheduler()
    schedule.add_job(scheduler.is_alive_dino, "interval", seconds=10)
    schedule.start()
