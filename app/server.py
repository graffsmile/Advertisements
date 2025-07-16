import datetime

import uvicorn
from fastapi import FastAPI, Query
from schema import (CreateUserRequest, UpdateUserRequest, CreateUserResponse, UpdateUserResponse, GetUserResponse,
                    SearchUserResponse, DeleteUserResponse, CreateAdvertRequest, UpdateAdvertRequest, CreateAdvertResponse,
                    UpdateAdvertResponse, GetAdvertResponse, SearchAdvertResponse, DeleteAdvertResponse)

from  lifespan import lifespan
from dependency import SessionDependency
from constants import SUCCESS_RESPONSE
import models
import crud
from sqlalchemy import select



app = FastAPI(
    title="Advertisements",
    description="Advertisements app",
    lifespan=lifespan,
)


@app.post("/api/v1/user", tags=["user"], response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, session: SessionDependency):
    user_dict = user.model_dump(exclude_unset=True)
    user_orm_obj = models.User(**user_dict)
    await crud.add_user(session, user_orm_obj)
    return user_orm_obj.id_dict

@app.get("/api/v1/user/{user_id}", tags=["user"], response_model=GetUserResponse)
async def get_user(session: SessionDependency, user_id: int):
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)
    return user_orm_obj.dict

@app.get("/api/v1/user?{query_string}", response_model=SearchUserResponse, tags=["user"])
async def search_user(
        session: SessionDependency,
        name: str,
        ):
    query_string = (
        select(models.User)
        .where(models.User.name == name)
        .limit(10000)
    )
    users = await session.scalar(query_string)
    return {"results": [user.dict for user in users]}


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse)
async def update_user(
        user_id: int, user_data: UpdateUserRequest, session: SessionDependency
):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)

    for field, value in user_dict.items():
        setattr(user_orm_obj, field, value)
    await crud.add_user(session, user_orm_obj)
    return SUCCESS_RESPONSE


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency):
    user_orm_obj = await crud.get_user_by_id(session, models.User, user_id)
    await crud.delete_user(session, user_orm_obj)
    return SUCCESS_RESPONSE



@app.post("/api/v1/advertisement", tags=["advertisement"], response_model=CreateAdvertResponse)
async def create_user(advertisement: CreateAdvertRequest, session: SessionDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True)
    advertisement_orm_obj = models.Adverts(**advertisement_dict)
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
    query_string = (
        select(models.Adverts).where(
            models.Adverts.title == title,
            models.Adverts.description == description,
            models.Adverts.price == price,
            models.Adverts.author_id == author_id,
        )
    )

    adverts = await session.scalar(query_string)
    return {"results": [advert.dict for advert in adverts]}


@app.patch("/api/v1/advertisement/{advert_id}", response_model=UpdateAdvertResponse)
async def update_advertisement(
        advert_id: int, advert_data: UpdateAdvertRequest, session: SessionDependency
):
    advert_dict = advert_data.model_dump(exclude_unset=True)
    advert_orm_obj = await crud.get_advert_by_id(session, models.Adverts, advert_id)

    for field, value in advert_dict.items():
        setattr(advert_orm_obj, field, value)
    await crud.add_advert(session, advert_orm_obj)
    return SUCCESS_RESPONSE


@app.delete("/api/v1/advertisement/{advert_id}", response_model=DeleteAdvertResponse)
async def delete_advert(advert_id: int, session: SessionDependency):
    advert_orm_obj = await crud.get_advert_by_id(session, models.Adverts, advert_id)
    await crud.delete_advert(session, advert_orm_obj)
    return SUCCESS_RESPONSE

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
