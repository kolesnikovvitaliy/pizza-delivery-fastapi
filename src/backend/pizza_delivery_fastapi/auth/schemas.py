import re
from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, validator

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class UserCreate(CustomModel):
    username: Annotated[str, MinLen(1), MaxLen(20)]
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    is_staff: bool
    is_active: bool

    @validator("username")
    @classmethod
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class ShowUser(CustomModel):
    id: int
    username: Annotated[str, MinLen(1), MaxLen(20)]
    email: EmailStr
    is_active: bool
    is_staff: bool
    created_at: datetime
    # update_at: datetime


class CreateRefreshToken(CustomModel):
    uuid: str
    user_id: int
    refresh_token: str
    expires_at: datetime


class ShowRefreshToken(CustomModel):
    uuid: str
    refresh_token: str
    expires_at: datetime
    user_id: int


class DeleteUserResponse(CustomModel):
    deleted_user_id: int


class UpdatedUserResponse(CustomModel):
    updated_user_id: int


class UpdateUserRequest(CustomModel):
    username: Annotated[str, MinLen(3), MaxLen(25)]
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    is_staff: bool
    is_active: bool

    @validator("username")
    @classmethod
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    exp: datetime = Field(alias="exp")
    is_active: bool = Field(alias="is_active")


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str
