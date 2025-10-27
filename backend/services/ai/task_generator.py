"""Gemini AI-powered task generator"""

import google.generativeai as genai
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import os
import random

from .trait_analyzer import TraitAnalyzer
from backend.core.config import settings


class TaskGeneratorService:
    """Generate dynamic tasks using Gemini AI based on player traits"""

    def __init__(self):
        """Initialize Gemini AI client"""
        api_key = settings.GEMINI_API_KEY or os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.trait_analyzer = TraitAnalyzer()

    async def generate_task(self, player_data: Dict) -> Dict:
        """
        Generate a personalized task for the player based on their traits.
        
        Args:
            player_data: Dictionary containing player information including traits
            
        Returns:
            Dictionary containing task details
        """
        # Analyze player traits
        traits = player_data.get('traits', {})
        analysis = self.trait_analyzer.analyze_player(traits)
        
        # Prepare prompt for Gemini
        prompt = self._build_task_prompt(player_data, analysis)
        
        try:
            # Generate task using Gemini
            response = self.model.generate_content(prompt)
            task_description = response.text.strip()
            
            # Parse and structure the task
            task = self._structure_task(
                description=task_description,
                player_id=player_data.get('player_id'),
                task_type=analysis['task_preference'],
                alignment=analysis['alignment']
            )
            
            return task
            
        except Exception as e:
            # Fallback to template-based task if AI fails
            print(f"AI task generation failed: {e}. Using fallback.")
            return self._generate_fallback_task(player_data, analysis)

    def _build_task_prompt(self, player_data: Dict, analysis: Dict) -> str:
        """
        Build a detailed prompt for Gemini to generate contextual tasks.
        
        Args:
            player_data: Player information
            analysis: Trait analysis results
            
        Returns:
            Formatted prompt string
        """
        alignment = analysis['alignment']
        task_type = analysis['task_preference']
        top_virtues = [v[0] for v in analysis['top_virtues'][:3]]
        top_vices = [v[0] for v in analysis['top_vices'][:3]]
        top_skills = [s[0] for s in analysis['top_skills'][:3]]
        
        player_name = player_data.get('username', 'Player')
        player_level = player_data.get('level', 1)
        
        # Build character description
        virtue_str = ", ".join(top_virtues) if top_virtues else "balanced"
        vice_str = ", ".join(top_vices) if top_vices else "controlled"
        skill_str = ", ".join(top_skills) if top_skills else "developing"
        
        if task_type == "good":
            task_direction = "a virtuous, helpful task that aligns with their noble character. The task should involve helping others, protecting the innocent, or contributing positively to society."
        elif task_type == "bad":
            task_direction = "a morally questionable task that aligns with their darker tendencies. The task might involve theft, deception, sabotage, or other illicit activities."
        else:
            task_direction = "a neutral task that tests their character. The task should be morally ambiguous or practical in nature."
        
        prompt = f"""
You are the AI task master in Karma Nexus, a futuristic RPG game. Generate a single, specific task for a player.

Player Profile:
- Name: {player_name}
- Level: {player_level}
- Alignment: {alignment}
- Top Virtues: {virtue_str}
- Top Vices: {vice_str}
- Top Skills: {skill_str}

Task Requirements:
- Generate {task_direction}
- The task should be specific and actionable (e.g., "Deliver medical supplies to the refugee camp in Sector 7")
- Keep it concise (1-2 sentences, max 150 characters)
- Make it fit the cyberpunk/futuristic setting
- Include specific locations, NPCs, or items when relevant
- Do NOT include rewards or completion instructions
- Return ONLY the task description, nothing else

Example good task: "Help merchant Sarah repair her broken security drone in the Downtown Market."
Example bad task: "Steal prototype tech from the Corporate Security vault in Tower 23."
Example neutral task: "Collect 5 scrap metal pieces from the abandoned factory district."

Generate task:
"""
        return prompt

    def _structure_task(self, description: str, player_id: str, task_type: str, alignment: str) -> Dict:
        """
        Structure the AI-generated task into a proper format.
        
        Args:
            description: Task description from AI
            player_id: Player's ID
            task_type: Type of task (good/bad/neutral)
            alignment: Player alignment
            
        Returns:
            Structured task dictionary
        """
        # Calculate reward based on task type
        base_reward = random.randint(50, 200)
        
        # Adjust reward based on alignment match
        if (task_type == "good" and alignment == "virtuous") or \
           (task_type == "bad" and alignment == "corrupt"):
            base_reward = int(base_reward * 1.2)  # 20% bonus for aligned tasks
        
        # Task expires in 30 minutes
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        
        task = {
            "task_id": str(uuid.uuid4()),
            "player_id": player_id,
            "description": description[:200],  # Limit description length
            "task_type": task_type,
            "base_reward": base_reward,
            "actual_reward": base_reward,  # Will be calculated with bonuses on completion
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat()
        }
        
        return task

    def _generate_fallback_task(self, player_data: Dict, analysis: Dict) -> Dict:
        """
        Generate a template-based task as fallback when AI fails.
        
        Args:
            player_data: Player information
            analysis: Trait analysis results
            
        Returns:
            Structured task dictionary
        """
        task_type = analysis['task_preference']
        
        # Template tasks for each type
        good_tasks = [
            "Help the local merchant repair their damaged storefront.",
            "Deliver medical supplies to the clinic in the refugee district.",
            "Escort a civilian safely through the dangerous sector.",
            "Donate spare equipment to the community shelter.",
            "Assist in repairing damaged infrastructure in the slums."
        ]
        
        bad_tasks = [
            "Steal valuable data from the corporate database.",
            "Sabotage a rival gang's supply shipment.",
            "Hack into the security system of a wealthy merchant.",
            "Extort protection money from local shop owners.",
            "Smuggle contraband through the checkpoint."
        ]
        
        neutral_tasks = [
            "Collect 10 scrap metal pieces from the junkyard.",
            "Scout the abandoned factory for useful resources.",
            "Test the new combat simulator in the training facility.",
            "Explore the underground tunnels and map the route.",
            "Gather information about the new trading post."
        ]
        
        # Select appropriate task list
        if task_type == "good":
            task_list = good_tasks
        elif task_type == "bad":
            task_list = bad_tasks
        else:
            task_list = neutral_tasks
        
        description = random.choice(task_list)
        
        return self._structure_task(
            description=description,
            player_id=player_data.get('player_id'),
            task_type=task_type,
            alignment=analysis['alignment']
        )
