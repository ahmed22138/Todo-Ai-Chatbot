"""CORS middleware configuration for FastAPI."""

import os
from typing import List

from fastapi.middleware.cors import CORSMiddleware

# Frontend origin from environment or default to localhost:3000
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# Additional allowed origins (comma-separated in environment)
ADDITIONAL_ORIGINS = os.getenv("ADDITIONAL_ORIGINS", "")


def get_cors_middleware_config() -> dict:
    """Get CORS middleware configuration.

    Returns:
        dict: Configuration for CORSMiddleware with allowed origins,
              methods, headers, and credentials settings.

    Example:
        app.add_middleware(CORSMiddleware, **get_cors_middleware_config())
    """
    # Build list of allowed origins
    allowed_origins: List[str] = [FRONTEND_ORIGIN]

    # Add additional origins if specified
    if ADDITIONAL_ORIGINS:
        additional = [origin.strip() for origin in ADDITIONAL_ORIGINS.split(",") if origin.strip()]
        allowed_origins.extend(additional)

    return {
        "allow_origins": allowed_origins,
        "allow_credentials": True,  # Allow cookies and Authorization headers
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "User-Agent",
            "DNT",
            "Cache-Control",
            "X-Requested-With",
        ],
        "expose_headers": [
            "Content-Length",
            "Content-Type",
            "X-Request-ID",
        ],
        "max_age": 600,  # Cache preflight requests for 10 minutes
    }


def configure_cors(app) -> None:
    """Configure CORS middleware for FastAPI application.

    Args:
        app: FastAPI application instance.

    Example:
        from fastapi import FastAPI
        app = FastAPI()
        configure_cors(app)
    """
    config = get_cors_middleware_config()
    app.add_middleware(CORSMiddleware, **config)
