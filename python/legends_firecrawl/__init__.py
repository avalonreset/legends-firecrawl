"""Legends Firecrawl runtime."""

from .client import ApiError, CredentialError, FirecrawlClient, SafetyError

__version__ = "0.3.5"

__all__ = [
    "ApiError",
    "CredentialError",
    "FirecrawlClient",
    "SafetyError",
    "__version__",
]

