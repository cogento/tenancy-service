from cogento_core.db.models import Company
from cogento_core.db.repository import SqlRepository
from cogento_core.exceptions import EntityNotFoundError

from repositories.base_repositories import CompanyRepository


class SqlCompanyRepository(CompanyRepository, SqlRepository):
    def get_by_id(self, company_id: int) -> Company:
        entity = self.session.query(Company).filter_by(company_id=company_id).first()
        if entity is None:
            raise EntityNotFoundError(f"Company with id {company_id} not found")

        return entity

    def update_attrs(self, company_id: int, friendly_name: str = None, industry_id: int = None,
                     estimated_revenue: float = None) -> None:
        company = self.get_by_id(company_id)
        if friendly_name is not None:
            company.friendly_name = friendly_name
        if industry_id is not None:
            company.industry_id = industry_id
        if estimated_revenue is not None:
            company.estimated_revenue = estimated_revenue
        self.session.commit()
        return company

    def create_company(self, company: Company) -> Company:
        self.session.add(company)
        self.session.commit()
        return company
