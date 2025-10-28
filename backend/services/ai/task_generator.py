"""Gemini AI Task Generator Service

Generates personalized tasks for players based on their traits using Gemini AI.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
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
        
    async def generate_task(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a task for a player based on their traits"""
        try:
            # Determine task type based on player's moral class and traits
            task_type = self._determine_task_type(player)
            
            # Get top traits
            traits = player.get('traits', {})
            virtues = {k: v for k, v in traits.items() if k in self._get_virtue_names() and v > 60}
            vices = {k: v for k, v in traits.items() if k in self._get_vice_names() and v > 60}
            
            # Create prompt
            prompt = self._create_task_prompt(player, task_type, virtues, vices)
            
            # Generate with Gemini
            response = self.model.generate_content(prompt)
            task_data = json.loads(response.text)
            
            # Add metadata
            task_data['task_type'] = task_type
            task_data['player_id'] = player['_id']
            task_data['generated_at'] = datetime.utcnow().isoformat()
            task_data['expires_at'] = (datetime.utcnow() + timedelta(hours=2)).isoformat()
            task_data['status'] = 'active'
            
            return task_data
            
        except Exception as e:
            logger.error(f"Error generating task: {e}")
            # Fallback to simple task
            return self._generate_fallback_task(player)
    
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
    
    def _create_task_prompt(self, player: Dict[str, Any], task_type: str, virtues: Dict, vices: Dict) -> str:
        """Create prompt for Gemini AI"""
        username = player.get('username', 'Player')
        level = player.get('level', 1)
        
        if task_type == 'good':
            trait_info = f"Top Virtues: {', '.join([f'{k}: {v}%' for k, v in list(virtues.items())[:3]])}"
            task_guidance = "a virtuous, helpful, or constructive task that helps others or improves the community"
        elif task_type == 'bad':
            trait_info = f"Top Vices: {', '.join([f'{k}: {v}%' for k, v in list(vices.items())[:3]])}"
            task_guidance = "a mischievous, selfish, or morally questionable task that benefits the player at others' expense"
        else:
            trait_info = "Balanced traits"
            task_guidance = "a neutral task that tests moral decision-making"
        
        prompt = f"""Generate a game task for player "{username}" (Level {level}).

Player Profile:
- Moral Alignment: {task_type.upper()}
- {trait_info}

Generate {task_guidance}.

Requirements:
1. Task should be engaging and fit the player's character
2. Description should be 1-2 sentences, action-oriented
3. Coin reward should be 50-200 based on difficulty
4. Include clear success condition

Return ONLY valid JSON in this exact format:
{{
  "title": "Task Title",
  "description": "Brief description of what player must do",
  "coin_reward": 100,
  "difficulty": "easy|medium|hard",
  "success_condition": "What counts as completion"
}}
"""
        return prompt
    
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
