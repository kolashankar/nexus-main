from pydantic import BaseModel, Field
from typing import Dict, List

class TraitAllocateRequest(BaseModel):
    """Request to allocate trait points."""
    trait_name: str = Field(..., min_length=1)
    points: int = Field(..., ge=1, le=10)

class TraitsResponse(BaseModel):
    """All traits response."""
    traits: Dict[str, float]
    meta_traits: Dict[str, float]
    total_traits: int = 80

class TraitDetailsResponse(BaseModel):
    """Detailed trait information."""
    trait_name: str
    current_value: float
    category: str  # virtue, vice, skill, or meta
    description: str
    affects: List[str] = Field(default_factory=list)

class TraitCategory(BaseModel):
    """Trait category grouping."""
    virtues: Dict[str, float]
    vices: Dict[str, float]
    skills: Dict[str, float]
    meta: Dict[str, float]