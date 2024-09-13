from pydantic import BaseModel, Field


class InvitedUserConfirmation(BaseModel):
    user_invitation_id: str
    organization_id: int
    invite_url: str = Field(..., description="URL to confirm user invite")
    expires_at: str = Field(..., description="Expiration date of user invite in ISO-8601 format")


class CreatedCompanyConfirmation(BaseModel):
    company_id: int
    friendly_name: str
    internal_name: str

