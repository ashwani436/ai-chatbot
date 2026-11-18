from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import SignInRequest, SignUpRequest, TokenResponse


class AuthService:
    """Business rules for account registration and authentication."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._users = UserRepository(session)

    def signup(self, payload: SignUpRequest) -> User:
        if self._users.get_by_email(payload.email) is not None:
            raise DuplicateEmailError
        user = User(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password))
        self._users.add(user)
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise DuplicateEmailError from exc
        self._session.refresh(user)
        return user

    def signin(self, payload: SignInRequest) -> TokenResponse:
        user = self._users.get_by_email(payload.email)
        if user is None or not user.is_active or not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsError
        return TokenResponse(access_token=create_access_token(str(user.id)))
