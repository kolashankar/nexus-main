"""
Authentication Handlers
8-Level Nested Architecture: routes/auth/management/operations/handlers/auth_handlers.py
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class AuthHandlers:
    """Handlers for Authentication operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.admin_collection = db.admin_users
        self.user_collection = db.app_users
    
    # =============================================================================
    # PASSWORD UTILITIES
    # =============================================================================
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None
    
    # =============================================================================
    # ADMIN AUTHENTICATION
    # =============================================================================
    
    async def register_admin(self, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new admin user"""
        # Check if admin already exists
        existing_admin = await self.admin_collection.find_one({
            "$or": [
                {"email": admin_data["email"]},
                {"username": admin_data["username"]}
            ]
        })
        
        if existing_admin:
            return {"success": False, "message": "Admin with this email or username already exists"}
        
        # Hash password
        password = admin_data.pop("password")
        admin_data["password_hash"] = self.hash_password(password)
        
        # Set timestamps
        admin_data["created_at"] = datetime.utcnow()
        admin_data["updated_at"] = datetime.utcnow()
        admin_data["last_login"] = None
        admin_data["is_active"] = True
        
        # Insert admin
        result = await self.admin_collection.insert_one(admin_data)
        admin_data["_id"] = result.inserted_id
        
        # Create token
        token_data = {
            "sub": str(result.inserted_id),
            "email": admin_data["email"],
            "user_type": "admin",
            "role": admin_data.get("role", "admin")
        }
        access_token = self.create_access_token(token_data)
        
        return {
            "success": True,
            "message": "Admin registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user_type": "admin",
            "user_id": str(result.inserted_id),
            "email": admin_data["email"],
            "full_name": admin_data["full_name"]
        }
    
    async def login_admin(self, email: str, password: str) -> Dict[str, Any]:
        """Admin login"""
        admin = await self.admin_collection.find_one({"email": email})
        
        if not admin:
            return {"success": False, "message": "Invalid email or password"}
        
        if not admin.get("is_active", True):
            return {"success": False, "message": "Account is deactivated"}
        
        if not self.verify_password(password, admin["password_hash"]):
            return {"success": False, "message": "Invalid email or password"}
        
        # Update last login
        await self.admin_collection.update_one(
            {"_id": admin["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create token
        token_data = {
            "sub": str(admin["_id"]),
            "email": admin["email"],
            "user_type": "admin",
            "role": admin.get("role", "admin")
        }
        access_token = self.create_access_token(token_data)
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user_type": "admin",
            "user_id": str(admin["_id"]),
            "email": admin["email"],
            "full_name": admin["full_name"]
        }
    
    # =============================================================================
    # APP USER AUTHENTICATION
    # =============================================================================
    
    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new app user"""
        # Check if user already exists
        existing_user = await self.user_collection.find_one({"email": user_data["email"]})
        
        if existing_user:
            return {"success": False, "message": "User with this email already exists"}
        
        # Hash password
        password = user_data.pop("password")
        user_data["password_hash"] = self.hash_password(password)
        
        # Set default values
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        user_data["last_login"] = None
        user_data["is_active"] = True
        user_data["is_verified"] = False
        user_data["career_tools_used"] = 0
        user_data.setdefault("skills", [])
        
        # Insert user
        result = await self.user_collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        
        # Create token
        token_data = {
            "sub": str(result.inserted_id),
            "email": user_data["email"],
            "user_type": "user"
        }
        access_token = self.create_access_token(token_data)
        
        return {
            "success": True,
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user_type": "user",
            "user_id": str(result.inserted_id),
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        }
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """App user login"""
        user = await self.user_collection.find_one({"email": email})
        
        if not user:
            return {"success": False, "message": "Invalid email or password"}
        
        if not user.get("is_active", True):
            return {"success": False, "message": "Account is deactivated"}
        
        if not self.verify_password(password, user["password_hash"]):
            return {"success": False, "message": "Invalid email or password"}
        
        # Update last login
        await self.user_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create token
        token_data = {
            "sub": str(user["_id"]),
            "email": user["email"],
            "user_type": "user"
        }
        access_token = self.create_access_token(token_data)
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user_type": "user",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"]
        }
    
    # =============================================================================
    # TOKEN VERIFICATION
    # =============================================================================
    
    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from token"""
        payload = self.verify_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        user_type = payload.get("user_type")
        
        if not user_id or not user_type:
            return None
        
        try:
            if user_type == "admin":
                user = await self.admin_collection.find_one({"_id": ObjectId(user_id)})
            else:
                user = await self.user_collection.find_one({"_id": ObjectId(user_id)})
            
            if user:
                user["id"] = str(user.pop("_id"))
                user["user_type"] = user_type
                return user
            
            return None
        except Exception:
            return None
    
    # =============================================================================
    # PROFILE MANAGEMENT
    # =============================================================================
    
    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.user_collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                result["id"] = str(result.pop("_id"))
                result.pop("password_hash", None)  # Remove password hash from response
                return {"success": True, "user": result}
            
            return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def change_password(self, user_id: str, user_type: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        try:
            collection = self.admin_collection if user_type == "admin" else self.user_collection
            user = await collection.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return {"success": False, "message": "User not found"}
            
            if not self.verify_password(old_password, user["password_hash"]):
                return {"success": False, "message": "Invalid old password"}
            
            new_hash = self.hash_password(new_password)
            
            await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password_hash": new_hash, "updated_at": datetime.utcnow()}}
            )
            
            return {"success": True, "message": "Password changed successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}


    # =============================================================================
    # SUB-ADMIN MANAGEMENT (Super Admin Only)
    # =============================================================================
    
    async def create_sub_admin(self, admin_data: Dict[str, Any], creator_role: str) -> Dict[str, Any]:
        """Create a new sub-admin (only super_admin can do this)"""
        # Only super admins can create sub-admins
        if creator_role != "super_admin":
            return {"success": False, "message": "Only super admins can create sub-admins"}
        
        # Check if admin already exists
        existing_admin = await self.admin_collection.find_one({
            "$or": [
                {"email": admin_data["email"]},
                {"username": admin_data["username"]}
            ]
        })
        
        if existing_admin:
            return {"success": False, "message": "Admin with this email or username already exists"}
        
        # Hash password
        password = admin_data.pop("password")
        admin_data["password_hash"] = self.hash_password(password)
        
        # Set timestamps and defaults
        admin_data["created_at"] = datetime.utcnow()
        admin_data["updated_at"] = datetime.utcnow()
        admin_data["last_login"] = None
        admin_data["is_active"] = True
        admin_data["role"] = admin_data.get("role", "sub_admin")  # Default to sub_admin
        
        # Insert admin
        result = await self.admin_collection.insert_one(admin_data)
        
        return {
            "success": True,
            "message": "Sub-admin created successfully",
            "admin_id": str(result.inserted_id),
            "email": admin_data["email"],
            "username": admin_data["username"],
            "role": admin_data["role"]
        }
    
    async def get_all_admins(
        self,
        skip: int = 0,
        limit: int = 50,
        role: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of all admins"""
        query = {}
        if role:
            query["role"] = role
        
        total = await self.admin_collection.count_documents(query)
        cursor = self.admin_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        admins = await cursor.to_list(length=limit)
        
        # Format admins
        formatted_admins = []
        for admin in admins:
            admin["id"] = str(admin.pop("_id"))
            admin.pop("password_hash", None)
            if "created_at" in admin and admin["created_at"]:
                admin["created_at"] = admin["created_at"].isoformat()
            if "updated_at" in admin and admin["updated_at"]:
                admin["updated_at"] = admin["updated_at"].isoformat()
            if "last_login" in admin and admin["last_login"]:
                admin["last_login"] = admin["last_login"].isoformat()
            formatted_admins.append(admin)
        
        return {
            "success": True,
            "admins": formatted_admins,
            "total": total,
            "page": (skip // limit) + 1,
            "limit": limit
        }
    
    async def get_admin_by_id(self, admin_id: str) -> Optional[Dict[str, Any]]:
        """Get single admin by ID"""
        try:
            admin = await self.admin_collection.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin["id"] = str(admin.pop("_id"))
                admin.pop("password_hash", None)
                if "created_at" in admin and admin["created_at"]:
                    admin["created_at"] = admin["created_at"].isoformat()
                if "updated_at" in admin and admin["updated_at"]:
                    admin["updated_at"] = admin["updated_at"].isoformat()
                if "last_login" in admin and admin["last_login"]:
                    admin["last_login"] = admin["last_login"].isoformat()
                return admin
            return None
        except Exception:
            return None
    
    async def update_admin(self, admin_id: str, update_data: Dict[str, Any], updater_role: str) -> Dict[str, Any]:
        """Update admin details (only super_admin can do this)"""
        if updater_role != "super_admin":
            return {"success": False, "message": "Only super admins can update admin details"}
        
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            # Don't allow changing password through this endpoint
            update_data.pop("password", None)
            update_data.pop("password_hash", None)
            
            result = await self.admin_collection.find_one_and_update(
                {"_id": ObjectId(admin_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                result["id"] = str(result.pop("_id"))
                result.pop("password_hash", None)
                return {"success": True, "admin": result}
            
            return {"success": False, "message": "Admin not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_admin(self, admin_id: str, deleter_role: str) -> Dict[str, Any]:
        """Delete admin (only super_admin can do this)"""
        if deleter_role != "super_admin":
            return {"success": False, "message": "Only super admins can delete admins"}
        
        try:
            # Check if trying to delete super admin
            admin = await self.admin_collection.find_one({"_id": ObjectId(admin_id)})
            if not admin:
                return {"success": False, "message": "Admin not found"}
            
            if admin.get("role") == "super_admin":
                return {"success": False, "message": "Cannot delete super admin"}
            
            result = await self.admin_collection.delete_one({"_id": ObjectId(admin_id)})
            return {
                "success": result.deleted_count > 0,
                "message": "Admin deleted successfully" if result.deleted_count > 0 else "Admin not found"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def toggle_admin_status(self, admin_id: str, toggler_role: str) -> Dict[str, Any]:
        """Toggle admin active status (only super_admin can do this)"""
        if toggler_role != "super_admin":
            return {"success": False, "message": "Only super admins can toggle admin status"}
        
        try:
            admin = await self.admin_collection.find_one({"_id": ObjectId(admin_id)})
            if not admin:
                return {"success": False, "message": "Admin not found"}
            
            if admin.get("role") == "super_admin":
                return {"success": False, "message": "Cannot toggle super admin status"}
            
            new_status = not admin.get("is_active", True)
            
            await self.admin_collection.update_one(
                {"_id": ObjectId(admin_id)},
                {"$set": {"is_active": new_status, "updated_at": datetime.utcnow()}}
            )
            
            return {
                "success": True,
                "is_active": new_status,
                "message": f"Admin {'activated' if new_status else 'deactivated'} successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
