import datetime
import uuid
from typing import Literal

from pydantic import BaseModel




class SuccessResponse(BaseModel):
    status: Literal["success"]


class CreateUserRequest(BaseModel):
    name: str
    password: str
    role: str

class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None

class CreateUserResponse(BaseModel):
    id: int

class UpdateUserResponse(SuccessResponse):
    pass

class GetUserResponse(BaseModel):
    id: int
    name: str
    registration_time: datetime.datetime

class SearchUserResponse(BaseModel):
    results: list[GetUserResponse]

class DeleteUserResponse(SuccessResponse):
    pass


class CreateAdvertRequest(BaseModel):
    title: str
    description: str
    price: int


class UpdateAdvertRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None

class CreateAdvertResponse(BaseModel):
    id: int

class UpdateAdvertResponse(SuccessResponse):
    pass

class GetAdvertResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    author_id: int
    author_name: str
    creation_time: datetime.datetime

class SearchAdvertResponse(BaseModel):
    results: list[GetAdvertResponse]

class DeleteAdvertResponse(SuccessResponse):
    pass



class LoginRequest(CreateUserRequest):
    pass

class LoginResponse(BaseModel):
    token: uuid.UUID