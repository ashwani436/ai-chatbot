class DuplicateEmailError(Exception):
    """Raised when a registration attempts to use an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when supplied sign-in credentials cannot be authenticated."""


class AuthenticationError(Exception):
    """Raised when a bearer token cannot identify an active user."""
