from uuid import UUID
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["User Userson"])

    model_config = ConfigDict(extra="forbid")


class UserAuthValidatorShema(BaseModel):
    email: EmailStr = Field(examples=["user.userson@example.com"])
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not PASSWORD_PATTERN.match(v):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one number and one special character"
            )
        return v


class UserCreateSchema(UserBaseSchema, UserAuthValidatorShema):
    pass


class UserSignInSchema(UserAuthValidatorShema):
    pass


class UserResponseSchema(UserBaseSchema):
    id: UUID
    email: EmailStr = Field(examples=["user.userson@example.com"])
    active: bool
