from cogento_core.db.models import Company
from cogento_core.logging import logger
from cogento_core.utils import global_manager as gm
from fastapi import APIRouter, Depends
from starlette import status

from models.request_models import CreateCompanyRequest, UpdateCompanyRequest
from models.response_models import InvitedUserConfirmation
from repositories.base_repositories import CompanyRepository
from repositories.company_repository import SqlCompanyRepository
from services.auth0_service import Auth0Provider
from services.stripe_service import StripeService

router = APIRouter(
    prefix="/company",
    tags=["company"]
)


@router.get(
    "/{company_id}",
    response_model=Company,
    status_code=status.HTTP_200_OK,
    operation_id="get_company_by_id"
)
async def get_company_by_id(
        company_id: int,
        company_repo: CompanyRepository = Depends(SqlCompanyRepository)
) -> Company:
    """
    Retrieve a company by its company_id.
    """
    logger.info("Retrieving company {} by ID", company_id)
    return company_repo.get_by_id(company_id=company_id)


@router.post(
    "/",
    response_model=Company,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_company"
)
async def create_company(
        create_company_request: CreateCompanyRequest,
        company_repo: CompanyRepository = Depends(SqlCompanyRepository),
        auth0_provider: Auth0Provider = gm.depends(Auth0Provider),
        stripe_provider: StripeService = gm.depends(StripeService),
) -> Company:
    """
    Create a new company with the given details. This will provision a new customer in
    Stripe, an organization in Auth0, and a new company in the database.
    """
    company = create_company_request.to_company()
    logger.info("Creating company {} in Auth0", company.friendly_name)
    auth0_organization_id = auth0_provider.create_organization(
        organization_name=company.name,
        organization_display_name=company.friendly_name
    )
    logger.info("Provisioned organization {} in Auth0 with ID {}", company.friendly_name, auth0_organization_id)
    company.auth0_organization_id = auth0_organization_id
    logger.info("Provisioning company {} in Stripe", company.friendly_name)
    stripe_customer_id = stripe_provider.customers.create(
        name=company.friendly_name,
        email=company.email,
        address=stripe_provider.customers.CreateParamsAddress(
            city=company.city,
            country=company.country,
            line1=create_company_request.billing_info.address_line1,
            line2=create_company_request.billing_info.address_line2,
            postal_code=company.postal_code,
            state=company.state
        )
    ).id
    logger.info("Provisioned company {} in Stripe with ID {}", company.friendly_name, stripe_customer_id)
    company.stripe_customer_id = stripe_customer_id
    company_repo.create_company(company)
    return company


@router.put(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    operation_id="update_company"
)
async def update_company(
        company_id: int,
        update_request: UpdateCompanyRequest,
        company_repo: CompanyRepository = Depends(SqlCompanyRepository)
) -> None:
    """
    Update the details of a company by its company_id.
    """
    logger.info("Updating company {} with new details {}", company_id, update_request.dict())
    return company_repo.update_attrs(
        company_id=company_id,
        friendly_name=update_request.friendly_name,
        industry_id=update_request.industry_id,
        estimated_revenue=update_request.estimated_revenue
    )


@router.post(
    "/{company_id}/invite",
    operation_id="invite_user",
    response_model=InvitedUserConfirmation,
    status_code=status.HTTP_201_CREATED
)
async def invite_user(
        company_id: int,
        user_email: str,
        company_repo: CompanyRepository = Depends(SqlCompanyRepository),
        auth0_provider: Auth0Provider = gm.depends(Auth0Provider)
) -> InvitedUserConfirmation:
    """
    Invite a user to join a company.
    """
    company = company_repo.get_by_id(company_id)
    logger.info("Inviting user {} to company {}", user_email, company.friendly_name)
    response = auth0_provider.invite_user(
        organization_id=company.auth0_organization_id,
        organization_name=company.friendly_name,
        email=user_email
    )

    return InvitedUserConfirmation(
        user_invitation_id=0,
        organization_id=company_id,
        invite_url=response['invite_url'],
        expires_at="2021-12-31T23:59:59Z"
    )
