# Request Schemas

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


# Request Schema
class CreateUserDataRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., min_length=2, max_length=100)
    # Optional so clients that only send name and email keep working.
    is_student: bool | None = None
    college_id: UUID | None = None
    college_name: str | None = Field(None, min_length=2, max_length=255)

    @model_validator(mode="after")
    def check_college(self):
        if self.is_student:
            if self.college_name is None:
                raise ValueError("college_name is required when is_student is true")
        elif self.college_id or self.college_name:
            raise ValueError("college fields are only allowed when is_student is true")
        return self


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
