import re
from typing import List

from pydantic import BaseModel, EmailStr, field_validator

from models import TaskStatus


class UserCreateSchema(BaseModel):
    username : str
    password : str
    email : EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must be at least one Upper letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must be at least one number")
        if not re.search(r"[!@#$%^&*()_+\".]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class UserLoginSchema(BaseModel):
    username : str
    password : str


class TaskCreateSchema(BaseModel):
    title : str



    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if re.search(r"[!@#$%^&*()-_=+\".,]", value):
            raise ValueError("Title cant contain special character")
        return value

class TaskUpdateSchema(BaseModel):
    title : str
    status : TaskStatus

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        allowed_statuses = {status.value for status in TaskStatus}
        if value not in allowed_statuses:
            raise ValueError(f"Invalid status: {value}. Allowed values: {allowed_statuses}")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if re.search(r"[!@#$%^&*()-_=+\".,]", value):
            raise ValueError("Title cant contain special character")
        return value
