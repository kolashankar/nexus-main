"""Location-based task spawning service."""

import random
from typing import Dict, Any, List, Tuple
from backend.models.tasks.task_location import TaskLocation

class LocationSpawner:
    """Spawns tasks at specific locations in the game world."""
    
    # Predefined locations in the game world
    GAME_LOCATIONS = [
        {
            "name": "Central Plaza",
            "zone": "city",
            "coordinates": {"x": 0, "y": 0, "z": 0},
            "radius": 100,
            "description": "The heart of the city, always bustling with activity",
            "is_dangerous": False,
            "required_level": 1,
            "task_types": ["social", "economic", "relationship"]
        },
        {
            "name": "Wasteland Outpost",
            "zone": "wasteland",
            "coordinates": {"x": 500, "y": 0, "z": -300},
            "radius": 75,
            "description": "A small outpost on the edge of the wasteland",
            "is_dangerous": True,
            "required_level": 5,
            "task_types": ["combat", "exploration", "survival"]
        },
        {
            "name": "Tech District",
            "zone": "city",
            "coordinates": {"x": -200, "y": 0, "z": 150},
            "radius": 80,
            "description": "High-tech area with advanced facilities",
            "is_dangerous": False,
            "required_level": 3,
            "task_types": ["skill_based", "economic", "hacking"]
        },
        {
            "name": "Guild Halls",
            "zone": "city",
            "coordinates": {"x": 300, "y": 0, "z": 200},
            "radius": 60,
            "description": "Where guilds gather and compete",
            "is_dangerous": False,
            "required_level": 5,
            "task_types": ["guild", "social", "combat"]
        },
        {
            "name": "Black Market",
            "zone": "underground",
            "coordinates": {"x": -400, "y": -50, "z": -200},
            "radius": 50,
            "description": "Shady deals and illegal trade",
            "is_dangerous": True,
            "required_level": 8,
            "task_types": ["economic", "combat", "ethical_dilemma"]
        },
        {
            "name": "Refugee Camp",
            "zone": "wasteland",
            "coordinates": {"x": 250, "y": 0, "z": -500},
            "radius": 90,
            "description": "Those displaced by the wasteland wars",
            "is_dangerous": False,
            "required_level": 3,
            "task_types": ["relationship", "ethical_dilemma", "social"]
        },
        {
            "name": "Arena",
            "zone": "city",
            "coordinates": {"x": 100, "y": 0, "z": -100},
            "radius": 70,
            "description": "Where warriors prove their worth",
            "is_dangerous": True,
            "required_level": 10,
            "task_types": ["combat", "competitive", "guild"]
        },
        {
            "name": "Research Lab",
            "zone": "city",
            "coordinates": {"x": -300, "y": 0, "z": 300},
            "radius": 55,
            "description": "Scientific research and experiments",
            "is_dangerous": False,
            "required_level": 7,
            "task_types": ["ethical_dilemma", "skill_based", "exploration"]
        }
    ]
    
    def get_location_for_task_type(self, task_type: str, player_level: int) -> TaskLocation:
        """Get a suitable location for a task type."""
        # Filter locations by task type and player level
        suitable_locations = [
            loc for loc in self.GAME_LOCATIONS
            if task_type in loc["task_types"] and player_level >= loc["required_level"]
        ]
        
        if not suitable_locations:
            # Fallback to Central Plaza
            suitable_locations = [self.GAME_LOCATIONS[0]]
        
        location_data = random.choice(suitable_locations)
        
        return TaskLocation(
            name=location_data["name"],
            zone=location_data["zone"],
            coordinates=location_data["coordinates"],
            radius=location_data["radius"],
            description=location_data["description"],
            is_dangerous=location_data["is_dangerous"],
            required_level=location_data["required_level"]
        )
    
    def calculate_distance(self, pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """Calculate 3D distance between two positions."""
        dx = pos1.get("x", 0) - pos2.get("x", 0)
        dy = pos1.get("y", 0) - pos2.get("y", 0)
        dz = pos1.get("z", 0) - pos2.get("z", 0)
        
        return (dx**2 + dy**2 + dz**2) ** 0.5
    
    def is_player_at_location(self, player_position: Dict[str, float], location: TaskLocation) -> bool:
        """Check if player is within location radius."""
        distance = self.calculate_distance(player_position, location.coordinates)
        return distance <= location.radius
    
    def get_nearby_locations(self, player_position: Dict[str, float], max_distance: float = 200) -> List[Dict[str, Any]]:
        """Get all locations within a certain distance."""
        nearby = []
        
        for location_data in self.GAME_LOCATIONS:
            distance = self.calculate_distance(player_position, location_data["coordinates"])
            
            if distance <= max_distance:
                nearby.append({
                    **location_data,
                    "distance": round(distance, 1)
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x["distance"])
        
        return nearby
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        """Get all available locations."""
        return self.GAME_LOCATIONS.copy()
    
    def add_location_to_task(self, task_data: Dict[str, Any], player_level: int) -> Dict[str, Any]:
        """Add location requirement to a task."""
        task_type = task_data.get("type", "moral_choice")
        location = self.get_location_for_task_type(task_type, player_level)
        
        task_data["location_requirement"] = location.model_dump()
        
        return task_data
    
    def generate_random_position_in_location(self, location: TaskLocation) -> Dict[str, float]:
        """Generate a random position within a location's radius."""
        # Random angle and distance
        angle = random.uniform(0, 2 * 3.14159)  # 0 to 2π
        distance = random.uniform(0, location.radius * 0.8)  # Stay within 80% of radius
        
        # Calculate offset
        x_offset = distance * random.uniform(-1, 1)
        z_offset = distance * random.uniform(-1, 1)
        
        return {
            "x": location.coordinates["x"] + x_offset,
            "y": location.coordinates["y"],
            "z": location.coordinates["z"] + z_offset
        }
