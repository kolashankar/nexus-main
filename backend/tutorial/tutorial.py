"""Tutorial manager for guiding new players."""

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class TutorialStatus(str, Enum):
    """Tutorial completion status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TutorialStep:
    """Individual tutorial step."""

    def __init__(
        self,
        step_id: str,
        title: str,
        description: str,
        task_description: str,
        completion_condition: str,
        reward: Dict[str, Any],
        next_step: Optional[str] = None,
        skippable: bool = True
    ):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.task_description = task_description
        self.completion_condition = completion_condition
        self.reward = reward
        self.next_step = next_step
        self.skippable = skippable


class TutorialManager:
    """Manage player tutorial progress."""

    def __init__(self, player_id: str, db_client):
        self.player_id = player_id
        self.db = db_client
        self.tutorial_collection = db_client['tutorial_progress']

    async def start_tutorial(self) -> Dict[str, Any]:
        """Start the tutorial for a new player."""
        tutorial_data = {
            'player_id': self.player_id,
            'status': TutorialStatus.IN_PROGRESS,
            'current_step': 'welcome',
            'completed_steps': [],
            'skipped_steps': [],
            'started_at': datetime.utcnow(),
            'completed_at': None
        }

        await self.tutorial_collection.insert_one(tutorial_data)
        return await self.get_current_step()

    async def get_progress(self) -> Dict[str, Any]:
        """Get player's tutorial progress."""
        progress = await self.tutorial_collection.find_one(
            {'player_id': self.player_id}
        )

        if not progress:
            return {
                'status': TutorialStatus.NOT_STARTED,
                'current_step': None,
                'progress_percent': 0
            }

        total_steps = len(tutorial_steps)
        completed_steps = len(progress.get('completed_steps', []))

        return {
            'status': progress['status'],
            'current_step': progress.get('current_step'),
            'completed_steps': progress.get('completed_steps', []),
            'progress_percent': round((completed_steps / total_steps) * 100, 2)
        }

    async def get_current_step(self) -> Optional[Dict[str, Any]]:
        """Get the current tutorial step."""
        progress = await self.tutorial_collection.find_one(
            {'player_id': self.player_id}
        )

        if not progress or progress['status'] == TutorialStatus.NOT_STARTED:
            return None

        if progress['status'] in [TutorialStatus.COMPLETED, TutorialStatus.SKIPPED]:
            return None

        current_step_id = progress['current_step']
        step = tutorial_steps.get(current_step_id)

        if not step:
            return None

        return {
            'step_id': step.step_id,
            'title': step.title,
            'description': step.description,
            'task': step.task_description,
            'reward': step.reward,
            'skippable': step.skippable
        }

    async def complete_step(self, step_id: str) -> Dict[str, Any]:
        """Mark a tutorial step as completed."""
        progress = await self.tutorial_collection.find_one(
            {'player_id': self.player_id}
        )

        if not progress:
            raise ValueError("Tutorial not started")

        step = tutorial_steps.get(step_id)
        if not step:
            raise ValueError(f"Invalid step: {step_id}")

        # Update progress
        update_data = {
            '$addToSet': {'completed_steps': step_id},
            '$set': {'current_step': step.next_step}
        }

        # If no next step, mark tutorial as completed
        if not step.next_step:
            update_data['$set']['status'] = TutorialStatus.COMPLETED
            update_data['$set']['completed_at'] = datetime.utcnow()

        await self.tutorial_collection.update_one(
            {'player_id': self.player_id},
            update_data
        )

        # Award reward
        await self._award_reward(step.reward)

        return {
            'step_completed': step_id,
            'reward': step.reward,
            'next_step': step.next_step,
            'tutorial_complete': not step.next_step
        }

    async def skip_step(self, step_id: str) -> Dict[str, Any]:
        """Skip a tutorial step."""
        step = tutorial_steps.get(step_id)

        if not step or not step.skippable:
            raise ValueError("Step cannot be skipped")

        await self.tutorial_collection.update_one(
            {'player_id': self.player_id},
            {
                '$addToSet': {'skipped_steps': step_id},
                '$set': {'current_step': step.next_step}
            }
        )

        return {
            'step_skipped': step_id,
            'next_step': step.next_step
        }

    async def skip_tutorial(self) -> Dict[str, Any]:
        """Skip the entire tutorial."""
        await self.tutorial_collection.update_one(
            {'player_id': self.player_id},
            {
                '$set': {
                    'status': TutorialStatus.SKIPPED,
                    'completed_at': datetime.utcnow()
                }
            }
        )

        return {'tutorial_skipped': True}

    async def reset_tutorial(self) -> Dict[str, Any]:
        """Reset tutorial progress."""
        await self.tutorial_collection.delete_one(
            {'player_id': self.player_id}
        )

        return await self.start_tutorial()

    async def _award_reward(self, reward: Dict[str, Any]):
        """Award tutorial step reward to player."""
        players_collection = self.db['players']

        update_data = {}

        if 'credits' in reward:
            update_data['$inc'] = {'currencies.credits': reward['credits']}

        if 'xp' in reward:
            if '$inc' not in update_data:
                update_data['$inc'] = {}
            update_data['$inc']['xp'] = reward['xp']

        if 'items' in reward:
            update_data['$push'] = {'items': {'$each': reward['items']}}

        if update_data:
            await players_collection.update_one(
                {'_id': self.player_id},
                update_data
            )


# Define tutorial steps
tutorial_steps = {
    'welcome': TutorialStep(
        step_id='welcome',
        title='Welcome to Karma Nexus!',
        description='Welcome, Player! You\'ve entered a world where every action shapes your destiny.',
        task_description='Meet your AI Companion to begin your journey',
        completion_condition='talk_to_companion',
        reward={'credits': 500, 'xp': 100},
        next_step='learn_traits',
        skippable=False
    ),
    'learn_traits': TutorialStep(
        step_id='learn_traits',
        title='Understanding Traits',
        description='Your character has 80 dynamic traits that evolve based on your actions.',
        task_description='Open your trait panel and review your starting traits',
        completion_condition='view_traits',
        reward={'credits': 200, 'xp': 50},
        next_step='first_action'
    ),
    'first_action': TutorialStep(
        step_id='first_action',
        title='Take Your First Action',
        description='Actions are the core of gameplay. Choose wisely - each action affects your karma.',
        task_description='Perform a Help action on another player',
        completion_condition='perform_help_action',
        reward={'credits': 500, 'xp': 100},
        next_step='karma_intro'
    ),
    'karma_intro': TutorialStep(
        step_id='karma_intro',
        title='Karma System',
        description='Your karma score reflects your moral choices. It affects everything in the game.',
        task_description='Check your karma score in the dashboard',
        completion_condition='view_karma',
        reward={'credits': 200, 'xp': 50},
        next_step='first_quest'
    ),
    'first_quest': TutorialStep(
        step_id='first_quest',
        title='Your First Quest',
        description='The Oracle AI generates unique quests tailored to your character.',
        task_description='Accept and complete your first daily quest',
        completion_condition='complete_quest',
        reward={'credits': 1000, 'xp': 200},
        next_step='combat_intro'
    ),
    'combat_intro': TutorialStep(
        step_id='combat_intro',
        title='Combat Basics',
        description='Learn the turn-based combat system to defend yourself and challenge others.',
        task_description='Complete the combat training session',
        completion_condition='complete_combat_training',
        reward={'credits': 500, 'xp': 150},
        next_step='guilds_intro'
    ),
    'guilds_intro': TutorialStep(
        step_id='guilds_intro',
        title='Join a Guild',
        description='Guilds provide community, resources, and territory control opportunities.',
        task_description='Browse guilds and consider joining one (optional)',
        completion_condition='visit_guild_hall',
        reward={'credits': 300, 'xp': 100},
        next_step='marketplace_intro'
    ),
    'marketplace_intro': TutorialStep(
        step_id='marketplace_intro',
        title='The Marketplace',
        description='Buy robots, items, and invest in the stock market to grow your wealth.',
        task_description='Visit the marketplace and browse available items',
        completion_condition='visit_marketplace',
        reward={'credits': 500, 'xp': 100},
        next_step='tutorial_complete'
    ),
    'tutorial_complete': TutorialStep(
        step_id='tutorial_complete',
        title='Tutorial Complete!',
        description='You\'ve mastered the basics! Your journey in Karma Nexus truly begins now.',
        task_description='Explore the world and forge your destiny!',
        completion_condition='auto_complete',
        reward={'credits': 2000, 'xp': 500, 'items': ['starter_pack']},
        next_step=None,
        skippable=False
    )
}
