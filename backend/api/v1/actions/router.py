from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
import random

from .schemas import (
    HackAction, HelpAction, StealAction, DonateAction, TradeAction, ActionResponse
)
from backend.core.database import get_database
from backend.api.v1.auth.router import get_current_user_dep
from backend.models.player.player import Player
from backend.models.actions.action import Action

router = APIRouter(prefix="/actions", tags=["actions"])

def calculate_basic_karma(action_type: str, actor: Player, target: Player, amount: int = 0) -> dict:
    """
    Basic karma calculation (rule-based, before AI integration).
    Returns: {karma_change: int, trait_changes: dict, message: str}
    """
    karma_change = 0
    trait_changes = {}
    message = ""

    if action_type == "hack":
        # Negative karma for hacking
        karma_change = -20

        # Trait changes based on target's moral class
        if target.moral_class == "good":
            karma_change -= 15  # Extra penalty for hacking good people
            trait_changes["deceit"] = 5
            trait_changes["integrity"] = -8
        elif target.moral_class == "bad":
            karma_change += 5  # Less penalty for hacking bad people

        # Improve hacking skill
        trait_changes["hacking"] = 3
        trait_changes["technical_knowledge"] = 2

        message = f"You hacked {target.username}. Your skills improved but your reputation suffered."

    elif action_type == "help":
        # Positive karma for helping
        karma_change = 15

        # More karma for helping poor
        if target.economic_class == "poor":
            karma_change += 10

        # Trait changes
        trait_changes["kindness"] = 5
        trait_changes["empathy"] = 3
        trait_changes["generosity"] = 4
        trait_changes["selfishness"] = -3

        message = f"You helped {target.username}. Your compassion grows."

    elif action_type == "steal":
        # Very negative karma for stealing
        karma_change = -30

        # Even worse for stealing from good/poor people
        if target.moral_class == "good":
            karma_change -= 20
        if target.economic_class == "poor":
            karma_change -= 15

        # Trait changes
        trait_changes["greed"] = 6
        trait_changes["deceit"] = 5
        trait_changes["honesty"] = -7
        trait_changes["stealth"] = 4

        message = f"You stole from {target.username}. Your greed consumes you."

    elif action_type == "donate":
        # Very positive karma for donating
        karma_change = 25

        # More karma for donating to poor/good
        if target.economic_class == "poor":
            karma_change += 15
        if target.moral_class == "good":
            karma_change += 10

        # Trait changes
        trait_changes["generosity"] = 7
        trait_changes["kindness"] = 5
        trait_changes["compassion"] = 6
        trait_changes["greed"] = -5
        trait_changes["selfishness"] = -6

        message = f"You donated {amount} credits to {target.username}. Your generosity inspires others."

    elif action_type == "trade":
        # Neutral to slightly positive karma for fair trade
        karma_change = 5

        # Trait changes
        trait_changes["negotiation"] = 4
        trait_changes["trading"] = 5
        trait_changes["business_acumen"] = 3

        message = f"You traded with {target.username}. Your business skills grow."

    return {
        "karma_change": karma_change,
        "trait_changes": trait_changes,
        "message": message
    }

async def apply_trait_changes(db: AsyncIOMotorDatabase, player_id: str, trait_changes: dict):
    """Apply trait changes to a player."""
    update_dict = {}
    for trait, change in trait_changes.items():
        # Handle both regular traits and meta traits
        if trait in ["reputation", "influence", "fame", "infamy", "trustworthiness",
                     "combat_rating", "tactical_mastery", "survival_instinct",
                     "business_acumen", "market_intuition", "wealth_management",
                     "enlightenment", "karmic_balance", "divine_favor",
                     "guild_loyalty", "political_power", "diplomatic_skill",
                     "legendary_status", "mentorship", "historical_impact"]:
            update_dict[f"meta_traits.{trait}"] = change
        else:
            update_dict[f"traits.{trait}"] = change

    if update_dict:
        # Build update operations
        for key, value in update_dict.items():
            await db.players.update_one(
                {"_id": player_id},
                {"$inc": {key: value}}
            )

            # Clamp values between 0 and 100
            await db.players.update_one(
                {"_id": player_id, key: {"$gt": 100}},
                {"$set": {key: 100}}
            )
            await db.players.update_one(
                {"_id": player_id, key: {"$lt": 0}},
                {"$set": {key: 0}}
            )

@router.post("/hack", response_model=ActionResponse)
async def hack_player(
    action: HackAction,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Hack another player to steal credits.
    Success depends on hacking skill vs target's technical knowledge.
    """
    # Get target player
    target_dict = await db.players.find_one({"_id": action.target_id})
    if not target_dict:
        raise HTTPException(status_code=404, detail="Target player not found")

    target = Player(**target_dict)

    # Can't hack yourself
    if target.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot hack yourself")

    # Calculate success chance
    hacker_skill = current_user.traits.hacking + \
        current_user.traits.technical_knowledge
    target_defense = target.traits.technical_knowledge + \
        target.meta_traits.tactical_mastery

    success_chance = min(
        80, max(20, (hacker_skill / (hacker_skill + target_defense)) * 100))
    success = random.random() * 100 < success_chance

    if success:
        # Steal 10-30% of target's credits
        steal_percentage = random.uniform(0.1, 0.3)
        stolen_amount = int(target.currencies.credits * steal_percentage)

        if stolen_amount > 0:
            # Update credits
            await db.players.update_one(
                {"_id": target.id},
                {"$inc": {"currencies.credits": -stolen_amount}}
            )
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"currencies.credits": stolen_amount}}
            )

            # Calculate karma
            result = calculate_basic_karma(
                "hack", current_user, target, stolen_amount)

            # Apply trait changes
            await apply_trait_changes(db, current_user.id, result["trait_changes"])

            # Update karma
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"karma_points": result["karma_change"]}}
            )

            # Log action
            action_log = Action(
                action_type="hack",
                actor_id=current_user.id,
                target_id=target.id,
                amount=stolen_amount,
                success=True,
                karma_change=result["karma_change"],
                trait_changes=result["trait_changes"],
                message=result["message"]
            )
            await db.actions.insert_one(action_log.model_dump(by_alias=True))

            # Update stats
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"stats.total_actions": 1, "stats.total_stolen": stolen_amount}}
            )

            return ActionResponse(
                success=True,
                message=f"Successfully hacked {target.username} and stole {stolen_amount} credits! {result['message']}",
                karma_change=result["karma_change"],
                trait_changes=result["trait_changes"],
                credits_change=stolen_amount
            )
        else:
            return ActionResponse(
                success=False,
                message=f"{target.username} has no credits to steal!",
                karma_change=-10,
                trait_changes={"hacking": 1},
                credits_change=0
            )
    else:
        # Failed hack
        await db.players.update_one(
            {"_id": current_user.id},
            {"$inc": {"karma_points": -10, "stats.total_actions": 1}}
        )

        return ActionResponse(
            success=False,
            message=f"Failed to hack {target.username}. They detected your attempt!",
            karma_change=-10,
            trait_changes={"hacking": 1},
            credits_change=0
        )

@router.post("/help", response_model=ActionResponse)
async def help_player(
    action: HelpAction,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Help another player by giving them credits.
    """
    # Get target player
    target_dict = await db.players.find_one({"_id": action.target_id})
    if not target_dict:
        raise HTTPException(status_code=404, detail="Target player not found")

    target = Player(**target_dict)

    # Can't help yourself
    if target.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot help yourself")

    # Check if player has enough credits
    if current_user.currencies.credits < action.amount:
        raise HTTPException(status_code=400, detail="Insufficient credits")

    # Transfer credits
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"currencies.credits": -action.amount}}
    )
    await db.players.update_one(
        {"_id": target.id},
        {"$inc": {"currencies.credits": action.amount}}
    )

    # Calculate karma
    result = calculate_basic_karma("help", current_user, target, action.amount)

    # Apply trait changes
    await apply_trait_changes(db, current_user.id, result["trait_changes"])

    # Update karma
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"karma_points": result["karma_change"]}}
    )

    # Log action
    action_log = Action(
        action_type="help",
        actor_id=current_user.id,
        target_id=target.id,
        amount=action.amount,
        success=True,
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        message=result["message"]
    )
    await db.actions.insert_one(action_log.model_dump(by_alias=True))

    # Update stats
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"stats.total_actions": 1}}
    )

    return ActionResponse(
        success=True,
        message=f"You helped {target.username} with {action.amount} credits. {result['message']}",
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        credits_change=-action.amount
    )

@router.post("/steal", response_model=ActionResponse)
async def steal_from_player(
    action: StealAction,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Steal credits from another player (more aggressive than hacking).
    """
    # Get target player
    target_dict = await db.players.find_one({"_id": action.target_id})
    if not target_dict:
        raise HTTPException(status_code=404, detail="Target player not found")

    target = Player(**target_dict)

    # Can't steal from yourself
    if target.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Cannot steal from yourself")

    # Calculate success chance (stealth-based)
    thief_skill = current_user.traits.stealth + current_user.traits.dexterity
    target_awareness = target.traits.perception + \
        target.meta_traits.survival_instinct

    success_chance = min(
        75, max(15, (thief_skill / (thief_skill + target_awareness)) * 100))
    success = random.random() * 100 < success_chance

    if success:
        # Steal 20-50% of target's credits (more than hacking)
        steal_percentage = random.uniform(0.2, 0.5)
        stolen_amount = int(target.currencies.credits * steal_percentage)

        if stolen_amount > 0:
            # Update credits
            await db.players.update_one(
                {"_id": target.id},
                {"$inc": {"currencies.credits": -stolen_amount}}
            )
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"currencies.credits": stolen_amount}}
            )

            # Calculate karma
            result = calculate_basic_karma(
                "steal", current_user, target, stolen_amount)

            # Apply trait changes
            await apply_trait_changes(db, current_user.id, result["trait_changes"])

            # Update karma
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"karma_points": result["karma_change"]}}
            )

            # Log action
            action_log = Action(
                action_type="steal",
                actor_id=current_user.id,
                target_id=target.id,
                amount=stolen_amount,
                success=True,
                karma_change=result["karma_change"],
                trait_changes=result["trait_changes"],
                message=result["message"]
            )
            await db.actions.insert_one(action_log.model_dump(by_alias=True))

            # Update stats
            await db.players.update_one(
                {"_id": current_user.id},
                {"$inc": {"stats.total_actions": 1, "stats.total_stolen": stolen_amount}}
            )

            return ActionResponse(
                success=True,
                message=f"You stole {stolen_amount} credits from {target.username}! {result['message']}",
                karma_change=result["karma_change"],
                trait_changes=result["trait_changes"],
                credits_change=stolen_amount
            )
        else:
            return ActionResponse(
                success=False,
                message=f"{target.username} has no credits to steal!",
                karma_change=-15,
                trait_changes={"stealth": 1},
                credits_change=0
            )
    else:
        # Failed steal - caught!
        await db.players.update_one(
            {"_id": current_user.id},
            {"$inc": {"karma_points": -20, "stats.total_actions": 1}}
        )

        return ActionResponse(
            success=False,
            message=f"You were caught trying to steal from {target.username}!",
            karma_change=-20,
            trait_changes={"stealth": 1, "reputation": -5},
            credits_change=0
        )

@router.post("/donate", response_model=ActionResponse)
async def donate_to_player(
    action: DonateAction,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Donate credits to another player (more generous than helping).
    """
    # Get target player
    target_dict = await db.players.find_one({"_id": action.target_id})
    if not target_dict:
        raise HTTPException(status_code=404, detail="Target player not found")

    target = Player(**target_dict)

    # Can't donate to yourself
    if target.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Cannot donate to yourself")

    # Check if player has enough credits
    if current_user.currencies.credits < action.amount:
        raise HTTPException(status_code=400, detail="Insufficient credits")

    # Transfer credits
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"currencies.credits": -action.amount}}
    )
    await db.players.update_one(
        {"_id": target.id},
        {"$inc": {"currencies.credits": action.amount}}
    )

    # Calculate karma
    result = calculate_basic_karma(
        "donate", current_user, target, action.amount)

    # Apply trait changes
    await apply_trait_changes(db, current_user.id, result["trait_changes"])

    # Update karma
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"karma_points": result["karma_change"]}}
    )

    # Log action
    action_log = Action(
        action_type="donate",
        actor_id=current_user.id,
        target_id=target.id,
        amount=action.amount,
        success=True,
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        message=result["message"]
    )
    await db.actions.insert_one(action_log.model_dump(by_alias=True))

    # Update stats
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"stats.total_actions": 1, "stats.total_donated": action.amount}}
    )

    return ActionResponse(
        success=True,
        message=f"You donated {action.amount} credits to {target.username}. {result['message']}",
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        credits_change=-action.amount
    )

@router.post("/trade", response_model=ActionResponse)
async def trade_with_player(
    action: TradeAction,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Initiate a trade with another player.
    For now, this is a simplified direct trade (will be expanded with accept/reject later).
    """
    # Get target player
    target_dict = await db.players.find_one({"_id": action.target_id})
    if not target_dict:
        raise HTTPException(status_code=404, detail="Target player not found")

    target = Player(**target_dict)

    # Can't trade with yourself
    if target.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Cannot trade with yourself")

    # Check if both players have enough credits
    if current_user.currencies.credits < action.offer_amount:
        raise HTTPException(
            status_code=400, detail="Insufficient credits for offer")

    if target.currencies.credits < action.request_amount:
        raise HTTPException(
            status_code=400, detail="Target has insufficient credits")

    # Execute trade
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"currencies.credits": -action.offer_amount + action.request_amount}}
    )
    await db.players.update_one(
        {"_id": target.id},
        {"$inc": {"currencies.credits": action.offer_amount - action.request_amount}}
    )

    # Calculate karma
    result = calculate_basic_karma(
        "trade", current_user, target, action.offer_amount)

    # Apply trait changes
    await apply_trait_changes(db, current_user.id, result["trait_changes"])

    # Update karma
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"karma_points": result["karma_change"]}}
    )

    # Log action
    action_log = Action(
        action_type="trade",
        actor_id=current_user.id,
        target_id=target.id,
        amount=action.offer_amount,
        success=True,
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        message=result["message"]
    )
    await db.actions.insert_one(action_log.model_dump(by_alias=True))

    # Update stats
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"stats.total_actions": 1}}
    )

    net_change = action.request_amount - action.offer_amount

    return ActionResponse(
        success=True,
        message=f"Trade completed with {target.username}. {result['message']}",
        karma_change=result["karma_change"],
        trait_changes=result["trait_changes"],
        credits_change=net_change
    )

@router.get("/history")
async def get_action_history(
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = 20
):
    """
    Get action history for current player.
    """
    actions = await db.actions.find(
        {"actor_id": current_user.id}
    ).sort("timestamp", -1).limit(limit).to_list(limit)

    return {"actions": actions, "count": len(actions)}
