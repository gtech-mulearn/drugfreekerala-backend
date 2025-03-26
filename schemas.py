# Request Schemas

from pydantic import BaseModel, EmailStr, Field


# Request Schema
class CreateUserDataRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., min_length=2, max_length=100)


class UserDataRequest(BaseModel):
    email: EmailStr = Field(..., min_length=2, max_length=100)


# Response Schemas
class TotalUserResponse(BaseModel):
    total: int


class UserDataResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str
    updated_at: str
