"""Oracle - The Quest Generator AI"""

from .oracle import Oracle
from .generator import QuestGenerator
from .prompts import ORACLE_SYSTEM, QUEST_GENERATION_TEMPLATE

__all__ = [
    "Oracle",
    "QuestGenerator",
    "ORACLE_SYSTEM",
    "QUEST_GENERATION_TEMPLATE",
]
