"""Legends Firecrawl runtime."""

from .client import ApiError, CredentialError, FirecrawlClient, SafetyError

__version__ = "0.2.0"

__all__ = [
    "ApiError",
    "CredentialError",
    "FirecrawlClient",
    "SafetyError",
    "__version__",
]

