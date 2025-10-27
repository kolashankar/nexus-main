from typing import Dict
from backend.models.player.skill_trees import (
    PlayerSkillTrees, SkillTree, SkillNode
)
import logging

logger = logging.getLogger(__name__)

# All 80 traits (60 base + 20 meta)
ALL_TRAITS = [
    # Virtues (1-20)
    "empathy", "integrity", "discipline", "creativity", "resilience",
    "curiosity", "kindness", "courage", "patience", "adaptability",
    "wisdom", "humility", "vision", "honesty", "loyalty",
    "generosity", "self_awareness", "gratitude", "optimism", "loveability",
    # Vices (21-40)
    "greed", "arrogance", "deceit", "cruelty", "selfishness",
    "envy", "wrath", "cowardice", "laziness", "gluttony",
    "paranoia", "impulsiveness", "vengefulness", "manipulation", "prejudice",
    "betrayal", "stubbornness", "pessimism", "recklessness", "vanity",
    # Skills (41-60)
    "hacking", "negotiation", "stealth", "leadership", "technical_knowledge",
    "physical_strength", "speed", "intelligence", "charisma", "perception",
    "endurance", "dexterity", "memory", "focus", "networking",
    "strategy", "trading", "engineering", "medicine", "meditation",
    # Meta Traits (61-80)
    "reputation", "influence", "fame", "infamy", "trustworthiness",
    "combat_rating", "tactical_mastery", "survival_instinct", "business_acumen", "market_intuition",
    "wealth_management", "enlightenment", "karmic_balance", "divine_favor", "guild_loyalty",
    "political_power", "diplomatic_skill", "legendary_status", "mentorship", "historical_impact"
]

class SkillTreeService:
    """Service for managing player skill trees"""

    @staticmethod
    def initialize_skill_trees(player_id: str) -> PlayerSkillTrees:
        """Initialize all 80 skill trees for a new player"""
        skill_trees = {}

        for trait in ALL_TRAITS:
            # Create 20 nodes for each trait
            nodes = [SkillNode(node_id=i) for i in range(1, 21)]

            skill_tree = SkillTree(
                trait_name=trait,
                nodes=nodes
            )
            skill_trees[trait] = skill_tree

        return PlayerSkillTrees(
            player_id=player_id,
            skill_trees=skill_trees,
            available_points=3  # Starting points
        )

    @staticmethod
    def unlock_node(
        player_skill_trees: PlayerSkillTrees,
        trait_name: str,
        node_id: int
    ) -> tuple[bool, str]:
        """Unlock a skill node"""
        if trait_name not in ALL_TRAITS:
            return False, f"Invalid trait: {trait_name}"

        if player_skill_trees.available_points <= 0:
            return False, "No skill points available"

        if trait_name not in player_skill_trees.skill_trees:
            return False, f"Skill tree not found for trait: {trait_name}"

        skill_tree = player_skill_trees.skill_trees[trait_name]

        # Check if previous nodes are unlocked (sequential unlock)
        if node_id > 1:
            previous_node = next(
                (n for n in skill_tree.nodes if n.node_id == node_id - 1), None)
            if not previous_node or not previous_node.unlocked:
                return False, "Must unlock previous nodes first"

        success = player_skill_trees.spend_skill_point(trait_name, node_id)
        if success:
            # Check for milestones (every 5 nodes)
            if node_id % 5 == 0 and node_id not in skill_tree.milestones_reached:
                skill_tree.milestones_reached.append(node_id)

            return True, "Node unlocked successfully"

        return False, "Failed to unlock node"

    @staticmethod
    def choose_branch(
        player_skill_trees: PlayerSkillTrees,
        trait_name: str,
        branch: str
    ) -> tuple[bool, str]:
        """Choose a branch path (A or B) at node 10"""
        if trait_name not in player_skill_trees.skill_trees:
            return False, "Skill tree not found"

        skill_tree = player_skill_trees.skill_trees[trait_name]

        # Check if player has reached node 10 (branching point)
        node_10 = next((n for n in skill_tree.nodes if n.node_id == 10), None)
        if not node_10 or not node_10.unlocked:
            return False, "Must unlock node 10 to choose branch"

        success = skill_tree.choose_branch(branch)
        if success:
            return True, f"Branch {branch} selected"

        return False, "Branch already chosen or invalid"

    @staticmethod
    def calculate_synergy_bonuses(
        player_skill_trees: PlayerSkillTrees,
        player_traits: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate synergy bonuses between related skill trees"""
        bonuses = {}

        # Define synergies (example pairs)
        synergies = [
            (["hacking", "technical_knowledge"], "cyber_mastery", 0.15),
            (["leadership", "charisma"], "commanding_presence", 0.10),
            (["empathy", "kindness"], "compassion", 0.12),
            (["strategy", "intelligence"], "tactical_genius", 0.15),
            (["stealth", "speed"], "shadow_movement", 0.10),
        ]

        for traits_pair, bonus_name, bonus_value in synergies:
            # Check if both traits have investment
            if all(trait in player_skill_trees.skill_trees and
                   player_skill_trees.skill_trees[trait].total_points_invested >= 10
                   for trait in traits_pair):
                bonuses[bonus_name] = bonus_value

        return bonuses

    @staticmethod
    def get_skill_tree_summary(player_skill_trees: PlayerSkillTrees) -> Dict:
        """Get summary of all skill trees"""
        summary = {
            "total_points": player_skill_trees.total_skill_points,
            "spent_points": player_skill_trees.total_points_spent,
            "available_points": player_skill_trees.available_points,
            "trees_with_investment": 0,
            "total_milestones": 0,
            "branches_chosen": 0
        }

        for tree in player_skill_trees.skill_trees.values():
            if tree.total_points_invested > 0:
                summary["trees_with_investment"] += 1
            summary["total_milestones"] += len(tree.milestones_reached)
            if tree.active_branch:
                summary["branches_chosen"] += 1

        return summary
