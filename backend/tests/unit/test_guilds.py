"""Unit tests for guild system."""
import pytest
from backend.services.guilds.management import GuildService


class TestGuildCreation:
    """Test guild creation."""

    def test_create_guild_basic(self):
        """Test creating a basic guild."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="test_user",
            description="A test guild"
        )

        assert guild["name"] == "Test Guild"
        assert guild["tag"] == "TEST"
        assert guild["leader_id"] == "test_user"
        assert len(guild["members"]) == 1
        assert guild["members"][0]["player_id"] == "test_user"
        assert guild["members"][0]["rank"] == "leader"

    def test_guild_tag_length_validation(self):
        """Test that guild tag must be 3-5 characters."""
        service = GuildService()

        # Too short
        with pytest.raises(ValueError):
            service.create_guild(
                name="Test Guild",
                tag="AB",
                leader_id="test_user"
            )

        # Too long
        with pytest.raises(ValueError):
            service.create_guild(
                name="Test Guild",
                tag="TOOLONG",
                leader_id="test_user"
            )

    def test_guild_starts_at_level_1(self):
        """Test that new guilds start at level 1."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="test_user"
        )

        assert guild["level"] == 1
        assert guild["xp"] == 0


class TestGuildMembership:
    """Test guild membership management."""

    def test_add_member_to_guild(self):
        """Test adding a member to guild."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="leader"
        )

        updated_guild = service.add_member(guild, player_id="new_member")

        assert len(updated_guild["members"]) == 2
        assert any(m["player_id"] ==
                   "new_member" for m in updated_guild["members"])

    def test_new_member_has_recruit_rank(self):
        """Test that new members start as recruits."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="leader"
        )

        updated_guild = service.add_member(guild, player_id="new_member")

        new_member = next(
            m for m in updated_guild["members"] if m["player_id"] == "new_member")
        assert new_member["rank"] == "recruit"

    def test_remove_member_from_guild(self):
        """Test removing a member from guild."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="leader"
        )

        guild = service.add_member(guild, player_id="member1")
        guild = service.add_member(guild, player_id="member2")

        updated_guild = service.remove_member(guild, player_id="member1")

        assert len(updated_guild["members"]) == 2  # Leader + member2
        assert not any(m["player_id"] ==
                       "member1" for m in updated_guild["members"])

    def test_cannot_remove_leader(self):
        """Test that guild leader cannot be removed."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="leader"
        )

        with pytest.raises(ValueError):
            service.remove_member(guild, player_id="leader")

    def test_promote_member(self):
        """Test promoting a guild member."""
        service = GuildService()

        guild = service.create_guild(
            name="Test Guild",
            tag="TEST",
            leader_id="leader"
        )

        guild = service.add_member(guild, player_id="member1")
        updated_guild = service.promote_member(guild, player_id="member1")

        member = next(
            m for m in updated_guild["members"] if m["player_id"] == "member1")
        assert member["rank"] != "recruit"


class TestGuildWars:
    """Test guild war system."""

    def test_declare_war(self):
        """Test declaring war on another guild."""
        service = GuildService()

        guild1 = service.create_guild("Guild 1", "GLD1", "leader1")
        guild2 = service.create_guild("Guild 2", "GLD2", "leader2")

        updated_guild = service.declare_war(
            guild1, enemy_guild_id=guild2["_id"])

        assert len(updated_guild["active_wars"]) == 1
        assert updated_guild["active_wars"][0]["enemy_guild_id"] == guild2["_id"]
        assert updated_guild["active_wars"][0]["status"] == "active"

    def test_cannot_declare_war_on_self(self):
        """Test that guild cannot declare war on itself."""
        service = GuildService()

        guild = service.create_guild("Test Guild", "TEST", "leader")

        with pytest.raises(ValueError):
            service.declare_war(guild, enemy_guild_id=guild["_id"])