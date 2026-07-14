"""HITL approval gate before script generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApprovalRequest:
    action: str
    payload: str
    message: str


def request_script_approval(brief: str) -> ApprovalRequest:
    preview = (brief or "").strip()
    if len(preview) > 160:
        preview = preview[:157] + "..."
    return ApprovalRequest(
        action="generate_script",
        payload=brief or "",
        message=(
            "Approve generating a short-form video script from this research brief? "
            f"Preview: {preview or '(empty brief)'}"
        ),
    )


def apply_approval(approved: bool) -> bool:
    return bool(approved)
