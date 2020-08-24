import functools

from tea_client.errors import PydanticValidationError, ValidationError


def handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PydanticValidationError as e:
            raise ValidationError(error=e)

    return wrapper
