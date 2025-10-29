"""Skill requirement validation service."""

from typing import Dict, Any, List, Tuple

class SkillRequirementValidator:
    """Validates if players meet skill requirements for tasks."""
    
    # Map of trait names to skill categories
    TRAIT_TO_SKILL_MAP = {
        "hacking": ["intelligence", "cunning"],
        "combat": ["strength", "courage", "aggression"],
        "diplomacy": ["charisma", "wisdom", "compassion"],
        "stealth": ["cunning", "patience", "adaptability"],
        "engineering": ["intelligence", "creativity", "patience"],
        "leadership": ["charisma", "wisdom", "courage"],
        "survival": ["resilience", "adaptability", "wisdom"],
        "trading": ["charisma", "greed", "intelligence"],
        "medical": ["compassion", "intelligence", "patience"],
        "magic": ["intelligence", "wisdom", "creativity"]
    }
    
    def validate_skill_requirements(
        self, 
        player_traits: Dict[str, float], 
        skill_requirements: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """Validate if player meets skill requirements.
        
        Returns:
            Tuple of (meets_requirements, list_of_missing_skills)
        """
        if not skill_requirements:
            return True, []
        
        missing_skills = []
        
        for req in skill_requirements:
            skill_name = req.get("skill_name")
            min_level = req.get("min_level", 0)
            
            # Check if player has the skill level
            if not self._has_skill_level(player_traits, skill_name, min_level):
                missing_skills.append(f"{skill_name} (need {min_level})")
        
        return len(missing_skills) == 0, missing_skills
    
    def _has_skill_level(self, player_traits: Dict[str, float], skill_name: str, min_level: int) -> bool:
        """Check if player has required skill level."""
        # Get related traits for this skill
        related_traits = self.TRAIT_TO_SKILL_MAP.get(skill_name.lower(), [skill_name.lower()])
        
        # Calculate skill level as average of related traits
        trait_values = []
        for trait in related_traits:
            if trait in player_traits:
                trait_values.append(player_traits[trait])
        
        if not trait_values:
            return False
        
        avg_skill_level = sum(trait_values) / len(trait_values)
        return avg_skill_level >= min_level
    
    def get_skill_level(self, player_traits: Dict[str, float], skill_name: str) -> float:
        """Get player's effective level in a skill."""
        related_traits = self.TRAIT_TO_SKILL_MAP.get(skill_name.lower(), [skill_name.lower()])
        
        trait_values = []
        for trait in related_traits:
            if trait in player_traits:
                trait_values.append(player_traits[trait])
        
        if not trait_values:
            return 0.0
        
        return sum(trait_values) / len(trait_values)
    
    def get_recommended_tasks_for_skills(
        self,
        player_traits: Dict[str, float],
        available_tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter tasks to those the player can currently attempt."""
        recommended = []
        
        for task in available_tasks:
            skill_reqs = task.get("skill_requirements", [])
            meets_requirements, _ = self.validate_skill_requirements(player_traits, skill_reqs)
            
            if meets_requirements:
                recommended.append(task)
        
        return recommended
    
    def calculate_task_difficulty_adjustment(
        self,
        player_traits: Dict[str, float],
        skill_requirements: List[Dict[str, Any]]
    ) -> float:
        """Calculate how much easier/harder a task is based on player skills.
        
        Returns a multiplier (0.5 = 50% easier, 2.0 = 200% harder).
        """
        if not skill_requirements:
            return 1.0
        
        total_adjustment = 0.0
        
        for req in skill_requirements:
            skill_name = req.get("skill_name")
            min_level = req.get("min_level", 0)
            
            player_skill = self.get_skill_level(player_traits, skill_name)
            difference = player_skill - min_level
            
            # Each 10 points above requirement makes task 10% easier
            # Each 10 points below makes it 15% harder
            if difference > 0:
                total_adjustment -= (difference / 10) * 0.1
            else:
                total_adjustment += (abs(difference) / 10) * 0.15
        
        # Average the adjustments
        avg_adjustment = total_adjustment / len(skill_requirements)
        multiplier = 1.0 + avg_adjustment
        
        # Clamp between 0.3 and 3.0
        return max(0.3, min(3.0, multiplier))
    
    def suggest_skill_improvements(
        self,
        player_traits: Dict[str, float],
        failed_task_requirements: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Suggest which skills the player should improve."""
        suggestions = []
        
        for req in failed_task_requirements:
            skill_name = req.get("skill_name")
            min_level = req.get("min_level", 0)
            current_level = self.get_skill_level(player_traits, skill_name)
            
            if current_level < min_level:
                related_traits = self.TRAIT_TO_SKILL_MAP.get(skill_name.lower(), [skill_name.lower()])
                suggestions.append({
                    "skill": skill_name,
                    "current_level": round(current_level, 1),
                    "required_level": min_level,
                    "gap": round(min_level - current_level, 1),
                    "improve_traits": related_traits
                })
        
        # Sort by gap (largest first)
        suggestions.sort(key=lambda x: x["gap"], reverse=True)
        
        return suggestions
