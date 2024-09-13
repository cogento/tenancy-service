from cogento_core.db.models import CompanyIndustry
from pydantic import BaseModel, Field


class InvitedUserConfirmation(BaseModel):
    user_invitation_id: int
    organization_id: int
    invite_url: str = Field(..., description="URL to confirm user invite")
    expires_at: str = Field(..., description="Expiration date of user invite in ISO-8601 format")


class CompanyIndustryGroup(BaseModel):
    category_name: str
    desc: str
    industries: list[CompanyIndustry]


class CompanyIndustryHierarchy(BaseModel):
    industry_groups: list[CompanyIndustryGroup]
