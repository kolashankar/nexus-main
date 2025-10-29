"""Trait evolution tracker - tracks changes in player traits over time."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

class TraitEvolutionTracker:
    """Tracks and analyzes trait evolution over time."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.snapshots_collection = db.trait_snapshots
        self.history_collection = db.task_history
    
    async def create_trait_snapshot(
        self,
        player_id: str,
        traits: Dict[str, float],
        source: str = "manual"
    ) -> Dict:
        """Create a snapshot of player's current traits.
        
        Args:
            player_id: Player's ID
            traits: Current trait values
            source: Source of snapshot (manual, automatic, task_completion)
        
        Returns:
            Snapshot record
        """
        snapshot = {
            "_id": f"snapshot_{datetime.now().strftime('%Y%m%d%H%M%S')}_{player_id[:8]}",
            "player_id": player_id,
            "timestamp": datetime.now(),
            "traits": traits,
            "source": source
        }
        
        await self.snapshots_collection.insert_one(snapshot)
        return snapshot
    
    async def get_trait_evolution(
        self,
        player_id: str,
        trait_name: Optional[str] = None,
        days: int = 30
    ) -> Dict:
        """Get trait evolution data for charting.
        
        Args:
            player_id: Player's ID
            trait_name: Specific trait to track (or all if None)
            days: Number of days to retrieve
        
        Returns:
            Evolution data for charting
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Get snapshots
        snapshots = await self.snapshots_collection.find({
            "player_id": player_id,
            "timestamp": {"$gte": start_date}
        }).sort("timestamp", 1).to_list(length=1000)
        
        if not snapshots:
            return {
                "player_id": player_id,
                "trait_name": trait_name,
                "data_points": [],
                "summary": {
                    "start_value": 0,
                    "end_value": 0,
                    "total_change": 0,
                    "trend": "stable"
                }
            }
        
        # Extract data points
        if trait_name:
            # Single trait evolution
            data_points = [
                {
                    "timestamp": snapshot["timestamp"].isoformat(),
                    "value": snapshot["traits"].get(trait_name, 50)
                }
                for snapshot in snapshots
            ]
            
            start_value = data_points[0]["value"] if data_points else 50
            end_value = data_points[-1]["value"] if data_points else 50
            total_change = end_value - start_value
            
            # Determine trend
            if total_change > 5:
                trend = "increasing"
            elif total_change < -5:
                trend = "decreasing"
            else:
                trend = "stable"
            
            return {
                "player_id": player_id,
                "trait_name": trait_name,
                "data_points": data_points,
                "summary": {
                    "start_value": round(start_value, 1),
                    "end_value": round(end_value, 1),
                    "total_change": round(total_change, 1),
                    "trend": trend
                }
            }
        else:
            # All traits evolution
            all_traits = set()
            for snapshot in snapshots:
                all_traits.update(snapshot["traits"].keys())
            
            traits_evolution = {}
            for trait in all_traits:
                data_points = [
                    {
                        "timestamp": snapshot["timestamp"].isoformat(),
                        "value": snapshot["traits"].get(trait, 50)
                    }
                    for snapshot in snapshots
                ]
                
                start_value = data_points[0]["value"] if data_points else 50
                end_value = data_points[-1]["value"] if data_points else 50
                total_change = end_value - start_value
                
                traits_evolution[trait] = {
                    "data_points": data_points,
                    "start_value": round(start_value, 1),
                    "end_value": round(end_value, 1),
                    "total_change": round(total_change, 1)
                }
            
            return {
                "player_id": player_id,
                "traits_evolution": traits_evolution,
                "period_days": days
            }
    
    async def get_trait_changes_from_tasks(
        self,
        player_id: str,
        days: int = 30
    ) -> List[Dict]:
        """Get trait changes caused by task completions.
        
        Args:
            player_id: Player's ID
            days: Number of days to retrieve
        
        Returns:
            List of trait changes from tasks
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Get task history with trait changes
        history = await self.history_collection.find({
            "player_id": player_id,
            "completed_at": {"$gte": start_date},
            "trait_changes": {"$ne": None, "$ne": {}}
        }).sort("completed_at", 1).to_list(length=500)
        
        changes = []
        for record in history:
            trait_changes = record.get("trait_changes", {})
            if trait_changes:
                changes.append({
                    "timestamp": record["completed_at"].isoformat(),
                    "task_title": record.get("task_title"),
                    "task_type": record.get("task_type"),
                    "trait_changes": trait_changes,
                    "choice_made": record.get("choice_made", {}).get("text") if record.get("choice_made") else None
                })
        
        return changes
    
    async def get_trait_milestones(
        self,
        player_id: str,
        trait_name: str
    ) -> List[Dict]:
        """Get milestones reached for a specific trait.
        
        Args:
            player_id: Player's ID
            trait_name: Name of the trait
        
        Returns:
            List of milestone achievements
        """
        milestones = [25, 50, 75, 100]
        
        # Get all snapshots for this trait
        snapshots = await self.snapshots_collection.find({
            "player_id": player_id
        }).sort("timestamp", 1).to_list(length=5000)
        
        if not snapshots:
            return []
        
        achieved_milestones = []
        previous_value = 0
        
        for snapshot in snapshots:
            current_value = snapshot["traits"].get(trait_name, 50)
            
            # Check if crossed any milestone
            for milestone in milestones:
                if previous_value < milestone <= current_value:
                    achieved_milestones.append({
                        "milestone": milestone,
                        "achieved_at": snapshot["timestamp"].isoformat(),
                        "trait_name": trait_name
                    })
            
            previous_value = current_value
        
        return achieved_milestones
    
    async def get_trait_velocity(
        self,
        player_id: str,
        days: int = 7
    ) -> Dict[str, float]:
        """Calculate rate of change for each trait.
        
        Args:
            player_id: Player's ID
            days: Period to calculate velocity over
        
        Returns:
            Dictionary mapping trait names to velocity (points per day)
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Get snapshots in period
        snapshots = await self.snapshots_collection.find({
            "player_id": player_id,
            "timestamp": {"$gte": start_date}
        }).sort("timestamp", 1).to_list(length=1000)
        
        if len(snapshots) < 2:
            return {}
        
        first_snapshot = snapshots[0]
        last_snapshot = snapshots[-1]
        
        time_diff_days = (last_snapshot["timestamp"] - first_snapshot["timestamp"]).days
        if time_diff_days == 0:
            time_diff_days = 1  # Avoid division by zero
        
        velocities = {}
        all_traits = set(first_snapshot["traits"].keys()) | set(last_snapshot["traits"].keys())
        
        for trait in all_traits:
            start_value = first_snapshot["traits"].get(trait, 50)
            end_value = last_snapshot["traits"].get(trait, 50)
            change = end_value - start_value
            velocity = change / time_diff_days
            
            velocities[trait] = round(velocity, 2)
        
        return velocities
    
    async def predict_trait_value(
        self,
        player_id: str,
        trait_name: str,
        days_ahead: int = 7
    ) -> Dict:
        """Predict future trait value based on current velocity.
        
        Args:
            player_id: Player's ID
            trait_name: Name of the trait
            days_ahead: Number of days to predict
        
        Returns:
            Prediction data
        """
        # Get current velocity
        velocities = await self.trait_velocity(player_id, days=7)
        velocity = velocities.get(trait_name, 0)
        
        # Get current value
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "error": "Player not found"
            }
        
        current_value = player.get("traits", {}).get(trait_name, 50)
        predicted_value = current_value + (velocity * days_ahead)
        
        # Clamp to 0-100
        predicted_value = max(0, min(100, predicted_value))
        
        confidence = "high" if abs(velocity) > 1 else "low"
        
        return {
            "trait_name": trait_name,
            "current_value": round(current_value, 1),
            "predicted_value": round(predicted_value, 1),
            "days_ahead": days_ahead,
            "velocity": velocity,
            "confidence": confidence
        }
    
    async def auto_create_snapshots(
        self,
        interval_hours: int = 6
    ) -> int:
        """Auto-create trait snapshots for all active players.
        
        Args:
            interval_hours: Hours between snapshots
        
        Returns:
            Number of snapshots created
        """
        cutoff_time = datetime.now() - timedelta(hours=interval_hours)
        
        # Find players who need new snapshots
        pipeline = [
            {
                "$lookup": {
                    "from": "trait_snapshots",
                    "localField": "_id",
                    "foreignField": "player_id",
                    "as": "recent_snapshots"
                }
            },
            {
                "$match": {
                    "$or": [
                        {"recent_snapshots": {"$size": 0}},
                        {"recent_snapshots.timestamp": {"$lt": cutoff_time}}
                    ]
                }
            }
        ]
        
        cursor = self.db.players.aggregate(pipeline)
        players = await cursor.to_list(length=1000)
        
        snapshots_created = 0
        for player in players:
            if "traits" in player:
                await self.create_trait_snapshot(
                    player_id=player["_id"],
                    traits=player["traits"],
                    source="automatic"
                )
                snapshots_created += 1
        
        return snapshots_created
