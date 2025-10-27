from typing import List, Dict, Optional


class PropertyTypes:
    """Defines available property types and their characteristics."""

    def __init__(self):
        self.properties = self._initialize_properties()

    def _initialize_properties(self) -> Dict[str, Dict]:
        """Initialize property database."""
        return {
            "apartment_1": {
                "id": "apartment_1",
                "name": "Downtown Apartment",
                "description": "Cozy apartment in the city center",
                "property_type": "apartment",
                "size": 60,
                "location": {"x": 100, "y": 200, "territory_id": 1},
                "territory_id": 1,
                "price": 50000,
                "passive_income": 100,
                "maintenance_cost": 20,
                "status": "available",
                "upgrades": []
            },
            "house_1": {
                "id": "house_1",
                "name": "Suburban House",
                "description": "Spacious house in quiet neighborhood",
                "property_type": "house",
                "size": 150,
                "location": {"x": 300, "y": 400, "territory_id": 2},
                "territory_id": 2,
                "price": 150000,
                "passive_income": 300,
                "maintenance_cost": 50,
                "status": "available",
                "upgrades": []
            },
            "mansion_1": {
                "id": "mansion_1",
                "name": "Luxury Mansion",
                "description": "Opulent mansion with premium amenities",
                "property_type": "mansion",
                "size": 500,
                "location": {"x": 500, "y": 600, "territory_id": 3},
                "territory_id": 3,
                "price": 1000000,
                "passive_income": 2000,
                "maintenance_cost": 200,
                "status": "available",
                "upgrades": []
            },
            "commercial_1": {
                "id": "commercial_1",
                "name": "Retail Space",
                "description": "Prime commercial location for business",
                "property_type": "commercial",
                "size": 200,
                "location": {"x": 700, "y": 800, "territory_id": 1},
                "territory_id": 1,
                "price": 300000,
                "passive_income": 800,
                "maintenance_cost": 100,
                "status": "available",
                "upgrades": []
            },
            "industrial_1": {
                "id": "industrial_1",
                "name": "Warehouse Complex",
                "description": "Large warehouse for storage and operations",
                "property_type": "industrial",
                "size": 1000,
                "location": {"x": 900, "y": 1000, "territory_id": 4},
                "territory_id": 4,
                "price": 500000,
                "passive_income": 1500,
                "maintenance_cost": 150,
                "status": "available",
                "upgrades": []
            },
            "penthouse_1": {
                "id": "penthouse_1",
                "name": "Sky Penthouse",
                "description": "Ultra-luxury penthouse with panoramic views",
                "property_type": "apartment",
                "size": 300,
                "location": {"x": 150, "y": 250, "territory_id": 1},
                "territory_id": 1,
                "price": 2000000,
                "passive_income": 3000,
                "maintenance_cost": 300,
                "status": "available",
                "upgrades": []
            },
            "office_tower": {
                "id": "office_tower",
                "name": "Corporate Tower",
                "description": "High-rise office building",
                "property_type": "commercial",
                "size": 5000,
                "location": {"x": 800, "y": 900, "territory_id": 1},
                "territory_id": 1,
                "price": 5000000,
                "passive_income": 10000,
                "maintenance_cost": 500,
                "status": "available",
                "upgrades": []
            },
            "tech_lab": {
                "id": "tech_lab",
                "name": "Research Laboratory",
                "description": "State-of-the-art research facility",
                "property_type": "industrial",
                "size": 2000,
                "location": {"x": 1100, "y": 1200, "territory_id": 5},
                "territory_id": 5,
                "price": 3000000,
                "passive_income": 5000,
                "maintenance_cost": 400,
                "status": "available",
                "upgrades": []
            }
        }

    def get_all_properties(self) -> List[Dict]:
        """Get all properties."""
        return list(self.properties.values())

    def get_property_by_id(self, property_id: str) -> Optional[Dict]:
        """Get a property by ID."""
        return self.properties.get(property_id)

    def get_properties_by_type(self, property_type: str) -> List[Dict]:
        """Get properties by type."""
        return [
            prop for prop in self.properties.values()
            if prop.get("property_type") == property_type
        ]

    def get_properties_by_territory(self, territory_id: int) -> List[Dict]:
        """Get properties in a specific territory."""
        return [
            prop for prop in self.properties.values()
            if prop.get("territory_id") == territory_id
        ]
