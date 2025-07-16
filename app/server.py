import datetime

from fastapi import FastAPI, HTTPException


from schema import (CreateUserRequest, UpdateUserRequest, CreateUserResponse, UpdateUserResponse, GetUserResponse,
                    SearchUserResponse, DeleteUserResponse, CreateAdvertRequest, UpdateAdvertRequest, CreateAdvertResponse,
                    UpdateAdvertResponse, GetAdvertResponse, SearchAdvertResponse, DeleteAdvertResponse, LoginRequest, LoginResponse)

from  lifespan import lifespan
from dependency import SessionDependency, TokenDependency
from constants import SUCCESS_RESPONSE
import models
import crud
from sqlalchemy import select, and_
from auth import check_password, hash_password



app = FastAPI(
    title="Advertisements",
    description="Advertisements app",
    lifespan=lifespan,
)


@app.post("/api/v1/user", tags=["user"], response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, session: SessionDependency):
    user_dict = user.model_dump(exclude_unset=True)
    user_dict['password'] = hash_password(user_dict['password'])
    user_orm_obj = models.User(**user_dict)
    await crud.add_user(session, user_orm_obj)
    return user_orm_obj.id_dict

@app.get("/api/v1/user/{user_id}", tags=["user"], response_model=GetUserResponse)
async def get_user(session: SessionDependency, user_id: int, token: TokenDependency):
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)
    return user_orm_obj.dict

@app.get("/api/v1/user", response_model=SearchUserResponse, tags=["user"])
async def search_user(
        session: SessionDependency,
        id: int | None = None,
        name: str | None = None
        ):
    query_string = (
        select(models.User)
        .where(models.User.id == id,
               models.User.name == name,
               )
    )
    users = await session.scalars(query_string)
    return {"results": [user.dict for user in users]}


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse)
async def update_user(
        user_id: int, user_data: UpdateUserRequest, session: SessionDependency, token: TokenDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict['password'] = hash_password(user_dict['password'])
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)
    if token.user.role == "admin" or user_orm_obj.id == token.user_id:
        for field, value in user_dict.items():
            setattr(user_orm_obj, field, value)
        await crud.add_user(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Invalid privileges")


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)
    if token.user.role == "admin" or user_orm_obj.id == token.user_id:
        await crud.delete_user(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Invalid privileges")

@app.post("/api/v1/login", tags=["user"], response_model=LoginResponse)
async def login (login_data: LoginRequest, session: SessionDependency):
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, "Invalid credentials")
    if not check_password(login_data.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict


@app.post("/api/v1/advertisement", tags=["advertisement"], response_model=CreateAdvertResponse)
async def create_user(advertisement: CreateAdvertRequest, session: SessionDependency, token: TokenDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True)
    advertisement_orm_obj = models.Adverts(**advertisement_dict, author_id=token.user_id)
    await crud.add_advert(session, advertisement_orm_obj)
    return advertisement_orm_obj.id_dict

@app.get("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=GetAdvertResponse)
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement_orm_obj = await crud.get_user_by_id(session, models.Adverts, advertisement_id)
    return advertisement_orm_obj.dict


@app.get("/api/v1/advertisement", response_model=SearchAdvertResponse, tags=["advertisement"])
async def search_adverts(
        session: SessionDependency,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        author_id: int | None = None,
        ):
    query_string = select(models.Adverts).where(
            models.Adverts.title == title,
            models.Adverts.description == description,
            models.Adverts.price == price,
            models.Adverts.author_id == author_id,
        )

    adverts = await session.scalars(query_string)
    return {"results": [advert.dict for advert in adverts]}


# @app.get("/api/v1/advertisement", response_model=SearchAdvertResponse, tags=["advertisement"])
# async def search_adverts(
#         session: SessionDependency,
#         title: str | None = None,
#         description: str | None = None,
#         price: int | None = None,
#         author_id: int | None = None,
# ):
#     query_string = {}
#     if title:
#         query_string["title"] = title
#     if description:
#         query_string["description"] = description
#     if price:
#         query_string["price"] = price
#     if author_id:
#         query_string["author_id"] = author_id
#     advertisement_orm_obj = await crud.get_advert_by_qs(session, models.Adverts, **query_string)
#     result = [advert.dict for advert in advertisement_orm_obj.scalars().all()]
#     return result
"""
Response:
500
"""


@app.patch("/api/v1/advertisement/{advert_id}", response_model=UpdateAdvertResponse)
async def update_advertisement(
        advert_id: int, advert_data: UpdateAdvertRequest, session: SessionDependency, token: TokenDependency):
    advert_dict = advert_data.model_dump(exclude_unset=True)
    advert_orm_obj = await crud.get_advert_by_id(session, models.Adverts, advert_id)
    if token.user.role == "admin" or advert_orm_obj.author_id == token.user_id:
        for field, value in advert_dict.items():
            setattr(advert_orm_obj, field, value)
        await crud.add_advert(session, advert_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Invalid privileges")


@app.delete("/api/v1/advertisement/{advert_id}", response_model=DeleteAdvertResponse)
async def delete_advert(advert_id: int, session: SessionDependency, token: TokenDependency):
    advert_orm_obj = await crud.get_advert_by_id(session, models.Adverts, advert_id)
    if token.user.role == "admin" or advert_orm_obj.author_id == token.user_id:
        await crud.delete_advert(session, advert_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Invalid privileges")

