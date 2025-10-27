from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from .schemas import LoginRequest, RegisterRequest, TokenResponse
from backend.core.database import get_database
from backend.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from backend.models.player.player import Player, PlayerCreate, PlayerResponse

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Register a new player.
    """
    # Check if username exists
    existing_user = await db.players.find_one({"username": request.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    existing_email = await db.players.find_one({"email": request.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create player
    player_data = PlayerCreate(
        username=request.username,
        email=request.email,
        password=request.password,
        economic_class=request.economic_class,
        moral_class=request.moral_class
    )

    # Hash password
    password_hash = get_password_hash(player_data.password)

    # Create player object
    player = Player(
        username=player_data.username,
        email=player_data.email,
        password_hash=password_hash,
        economic_class=player_data.economic_class,
        moral_class=player_data.moral_class,
        last_login=datetime.utcnow()
    )

    # Insert into database
    player_dict = player.model_dump(by_alias=True)
    await db.players.insert_one(player_dict)

    # Create access token
    access_token = create_access_token(
        data={"sub": player.id, "username": player.username})

    # Create response
    player_response = PlayerResponse.from_player(
        player, requester_id=player.id)

    return TokenResponse(
        access_token=access_token,
        player=player_response.model_dump()
    )

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Login with email and password.
    """
    # Find user by email
    user_dict = await db.players.find_one({"email": request.email})
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(request.password, user_dict["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create player object
    player = Player(**user_dict)

    # Update last login
    await db.players.update_one(
        {"_id": player.id},
        {"$set": {"last_login": datetime.utcnow(), "online": True}}
    )
    player.last_login = datetime.utcnow()
    player.online = True

    # Create access token
    access_token = create_access_token(
        data={"sub": player.id, "username": player.username})

    # Create response
    player_response = PlayerResponse.from_player(
        player, requester_id=player.id)

    return TokenResponse(
        access_token=access_token,
        player=player_response.model_dump()
    )

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Logout current user.
    """
    # Decode token
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Update online status
    await db.players.update_one(
        {"_id": payload.get("sub")},
        {"$set": {"online": False}}
    )

    return {"message": "Successfully logged out"}

@router.get("/me", response_model=PlayerResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get current authenticated user.
    """
    # Decode token
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Get user from database
    user_dict = await db.players.find_one({"_id": payload.get("sub")})
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    player = Player(**user_dict)
    return PlayerResponse.from_player(player, requester_id=player.id)

# Dependency for getting current user
async def get_current_user_dep(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Player:
    """Dependency to get current authenticated player."""
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user_dict = await db.players.find_one({"_id": payload.get("sub")})
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return Player(**user_dict)
