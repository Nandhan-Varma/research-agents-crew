# src/ai_research_crew/models.py

from pydantic import BaseModel, Field
from typing import Optional


# ---------- research_task output ----------

class Finding(BaseModel):
    url: str = Field(description="Source URL the content was found at")
    raw_content: str = Field(
        description="Full extracted page content (via the extractor tool) where available; Falls back to the search snippet only if extraction failed")
    query_used: Optional[str] = Field(
        None, description="The search query that surfaced this result")


class ResearchFindings(BaseModel):
    findings: list[Finding]


# ---------- analyst_task output ----------

class Claim(BaseModel):
    source_url: str = Field(description="URL where the detail was extracted from")
    category: str = Field(description="A short(2-4 word) thematic label derived from this claim's own content. "
                    "Do not use a fixed or predetermined list — the label must fit whatever topic "
                    "is given. Merge near-identical categories into a single shared label.")
    detail: str = Field(description="A short paragraph(3-4 sentences) synthesizing the concrete facts, figures, "
                    "and specifics this source reports, in your own words. Not a one-line summary "
                    "and not a copy of the raw content.")
    conflicts_with: Optional[str] = Field(
        None, description="Description of a contradicting claim, if one exists; null if none"
    )


class AnalystFindings(BaseModel):
    claims: list[Claim]


# ---------- writer_task output ----------

class KeyFinding(BaseModel):
    text: str = Field(...,
                      description="he source's detail paragraph, lightly smoothed for readability")
    source_url: str = Field(...,
                            description="Source URL this finding traces back to")

    category: str = Field(description="Thematic label carried through from the analyst claim  ")

class ResearchReport(BaseModel):
    executive_summary: str
    key_findings: list[KeyFinding]
    sources: list[str]
    future_outlook: str


# ---------- verify_task output ----------

class VerifiedReport(ResearchReport):
    unverified_claims: list[str] = Field(
        default_factory=list,
        description="Key findings whose source_url could not be traced back to the analyst's claims",
    )
