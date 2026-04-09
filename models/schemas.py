from pydantic import BaseModel
from typing import List, Optional, Literal


class Observation(BaseModel):
    claim_id: str
    procedure: str
    submitted_code: str
    denial_reasons: List[str]
    documents: List[str]
    status: str


class Action(BaseModel):
    action_type: Literal[
        "fix_code",
        "add_document",
        "validate_policy",
        "resubmit",
        "appeal"
    ]
    value: Optional[str] = None


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict