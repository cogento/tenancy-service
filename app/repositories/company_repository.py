from cogento_core.db.models import Company
from cogento_core.db.repository import SqlRepository
from cogento_core.exceptions import EntityNotFoundError

from repositories.base_repositories import CompanyRepository


class SqlCompanyRepository(CompanyRepository, SqlRepository):
    def get_by_id(self, company_id: int):
        result = self.session.query(Company).filter(Company.company_id == company_id).first()
        if not result:
            raise EntityNotFoundError(f"Company with id '{company_id}' not found")
        return result

    def get_by_name(self, name: str):
        result = self.session.query(Company).filter(Company.name == name).first()
        if not result:
            raise EntityNotFoundError(f"Company with name '{name}' not found")
        return result

    def update_descriptors(self, company_id: int, estimated_revenue: float = None):
        company = self.get_by_id(company_id)
        if estimated_revenue is not None:
            company.estimated_revenue = estimated_revenue

        self.session.add(company)
        self.session.commit()
        return company

    def update(self, company: Company):
        self.session.add(company)
        self.session.commit()
        return company

    def create(self, company: Company):
        self.session.add(company)
        self.session.commit()
        return company
