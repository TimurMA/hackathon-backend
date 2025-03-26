from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db import init_db, close_connection

from .vacancy.routes import vacancy

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(router=vacancy)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
