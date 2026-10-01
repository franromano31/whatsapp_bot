from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.exceptions.user_exp import UserAlreadyExistsError
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:

    def create_user(
        self,
        request: UserCreate,
    ) -> User:

        with SessionLocal() as db:

            existing_user = db.scalar(
                select(User).where(
                    User.phone == request.phone
                )
            )

            if existing_user:
                raise UserAlreadyExistsError(
                    "Ya existe un usuario con ese teléfono"
                )

            user = User(
                phone=request.phone,
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
            )

            db.add(user)

            try:
                db.commit()
            except IntegrityError:
                db.rollback()

                raise UserAlreadyExistsError(
                    "Ya existe un usuario con ese teléfono"
                )

            db.refresh(user)

            return user

    def get_user_by_phone(
        self,
        phone: str,
    ) -> User | None:

        with SessionLocal() as db:

            statement = select(User).where(
                User.phone == phone
            )

            return db.scalar(statement)

    def get_or_create_user(
        self,
        phone: str,
    ) -> User:

        with SessionLocal() as db:

            user = db.scalar(
                select(User).where(
                    User.phone == phone
                )
            )

            if user:
                return user

            user = User(
                phone=phone
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return user


user_service = UserService()