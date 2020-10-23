import logging
import functools

from tea_client.errors import (
    HttpClientError,
    PydanticValidationError,
    ValidationError,
)


logger = logging.getLogger(__name__)


def handler(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HttpClientError as e:
            if e.status_code == 401:
                # Try to refresh the token and call the function again.
                if (
                    self.http.authorization_method
                    == self.http.Authorization.jwt
                ):
                    try:
                        self.refresh()
                        return func(self, *args, **kwargs)
                    except Exception as e:
                        logger.warning("Failed to refresh token: %s", e)
            raise
        except PydanticValidationError as e:
            raise ValidationError(error=e)

    return wrapper
