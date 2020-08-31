import re
from typing import Optional

from pydantic import BaseModel, validator


class TeaClientModel(BaseModel):
    pass


# Auth


class Auth(TeaClientModel):
    token_access: str
    token_refresh: str


class AuthRequest(TeaClientModel):
    username: str
    password: str


class AuthRefreshRequest(TeaClientModel):
    refresh: str


# Colored


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6})$")


def color_validator(value):
    if COLOR_RE.match(value) is None:
        raise ValueError(f"Invalid color string: {value}")
    return value


class ColoredModel(TeaClientModel):
    color: str

    @validator("color")
    def validate_color(cls, value):
        return color_validator(value)


class ColoredUpdateModel(TeaClientModel):
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        return color_validator(value)
