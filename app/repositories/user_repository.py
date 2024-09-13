from typing import List

from cogento_core.db.models import User
from cogento_core.db.repository import SqlRepository
from cogento_core.exceptions import EntityNotFoundError

from repositories.base_repositories import UserRepository


class SqlUserRepository(UserRepository, SqlRepository):

    def get_by_id(self, user_id: int) -> User:
        entity = self.session.query(User).filter_by(user_id=user_id).first()
        if entity is None:
            raise EntityNotFoundError(f"User with id {user_id} not found")

        return entity

    def get_by_email(self, email: str) -> User:
        entity = self.session.query(User).filter_by(email=email).first()
        if entity is None:
            raise EntityNotFoundError(f"User with email {email} not found")

        return entity

    def list(self, company_id: int) -> List[User]:
        return (
            self.session.query(User)
            .filter_by(company_id=company_id)
            .all()
        )

    def create_user_if_not_exists(self, user: User) -> User:
        existing_user = self.session.query(User).filter_by(email=user.email).first()
        if existing_user is None:
            self.session.add(user)
            self.session.commit()
            return user
        return existing_user

    def update_attrs(self, user_id: int, first_name: str, last_name: str):
        user = self.get_by_id(user_id)
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        self.session.commit()
