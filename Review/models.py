from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    language: str = Field(..., description="Programming language of the submitted code, e.g. 'python', 'javascript'.")
    code: str = Field(..., description="Source code to review.")
    context: Optional[str] = Field(
        default=None,
        description="Optional extra context, e.g. 'this is a REST controller for user management'.",
    )


Verdict = Literal["approve", "approve_with_nits", "request_changes", "no_coverage"]
Severity = Literal["nit", "minor", "major"]


class ReviewIssue(BaseModel):
    id: str = Field(..., description="Stable identifier for this issue within the response.")
    severity: Severity
    description: str
    affected_code: Optional[str] = Field(
        default=None,
        description="Free-text reference to lines, snippets, or identifiers that are affected.",
    )
    rule_ids: List[str] = Field(
        default_factory=list,
        description="List of rule IDs from the standards corpus that justify this issue.",
    )


class PositiveFeedbackItem(BaseModel):
    message: str
    rule_ids: List[str] = Field(
        default_factory=list,
        description="Optional rule IDs that the positive feedback is grounded in.",
    )


class ReviewResponse(BaseModel):
    verdict: Verdict
    summary: str
    positive_feedback: List[PositiveFeedbackItem] = Field(default_factory=list)
    issues: List[ReviewIssue] = Field(default_factory=list)


class StandardsChunk(BaseModel):
    """
    Representation of a single chunked rule from the standards corpus.
    """

    rule_id: str
    scope: str
    doc_name: str
    section_title: str
    text: str

