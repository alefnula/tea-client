from typing import Optional

from httpx import Response
from pydantic import ValidationError as PydanticValidationError


class TeaClientError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

    @property
    def class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.class_name}({self.status_code}: {self.message})"

    __repr__ = __str__


class ValidationError(TeaClientError):
    def __init__(self, error: PydanticValidationError):
        self.error = error
        super().__init__(message="Request validation error.", status_code=400)

    @property
    def errors(self):
        return self.error.errors()


class HttpClientError(TeaClientError):
    def __init__(
        self,
        message: str,
        response: Optional[Response] = None,
        status_code: int = 500,
    ):
        super().__init__(
            message=message,
            status_code=(
                status_code if response is None else response.status_code
            ),
        )
        self.response: Response = response

    @property
    def data(self):
        return self.response.json()


class HttpClientTimeout(HttpClientError):
    """Http timeout error."""

    def __init__(self):
        super().__init__("Timeout exceeded")


class HttpRateLimitExceeded(HttpClientError):
    def __init__(self, response, limit, remaining, reset, retry):
        super().__init__("Rate limit exceeded.", response=response)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.retry = retry

    def __str__(self):
        return (
            f"{self.name}(limit={self.limit}, remaining={self.remaining}, "
            f"reset={self.reset}s, retry={self.retry}s)"
        )

    __repr__ = __str__


class SerializationError(TeaClientError):
    def __init__(self, errors):
        """Thrown when the client cannot serialize or deserialize an object.

        Args:
            errors (dict): Dictionary of found errors
        """
        super().__init__("Serialization error.")
        self.errors = errors
