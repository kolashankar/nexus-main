"""
Seed Default Admin User
Creates the default admin user if it doesn't exist
Email: kolashankar113@gmail.com
Password: Shankar@113
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)
db = client['careerguide']
admin_users_collection = db['admin_users']

# Default admin credentials
DEFAULT_ADMIN_EMAIL = "kolashankar113@gmail.com"
DEFAULT_ADMIN_PASSWORD = "Shankar@113"
DEFAULT_ADMIN_USERNAME = "kolashankar"
DEFAULT_ADMIN_FULLNAME = "Kola Shankar"

def create_default_admin():
    """Create default admin user if doesn't exist"""
    
    # Check if admin already exists
    existing_admin = admin_users_collection.find_one({"email": DEFAULT_ADMIN_EMAIL})
    
    if existing_admin:
        print(f"✓ Default admin already exists: {DEFAULT_ADMIN_EMAIL}")
        return
    
    # Hash the password
    password_hash = pwd_context.hash(DEFAULT_ADMIN_PASSWORD)
    
    # Create admin document
    admin_doc = {
        "email": DEFAULT_ADMIN_EMAIL,
        "username": DEFAULT_ADMIN_USERNAME,
        "password_hash": password_hash,
        "full_name": DEFAULT_ADMIN_FULLNAME,
        "role": "super_admin",  # Super admin with full permissions
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None
    }
    
    # Insert into database
    result = admin_users_collection.insert_one(admin_doc)
    
    if result.inserted_id:
        print(f"✓ Default admin created successfully!")
        print(f"  Email: {DEFAULT_ADMIN_EMAIL}")
        print(f"  Username: {DEFAULT_ADMIN_USERNAME}")
        print(f"  Password: {DEFAULT_ADMIN_PASSWORD}")
        print(f"  Role: super_admin")
    else:
        print("✗ Failed to create default admin")

if __name__ == "__main__":
    try:
        create_default_admin()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
