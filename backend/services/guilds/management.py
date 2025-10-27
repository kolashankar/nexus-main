from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.guilds.guild import Guild, GuildMember, GuildRank


class GuildManagementService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.guilds = db.guilds
        self.players = db.players

    async def create_guild(self, name: str, tag: str, description: str, leader_id: str) -> Guild:
        """Create a new guild"""
        # Check if tag is unique
        existing = await self.guilds.find_one({"tag": tag})
        if existing:
            raise ValueError("Guild tag already exists")

        # Create guild
        guild = Guild(
            name=name,
            tag=tag,
            description=description,
            leader_id=leader_id,
            members=[GuildMember(player_id=leader_id, rank=GuildRank.LEADER)],
            total_members=1
        )

        await self.guilds.insert_one(guild.model_dump())

        # Update player's guild
        await self.players.update_one(
            {"_id": leader_id},
            {"$set": {
                "guild_id": guild.id,
                "guild_rank": GuildRank.LEADER.value
            }}
        )

        return guild

    async def join_guild(self, guild_id: str, player_id: str) -> bool:
        """Player joins a guild"""
        guild = await self.guilds.find_one({"id": guild_id})
        if not guild:
            raise ValueError("Guild not found")

        # Check if guild is full
        if guild.get("total_members", 0) >= guild.get("max_members", 50):
            raise ValueError("Guild is full")

        # Check if recruitment is open
        if not guild.get("recruitment_open", True):
            raise ValueError("Guild recruitment is closed")

        # Add member
        new_member = GuildMember(player_id=player_id, rank=GuildRank.RECRUIT)

        await self.guilds.update_one(
            {"id": guild_id},
            {
                "$push": {"members": new_member.model_dump()},
                "$inc": {"total_members": 1}
            }
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$set": {
                "guild_id": guild_id,
                "guild_rank": GuildRank.RECRUIT.value
            }}
        )

        return True

    async def leave_guild(self, guild_id: str, player_id: str) -> bool:
        """Player leaves guild"""
        guild = await self.guilds.find_one({"id": guild_id})
        if not guild:
            raise ValueError("Guild not found")

        # Can't leave if you're the leader
        if guild.get("leader_id") == player_id:
            raise ValueError(
                "Leader must transfer leadership or disband guild")

        # Remove member
        await self.guilds.update_one(
            {"id": guild_id},
            {
                "$pull": {"members": {"player_id": player_id}},
                "$inc": {"total_members": -1}
            }
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$unset": {"guild_id": "", "guild_rank": ""}}
        )

        return True

    async def kick_member(self, guild_id: str, player_id: str, kicker_id: str) -> bool:
        """Kick a member from guild"""
        guild = await self.guilds.find_one({"id": guild_id})
        if not guild:
            raise ValueError("Guild not found")

        # Check permissions (only leader and officers can kick)
        kicker_member = next(
            (m for m in guild.get("members", [])
             if m.get("player_id") == kicker_id),
            None
        )

        if not kicker_member or kicker_member.get("rank") not in ["leader", "officer"]:
            raise ValueError("Insufficient permissions")

        # Can't kick the leader
        if guild.get("leader_id") == player_id:
            raise ValueError("Cannot kick the leader")

        # Remove member
        await self.guilds.update_one(
            {"id": guild_id},
            {
                "$pull": {"members": {"player_id": player_id}},
                "$inc": {"total_members": -1}
            }
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$unset": {"guild_id": "", "guild_rank": ""}}
        )

        return True

    async def promote_member(self, guild_id: str, player_id: str, new_rank: GuildRank, promoter_id: str) -> bool:
        """Promote/demote a member"""
        guild = await self.guilds.find_one({"id": guild_id})
        if not guild:
            raise ValueError("Guild not found")

        # Only leader can promote
        if guild.get("leader_id") != promoter_id:
            raise ValueError("Only leader can promote members")

        # Can't promote to leader
        if new_rank == GuildRank.LEADER:
            raise ValueError("Use transfer_leadership for this")

        # Update member rank
        await self.guilds.update_one(
            {"id": guild_id, "members.player_id": player_id},
            {"$set": {"members.$.rank": new_rank.value}}
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$set": {"guild_rank": new_rank.value}}
        )

        return True

    async def contribute_to_bank(self, guild_id: str, player_id: str, credits: int) -> bool:
        """Contribute credits to guild bank"""
        # Check player has enough credits
        player = await self.players.find_one({"_id": player_id})
        if not player or player.get("currencies", {}).get("credits", 0) < credits:
            raise ValueError("Insufficient credits")

        # Transfer credits
        await self.players.update_one(
            {"_id": player_id},
            {"$inc": {"currencies.credits": -credits}}
        )

        await self.guilds.update_one(
            {"id": guild_id},
            {"$inc": {"guild_bank.credits": credits}}
        )

        # Update member contribution
        await self.guilds.update_one(
            {"id": guild_id, "members.player_id": player_id},
            {"$inc": {"members.$.contribution": credits}}
        )

        return True

    async def get_guild(self, guild_id: str) -> Optional[dict]:
        """Get guild by ID"""
        return await self.guilds.find_one({"id": guild_id})

    async def list_guilds(self, skip: int = 0, limit: int = 20) -> List[dict]:
        """List all guilds"""
        cursor = self.guilds.find({}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_guild_members(self, guild_id: str) -> List[dict]:
        """Get all guild members with player details"""
        guild = await self.guilds.find_one({"id": guild_id})
        if not guild:
            return []

        member_ids = [m.get("player_id") for m in guild.get("members", [])]
        cursor = self.players.find({"_id": {"$in": member_ids}})
        return await cursor.to_list(length=len(member_ids))
