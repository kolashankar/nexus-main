"""Quest statistics schemas."""

from pydantic import BaseModel

class QuestStatsResponse(BaseModel):
    """Quest statistics response."""
    total: int
    active: int
    completed: int
    failed: int
    abandoned: int
    completion_rate: float

    class Config:
        json_schema_extra = {
            "example": {
                "total": 50,
                "active": 5,
                "completed": 40,
                "failed": 3,
                "abandoned": 2,
                "completion_rate": 85.5
            }
        }
