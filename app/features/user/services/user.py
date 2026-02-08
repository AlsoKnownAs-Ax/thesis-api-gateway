from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth.utils import get_password_hash
from app.core.database import get_db
from app.features.user.exceptions.user import UserAlreadyExistsException
from app.features.user.models.user import User
from app.features.user.schemas.user import UserCreate


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()

    def get_user_by_email(self, email: str) -> User | None:
        return self._db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate) -> User:
        if self.get_user_by_email(user.email):
            raise UserAlreadyExistsException()

        user = User(
            **user.model_dump(exclude={"password"}), password=get_password_hash(user.password)
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(session=db)