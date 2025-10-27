"""Skill Tree Node Configurations for all 80 Traits.

Each trait has 20 nodes with branching paths at nodes 10-15.
"""

from typing import Dict, List, Any

# Node structure:
# - node_id: 1-20
# - trait_name: string
# - level_required: minimum trait level
# - bonus_type: stat/ability/passive
# - bonus_value: effect value
# - branch: None, 'A', or 'B' (branches at node 10)

def get_all_skill_trees() -> Dict[str, List[Dict[str, Any]]]:
    """Get all skill tree configurations for 80 traits."""
    trees = {}

    # VIRTUES (20 traits)
    trees['empathy'] = generate_empathy_tree()
    trees['integrity'] = generate_integrity_tree()
    trees['discipline'] = generate_discipline_tree()
    trees['creativity'] = generate_creativity_tree()
    trees['resilience'] = generate_resilience_tree()
    trees['curiosity'] = generate_curiosity_tree()
    trees['kindness'] = generate_kindness_tree()
    trees['courage'] = generate_courage_tree()
    trees['patience'] = generate_patience_tree()
    trees['adaptability'] = generate_adaptability_tree()
    trees['wisdom'] = generate_wisdom_tree()
    trees['humility'] = generate_humility_tree()
    trees['vision'] = generate_vision_tree()
    trees['honesty'] = generate_honesty_tree()
    trees['loyalty'] = generate_loyalty_tree()
    trees['generosity'] = generate_generosity_tree()
    trees['self_awareness'] = generate_self_awareness_tree()
    trees['gratitude'] = generate_gratitude_tree()
    trees['optimism'] = generate_optimism_tree()
    trees['loveability'] = generate_loveability_tree()

    # VICES (20 traits)
    trees['greed'] = generate_greed_tree()
    trees['arrogance'] = generate_arrogance_tree()
    trees['deceit'] = generate_deceit_tree()
    trees['cruelty'] = generate_cruelty_tree()
    trees['selfishness'] = generate_selfishness_tree()
    trees['envy'] = generate_envy_tree()
    trees['wrath'] = generate_wrath_tree()
    trees['cowardice'] = generate_cowardice_tree()
    trees['laziness'] = generate_laziness_tree()
    trees['gluttony'] = generate_gluttony_tree()
    trees['paranoia'] = generate_paranoia_tree()
    trees['impulsiveness'] = generate_impulsiveness_tree()
    trees['vengefulness'] = generate_vengefulness_tree()
    trees['manipulation'] = generate_manipulation_tree()
    trees['prejudice'] = generate_prejudice_tree()
    trees['betrayal'] = generate_betrayal_tree()
    trees['stubbornness'] = generate_stubbornness_tree()
    trees['pessimism'] = generate_pessimism_tree()
    trees['recklessness'] = generate_recklessness_tree()
    trees['vanity'] = generate_vanity_tree()

    # SKILLS (20 traits)
    trees['hacking'] = generate_hacking_tree()
    trees['negotiation'] = generate_negotiation_tree()
    trees['stealth'] = generate_stealth_tree()
    trees['leadership'] = generate_leadership_tree()
    trees['technical_knowledge'] = generate_technical_knowledge_tree()
    trees['physical_strength'] = generate_physical_strength_tree()
    trees['speed'] = generate_speed_tree()
    trees['intelligence'] = generate_intelligence_tree()
    trees['charisma'] = generate_charisma_tree()
    trees['perception'] = generate_perception_tree()
    trees['endurance'] = generate_endurance_tree()
    trees['dexterity'] = generate_dexterity_tree()
    trees['memory'] = generate_memory_tree()
    trees['focus'] = generate_focus_tree()
    trees['networking'] = generate_networking_tree()
    trees['strategy'] = generate_strategy_tree()
    trees['trading'] = generate_trading_tree()
    trees['engineering'] = generate_engineering_tree()
    trees['medicine'] = generate_medicine_tree()
    trees['meditation'] = generate_meditation_tree()

    # META TRAITS (20 traits)
    trees['reputation'] = generate_reputation_tree()
    trees['influence'] = generate_influence_tree()
    trees['fame'] = generate_fame_tree()
    trees['infamy'] = generate_infamy_tree()
    trees['trustworthiness'] = generate_trustworthiness_tree()
    trees['combat_rating'] = generate_combat_rating_tree()
    trees['tactical_mastery'] = generate_tactical_mastery_tree()
    trees['survival_instinct'] = generate_survival_instinct_tree()
    trees['business_acumen'] = generate_business_acumen_tree()
    trees['market_intuition'] = generate_market_intuition_tree()
    trees['wealth_management'] = generate_wealth_management_tree()
    trees['enlightenment'] = generate_enlightenment_tree()
    trees['karmic_balance'] = generate_karmic_balance_tree()
    trees['divine_favor'] = generate_divine_favor_tree()
    trees['guild_loyalty'] = generate_guild_loyalty_tree()
    trees['political_power'] = generate_political_power_tree()
    trees['diplomatic_skill'] = generate_diplomatic_skill_tree()
    trees['legendary_status'] = generate_legendary_status_tree()
    trees['mentorship'] = generate_mentorship_tree()
    trees['historical_impact'] = generate_historical_impact_tree()

    return trees

def generate_empathy_tree() -> List[Dict[str, Any]]:
    """Generate skill tree for Empathy trait."""
    return [
        # Nodes 1-9: Linear progression
        {"node_id": 1, "level_required": 5, "bonus_type": "stat",
            "bonus_value": {"empathy": 2}, "branch": None},
        {"node_id": 2, "level_required": 10, "bonus_type": "stat",
            "bonus_value": {"empathy": 3}, "branch": None},
        {"node_id": 3, "level_required": 15, "bonus_type": "passive", "bonus_value": {
            "description": "Sense nearby player emotions", "range": 50}, "branch": None},
        {"node_id": 4, "level_required": 20, "bonus_type": "stat",
            "bonus_value": {"empathy": 4, "kindness": 2}, "branch": None},
        {"node_id": 5, "level_required": 25, "bonus_type": "ability", "bonus_value": {
            "name": "Emotion Reading", "cooldown": 60}, "branch": None},
        {"node_id": 6, "level_required": 30, "bonus_type": "stat",
            "bonus_value": {"empathy": 5}, "branch": None},
        {"node_id": 7, "level_required": 35, "bonus_type": "passive", "bonus_value": {
            "description": "+10% healing to others", "value": 0.1}, "branch": None},
        {"node_id": 8, "level_required": 40, "bonus_type": "stat",
            "bonus_value": {"empathy": 6, "loveability": 3}, "branch": None},
        {"node_id": 9, "level_required": 45, "bonus_type": "passive", "bonus_value": {
            "description": "Reduce conflict damage by 15%", "value": 0.15}, "branch": None},

        # Node 10: Branching point
        # Branch A: Healer path (boost kindness)
        {"node_id": 10, "level_required": 50, "bonus_type": "ability", "bonus_value": {
            "name": "Empathic Healing", "heals": 50}, "branch": "A"},
        {"node_id": 11, "level_required": 55, "bonus_type": "stat",
            "bonus_value": {"kindness": 5, "medicine": 3}, "branch": "A"},
        {"node_id": 12, "level_required": 60, "bonus_type": "passive", "bonus_value": {
            "description": "+25% healing effectiveness", "value": 0.25}, "branch": "A"},
        {"node_id": 13, "level_required": 65, "bonus_type": "ability",
            "bonus_value": {"name": "Group Heal", "radius": 30}, "branch": "A"},
        {"node_id": 14, "level_required": 70, "bonus_type": "stat",
            "bonus_value": {"empathy": 8, "kindness": 8}, "branch": "A"},
        {"node_id": 15, "level_required": 75, "bonus_type": "passive", "bonus_value": {
            "description": "Healing also removes debuffs", "value": 1}, "branch": "A"},

        # Branch B: Manipulator path (boost deceit)
        {"node_id": 10, "level_required": 50, "bonus_type": "ability", "bonus_value": {
            "name": "Emotional Manipulation", "duration": 30}, "branch": "B"},
        {"node_id": 11, "level_required": 55, "bonus_type": "stat",
            "bonus_value": {"manipulation": 5, "charisma": 3}, "branch": "B"},
        {"node_id": 12, "level_required": 60, "bonus_type": "passive", "bonus_value": {
            "description": "+20% persuasion success", "value": 0.2}, "branch": "B"},
        {"node_id": 13, "level_required": 65, "bonus_type": "ability", "bonus_value": {
            "name": "Fear Projection", "stun_duration": 3}, "branch": "B"},
        {"node_id": 14, "level_required": 70, "bonus_type": "stat",
            "bonus_value": {"empathy": 8, "manipulation": 8}, "branch": "B"},
        {"node_id": 15, "level_required": 75, "bonus_type": "passive", "bonus_value": {
            "description": "Control weak-willed NPCs", "value": 1}, "branch": "B"},

        # Nodes 16-20: Convergence (available after either branch)
        {"node_id": 16, "level_required": 80, "bonus_type": "stat",
            "bonus_value": {"empathy": 10}, "branch": None},
        {"node_id": 17, "level_required": 85, "bonus_type": "passive", "bonus_value": {
            "description": "Read hidden traits of others", "value": 1}, "branch": None},
        {"node_id": 18, "level_required": 90, "bonus_type": "ability", "bonus_value": {
            "name": "Empathic Link", "shares_buffs": True}, "branch": None},
        {"node_id": 19, "level_required": 95, "bonus_type": "stat",
            "bonus_value": {"empathy": 15, "loveability": 10}, "branch": None},
        {"node_id": 20, "level_required": 100, "bonus_type": "passive", "bonus_value": {
            "description": "MASTERY: Feel all players' emotions in area", "radius": 100}, "branch": None}
    ]

# For brevity, I'll create template functions for other traits
# In production, each would have unique bonuses and branches

def generate_standard_tree(trait_name: str, primary_bonus: str, secondary_bonus: str = None) -> List[Dict[str, Any]]:
    """Generate a standard skill tree template."""
    tree = []
    for i in range(1, 21):
        level_req = i * 5

        if i < 10:  # Linear progression
            tree.append({
                "node_id": i,
                "level_required": level_req,
                "bonus_type": "stat" if i % 2 == 1 else "passive",
                "bonus_value": {trait_name: i} if i % 2 == 1 else {"description": f"{trait_name.title()} bonus {i}", "value": i * 0.02},
                "branch": None
            })
        elif i <= 15:  # Branching
            # Branch A
            tree.append({
                "node_id": i,
                "level_required": level_req,
                "bonus_type": "stat",
                "bonus_value": {trait_name: i * 2, primary_bonus: i},
                "branch": "A"
            })
            # Branch B
            if secondary_bonus:
                tree.append({
                    "node_id": i,
                    "level_required": level_req,
                    "bonus_type": "stat",
                    "bonus_value": {trait_name: i * 2, secondary_bonus: i},
                    "branch": "B"
                })
        else:  # Convergence
            tree.append({
                "node_id": i,
                "level_required": level_req,
                "bonus_type": "ability" if i == 20 else "stat",
                "bonus_value": {trait_name: i * 3} if i < 20 else {"name": f"{trait_name.title()} Mastery", "ultimate": True},
                "branch": None
            })

    return tree

# Generate trees for all other traits using template
def generate_integrity_tree(): return generate_standard_tree(
    "integrity", "honesty", "loyalty")
def generate_discipline_tree(): return generate_standard_tree(
    "discipline", "focus", "patience")
def generate_creativity_tree(): return generate_standard_tree(
    "creativity", "intelligence", "vision")
def generate_resilience_tree(): return generate_standard_tree(
    "resilience", "endurance", "courage")
def generate_curiosity_tree(): return generate_standard_tree(
    "curiosity", "perception", "intelligence")
def generate_kindness_tree(): return generate_standard_tree(
    "kindness", "empathy", "generosity")
def generate_courage_tree(): return generate_standard_tree(
    "courage", "physical_strength", "resilience")
def generate_patience_tree(): return generate_standard_tree(
    "patience", "discipline", "wisdom")
def generate_adaptability_tree(): return generate_standard_tree(
    "adaptability", "intelligence", "perception")
def generate_wisdom_tree(): return generate_standard_tree(
    "wisdom", "intelligence", "patience")
def generate_humility_tree(): return generate_standard_tree(
    "humility", "self_awareness", "gratitude")
def generate_vision_tree(): return generate_standard_tree(
    "vision", "wisdom", "strategy")
def generate_honesty_tree(): return generate_standard_tree(
    "honesty", "integrity", "trustworthiness")
def generate_loyalty_tree(): return generate_standard_tree(
    "loyalty", "integrity", "guild_loyalty")
def generate_generosity_tree(): return generate_standard_tree(
    "generosity", "kindness", "wealth_management")
def generate_self_awareness_tree(): return generate_standard_tree(
    "self_awareness", "wisdom", "intelligence")
def generate_gratitude_tree(): return generate_standard_tree(
    "gratitude", "humility", "loveability")
def generate_optimism_tree(): return generate_standard_tree(
    "optimism", "resilience", "vision")
def generate_loveability_tree(): return generate_standard_tree(
    "loveability", "empathy", "charisma")

# Vices
def generate_greed_tree(): return generate_standard_tree(
    "greed", "trading", "business_acumen")
def generate_arrogance_tree(): return generate_standard_tree(
    "arrogance", "charisma", "vanity")
def generate_deceit_tree(): return generate_standard_tree(
    "deceit", "manipulation", "stealth")
def generate_cruelty_tree(): return generate_standard_tree(
    "cruelty", "wrath", "physical_strength")
def generate_selfishness_tree(): return generate_standard_tree(
    "selfishness", "greed", "manipulation")
def generate_envy_tree(): return generate_standard_tree("envy", "greed", "wrath")
def generate_wrath_tree(): return generate_standard_tree(
    "wrath", "cruelty", "combat_rating")
def generate_cowardice_tree(): return generate_standard_tree(
    "cowardice", "stealth", "survival_instinct")
def generate_laziness_tree(): return generate_standard_tree(
    "laziness", "efficiency", "automation")
def generate_gluttony_tree(): return generate_standard_tree(
    "gluttony", "endurance", "greed")
def generate_paranoia_tree(): return generate_standard_tree(
    "paranoia", "perception", "survival_instinct")
def generate_impulsiveness_tree(): return generate_standard_tree(
    "impulsiveness", "speed", "recklessness")
def generate_vengefulness_tree(): return generate_standard_tree(
    "vengefulness", "wrath", "patience")
def generate_manipulation_tree(): return generate_standard_tree(
    "manipulation", "deceit", "charisma")
def generate_prejudice_tree(): return generate_standard_tree(
    "prejudice", "arrogance", "stubbornness")
def generate_betrayal_tree(): return generate_standard_tree(
    "betrayal", "deceit", "manipulation")
def generate_stubbornness_tree(): return generate_standard_tree(
    "stubbornness", "discipline", "prejudice")
def generate_pessimism_tree(): return generate_standard_tree(
    "pessimism", "perception", "paranoia")
def generate_recklessness_tree(): return generate_standard_tree(
    "recklessness", "impulsiveness", "courage")
def generate_vanity_tree(): return generate_standard_tree(
    "vanity", "arrogance", "charisma")

# Skills
def generate_hacking_tree(): return generate_standard_tree(
    "hacking", "technical_knowledge", "intelligence")
def generate_negotiation_tree(): return generate_standard_tree(
    "negotiation", "charisma", "intelligence")
def generate_stealth_tree(): return generate_standard_tree(
    "stealth", "dexterity", "perception")
def generate_leadership_tree(): return generate_standard_tree(
    "leadership", "charisma", "wisdom")
def generate_technical_knowledge_tree(): return generate_standard_tree(
    "technical_knowledge", "intelligence", "hacking")
def generate_physical_strength_tree(): return generate_standard_tree(
    "physical_strength", "endurance", "combat_rating")
def generate_speed_tree(): return generate_standard_tree(
    "speed", "dexterity", "endurance")
def generate_intelligence_tree(): return generate_standard_tree(
    "intelligence", "memory", "focus")
def generate_charisma_tree(): return generate_standard_tree(
    "charisma", "negotiation", "influence")
def generate_perception_tree(): return generate_standard_tree(
    "perception", "focus", "survival_instinct")
def generate_endurance_tree(): return generate_standard_tree(
    "endurance", "resilience", "physical_strength")
def generate_dexterity_tree(): return generate_standard_tree(
    "dexterity", "speed", "combat_rating")
def generate_memory_tree(): return generate_standard_tree(
    "memory", "intelligence", "focus")
def generate_focus_tree(): return generate_standard_tree(
    "focus", "discipline", "meditation")
def generate_networking_tree(): return generate_standard_tree(
    "networking", "charisma", "influence")
def generate_strategy_tree(): return generate_standard_tree(
    "strategy", "intelligence", "tactical_mastery")
def generate_trading_tree(): return generate_standard_tree(
    "trading", "negotiation", "business_acumen")
def generate_engineering_tree(): return generate_standard_tree(
    "engineering", "technical_knowledge", "creativity")
def generate_medicine_tree(): return generate_standard_tree(
    "medicine", "intelligence", "empathy")
def generate_meditation_tree(): return generate_standard_tree(
    "meditation", "focus", "enlightenment")

# Meta Traits
def generate_reputation_tree(): return generate_standard_tree(
    "reputation", "fame", "influence")
def generate_influence_tree(): return generate_standard_tree(
    "influence", "charisma", "political_power")
def generate_fame_tree(): return generate_standard_tree(
    "fame", "reputation", "legendary_status")
def generate_infamy_tree(): return generate_standard_tree(
    "infamy", "wrath", "cruelty")
def generate_trustworthiness_tree(): return generate_standard_tree(
    "trustworthiness", "honesty", "loyalty")
def generate_combat_rating_tree(): return generate_standard_tree(
    "combat_rating", "tactical_mastery", "physical_strength")
def generate_tactical_mastery_tree(): return generate_standard_tree(
    "tactical_mastery", "strategy", "combat_rating")
def generate_survival_instinct_tree(): return generate_standard_tree(
    "survival_instinct", "perception", "adaptability")
def generate_business_acumen_tree(): return generate_standard_tree(
    "business_acumen", "trading", "market_intuition")
def generate_market_intuition_tree(): return generate_standard_tree(
    "market_intuition", "perception", "business_acumen")
def generate_wealth_management_tree(): return generate_standard_tree(
    "wealth_management", "business_acumen", "strategy")
def generate_enlightenment_tree(): return generate_standard_tree(
    "enlightenment", "meditation", "wisdom")
def generate_karmic_balance_tree(): return generate_standard_tree(
    "karmic_balance", "wisdom", "divine_favor")
def generate_divine_favor_tree(): return generate_standard_tree(
    "divine_favor", "karmic_balance", "legendary_status")
def generate_guild_loyalty_tree(): return generate_standard_tree(
    "guild_loyalty", "loyalty", "political_power")
def generate_political_power_tree(): return generate_standard_tree(
    "political_power", "influence", "diplomatic_skill")
def generate_diplomatic_skill_tree(): return generate_standard_tree(
    "diplomatic_skill", "negotiation", "wisdom")
def generate_legendary_status_tree(): return generate_standard_tree(
    "legendary_status", "fame", "historical_impact")
def generate_mentorship_tree(): return generate_standard_tree(
    "mentorship", "wisdom", "patience")
def generate_historical_impact_tree(): return generate_standard_tree(
    "historical_impact", "influence", "legendary_status")
