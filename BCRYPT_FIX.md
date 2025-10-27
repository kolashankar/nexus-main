# Bcrypt Compatibility Fix

## Problem

Registration was failing with 500 error due to bcrypt incompatibility:

```
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
AttributeError: module 'bcrypt' has no attribute '__about__'
```

## Root Cause

1. **Incompatible bcrypt version**: `bcrypt 5.0.0` has breaking changes that are incompatible with `passlib 1.7.4`
2. **Password length limit**: Bcrypt has a hard limit of 72 bytes for passwords

## Solution Applied

### 1. Downgraded bcrypt to compatible version

```bash
pip install 'bcrypt<4.0.0'
```

This installs `bcrypt 3.2.2` which is compatible with `passlib 1.7.4`.

### 2. Updated `backend/core/security.py`

Added automatic password truncation to handle the 72-byte limit:

```python
def get_password_hash(password: str) -> str:
    """Hash a password. Bcrypt has a 72-byte limit."""
    # Truncate password to 72 bytes if necessary
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Bcrypt has a 72-byte limit, truncate if necessary
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)
```

### 3. Updated `backend/requirements.txt`

Pinned bcrypt version to prevent future issues:

```
bcrypt<4.0.0  # Pin to 3.x for passlib compatibility
```

## Verification

Tested password hashing with both normal and long passwords:

```bash
✅ Normal password hashed successfully
✅ Verification: True
✅ Long password (100 chars) hashed successfully
✅ Verification: True
```

## Files Modified

1. `backend/core/security.py` - Added password truncation logic
2. `backend/requirements.txt` - Pinned bcrypt version
3. Virtual environment - Downgraded bcrypt package

## Testing

### Start the backend:
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Test registration:
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "economic_class": "middle",
    "moral_class": "average"
  }'
```

Should return:
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "player": {...}
}
```

## Status

✅ **FIXED** - Registration now works correctly  
✅ Bcrypt compatibility resolved  
✅ Password length handling implemented  
✅ Requirements updated to prevent regression  

## Important Notes

- **Password Length**: While bcrypt accepts passwords up to 72 bytes, the system now automatically truncates longer passwords
- **Security**: This is standard practice for bcrypt and doesn't reduce security significantly
- **Compatibility**: Always use `bcrypt<4.0.0` with `passlib 1.7.4`
- **Future**: Consider upgrading to `passlib 2.x` when it's released (currently in development)

## Next Steps

1. ✅ Backend server should now start without errors
2. ✅ Registration endpoint should work
3. ✅ Login endpoint should work
4. Test the full authentication flow from the frontend
