from pydantic import BaseModel, Field

from cogento_core.db.models import Company


class BillingInfo(BaseModel):
    address_line1: str = Field(..., description="Address line 1")
    address_line2: str = Field(None, description="Address line 2")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="Zip code")
    country: str = Field(..., description="Country")
    billing_email: str = Field(..., description="Billing email")


class CreateCompanyRequest(BaseModel):
    friendly_name: str = Field(..., description="Friendly name")
    estimated_revenue: float = Field(..., gt=0, description="Estimated revenue (millions)")
    billing_info: BillingInfo = Field(..., description="Billing information")

    def to_company(self) -> Company:
        return Company(
            name=self.friendly_name.replace(" ", "-").lower(),
            friendly_name=self.friendly_name,
            estimated_revenue=self.estimated_revenue,
            billing_email=self.billing_info.billing_email
        )


class UpdateCompanyRequest(BaseModel):
    friendly_name: str = Field(None, description="Friendly name")
    industry_id: int = Field(None, gt=0, description="Industry ID")
    estimated_revenue: float = Field(None, gt=0, description="Estimated revenue (millions)")
