from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# JWT secret
JWT_SECRET = os.environ.get("JWT_SECRET")
ALGORITHM = "HS256"

# Example user
user_id = "fighter0"

# Expiration time (timezone-aware UTC)
expire = datetime.now(tz=timezone.utc) + timedelta(minutes=30)

# Create JWT token
token = jwt.encode({"sub": user_id, "exp": expire}, JWT_SECRET, algorithm=ALGORITHM)

print("Your token:", token)
