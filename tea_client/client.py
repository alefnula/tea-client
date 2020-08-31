from tea_client.config import TeaClientConfig
from tea_client.http import HttpClient
from tea_client.handler import handler
from tea_client.models import Auth, AuthRequest, AuthRefreshRequest


class TeaClient:
    def __init__(self, config: TeaClientConfig):
        self.config = config
        self.http = HttpClient(
            url=(
                f"{self.config.server_url.rstrip('/')}"
                f"/api/v{config.api_version}"
            ),
            token=config.token_access or "",
        )
        self.token_refresh = config.token_refresh

    # Auth
    @handler
    def login(self, username: str, password: str) -> Auth:
        """Obtain authentication token.

        Args:
            username: Traktor username.
            password: Traktor password.

        Returns:
            str: Authentication token.
        """
        response = self.http.post(
            "/auth/token/",
            data=AuthRequest(username=username, password=password),
        )
        auth = Auth(
            token_access=response["access"], token_refresh=response["refresh"]
        )
        self.http.token = auth.token_access
        self.token_refresh = auth.token_refresh
        self.config.token_access = auth.token_access
        self.config.token_refresh = auth.token_refresh
        self.config.save()
        return auth

    @handler
    def refresh(self) -> str:
        """Try to refresh auth token."""
        response = self.http.post(
            "/auth/token/refresh/",
            data=AuthRefreshRequest(refresh=self.token_refresh),
        )
        token_access = response["access"]
        self.http.token = token_access
        self.config.token_access = token_access
        self.config.save()
        return token_access
