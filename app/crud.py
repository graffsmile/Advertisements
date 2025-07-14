from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.dialects.postgresql import Any

from models import USER_OBJ, USER_CLS, ADVERT_OBJ, ADVERT_CLS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(session: AsyncSession, user: USER_OBJ):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as err:
        raise HTTPException(409, "User already exists")

async def get_user_by_id(session: AsyncSession, user_cls: USER_CLS, user_id: int) -> USER_OBJ:
    user_obj = await session.get(user_cls, user_id)
    if user_obj is None:
        raise HTTPException(404, "User not found")
    return user_obj

async def delete_user(session: AsyncSession, user: USER_OBJ):
    await session.delete(user)
    await session.commit()


async def add_advert(session: AsyncSession, advert: ADVERT_OBJ):
    session.add(advert)
    try:
        await session.commit()
    except IntegrityError as err:
        raise HTTPException(409, "Advert already exists")

async def get_advert_by_id(session: AsyncSession, advert_cls: ADVERT_CLS, advert_id: int) -> ADVERT_OBJ:
    advert_obj = await session.get(advert_cls, advert_id)
    if advert_obj is None:
        raise HTTPException(404, "Advert not found")
    return advert_obj

async def get_advert_by_qs(session: AsyncSession, advert_cls: ADVERT_CLS, **query_string: dict) -> ADVERT_OBJ:
    advert_obj = await session.execute(select(advert_cls).filter_by(**query_string))
    return advert_obj

async def delete_advert(session: AsyncSession, advert: ADVERT_OBJ):
    await session.delete(advert)
    await session.commit()