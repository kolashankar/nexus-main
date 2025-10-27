"""Load testing configuration for Karma Nexus using Locust"""

from locust import HttpUser, task, between
import random


class KarmaNexusUser(HttpUser):
    """Simulated user for load testing"""

    wait_time = between(1, 5)

    def on_start(self):
        """Login when user starts"""
        response = self.client.post("/api/auth/login", json={
            "username": f"loadtest_user_{random.randint(1, 1000)}",
            "password": "testpass123"
        })

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            # Register if login fails
            register_response = self.client.post("/api/auth/register", json={
                "username": f"loadtest_user_{random.randint(1, 1000)}",
                "email": f"loadtest_{random.randint(1, 1000)}@test.com",
                "password": "testpass123"
            })

            if register_response.status_code in [200, 201]:
                # Login again
                login_response = self.client.post("/api/auth/login", json={
                    "username": f"loadtest_user_{random.randint(1, 1000)}",
                    "password": "testpass123"
                })
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(10)
    def view_profile(self):
        """View player profile"""
        self.client.get("/api/player/profile", headers=self.headers)

    @task(8)
    def view_traits(self):
        """View player traits"""
        self.client.get("/api/player/traits", headers=self.headers)

    @task(5)
    def view_quests(self):
        """View available quests"""
        self.client.get("/api/quests/available", headers=self.headers)

    @task(5)
    def view_marketplace(self):
        """View robot marketplace"""
        self.client.get("/api/robots/marketplace", headers=self.headers)

    @task(3)
    def view_leaderboards(self):
        """View karma leaderboard"""
        self.client.get("/api/leaderboards/karma")

    @task(2)
    def perform_action(self):
        """Perform a game action"""
        actions = ['hack', 'help', 'donate']
        action = random.choice(actions)

        self.client.post(
            f"/api/actions/{action}",
            json={"target_player_id": f"player_{random.randint(1, 100)}"},
            headers=self.headers
        )

    @task(2)
    def view_guilds(self):
        """View guild list"""
        self.client.get("/api/guilds/list", headers=self.headers)

    @task(1)
    def view_combat_stats(self):
        """View combat statistics"""
        self.client.get("/api/combat/stats", headers=self.headers)

    @task(1)
    def view_stocks(self):
        """View stock market"""
        self.client.get("/api/market/stocks", headers=self.headers)


class IntensiveUser(HttpUser):
    """User performing intensive operations"""

    wait_time = between(0.5, 2)

    def on_start(self):
        """Login when user starts"""
        response = self.client.post("/api/auth/login", json={
            "username": f"intensive_user_{random.randint(1, 100)}",
            "password": "testpass123"
        })

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def rapid_actions(self):
        """Rapidly perform multiple actions"""
        for _ in range(5):
            self.client.get("/api/player/profile", headers=self.headers)
            self.client.get("/api/player/traits", headers=self.headers)
            self.client.get("/api/quests/active", headers=self.headers)
