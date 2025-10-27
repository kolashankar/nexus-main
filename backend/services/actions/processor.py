from typing import Dict, Any, Optional
import random

class ActionProcessor:
    """Processes action logic and outcomes"""

    async def process_action(
        self,
        action_type: str,
        actor: Dict[str, Any],
        target: Optional[Dict[str, Any]],
        params: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process action and return result"""

        if action_type == "hack":
            return await self._process_hack(actor, target, params)
        elif action_type == "help":
            return await self._process_help(actor, target, params)
        elif action_type == "steal":
            return await self._process_steal(actor, target, params)
        elif action_type == "donate":
            return await self._process_donate(actor, target, params)
        elif action_type == "trade":
            return await self._process_trade(actor, target, params)
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    async def _process_hack(self, actor, target, params) -> Dict[str, Any]:
        """Process hacking action"""
        hacking_skill = actor["traits"].get("hacking", 0)
        target_tech = target["traits"].get("technical_knowledge", 50)

        # Calculate success probability
        success_chance = min(90, max(10, hacking_skill - target_tech + 50))
        success = random.randint(1, 100) <= success_chance

        if success:
            # Successful hack
            stolen_data = random.randint(50, 200)
            return {
                "success": True,
                "message": f"Successfully hacked {target['username']} and obtained {stolen_data} credits worth of data!",
                "credits_gained": stolen_data,
                "credits_lost": stolen_data
            }
        else:
            return {
                "success": False,
                "message": f"Hack attempt on {target['username']} failed! You were detected.",
                "credits_gained": 0,
                "credits_lost": 0
            }

    async def _process_help(self, actor, target, params) -> Dict[str, Any]:
        """Process helping action"""
        help_amount = random.randint(100, 300)

        return {
            "success": True,
            "message": f"You helped {target['username']} with {help_amount} credits!",
            "credits_given": help_amount,
            "karma_boost": 10
        }

    async def _process_steal(self, actor, target, params) -> Dict[str, Any]:
        """Process stealing action"""
        stealth_skill = actor["traits"].get("stealth", 0)
        target_perception = target["traits"].get("perception", 50)

        # Calculate success probability
        success_chance = min(
            85, max(15, stealth_skill - target_perception + 50))
        success = random.randint(1, 100) <= success_chance

        if success:
            stolen_amount = random.randint(100, 500)
            return {
                "success": True,
                "message": f"Successfully stole {stolen_amount} credits from {target['username']}!",
                "credits_gained": stolen_amount,
                "credits_lost": stolen_amount
            }
        else:
            return {
                "success": False,
                "message": f"Steal attempt on {target['username']} failed! You were caught.",
                "credits_gained": 0,
                "credits_lost": 0,
                "penalty": True
            }

    async def _process_donate(self, actor, target, params) -> Dict[str, Any]:
        """Process donation action"""
        amount = params.get("amount", 100)

        return {
            "success": True,
            "message": f"You donated {amount} credits to {target['username']}!",
            "credits_given": amount,
            "karma_boost": 15
        }

    async def _process_trade(self, actor, target, params) -> Dict[str, Any]:
        """Process trading action"""
        offer = params.get("offer", {})
        request = params.get("request", {})

        return {
            "success": True,
            "message": f"Trade initiated with {target['username']}",
            "trade_id": "pending",
            "offer": offer,
            "request": request
        }
