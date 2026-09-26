class ProviderError(Exception):
    """Base exception for all external data provider errors."""

    def __init__(self, provider_id: str, message: str, status_code: int | None = None):
        super().__init__(f"[{provider_id}] {message}")
        self.provider_id = provider_id
        self.message = message
        self.status_code = status_code


class ProviderTimeoutError(ProviderError):
    """Raised when request to external provider times out."""


class ProviderRateLimitError(ProviderError):
    """Raised when external provider rate limit is exceeded (HTTP 429)."""

    def __init__(
        self,
        provider_id: str,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ):
        super().__init__(provider_id, message, status_code=429)
        self.retry_after = retry_after


class ProviderResponseError(ProviderError):
    """Raised when external provider returns malformed or error payload."""


class ProviderUnavailableError(ProviderError):
    """Raised when external provider is disabled, unreachable, or in circuit-breaker state."""


class ProviderConfigError(ProviderError):
    """Raised when provider configuration or API keys are missing/invalid."""
