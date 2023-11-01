from pydantic import BaseModel, EmailStr, HttpUrl, Field
from datetime import date,datetime

class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: str

class ContactCreate(ContactModel):
    pass

class ContactUpdate(ContactModel):
    pass

class ContactResponse(ContactModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RequestEmail(BaseModel):
    email: EmailStr