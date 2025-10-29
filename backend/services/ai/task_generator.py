"""Gemini AI Task Generator Service

Generates personalized tasks for players based on their traits using Gemini AI.
Handles both new players (no established traits) and experienced players.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCrDnhg5VTo-XrfOK1eoamZD9R6wVlqYSM')
genai.configure(api_key=GEMINI_API_KEY)

class TaskGenerator:
    """Generate AI-powered tasks based on player traits"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("✅ Gemini AI Task Generator initialized successfully")
        
    def is_new_player(self, traits: Dict[str, float]) -> bool:
        """Check if player is new (has mostly default traits at 50.0)"""
        if not traits:
            return True
        
        values = list(traits.values())
        default_count = sum(1 for v in values if v == 50.0)
        
        # If more than 80% of traits are at default, consider new player
        return default_count > (len(values) * 0.8)
    
    async def generate_initial_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate initial character-defining task for new players.
        These tasks are neutral and help establish the player's personality.
        """
        username = player.get('username', 'Player')
        level = player.get('level', 1)
        
        prompt = f"""Generate a character-defining task for a NEW player named "{username}" (Level {level}) in a cyberpunk RPG game.

Context: This is their FIRST task. They have NO established personality traits yet. This task should help define who they become.

Requirements:
1. Create a NEUTRAL moral scenario (not obviously good or evil)
2. Scenario should be relatable and immersive
3. Provide 3-4 distinct choices with DIFFERENT consequences
4. Each choice should affect 2-4 different character traits
5. Description should be engaging and atmospheric (2-3 sentences)

Task Types (choose one):
- Moral dilemma (help stranger, witness crime, find lost item)
- Resource decision (share/keep/sell something valuable)
- Social interaction (mediate conflict, join group, ignore situation)
- Exploration choice (investigate danger, avoid risk, seek reward)

Return ONLY valid JSON in this EXACT format:
{{
  "title": "Task Title",
  "description": "Engaging 2-3 sentence scenario describing the situation",
  "type": "moral_choice",
  "difficulty": "easy",
  "xp_reward": 50,
  "credits_reward": 100,
  "choices": [
    {{
      "text": "Choice 1 description",
      "traits_impact": {{
        "kindness": 5,
        "honesty": 3,
        "karma_points": 10
      }}
    }},
    {{
      "text": "Choice 2 description",
      "traits_impact": {{
        "greed": 4,
        "selfishness": 3,
        "karma_points": -8
      }}
    }},
    {{
      "text": "Choice 3 description",
      "traits_impact": {{
        "wisdom": 3,
        "patience": 2,
        "karma_points": 2
      }}
    }}
  ]
}}

Important:
- Use trait names from: empathy, kindness, honesty, courage, greed, deceit, selfishness, wisdom, intelligence, charisma, stealth, hacking
- Trait changes should be 2-6 points
- Karma points: +5 to +15 for good, -5 to -15 for bad, 0-5 for neutral
"""
        
        try:
            response = self.model.generate_content(prompt)
            task_data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            
            # Add metadata
            task_data['player_id'] = player['_id']
            task_data['generated_at'] = datetime.utcnow().isoformat()
            task_data['expires_at'] = (datetime.utcnow() + timedelta(hours=24)).isoformat()
            task_data['status'] = 'active'
            
            logger.info(f"✅ Generated initial task for new player {username}: {task_data['title']}")
            return task_data
            
        except Exception as e:
            logger.error(f"❌ Error generating initial task: {e}")
            return self._generate_fallback_initial_task(player)
    
    async def generate_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a task for a player.
        Automatically detects if player is new or experienced.
        """
        traits = player.get('traits', {})
        
        # Check if player is new
        if self.is_new_player(traits):
            logger.info(f"🆕 Detected NEW player: {player.get('username')}. Generating character-defining task...")
            return await self.generate_initial_task(player)
        else:
            logger.info(f"⭐ Detected EXPERIENCED player: {player.get('username')}. Generating personality-matched task...")
            return await self.generate_personality_task(player)
    
    async def generate_personality_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate task for experienced player based on their established traits.
        80% tasks match their personality, 20% challenge their weaknesses.
        """
        try:
            # Determine task type based on player's traits
            task_type = self._determine_task_type(player)
            
            # Get top traits
            traits = player.get('traits', {})
            virtues = {k: v for k, v in traits.items() if k in self._get_virtue_names() and v > 60}
            vices = {k: v for k, v in traits.items() if k in self._get_vice_names() and v > 60}
            skills = {k: v for k, v in traits.items() if v > 60 and k not in self._get_virtue_names() and k not in self._get_vice_names()}
            
            # Create prompt
            prompt = self._create_personality_task_prompt(player, task_type, virtues, vices, skills)
            
            # Generate with Gemini
            response = self.model.generate_content(prompt)
            task_data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            
            # Add metadata
            task_data['task_type'] = task_type
            task_data['player_id'] = player['_id']
            task_data['generated_at'] = datetime.utcnow().isoformat()
            task_data['expires_at'] = (datetime.utcnow() + timedelta(hours=2)).isoformat()
            task_data['status'] = 'active'
            
            logger.info(f"✅ Generated personality task ({task_type}) for {player.get('username')}: {task_data.get('title')}")
            return task_data
            
        except Exception as e:
            logger.error(f"❌ Error generating personality task: {e}")
            return self._generate_fallback_task(player)
    
    def _create_personality_task_prompt(self, player: Dict[str, Any], task_type: str, virtues: Dict, vices: Dict, skills: Dict) -> str:
        """Create prompt for Gemini AI for experienced players"""
        username = player.get('username', 'Player')
        level = player.get('level', 1)
        karma = player.get('karma_points', 0)
        
        # Build personality profile
        personality_traits = []
        if virtues:
            top_virtues = sorted(virtues.items(), key=lambda x: x[1], reverse=True)[:3]
            virtues_str = ', '.join([f"{k.replace('_', ' ')}: {v:.0f}" for k, v in top_virtues])
            personality_traits.append(f"Virtues: {virtues_str}")
        if vices:
            top_vices = sorted(vices.items(), key=lambda x: x[1], reverse=True)[:3]
            vices_str = ', '.join([f"{k.replace('_', ' ')}: {v:.0f}" for k, v in top_vices])
            personality_traits.append(f"Vices: {vices_str}")
        if skills:
            top_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)[:3]
            skills_str = ', '.join([f"{k.replace('_', ' ')}: {v:.0f}" for k, v in top_skills])
            personality_traits.append(f"Skills: {skills_str}")
        
        personality_info = "\n".join(personality_traits) if personality_traits else "Balanced personality"
        
        if task_type == 'good':
            task_guidance = "a VIRTUOUS task that lets them use their good traits to help others or improve the world"
            moral_hint = "This player tends toward good. Create a heroic or helpful scenario."
        elif task_type == 'bad':
            task_guidance = "a DARK task that tempts them with selfish gains or morally questionable actions"
            moral_hint = "This player has a darker side. Create a tempting or ruthless scenario."
        else:
            task_guidance = "a NEUTRAL task that tests their moral judgment"
            moral_hint = "This player is balanced. Create a complex moral dilemma."
        
        prompt = f"""Generate a game task for player "{username}" (Level {level}, Karma: {karma}).

Player's Established Personality:
{personality_info}

{moral_hint}

Generate {task_guidance}.

Requirements:
1. Task should MATCH their personality (80% alignment)
2. Let them use their established traits
3. Description should be 2-3 sentences, action-oriented
4. Rewards scale with difficulty
5. Include clear success condition

Return ONLY valid JSON in this exact format:
{{
  "title": "Task Title",
  "description": "Brief description matching their personality",
  "coin_reward": 150,
  "difficulty": "medium",
  "success_condition": "What counts as completion"
}}
"""
        return prompt
    
    def _determine_task_type(self, player: Dict[str, Any]) -> str:
        """Determine if task should be good or bad based on player traits"""
        traits = player.get('traits', {})
        moral_class = player.get('moral_class', 'average')
        
        # Calculate virtue vs vice balance
        virtue_sum = sum(traits.get(v, 0) for v in self._get_virtue_names())
        vice_sum = sum(traits.get(v, 0) for v in self._get_vice_names())
        
        if moral_class == 'good' or virtue_sum > vice_sum:
            return 'good'
        elif moral_class == 'bad' or vice_sum > virtue_sum:
            return 'bad'
        else:
            return 'neutral'
    
    def _generate_fallback_initial_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback initial task if AI fails"""
        import random
        
        tasks = [
            {
                "title": "The Lost Data Chip",
                "description": "You found a valuable data chip on the street. Its owner seems desperate to find it.",
                "type": "moral_choice",
                "difficulty": "easy",
                "xp_reward": 50,
                "credits_reward": 100,
                "choices": [
                    {
                        "text": "Return it to the owner immediately",
                        "traits_impact": {"honesty": 5, "kindness": 4, "karma_points": 10}
                    },
                    {
                        "text": "Sell it to a data broker",
                        "traits_impact": {"greed": 5, "deceit": 3, "karma_points": -10}
                    },
                    {
                        "text": "Keep it and examine its contents",
                        "traits_impact": {"curiosity": 4, "selfishness": 2, "karma_points": -3}
                    }
                ]
            },
            {
                "title": "Helping Hand",
                "description": "An elderly citizen struggles with heavy cargo. Nobody else seems to notice or care.",
                "type": "moral_choice",
                "difficulty": "easy",
                "xp_reward": 45,
                "credits_reward": 90,
                "choices": [
                    {
                        "text": "Help them carry the cargo",
                        "traits_impact": {"kindness": 5, "empathy": 4, "karma_points": 12}
                    },
                    {
                        "text": "Walk past without helping",
                        "traits_impact": {"selfishness": 3, "karma_points": -5}
                    },
                    {
                        "text": "Offer help for a small payment",
                        "traits_impact": {"negotiation": 3, "greed": 2, "karma_points": 0}
                    }
                ]
            }
        ]
        
        task = random.choice(tasks)
        task['player_id'] = player['_id']
        task['generated_at'] = datetime.utcnow().isoformat()
        task['expires_at'] = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        task['status'] = 'active'
        
        logger.warning(f"⚠️ Using fallback initial task for {player.get('username')}")
        return task
    
    def _generate_fallback_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Generate simple fallback task if AI fails"""
        task_type = self._determine_task_type(player)
        
        if task_type == 'good':
            tasks = [
                {"title": "Help a Citizen", "description": "Assist an NPC with their daily tasks", "coin_reward": 100},
                {"title": "Donate Resources", "description": "Share your resources with those in need", "coin_reward": 150},
                {"title": "Protect the Weak", "description": "Defend NPCs from threats", "coin_reward": 200}
            ]
        else:
            tasks = [
                {"title": "Steal Supplies", "description": "Take resources from an unguarded warehouse", "coin_reward": 120},
                {"title": "Spread Rumors", "description": "Damage a rival's reputation", "coin_reward": 100},
                {"title": "Sabotage Equipment", "description": "Disable a competitor's machinery", "coin_reward": 180}
            ]
        
        import random
        task = random.choice(tasks)
        
        return {
            'task_type': task_type,
            'player_id': player['_id'],
            'title': task['title'],
            'description': task['description'],
            'coin_reward': task['coin_reward'],
            'difficulty': 'medium',
            'success_condition': 'Complete the task objective',
            'generated_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(hours=2)).isoformat(),
            'status': 'active'
        }
    
    def _get_virtue_names(self) -> list:
        return [
            'empathy', 'integrity', 'discipline', 'creativity', 'resilience',
            'curiosity', 'kindness', 'courage', 'patience', 'adaptability',
            'wisdom', 'humility', 'vision', 'honesty', 'loyalty',
            'generosity', 'self_awareness', 'gratitude', 'optimism', 'loveability'
        ]
    
    def _get_vice_names(self) -> list:
        return [
            'greed', 'arrogance', 'deceit', 'cruelty', 'selfishness',
            'envy', 'wrath', 'cowardice', 'laziness', 'gluttony',
            'paranoia', 'impulsiveness', 'vengefulness', 'manipulation', 'prejudice',
            'betrayal', 'stubbornness', 'pessimism', 'recklessness', 'vanity'
        ]
