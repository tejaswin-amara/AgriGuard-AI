import asyncio
import logging
import time
from collections.abc import Mapping
from typing import Any

import httpx

from app.services.external.errors import (
    ProviderError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)

logger = logging.getLogger("agriguard.external.transport")


class AsyncHttpTransport:
    """Shared HTTP client wrapper with timeout, retry with exponential backoff, and error mapping."""

    def __init__(
        self,
        default_headers: dict[str, str] | None = None,
        timeout_seconds: float = 8.0,
        max_retries: int = 2,
    ):
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        headers = {"User-Agent": "AgriGuard-AI/2.0 (Agricultural Intelligence Platform; contact@agriguard.ai)"}
        if default_headers:
            headers.update(default_headers)
        self.headers = headers

    async def get_json(
        self,
        provider_id: str,
        url: str,
        params: Mapping[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any] | list[Any]:
        req_headers = dict(self.headers)
        if extra_headers:
            req_headers.update(extra_headers)

        req_timeout = timeout or self.timeout_seconds
        attempt = 0
        backoff = 0.5

        while True:
            attempt += 1
            start_time = time.perf_counter()
            try:
                async with httpx.AsyncClient(timeout=req_timeout, follow_redirects=True) as client:
                    response = await client.get(url, params=params, headers=req_headers)
                    duration_ms = (time.perf_counter() - start_time) * 1000

                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After")
                        wait_sec = int(retry_after) if retry_after and retry_after.isdigit() else backoff
                        if attempt <= self.max_retries:
                            logger.warning(
                                f"[{provider_id}] Rate limited (429). Retrying in {wait_sec}s (attempt {attempt}/{self.max_retries})"
                            )
                            await asyncio.sleep(wait_sec)
                            backoff *= 2
                            continue
                        raise ProviderRateLimitError(provider_id, "Rate limit exceeded", retry_after=wait_sec)

                    if response.status_code >= 500:
                        if attempt <= self.max_retries:
                            logger.warning(
                                f"[{provider_id}] Server error ({response.status_code}). Retrying in {backoff}s (attempt {attempt}/{self.max_retries})"
                            )
                            await asyncio.sleep(backoff)
                            backoff *= 2
                            continue
                        raise ProviderError(
                            provider_id, f"Server error HTTP {response.status_code}", status_code=response.status_code
                        )

                    if response.status_code >= 400:
                        raise ProviderError(
                            provider_id, f"Client error HTTP {response.status_code}: {response.text[:200]}", status_code=response.status_code
                        )

                    logger.debug(f"[{provider_id}] HTTP GET {url} succeeded in {duration_ms:.1f}ms")
                    try:
                        return response.json()
                    except Exception as e:
                        raise ProviderResponseError(provider_id, f"Invalid JSON response: {e!s}")

            except httpx.TimeoutException:
                if attempt <= self.max_retries:
                    logger.warning(
                        f"[{provider_id}] Timeout ({req_timeout}s). Retrying in {backoff}s (attempt {attempt}/{self.max_retries})"
                    )
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise ProviderTimeoutError(provider_id, f"Request timed out after {req_timeout}s")
            except (httpx.NetworkError, httpx.ProtocolError) as e:
                if attempt <= self.max_retries:
                    logger.warning(
                        f"[{provider_id}] Network error: {e!s}. Retrying in {backoff}s (attempt {attempt}/{self.max_retries})"
                    )
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise ProviderError(provider_id, f"Network error: {e!s}")


transport = AsyncHttpTransport()
