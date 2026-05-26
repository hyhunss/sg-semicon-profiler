"""Pydantic schema for one Singapore semiconductor company profile."""

from __future__ import annotations

from datetime import date
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


COMPANY_COLUMNS = [
    "company_name",
    "website",
    "domain",
    "business_summary",
    "semicon_role",
    "products_services",
    "target_customer_type",
    "buyer_need",
    "evidence_url",
    "confidence",
    "last_checked",
    "notes",
]


def normalize_domain(url: str) -> str:
    candidate = url.strip()
    if not candidate:
        raise ValueError("url cannot be blank")
    if "://" not in candidate:
        candidate = "https://" + candidate

    parsed = urlparse(candidate)
    domain = (parsed.hostname or "").lower().strip(".")
    if domain.startswith("www."):
        domain = domain[4:]
    if not domain or "." not in domain:
        raise ValueError(f"could not normalize domain from {url!r}")
    return domain


class CompanyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str
    website: HttpUrl
    domain: str
    business_summary: str = Field(min_length=20)
    semicon_role: Literal[
        "idm",
        "fabless",
        "foundry",
        "packaging_test",
        "equipment",
        "precision_engineering",
        "materials",
        "systems_integrator",
        "distributor",
        "software",
        "unclear",
    ]
    products_services: str
    target_customer_type: str = Field(min_length=5)
    buyer_need: str = Field(min_length=5)
    evidence_url: HttpUrl
    confidence: Literal["high", "medium", "low"]
    last_checked: date
    notes: str = ""

    @model_validator(mode="after")
    def enforce_profile_rules(self) -> "CompanyProfile":
        website_domain = normalize_domain(str(self.website))
        normalized_domain = normalize_domain(self.domain)
        if normalized_domain != website_domain:
            raise ValueError(
                f"domain {self.domain!r} does not match website domain {website_domain!r}"
            )
        self.domain = normalized_domain

        return self


CompanyProfile.model_rebuild()
