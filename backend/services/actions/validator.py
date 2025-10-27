from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class ActionValidator:
    """Validates actions before execution"""

    async def validate_action(
        self,
        action_type: str,
        actor: Dict[str, Any],
        target: Optional[Dict[str, Any]],
        params: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate if action can be performed"""

        # Check cooldown
        if not self._check_cooldown(actor, action_type):
            return {
                "valid": False,
                "reason": "Action is on cooldown"
            }

        # Validate based on action type
        if action_type == "hack":
            return self._validate_hack(actor, target, params)
        elif action_type == "help":
            return self._validate_help(actor, target, params)
        elif action_type == "steal":
            return self._validate_steal(actor, target, params)
        elif action_type == "donate":
            return self._validate_donate(actor, target, params)
        elif action_type == "trade":
            return self._validate_trade(actor, target, params)
        else:
            return {
                "valid": False,
                "reason": f"Unknown action type: {action_type}"
            }

    def _check_cooldown(self, actor: Dict[str, Any], action_type: str) -> bool:
        """Check if action is off cooldown"""
        last_action = actor.get("last_action")
        if not last_action:
            return True

        # 1 second cooldown between actions
        cooldown = timedelta(seconds=1)
        return datetime.utcnow() - last_action > cooldown

    def _validate_hack(self, actor, target, params) -> Dict[str, Any]:
        """Validate hacking action"""
        if not target:
            return {"valid": False, "reason": "Target required for hacking"}

        # Check hacking skill
        if actor["traits"].get("hacking", 0) < 20:
            return {"valid": False, "reason": "Insufficient hacking skill"}

        return {"valid": True}

    def _validate_help(self, actor, target, params) -> Dict[str, Any]:
        """Validate helping action"""
        if not target:
            return {"valid": False, "reason": "Target required for helping"}

        # Check if target needs help (lower resources)
        if target["currencies"]["credits"] >= actor["currencies"]["credits"]:
            return {"valid": False, "reason": "Target doesn't need help"}

        return {"valid": True}

    def _validate_steal(self, actor, target, params) -> Dict[str, Any]:
        """Validate stealing action"""
        if not target:
            return {"valid": False, "reason": "Target required for stealing"}

        # Check stealth skill
        if actor["traits"].get("stealth", 0) < 15:
            return {"valid": False, "reason": "Insufficient stealth skill"}

        # Check if target has resources
        if target["currencies"]["credits"] < 100:
            return {"valid": False, "reason": "Target has insufficient resources"}

        return {"valid": True}

    def _validate_donate(self, actor, target, params) -> Dict[str, Any]:
        """Validate donation action"""
        if not target:
            return {"valid": False, "reason": "Target required for donation"}

        amount = params.get("amount", 0) if params else 0
        if amount <= 0:
            return {"valid": False, "reason": "Invalid donation amount"}

        if actor["currencies"]["credits"] < amount:
            return {"valid": False, "reason": "Insufficient credits"}

        return {"valid": True}

    def _validate_trade(self, actor, target, params) -> Dict[str, Any]:
        """Validate trading action"""
        if not target:
            return {"valid": False, "reason": "Target required for trading"}

        if not params or "offer" not in params or "request" not in params:
            return {"valid": False, "reason": "Invalid trade parameters"}

        return {"valid": True}
