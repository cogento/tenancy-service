from typing import List

from cogento_core.db.models import Company, CompanyIndustry
from fastapi import APIRouter, Depends
from repositories.base_repositories import CompanyRepository, CompanyIndustryRepository
from repositories.company_industry_repository import SqlCompanyIndustryRepository
from repositories.company_repository import SqlCompanyRepository
from starlette import status

router = APIRouter(
    prefix="/company",
    tags=["company"]
)


@router.get(
    path="/{company_id}",
    operation_id="get_company",
    description="Get Company by ID",
    status_code=status.HTTP_200_OK,
    response_model=Company
)
def get_company(company_id: int, company_repo: CompanyRepository = Depends(SqlCompanyRepository.get)) -> Company:
    """
    Get a company by id
    :return: company
    """
    return company_repo.get_by_id(company_id=company_id)


@router.get(
    path="/name/{name}",
    operation_id="get_company_by_name",
    description="Get Company by Name",
    status_code=status.HTTP_200_OK,
    response_model=Company
)
def get_company_by_name(name: str, company_repo: CompanyRepository = Depends(SqlCompanyRepository.get)) -> Company:
    """
    Get a company by name
    :return: company
    """
    return company_repo.get_by_name(name=name)


@router.put(
    path="/{company_id}",
    operation_id="update_company",
    description="Update Company",
    status_code=status.HTTP_200_OK,
    response_model=Company
)
def update_company(company_id: int, estimated_revenue: float = None,
                   company_repo: CompanyRepository = Depends(SqlCompanyRepository.get)) -> Company:
    """
    Update a company
    :return: company
    """
    return company_repo.update_descriptors(
        company_id=company_id,
        estimated_revenue=estimated_revenue
    )


@router.post(
    path="/",
    operation_id="create_company",
    description="Create Company",
    status_code=status.HTTP_200_OK,
    response_model=Company
)
def create_company(company: Company, company_repo: CompanyRepository = Depends(SqlCompanyRepository.get)) -> Company:
    """
    Create a company
    :return: company
    """
    return company_repo.create(company=company)


@router.get(
    path="/industry/list",
    operation_id="list_company_industries",
    description="List Company Industries",
    status_code=status.HTTP_200_OK,
    response_model=List[CompanyIndustry]
)
def list_company_industries(
        industry_repo: CompanyIndustryRepository = Depends(SqlCompanyIndustryRepository.get)
) -> List[CompanyIndustry]:
    """
    List company industries
    :return: list of company industries
    """
    return industry_repo.list()
