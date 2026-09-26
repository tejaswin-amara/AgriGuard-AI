import asyncio
import logging
import time
from typing import Any, Callable, Coroutine, TypeVar
from app.services.external.types import FreshnessState

logger = logging.getLogger("agriguard.external.cache")

T = TypeVar("T")

# Configurable Default TTLs in seconds
TTL_POLICIES = {
    "weather": 1800,         # 30 minutes
    "climate": 86400,        # 24 hours
    "geocoding": 604800,     # 7 days
    "air_quality": 3600,     # 1 hour
    "elevation": 604800,     # 7 days
    "biodiversity": 86400,   # 24 hours
    "news": 1800,            # 30 minutes
}

STALE_WINDOW_MULTIPLIER = 4.0  # Retain stale data up to 4x TTL for graceful degradation fallbacks


class CacheEntry:
    def __init__(self, key: str, value: Any, ttl_seconds: float):
        self.key = key
        self.value = value
        self.ttl_seconds = ttl_seconds
        self.created_at = time.time()

    def get_freshness(self) -> FreshnessState:
        age = time.time() - self.created_at
        if age <= self.ttl_seconds:
            return FreshnessState.FRESH if age < 10 else FreshnessState.CACHED
        elif age <= self.ttl_seconds * STALE_WINDOW_MULTIPLIER:
            return FreshnessState.STALE
        return FreshnessState.UNAVAILABLE


class ProviderCache:
    """Data-aware TTL cache with request coalescing and stale-data fallback support."""

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._inflight: dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()

    @staticmethod
    def make_key(category: str, *args, **kwargs) -> str:
        formatted_args = ":".join(str(a) for a in args)
        formatted_kwargs = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{category}:{formatted_args}:{formatted_kwargs}".strip(":")

    def get(self, key: str) -> tuple[Any | None, FreshnessState]:
        entry = self._cache.get(key)
        if not entry:
            return None, FreshnessState.UNAVAILABLE

        state = entry.get_freshness()
        if state == FreshnessState.UNAVAILABLE:
            return None, FreshnessState.UNAVAILABLE
        return entry.value, state

    def set(self, key: str, value: Any, ttl_seconds: float):
        self._cache[key] = CacheEntry(key, value, ttl_seconds)

    async def get_or_fetch(
        self,
        key: str,
        fetch_coro_fn: Callable[[], Coroutine[Any, Any, T]],
        category: str,
        allow_stale_on_error: bool = True,
    ) -> tuple[T, FreshnessState]:
        # 1. Check cache first
        val, freshness = self.get(key)
        if val is not None and freshness in (FreshnessState.FRESH, FreshnessState.CACHED):
            return val, FreshnessState.CACHED

        # 2. Check inflight deduplication
        async with self._lock:
            if key in self._inflight:
                fut = self._inflight[key]
                # Wait for inflight fetch
                try:
                    res = await fut
                    return res, FreshnessState.FRESH
                except Exception:
                    # Inflight failed, proceed to retry/fallback
                    pass

            # Register as inflight
            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            self._inflight[key] = fut

        # 3. Perform fetch
        ttl_seconds = TTL_POLICIES.get(category, 1800)
        try:
            result = await fetch_coro_fn()
            self.set(key, result, ttl_seconds)
            if not fut.done():
                fut.set_result(result)
            return result, FreshnessState.FRESH
        except Exception as e:
            if not fut.done():
                fut.set_exception(e)

            # 4. Graceful degradation to stale cache if available
            if allow_stale_on_error and val is not None and freshness == FreshnessState.STALE:
                logger.warning(f"Fetch for {key} failed ({str(e)}); serving stale cached fallback.")
                return val, FreshnessState.STALE
            raise e
        finally:
            async with self._lock:
                self._inflight.pop(key, None)


provider_cache = ProviderCache()
