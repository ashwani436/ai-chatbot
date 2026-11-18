from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def normalize_email(value: str) -> str:
    return value.strip().casefold()


class SignUpRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Ashwani"])
    email: EmailStr = Field(examples=["ashwani@example.com"])
    password: str = Field(min_length=8, max_length=128, examples=["StrongPass123"])

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank.")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email_address(cls, value: EmailStr) -> str:
        return normalize_email(str(value))


class SignInRequest(BaseModel):
    email: EmailStr = Field(examples=["ashwani@example.com"])
    password: str = Field(min_length=1, max_length=128, examples=["StrongPass123"])

    @field_validator("email")
    @classmethod
    def normalize_email_address(cls, value: EmailStr) -> str:
        return normalize_email(str(value))


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
