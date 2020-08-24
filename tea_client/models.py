import re
from typing import Optional

from pydantic import BaseModel, validator

# Auth


class AuthRequest(BaseModel):
    username: str
    password: str


# Colored


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6})$")


def color_validator(value):
    if COLOR_RE.match(value) is None:
        raise ValueError(f"Invalid color string: {value}")
    return value


class ColoredModel(BaseModel):
    color: str

    @validator("color")
    def validate_color(cls, value):
        return color_validator(value)


class ColoredUpdateModel(BaseModel):
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        return color_validator(value)
