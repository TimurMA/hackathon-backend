from app.db import Session
from app.user.service import *
from app.user.schemas import *

from fastapi import APIRouter
from fastapi_filter import FilterDepends


user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


user_router.get()