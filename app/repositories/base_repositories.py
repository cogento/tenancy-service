from abc import ABC, abstractmethod
from typing import List

from cogento_core.db.models import CompanyIndustry
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
    def get_by_company(self, company_id: int) -> List[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass


class CompanyRepository(AbstractRepository, ABC):
    @abstractmethod
    def get_by_id(self, company_id: int) -> Company:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Company:
        pass

    @abstractmethod
    def update_descriptors(self, company_id: int, estimated_revenue: float = None) -> Company:
        pass

    @abstractmethod
    def update(self, company: Company) -> Company:
        pass

    @abstractmethod
    def create(self, company: Company) -> Company:
        pass


class CompanyIndustryRepository(AbstractRepository, ABC):
    @abstractmethod
    def list(self) -> List[CompanyIndustry]:
        pass
