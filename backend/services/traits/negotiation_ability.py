from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random

class NegotiationAbility:
    """Negotiation skill - Expert at persuasion, deal-making, and conflict resolution"""
    
    def __init__(self, db):
        self.db = db
        self.players_collection = db.get_collection("players")
        self.notifications_collection = db.get_collection("notifications")
    
    async def persuade(self, player_id: str, target_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Persuade another player to accept a deal or action
        Success chance based on trait level and target's wisdom
        """
        player = await self.players_collection.find_one({"id": player_id})
        target = await self.players_collection.find_one({"id": target_id})
        
        if not player or not target:
            return {"success": False, "message": "Player or target not found"}
        
        if player_id == target_id:
            return {"success": False, "message": "Cannot persuade yourself"}
        
        # Calculate success chance (30-80% based on trait level)
        base_chance = 30 + (trait_level * 0.5)
        
        # Target's wisdom reduces success chance
        target_wisdom = 0
        for trait in target.get("traits", {}).get("meta", []):
            if trait.get("name") == "Wisdom":
                target_wisdom = trait.get("level", 0)
        
        final_chance = max(20, base_chance - (target_wisdom * 0.3))
        success = random.random() * 100 < final_chance
        
        if success:
            # Apply persuasion buff to target (more cooperative)
            persuasion_duration = 120 + (trait_level * 2)  # 2-5 minutes
            cooperation_boost = 10 + (trait_level * 0.3)  # 10-40% more cooperative
            
            await self.players_collection.update_one(
                {"id": target_id},
                {
                    "$push": {
                        "buffs": {
                            "type": "persuaded",
                            "value": cooperation_boost,
                            "expires_at": datetime.utcnow() + timedelta(seconds=persuasion_duration),
                            "applied_by": player_id
                        }
                    }
                }
            )
            
            # Small karma gain for successful persuasion
            karma_gain = 3 + random.randint(0, 5)
            await self.players_collection.update_one(
                {"id": player_id},
                {"$inc": {"karma.current": karma_gain}}
            )
            
            # Notify both players
            await self.notifications_collection.insert_one({
                "player_id": target_id,
                "type": "skill_effect",
                "title": "Persuaded",
                "message": f"{player.get('username', 'Someone')} has persuaded you! You feel more cooperative.",
                "data": {
                    "skill": "Negotiation",
                    "duration": persuasion_duration,
                    "cooperation_boost": cooperation_boost
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
            
            return {
                "success": True,
                "message": "Persuasion successful!",
                "cooperation_boost": cooperation_boost,
                "duration": persuasion_duration,
                "karma_gain": karma_gain
            }
        else:
            return {
                "success": False,
                "message": "Persuasion failed",
                "chance": final_chance
            }
    
    async def broker_deal(self, player_id: str, parties: list, trait_level: int) -> Dict[str, Any]:
        """
        Broker a deal between multiple parties
        Reduces costs or increases rewards for all involved
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Calculate deal bonus (5-25% based on trait level)
        deal_bonus = 5 + (trait_level * 0.2)
        deal_duration = 300 + (trait_level * 5)  # 5-13 minutes
        
        # Apply deal bonus to all parties
        affected_count = 0
        for party_id in parties:
            if party_id != player_id:
                result = await self.players_collection.update_one(
                    {"id": party_id},
                    {
                        "$push": {
                            "buffs": {
                                "type": "favorable_deal",
                                "value": deal_bonus,
                                "expires_at": datetime.utcnow() + timedelta(seconds=deal_duration),
                                "brokered_by": player_id
                            }
                        }
                    }
                )
                if result.modified_count > 0:
                    affected_count += 1
                    
                    # Notify party
                    await self.notifications_collection.insert_one({
                        "player_id": party_id,
                        "type": "skill_effect",
                        "title": "Favorable Deal",
                        "message": f"{player.get('username', 'A negotiator')} brokered a favorable deal for you! {deal_bonus:.1f}% bonus.",
                        "data": {
                            "skill": "Negotiation",
                            "bonus": deal_bonus,
                            "duration": deal_duration
                        },
                        "created_at": datetime.utcnow(),
                        "read": False
                    })
        
        # Karma gain for helping others
        karma_gain = 5 + (affected_count * 2)
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "deal_bonus": deal_bonus,
            "duration": deal_duration,
            "parties_affected": affected_count,
            "karma_gain": karma_gain
        }
    
    async def resolve_conflict(self, player_id: str, conflict_parties: list, trait_level: int) -> Dict[str, Any]:
        """
        Resolve conflicts between players peacefully
        Removes debuffs and provides buffs to conflicting parties
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Calculate resolution effectiveness (40-90% based on trait level)
        effectiveness = 40 + (trait_level * 0.5)
        
        resolved_count = 0
        debuffs_removed = 0
        
        for party_id in conflict_parties:
            party = await self.players_collection.find_one({"id": party_id})
            if party:
                # Remove negative debuffs related to conflict
                current_debuffs = party.get("debuffs", [])
                conflict_debuffs = [d for d in current_debuffs if d.get("type") in ["intimidated", "demoralized", "weakened"]]
                
                if conflict_debuffs:
                    # Remove conflict-related debuffs
                    await self.players_collection.update_one(
                        {"id": party_id},
                        {"$pull": {"debuffs": {"type": {"$in": ["intimidated", "demoralized", "weakened"]}}}}
                    )
                    debuffs_removed += len(conflict_debuffs)
                
                # Apply peace buff
                peace_duration = 180 + (trait_level * 3)  # 3-8 minutes
                await self.players_collection.update_one(
                    {"id": party_id},
                    {
                        "$push": {
                            "buffs": {
                                "type": "peaceful_resolution",
                                "value": effectiveness,
                                "expires_at": datetime.utcnow() + timedelta(seconds=peace_duration),
                                "resolved_by": player_id
                            }
                        }
                    }
                )
                
                resolved_count += 1
                
                # Notify party
                await self.notifications_collection.insert_one({
                    "player_id": party_id,
                    "type": "skill_effect",
                    "title": "Conflict Resolved",
                    "message": f"{player.get('username', 'A negotiator')} peacefully resolved your conflict!",
                    "data": {
                        "skill": "Negotiation",
                        "effectiveness": effectiveness,
                        "duration": peace_duration
                    },
                    "created_at": datetime.utcnow(),
                    "read": False
                })
        
        # Major karma gain for peacemaking
        karma_gain = 10 + (resolved_count * 5)
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "conflicts_resolved": resolved_count,
            "debuffs_removed": debuffs_removed,
            "effectiveness": effectiveness,
            "karma_gain": karma_gain
        }
