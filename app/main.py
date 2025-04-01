from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import init_db, close_connection
from app.competence.routes import competence_router
from app.nlp import init_nlp_module
# from app.user.routes import user_router

from app.vacancy.routes import vacancy_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_nlp_module()
    yield
    await close_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(router=vacancy_router)
app.include_router(router=competence_router)
# app.include_router(router=user_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
