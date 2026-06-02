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
    "evidence_urls",
    "evidence_summary",
    "confidence",
    "research_quality",
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
    evidence_urls: list[HttpUrl] = Field(min_length=1, max_length=5)
    evidence_summary: str = Field(min_length=20)
    confidence: Literal["high", "medium", "low"]
    research_quality: Literal[
        "complete",
        "limited_site",
        "thin_evidence",
        "inaccessible_site",
        "conflicting_sources",
    ]
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

        evidence_url = str(self.evidence_url).rstrip("/")
        evidence_urls = {str(url).rstrip("/") for url in self.evidence_urls}
        if evidence_url not in evidence_urls:
            raise ValueError("evidence_url must also appear in evidence_urls")

        company_site_count = sum(
            1 for url in self.evidence_urls if normalize_domain(str(url)) == website_domain
        )

        if self.confidence == "high":
            if self.research_quality != "complete":
                raise ValueError("high confidence requires research_quality='complete'")
            if len(evidence_urls) < 3:
                raise ValueError("high confidence requires at least 3 distinct evidence_urls")
            if company_site_count < 3:
                raise ValueError("high confidence requires at least 3 company-site evidence_urls")

        if self.research_quality == "complete" and len(evidence_urls) < 3:
            raise ValueError("research_quality='complete' requires at least 3 evidence_urls")
        if self.research_quality == "complete" and company_site_count < 3:
            raise ValueError("research_quality='complete' requires at least 3 company-site evidence_urls")

        return self


CompanyProfile.model_rebuild()
