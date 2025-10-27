from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class AppearanceCustomization(BaseModel):
    """Player appearance customization."""
    # Base model
    model: str = Field(default="base_male")  # base_male, base_female

    # Physical features
    skin_tone: str = Field(default="fair")
    hair_style: str = Field(default="short_001")
    hair_color: str = Field(default="#2C1810")  # Hex color

    # Face features
    face_features: Dict[str, Any] = Field(default_factory=dict)

    # Body type
    body_type: Dict[str, float] = Field(default_factory=lambda: {
        "height": 1.0,
        "build": 1.0,
        "proportions": 1.0
    })

    # Customizations
    tattoos: List[str] = Field(default_factory=list)
    scars: List[str] = Field(default_factory=list)
    augmentations: List[str] = Field(default_factory=list)

class CosmeticItems(BaseModel):
    """Cosmetic items owned/equipped."""
    outfits: List[str] = Field(default_factory=list)
    owned_outfits: List[str] = Field(default_factory=list)
    equipped_outfit: Optional[str] = "default"

    emotes: List[str] = Field(default_factory=list)
    victory_poses: List[str] = Field(default_factory=list)
    pets: List[str] = Field(default_factory=list)

# Alias for backward compatibility
PlayerAppearance = AppearanceCustomization