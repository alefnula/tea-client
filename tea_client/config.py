from typing import Optional


class TeaClientConfig:
    def __init__(
        self,
        server_url: str = "http:/127.0.0.1:8000",
        api_version: int = 0,
        token_access: Optional[str] = None,
        token_refresh: Optional[str] = None,
    ):
        self.server_url = server_url
        self.api_version = api_version
        self.token_access = token_access
        self.token_refresh = token_refresh

    def save(self):
        pass
