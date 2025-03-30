from app.db import Session
from app.user.service import *
from app.user.schemas import *

from fastapi import APIRouter
from fastapi_filter import FilterDepends


user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get("/{user_id}")
async def get_user_by_id_async(user_id: str, session: Session) -> UserPublic:
    return await get_user_by_id(user_id, session)


@user_router.get("/all")
async def get_all_users_async(session: Session, user_filter: UserFilter = FilterDepends(UserFilter)) -> Sequence[UserPublic]:
    return await get_all_users(session, user_filter)


@user_router.put("/update/{user_id}")
async def update_skill_async(user_id: str, user: UserSave, session: Session) -> UserPublic:
    return await update_user(user_id, user, session)


@user_router.put("/assign_skills/{user_id}")
async def assign_skills_to_user_async(user_id: str, skill_id_list: list[UUID], session: Session) -> UserPublic:
    return await update_user(user_id, skill_id_list, session)


@user_router.put("/restore/{user_id}")
async def restore_user_async(user_id: str, session: Session) -> UserPublic:
    return await restore_user(user_id, session)


@user_router.delete("/{user_id}")
async def delete_user_async(user_id: str, session: Session):
    return await delete_user(user_id, session)
