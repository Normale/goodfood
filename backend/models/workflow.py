"""Simplified workflow models."""

from typing import Any, List, Optional
from typing_extensions import TypedDict

from pydantic import BaseModel

from models.nutrition import NutritionRecord


class WorkflowState(TypedDict, total=False):
    """LangGraph workflow state."""

    ingredients: List[str]
    iteration: int
    max_iterations: int
    consensus_reached: bool
    final_result: Optional[dict]


class WorkflowResult(BaseModel):
    """Workflow result."""

    success: bool
    nutrition_record: Optional[NutritionRecord] = None
    error_message: Optional[str] = None
