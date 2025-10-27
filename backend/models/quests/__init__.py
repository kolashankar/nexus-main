"""Quest models package."""

from .quest import (
    Quest,
    QuestType,
    QuestStatus,
    QuestDifficulty,
    QuestObjective,
    QuestRewards
)
from .objective import ObjectiveType
from .campaign import Campaign, CampaignProgress, CampaignType, CampaignChoice, CampaignChapter

__all__ = [
    'Quest',
    'QuestType',
    'QuestStatus',
    'QuestDifficulty',
    'QuestObjective',
    'QuestRewards',
    'ObjectiveType',
    'Campaign',
    'CampaignProgress',
    'CampaignType',
    'CampaignChoice',
    'CampaignChapter',
    'campaign'
]

# Provide module alias for backward compatibility
import sys
from . import campaign as campaign_module
sys.modules[__name__ + '.campaign'] = campaign_module
campaign = campaign_module
