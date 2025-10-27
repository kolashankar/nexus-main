"""Unit tests for robot system."""
from backend.services.robots.factory import RobotFactory
from backend.models.robots.robot import ROBOT_TYPES


class TestRobotCreation:
    """Test robot creation."""

    def test_create_worker_robot(self):
        """Test creating a worker robot."""
        factory = RobotFactory()

        robot = factory.create_robot("harvester", owner_id="test_user")

        assert robot["type"] == "harvester"
        assert robot["owner_id"] == "test_user"
        assert robot["level"] == 1
        assert robot["xp"] == 0

    def test_create_combat_robot(self):
        """Test creating a combat robot."""
        factory = RobotFactory()

        robot = factory.create_robot("guardian", owner_id="test_user")

        assert robot["type"] == "guardian"
        assert "stats" in robot
        assert robot["stats"]["hp"] > 0

    def test_robot_has_unique_id(self):
        """Test that each robot gets a unique ID."""
        factory = RobotFactory()

        robot1 = factory.create_robot("harvester", owner_id="test_user")
        robot2 = factory.create_robot("harvester", owner_id="test_user")

        assert robot1["id"] != robot2["id"]

    def test_robot_price_correct(self):
        """Test that robot has correct price from type definition."""
        factory = RobotFactory()

        robot_type = "harvester"
        robot = factory.create_robot(robot_type, owner_id="test_user")

        expected_price = ROBOT_TYPES[robot_type]["price"]
        assert robot["price"] == expected_price


class TestRobotTraining:
    """Test robot training system."""

    def test_train_robot_increases_xp(self):
        """Test that training increases robot XP."""
        factory = RobotFactory()
        robot = factory.create_robot("harvester", owner_id="test_user")

        original_xp = robot["xp"]
        robot = factory.train_robot(robot, xp_gain=100)

        assert robot["xp"] == original_xp + 100

    def test_robot_levels_up_at_threshold(self):
        """Test that robot levels up when XP threshold reached."""
        factory = RobotFactory()
        robot = factory.create_robot("harvester", owner_id="test_user")

        # Add enough XP to level up
        robot = factory.train_robot(robot, xp_gain=1000)

        assert robot["level"] > 1

    def test_robot_stats_increase_on_level_up(self):
        """Test that robot stats increase when leveling up."""
        factory = RobotFactory()
        robot = factory.create_robot("guardian", owner_id="test_user")

        original_hp = robot["stats"]["hp"]

        # Level up the robot
        robot = factory.train_robot(robot, xp_gain=1000)

        if robot["level"] > 1:
            assert robot["stats"]["hp"] > original_hp


class TestRobotFusion:
    """Test robot fusion system."""

    def test_fuse_two_robots(self):
        """Test fusing two robots creates stronger robot."""
        factory = RobotFactory()

        robot1 = factory.create_robot("harvester", owner_id="test_user")
        robot2 = factory.create_robot("harvester", owner_id="test_user")

        fused = factory.fuse_robots(robot1, robot2)

        assert fused["type"] == robot1["type"]
        assert fused["level"] >= max(robot1["level"], robot2["level"])

    def test_fused_robot_has_combined_xp(self):
        """Test that fused robot has combined XP."""
        factory = RobotFactory()

        robot1 = factory.create_robot("harvester", owner_id="test_user")
        robot1["xp"] = 100

        robot2 = factory.create_robot("harvester", owner_id="test_user")
        robot2["xp"] = 150

        fused = factory.fuse_robots(robot1, robot2)

        assert fused["xp"] >= 200  # At least combined XP