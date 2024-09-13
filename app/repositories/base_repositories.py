from abc import ABC, abstractmethod
from typing import List

from cogento_core.db.models import User, Company
from cogento_core.db.repository import AbstractRepository


class UserRepository(AbstractRepository, ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def list(self, company_id: int) -> List[User]:
        pass

    @abstractmethod
    def create_user_if_not_exists(self, user: User) -> User:
        pass

    @abstractmethod
    def update_attrs(self, user_id: int, first_name: str, last_name: str):
        pass


class CompanyRepository(AbstractRepository, ABC):
    @abstractmethod
    def get_by_id(self, company_id: int) -> Company:
        pass

    @abstractmethod
    def update_attrs(
            self,
            company_id: int,
            friendly_name: str = None,
            industry_id: int = None,
            estimated_revenue: float = None
    ):
        pass

    @abstractmethod
    def create_company(self, company: Company) -> Company:
        pass
