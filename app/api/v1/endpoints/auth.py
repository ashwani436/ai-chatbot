from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import SignInRequest, SignUpRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register a user")
def signup(payload: SignUpRequest, db: DatabaseSession) -> UserResponse:
    """Create a user account with an Argon2-protected password."""
    try:
        user = AuthService(db).signup(payload)
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists.") from exc
    return UserResponse.model_validate(user)


@router.post("/signin", response_model=TokenResponse, summary="Sign in")
def signin(payload: SignInRequest, db: DatabaseSession) -> TokenResponse:
    """Verify credentials and issue a bearer access token."""
    try:
        return AuthService(db).signin(payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.get("/me", response_model=UserResponse, summary="Get the signed-in user")
def read_current_user(current_user: CurrentUser) -> UserResponse:
    """Return the profile belonging to the bearer token."""
    return UserResponse.model_validate(current_user)
