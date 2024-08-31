from cogento_core.db.models import CompanyIndustry
from cogento_core.db.repository import SqlRepository

from repositories.base_repositories import CompanyIndustryRepository


class SqlCompanyIndustryRepository(CompanyIndustryRepository, SqlRepository):
    def list(self):
        return self.session.query(CompanyIndustry).all()
