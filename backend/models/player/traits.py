"""Player traits model and definitions."""

from pydantic import BaseModel, Field

class TraitsModel(BaseModel):
    """Model for player traits (80 traits total)."""

    # Virtues (1-20)
    empathy: float = Field(default=50.0, ge=0, le=100)
    integrity: float = Field(default=50.0, ge=0, le=100)
    discipline: float = Field(default=50.0, ge=0, le=100)
    creativity: float = Field(default=50.0, ge=0, le=100)
    resilience: float = Field(default=50.0, ge=0, le=100)
    curiosity: float = Field(default=50.0, ge=0, le=100)
    kindness: float = Field(default=50.0, ge=0, le=100)
    courage: float = Field(default=50.0, ge=0, le=100)
    patience: float = Field(default=50.0, ge=0, le=100)
    adaptability: float = Field(default=50.0, ge=0, le=100)
    wisdom: float = Field(default=50.0, ge=0, le=100)
    humility: float = Field(default=50.0, ge=0, le=100)
    vision: float = Field(default=50.0, ge=0, le=100)
    honesty: float = Field(default=50.0, ge=0, le=100)
    loyalty: float = Field(default=50.0, ge=0, le=100)
    generosity: float = Field(default=50.0, ge=0, le=100)
    self_awareness: float = Field(default=50.0, ge=0, le=100)
    gratitude: float = Field(default=50.0, ge=0, le=100)
    optimism: float = Field(default=50.0, ge=0, le=100)
    loveability: float = Field(default=50.0, ge=0, le=100)

    # Vices (21-40)
    greed: float = Field(default=50.0, ge=0, le=100)
    arrogance: float = Field(default=50.0, ge=0, le=100)
    deceit: float = Field(default=50.0, ge=0, le=100)
    cruelty: float = Field(default=50.0, ge=0, le=100)
    selfishness: float = Field(default=50.0, ge=0, le=100)
    envy: float = Field(default=50.0, ge=0, le=100)
    wrath: float = Field(default=50.0, ge=0, le=100)
    cowardice: float = Field(default=50.0, ge=0, le=100)
    laziness: float = Field(default=50.0, ge=0, le=100)
    gluttony: float = Field(default=50.0, ge=0, le=100)
    paranoia: float = Field(default=50.0, ge=0, le=100)
    impulsiveness: float = Field(default=50.0, ge=0, le=100)
    vengefulness: float = Field(default=50.0, ge=0, le=100)
    manipulation: float = Field(default=50.0, ge=0, le=100)
    prejudice: float = Field(default=50.0, ge=0, le=100)
    betrayal: float = Field(default=50.0, ge=0, le=100)
    stubbornness: float = Field(default=50.0, ge=0, le=100)
    pessimism: float = Field(default=50.0, ge=0, le=100)
    recklessness: float = Field(default=50.0, ge=0, le=100)
    vanity: float = Field(default=50.0, ge=0, le=100)

    # Skills (41-60)
    hacking: float = Field(default=50.0, ge=0, le=100)
    negotiation: float = Field(default=50.0, ge=0, le=100)
    stealth: float = Field(default=50.0, ge=0, le=100)
    leadership: float = Field(default=50.0, ge=0, le=100)
    technical_knowledge: float = Field(default=50.0, ge=0, le=100)
    physical_strength: float = Field(default=50.0, ge=0, le=100)
    speed: float = Field(default=50.0, ge=0, le=100)
    intelligence: float = Field(default=50.0, ge=0, le=100)
    charisma: float = Field(default=50.0, ge=0, le=100)
    perception: float = Field(default=50.0, ge=0, le=100)
    endurance: float = Field(default=50.0, ge=0, le=100)
    dexterity: float = Field(default=50.0, ge=0, le=100)
    memory: float = Field(default=50.0, ge=0, le=100)
    focus: float = Field(default=50.0, ge=0, le=100)
    networking: float = Field(default=50.0, ge=0, le=100)
    strategy: float = Field(default=50.0, ge=0, le=100)
    trading: float = Field(default=50.0, ge=0, le=100)
    engineering: float = Field(default=50.0, ge=0, le=100)
    medicine: float = Field(default=50.0, ge=0, le=100)
    meditation: float = Field(default=50.0, ge=0, le=100)

class MetaTraitsModel(BaseModel):
    """Model for meta traits (61-80)."""

    # Social Meta Traits
    reputation: float = Field(default=50.0, ge=0, le=100)
    influence: float = Field(default=50.0, ge=0, le=100)
    fame: float = Field(default=50.0, ge=0, le=100)
    infamy: float = Field(default=50.0, ge=0, le=100)
    trustworthiness: float = Field(default=50.0, ge=0, le=100)

    # Combat Meta Traits
    combat_rating: float = Field(default=50.0, ge=0, le=100)
    tactical_mastery: float = Field(default=50.0, ge=0, le=100)
    survival_instinct: float = Field(default=50.0, ge=0, le=100)

    # Economic Meta Traits
    business_acumen: float = Field(default=50.0, ge=0, le=100)
    market_intuition: float = Field(default=50.0, ge=0, le=100)
    wealth_management: float = Field(default=50.0, ge=0, le=100)

    # Spiritual Meta Traits
    enlightenment: float = Field(default=50.0, ge=0, le=100)
    karmic_balance: float = Field(default=50.0, ge=0, le=100)
    divine_favor: float = Field(default=50.0, ge=0, le=100)

    # Guild Meta Traits
    guild_loyalty: float = Field(default=50.0, ge=0, le=100)
    political_power: float = Field(default=50.0, ge=0, le=100)
    diplomatic_skill: float = Field(default=50.0, ge=0, le=100)

    # Legacy Meta Traits
    legendary_status: float = Field(default=50.0, ge=0, le=100)
    mentorship: float = Field(default=50.0, ge=0, le=100)
    historical_impact: float = Field(default=50.0, ge=0, le=100)
