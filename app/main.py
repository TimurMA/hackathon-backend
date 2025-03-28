from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import init_db, close_connection

from app.vacancy.routes import vacancy_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(router=vacancy_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
