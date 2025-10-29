"""Difficulty scaling service for tasks."""

from typing import Dict, Any, List
from backend.models.tasks.task_types import TaskDifficulty

class DifficultyScaler:
    """Scales task difficulty based on player progression."""
    
    # Level ranges for each difficulty
    DIFFICULTY_LEVEL_RANGES = {
        TaskDifficulty.TUTORIAL: (1, 2),
        TaskDifficulty.EASY: (1, 5),
        TaskDifficulty.MEDIUM: (5, 15),
        TaskDifficulty.HARD: (10, 25),
        TaskDifficulty.EXPERT: (20, 40),
        TaskDifficulty.LEGENDARY: (35, 100)
    }
    
    # Reward multipliers by difficulty
    REWARD_MULTIPLIERS = {
        TaskDifficulty.TUTORIAL: 0.5,
        TaskDifficulty.EASY: 1.0,
        TaskDifficulty.MEDIUM: 1.8,
        TaskDifficulty.HARD: 3.0,
        TaskDifficulty.EXPERT: 5.0,
        TaskDifficulty.LEGENDARY: 8.0
    }
    
    def get_appropriate_difficulties(self, player_level: int) -> List[TaskDifficulty]:
        """Get list of appropriate difficulties for player level."""
        appropriate = []
        
        for difficulty, (min_level, max_level) in self.DIFFICULTY_LEVEL_RANGES.items():
            if min_level <= player_level <= max_level:
                appropriate.append(difficulty)
            elif player_level > max_level and difficulty != TaskDifficulty.TUTORIAL:
                # Still allow lower difficulties for variety
                appropriate.append(difficulty)
        
        return appropriate if appropriate else [TaskDifficulty.EASY]
    
    def is_difficulty_appropriate(self, player_level: int, difficulty: str) -> bool:
        """Check if a difficulty is appropriate for player level."""
        try:
            diff_enum = TaskDifficulty(difficulty)
            min_level, max_level = self.DIFFICULTY_LEVEL_RANGES.get(diff_enum, (1, 100))
            return min_level <= player_level
        except ValueError:
            return True  # Unknown difficulty, allow it
    
    def scale_rewards(self, base_xp: int, base_credits: int, difficulty: str) -> Dict[str, int]:
        """Scale rewards based on difficulty."""
        try:
            diff_enum = TaskDifficulty(difficulty)
            multiplier = self.REWARD_MULTIPLIERS.get(diff_enum, 1.0)
        except ValueError:
            multiplier = 1.0
        
        return {
            "xp": int(base_xp * multiplier),
            "credits": int(base_credits * multiplier)
        }
    
    def get_difficulty_progression(self, player_level: int, tasks_completed: int) -> TaskDifficulty:
        """Get recommended difficulty based on player progression."""
        # Progressive difficulty based on tasks completed
        if tasks_completed < 5:
            return TaskDifficulty.EASY
        elif tasks_completed < 15:
            return TaskDifficulty.MEDIUM if player_level >= 5 else TaskDifficulty.EASY
        elif tasks_completed < 30:
            return TaskDifficulty.HARD if player_level >= 10 else TaskDifficulty.MEDIUM
        elif tasks_completed < 50:
            return TaskDifficulty.EXPERT if player_level >= 20 else TaskDifficulty.HARD
        else:
            return TaskDifficulty.LEGENDARY if player_level >= 35 else TaskDifficulty.EXPERT
    
    def calculate_difficulty_score(self, task_data: Dict[str, Any]) -> int:
        """Calculate a numerical difficulty score for a task."""
        score = 0
        
        # Base difficulty
        difficulty_scores = {
            "tutorial": 1,
            "easy": 10,
            "medium": 25,
            "hard": 50,
            "expert": 80,
            "legendary": 100
        }
        score += difficulty_scores.get(task_data.get("difficulty", "easy"), 10)
        
        # Skill requirements add difficulty
        skill_reqs = task_data.get("skill_requirements", [])
        score += len(skill_reqs) * 5
        
        # Level requirement
        min_level = task_data.get("min_level", 1)
        score += min_level
        
        # Multiplayer tasks are harder
        if task_data.get("is_multiplayer", False):
            score += 15
        
        # Location requirements add complexity
        if task_data.get("location_requirement"):
            score += 10
        
        return score
    
    def suggest_difficulty(self, player_data: Dict[str, Any]) -> str:
        """Suggest appropriate difficulty for a player."""
        player_level = player_data.get("level", 1)
        tasks_completed = player_data.get("stats", {}).get("quests_completed", 0)
        
        # Get base recommendation
        recommended = self.get_difficulty_progression(player_level, tasks_completed)
        
        # Adjust based on player traits
        courage = player_data.get("traits", {}).get("courage", 50)
        wisdom = player_data.get("traits", {}).get("wisdom", 50)
        
        # High courage players can handle harder tasks
        if courage > 70 and wisdom > 60:
            difficulty_order = [d for d in TaskDifficulty]
            current_index = difficulty_order.index(recommended)
            if current_index < len(difficulty_order) - 1:
                recommended = difficulty_order[current_index + 1]
        
        return recommended.value
