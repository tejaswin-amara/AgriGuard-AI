"""Grounded advisory endpoint — wraps a disease or soil result in a
plain-language, source-cited recommendation via RAG.

Status: STUB. Needs the ICAR / state advisory corpus assembled and embedded
first (docs/TECHNICAL-ARCHITECTURE.md Section 2) — there is nothing to
retrieve against yet, so this must not fabricate a "grounded" answer.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/advisory", tags=["advisory"])


class AdvisoryRequestIn(BaseModel):
    source_reading_type: str  # "disease" | "soil"
    source_reading_id: int


@router.post("/generate")
async def generate_advisory(payload: AdvisoryRequestIn) -> dict:
    # TODO(rag): embed + retrieve from the advisory corpus, then call
    # IBM watsonx.ai / Granite (see docs/TECHNICAL-ARCHITECTURE.md
    # Section 4.4 — `ibm-watsonx-ai` is already in requirements.txt) to
    # phrase the grounded result. Granite Guardian's groundedness detector
    # is a real, purpose-built fit for enforcing this project's own rule
    # (see AGENTS.md): never return a recommendation without a real
    # retrieved source attached.
    raise HTTPException(
        status_code=501,
        detail=(
            "Advisory corpus not yet assembled — nothing to ground a "
            "recommendation in. See docs/TECHNICAL-ARCHITECTURE.md Section 2."
        ),
    )
