"""Better Auth integration service for JWT token validation."""

import os
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

# Better Auth configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


class AuthError(Exception):
    """Custom exception for authentication errors."""

    pass


class TokenExpiredError(AuthError):
    """Token has expired."""

    pass


class InvalidTokenError(AuthError):
    """Token is invalid."""

    pass


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload.

    Args:
        token: JWT token string from Authorization header.

    Returns:
        dict: Decoded token payload containing user information.

    Raises:
        TokenExpiredError: If token has expired.
        InvalidTokenError: If token is invalid or malformed.
        AuthError: For other authentication errors.

    Example:
        >>> payload = verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> user_id = payload.get("sub")
    """
    if not BETTER_AUTH_SECRET:
        raise AuthError("BETTER_AUTH_SECRET environment variable not configured")

    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")


def extract_user_id(token: str) -> UUID:
    """Extract user_id from JWT token.

    Args:
        token: JWT token string from Authorization header.

    Returns:
        UUID: User ID extracted from token subject claim.

    Raises:
        TokenExpiredError: If token has expired.
        InvalidTokenError: If token is invalid or missing user_id.
        AuthError: For other authentication errors.

    Example:
        >>> user_id = extract_user_id("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> print(user_id)
        550e8400-e29b-41d4-a716-446655440000
    """
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    payload = verify_token(token)

    # Extract user_id from "sub" claim (standard JWT subject claim)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenError("Token missing 'sub' claim (user_id)")

    try:
        user_id = UUID(user_id_str)
        return user_id
    except ValueError:
        raise InvalidTokenError(f"Invalid user_id format in token: {user_id_str}")


def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for a user.

    Args:
        user_id: User UUID to encode in token.
        expires_delta: Optional custom expiration time.

    Returns:
        str: Encoded JWT token.

    Example:
        >>> from uuid import uuid4
        >>> user_id = uuid4()
        >>> token = create_access_token(user_id)
    """
    if not BETTER_AUTH_SECRET:
        raise AuthError("BETTER_AUTH_SECRET environment variable not configured")

    to_encode = {"sub": str(user_id)}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def validate_bearer_token(authorization: Optional[str]) -> UUID:
    """Validate Authorization header and extract user_id.

    Args:
        authorization: Full Authorization header value (e.g., "Bearer <token>").

    Returns:
        UUID: User ID from token.

    Raises:
        InvalidTokenError: If Authorization header is missing or malformed.
        TokenExpiredError: If token has expired.
        AuthError: For other authentication errors.

    Example:
        >>> user_id = validate_bearer_token("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    """
    if not authorization:
        raise InvalidTokenError("Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise InvalidTokenError("Authorization header must start with 'Bearer '")

    # DEVELOPMENT MODE: Accept dev-token-{user_id} format for testing
    # In production, remove this block or check ENVIRONMENT != "development"
    environment = os.getenv("ENVIRONMENT", "production")
    if environment == "development" and "dev-token-" in authorization:
        # Extract user_id from dev-token-{user_id}
        token_part = authorization.replace("Bearer ", "")
        if token_part.startswith("dev-token-"):
            user_id_str = token_part.replace("dev-token-", "")
            try:
                user_id = UUID(user_id_str)
                return user_id
            except ValueError:
                raise InvalidTokenError(f"Invalid dev token format: {token_part}")

    return extract_user_id(authorization)
