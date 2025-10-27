from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Territory(BaseModel):
    territory_id: int  # 1-20
    name: str
    description: str

    # Control
    controlling_guild_id: Optional[str] = None
    controlled_since: Optional[datetime] = None
    contested: bool = False

    # Benefits
    passive_income: int = 100  # Credits per day
    resource_bonus: dict = Field(default_factory=dict)

    # Defense
    defense_level: int = 1
    last_attacked: Optional[datetime] = None

    # Location
    x: float = 0.0
    y: float = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "territory_id": 1,
                "name": "Central Plaza",
                "description": "The heart of the city",
                "passive_income": 200,
                "defense_level": 3
            }
        }


# Territory definitions
TERRITORIES = [
    {"territory_id": 1, "name": "Central Plaza",
        "description": "Heart of the city", "passive_income": 200, "x": 0, "y": 0},
    {"territory_id": 2, "name": "Tech District",
        "description": "Technology hub", "passive_income": 180, "x": 100, "y": 50},
    {"territory_id": 3, "name": "Market Square", "description": "Trade center",
        "passive_income": 220, "x": -50, "y": 100},
    {"territory_id": 4, "name": "Industrial Zone",
        "description": "Manufacturing area", "passive_income": 150, "x": 150, "y": -50},
    {"territory_id": 5, "name": "Residential Area",
        "description": "Housing district", "passive_income": 120, "x": -100, "y": -100},
    {"territory_id": 6, "name": "Financial District",
        "description": "Banking center", "passive_income": 250, "x": 50, "y": 150},
    {"territory_id": 7, "name": "Entertainment Zone",
        "description": "Leisure district", "passive_income": 160, "x": -150, "y": 50},
    {"territory_id": 8, "name": "Research Lab", "description": "Science facility",
        "passive_income": 190, "x": 80, "y": -120},
    {"territory_id": 9, "name": "Hacker Haven", "description": "Underground network",
        "passive_income": 170, "x": -80, "y": 80},
    {"territory_id": 10, "name": "Corporate Tower",
        "description": "Business HQ", "passive_income": 230, "x": 120, "y": 100},
    {"territory_id": 11, "name": "Data Center", "description": "Information hub",
        "passive_income": 200, "x": -120, "y": -50},
    {"territory_id": 12, "name": "Security Outpost",
        "description": "Defense station", "passive_income": 140, "x": 0, "y": -150},
    {"territory_id": 13, "name": "Medical District",
        "description": "Healthcare zone", "passive_income": 180, "x": 150, "y": 50},
    {"territory_id": 14, "name": "Transportation Hub",
        "description": "Transit center", "passive_income": 160, "x": -50, "y": -120},
    {"territory_id": 15, "name": "Education Quarter",
        "description": "Learning center", "passive_income": 150, "x": 70, "y": 120},
    {"territory_id": 16, "name": "Energy Plant", "description": "Power facility",
        "passive_income": 210, "x": -100, "y": 150},
    {"territory_id": 17, "name": "Communication Array",
        "description": "Network station", "passive_income": 190, "x": 100, "y": -100},
    {"territory_id": 18, "name": "Robot Factory", "description": "Manufacturing plant",
        "passive_income": 200, "x": -150, "y": -80},
    {"territory_id": 19, "name": "Black Market", "description": "Underground trade",
        "passive_income": 240, "x": 130, "y": -150},
    {"territory_id": 20, "name": "Admin Center",
        "description": "Government building", "passive_income": 260, "x": 0, "y": 130},
]
