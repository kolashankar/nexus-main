"""Locust load testing configuration."""
from locust import HttpUser, task, between
import random


class KarmaNexusUser(HttpUser):
    """Simulated Karma Nexus user for load testing."""

    wait_time = between(1, 3)
    token = None
    username = None

    def on_start(self):
        """Register and login when user starts."""
        # Register new user
        user_id = random.randint(1000, 999999)
        self.username = f"loadtest_{user_id}"

        response = self.client.post("/api/auth/register", json={
            "username": self.username,
            "email": f"{self.username}@example.com",
            "password": "testpass123"
        })

        if response.status_code == 200:
            self.token = response.json().get("access_token")

    def get_headers(self):
        """Get auth headers."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(10)
    def view_profile(self):
        """View player profile (most common action)."""
        self.client.get("/api/player/profile", headers=self.get_headers())

    @task(5)
    def view_traits(self):
        """View player traits."""
        self.client.get("/api/player/traits", headers=self.get_headers())

    @task(3)
    def perform_help_action(self):
        """Perform help action."""
        # Random target username
        target = f"loadtest_{random.randint(1000, 999999)}"
        self.client.post(
            "/api/actions/help",
            headers=self.get_headers(),
            json={
                "target_username": target,
                "amount": random.randint(50, 200)
            }
        )

    @task(2)
    def view_leaderboard(self):
        """View karma leaderboard."""
        self.client.get("/api/leaderboards/karma", headers=self.get_headers())

    @task(2)
    def get_quests(self):
        """Get available quests."""
        self.client.get("/api/quests/available", headers=self.get_headers())

    @task(1)
    def view_robots(self):
        """View robot marketplace."""
        self.client.get("/api/robots/marketplace", headers=self.get_headers())

    @task(1)
    def view_guilds(self):
        """View guild list."""
        self.client.get("/api/guilds/list", headers=self.get_headers())


class AdminUser(HttpUser):
    """Simulated admin user for testing admin endpoints."""

    wait_time = between(5, 10)

    @task
    def view_stats(self):
        """View admin stats."""
        self.client.get("/api/admin/stats")


class WebSocketUser(HttpUser):
    """Simulated WebSocket user."""

    wait_time = between(2, 5)

    @task(5)
    def connect_websocket(self):
        """Test WebSocket connection."""
        # Note: Locust has limited WebSocket support
        # This is a placeholder for WebSocket load testing
        pass