# import logging
# from typing import Sequence
#
# from app.user.schemas import UserPublic
#
# from sqlmodel import select, union_all
# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# async def get_user_by_id(user_id: str, session: AsyncSession) -> UserPublic:
#     statement = select(User).where((User.id == user_id), User.is_deleted == False)
#     result = await session.execute(statement)
#     result = result.first()
#     if result is None:
#         raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
#     return UserPublic.init_scheme(result)
#
#
# async def get_all_users(session: AsyncSession, user_filter: UserFilter) -> Sequence[UserPublic]:
#     query = select(User).where(User.is_deleted == False)
#     statement = user_filter.filter(query)
#     result = await session.execute(statement)
#     return list(map(UserPublic.init_scheme, result.all()))
#
# async def update_user(user_id: str, user_to_update: UserSave, session: AsyncSession) -> UserPublic:
#     try:
#         result = await session.execute(select(User).where(User.id == user_id))
#         user = result.scalar_one_or_none()
#         if user is None:
#             raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
#         if user.email != user_to_update.email:
#             existing_user = await session.execute(select(User).where(and_(User.email == user_to_update.email, User.id != user_id)))
#             if existing_user.scalar_one_or_none():
#                     raise HTTPException(status_code=400, detail="Email уже занят.")
#         user.first_name = user_to_update.first_name
#         user.last_name = user_to_update.last_name
#         user.email = user_to_update.email
#         user.phone = user_to_update.phone
#
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#         return UserPublic.init_scheme(user)
#
#     except Exception as e:
#         await session.rollback()
#         logging.error(e)
#         raise HTTPException(status_code=500, detail="Ошибка при обновлении пользователя.")
#
#
# async def assign_skills_to_user(user_id: UUID, skill_id_list: list[UUID], session: AsyncSession) -> list[UserSkillPublic]:
#     try:
#         user = await session.execute(select(User).where(User.id == user_id))
#         if user.scalar_one_or_none():
#             raise HTTPException(status_code=400, detail="Такая компетенция уже существует.")
#         existing_skills = await session.execute(select(Skill).where(Skill.id in skill_id_list))
#         existing_skill_id_list = {skill.id for skill in existing_skills.scalars()}
#         if len(existing_skill_id_list) != len(skill_id_list):
#             missing_skills = set(skill_id_list) - existing_skill_id_list
#             raise HTTPException(status_code=404, detail=f"Некоторые компетенции не были найдены: {missing_skills}.")
#         await session.execute(delete(UserSkill).where(UserSkill.user_id == user_id))
#         user_skills = [
#             UserSkill(user_id=user_id, skill_id=skill_id)
#             for skill_id in skill_id_list
#         ]
#         session.add_all(user_skills)
#         await session.commit()
#         result = await session.execute(select(UserSkill).where(UserSkill.user_id == user_id).join(Skill))
#         user_skills = result.scalars().all()
#         return [
#             UserSkillPublic(
#                 user_id=str(user_skill.user_id),
#                 skill_id=str(user_skill.skill_id),
#                 skill=SkillPublic.init_scheme(user_skill.skill))
#             for user_skill in user_skills
#         ]
#     except Exception as e:
#         await session.rollback()
#         logging.error(e)
#         raise HTTPException(status_code=500, detail="Ошибка при назначении навыков пользователю.")
#
#
# async def restore_user(user_id: UUID, session: AsyncSession) -> UserPublic:
#     try:
#         result = await session.execute(select(User).where(and_(User.id == user_id, User.is_deleted == True)))
#         user = result.scalar_one_or_none()
#         if user is None:
#             raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
#         user.is_deleted = False
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#         return UserPublic.init_scheme(user)
#     except Exception as e:
#         await session.rollback()
#         logging.error(e)
#         raise HTTPException(status_code=500, detail="Ошибка при восстановлении пользователя.")
#
#
# async def delete_user(user_id: UUID, session: AsyncSession):
#     try:
#         result = await session.execute(select(User).where(and_(User.id == user_id, User.is_deleted == False)))
#         user = result.scalar_one_or_none()
#         if user is None:
#             raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
#         user.is_deleted = True
#         session.add(user)
#         await session.commit()
#     except Exception as e:
#         await session.rollback()
#         logging.error(e)
#         raise HTTPException(status_code=500, detail="Ошибка при удалении пользователя.")
