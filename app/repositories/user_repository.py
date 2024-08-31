from cogento_core.db.models import User
from cogento_core.db.repository import SqlRepository
from cogento_core.exceptions import EntityNotFoundError

from repositories.base_repositories import UserRepository


class SqlUserRepository(UserRepository, SqlRepository):
    def get_by_id(self, user_id: int):
        result = self.session.query(User).filter(User.user_id == user_id).first()
        if not result:
            raise EntityNotFoundError(f"User with id '{user_id}' not found")
        return result

    def get_by_email(self, email: str):
        result = self.session.query(User).filter(User.email == email).first()
        if not result:
            raise EntityNotFoundError(f"User with email '{email}' not found")
        return result

    def get_by_company(self, company_id: int):
        return self.session.query(User).filter(User.company_id == company_id).all()

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        return user
