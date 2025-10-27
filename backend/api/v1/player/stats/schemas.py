"""Player stats schemas."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TraitAnalysis(BaseModel):
    """Trait analysis response."""

    moral_alignment: Dict[str,
        Any] = Field(..., description='Moral alignment data')
    balance: Dict[str, float] = Field(..., description='Trait balance metrics')
    dominant_traits: List[Dict[str, Any]
        ] = Field(..., description='Top traits')
    weakest_traits: List[Dict[str, Any]
        ] = Field(..., description='Weakest traits')
    improvement_suggestions: List[Dict[str, Any]
        ] = Field(..., description='Improvement suggestions')
    active_synergies: List[Dict[str, Any]
        ] = Field(..., description='Active trait synergies')

    class Config:
        json_schema_extra = {
            'example': {
                'moral_alignment': {
                    'class': 'good',
                    'score': 25
                },
                'balance': {
                    'balance_score': 75.5,
                    'spread': 60,
                    'specialization': 3
                },
                'dominant_traits': [
                    {'trait': 'hacking', 'value': 85},
                    {'trait': 'intelligence', 'value': 80}
                ],
                'weakest_traits': [
                    {'trait': 'physical_strength', 'value': 25}
                ],
                'improvement_suggestions': [
                    {
                        'trait': 'physical_strength',
                        'current_value': 25,
                        'suggested_target': 50,
                        'priority': 'high'
                    }
                ],
                'active_synergies': [
                    {
                        'name': 'Master Hacker',
                        'traits': ['hacking', 'technical_knowledge', 'intelligence'],
                        'bonus': 'Hacking actions 25% more effective'
                    }
                ]
            }
        }


class CategoryTraits(BaseModel):
    """Traits by category response."""

    category: str = Field(..., description='Category name')
    traits: Dict[str, int] = Field(..., description='Trait values')
    average: float = Field(..., description='Average value')
    count: int = Field(..., description='Number of traits')

    class Config:
        json_schema_extra = {
            'example': {
                'category': 'virtues',
                'traits': {
                    'empathy': 75,
                    'integrity': 70,
                    'courage': 65
                },
                'average': 70.0,
                'count': 20
            }
        }
