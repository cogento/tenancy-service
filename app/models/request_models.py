from pydantic import BaseModel, Field

from cogento_core.db.models import Company

from cogento_core.enums import CompanyClassification


class BillingInfo(BaseModel):
    address_line1: str = Field(..., description="Address line 1")
    address_line2: str = Field(None, description="Address line 2")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="Zip code")
    country: str = Field(..., description="Country")
    billing_email: str = Field(..., description="Billing email")


class CreateCompanyRequest(BaseModel):
    name: str = Field(..., description="Company name")
    friendly_name: str = Field(..., description="Friendly name")
    industry_id: int = Field(..., gt=0, description="Industry ID")
    estimated_revenue: float = Field(..., gt=0, description="Estimated revenue (millions)")
    billing_info: BillingInfo = Field(..., description="Billing information")

    def get_classification(self):
        if self.estimated_revenue < 1.0:  # million
            return CompanyClassification.SMALL
        elif self.estimated_revenue < 10.0:
            return CompanyClassification.MEDIUM
        elif self.estimated_revenue < 100.0:
            return CompanyClassification.LARGE
        else:
            return CompanyClassification.ENTERPRISE

    def to_company(self) -> Company:
        return Company(
            name=self.name,
            friendly_name=self.friendly_name,
            industry_id=self.industry_id,
            estimated_revenue=self.estimated_revenue,
            classification=self.get_classification()
        )


class UpdateCompanyRequest(BaseModel):
    friendly_name: str = Field(None, description="Friendly name")
    industry_id: int = Field(None, gt=0, description="Industry ID")
    estimated_revenue: float = Field(None, gt=0, description="Estimated revenue (millions)")
