from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict
from sqlmodel import SQLModel

from app.db import init_db, close_connection, init_common_competencies, init_competence_contiguity
from app.company.routes import company_router
from app.competence.routes import competence_router
from app.resume.routes import resume_router
from app.nlp import init_nlp_module
# from app.user.routes import user_router

from app.vacancy.routes import vacancy_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.model_config = ConfigDict(extra='allow')
    await init_db()
    init_nlp_module()
    await init_common_competencies()
    await init_competence_contiguity()
    yield
    await close_connection()

origins = ["*"]

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

app.include_router(router=vacancy_router)
app.include_router(router=competence_router)
app.include_router(router=company_router)
app.include_router(router=resume_router)
# app.include_router(router=user_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
