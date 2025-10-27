# Karma Nexus API Documentation

Complete API reference for Karma Nexus 2.0.

## Base URL

```
https://api.karmanexus.com/api
```

**Local Development:**
```
http://localhost:8001/api
```

## Authentication

Karma Nexus uses JWT (JSON Web Tokens) for authentication.

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "player123",
  "email": "player@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "username": "player123",
    "email": "player@example.com"
  }
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "player123",
  "password": "securePassword123"
}
```

### Using the Token
Include the token in the Authorization header:

```http
GET /player/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user
- `POST /auth/refresh` - Refresh token

### Player
- `GET /player/profile` - Get player profile
- `PUT /player/profile` - Update profile
- `GET /player/{player_id}` - Get other player (respects privacy)
- `GET /player/traits` - Get all traits
- `GET /player/superpowers` - Get unlocked superpowers
- `GET /player/skill-trees` - Get skill tree progress
- `POST /player/skill-trees/unlock` - Unlock skill node

### Actions
- `POST /actions/hack` - Hack another player
- `POST /actions/help` - Help another player
- `POST /actions/steal` - Steal from player
- `POST /actions/donate` - Donate to player
- `POST /actions/trade` - Trade with player
- `GET /actions/history` - Get action history

### Combat
- `POST /combat/challenge` - Challenge player to duel
- `POST /combat/accept` - Accept duel
- `POST /combat/action` - Perform combat action
- `GET /combat/state` - Get current combat state
- `POST /combat/arena/join` - Join arena queue

### Robots
- `GET /robots/marketplace` - Browse robot marketplace
- `POST /robots/purchase` - Buy a robot
- `GET /robots/my-robots` - Get owned robots
- `POST /robots/train` - Train a robot
- `POST /robots/fuse` - Fuse two robots

### Guilds
- `POST /guilds/create` - Create guild
- `GET /guilds/list` - List all guilds
- `POST /guilds/join` - Join guild
- `GET /guilds/{guild_id}` - Get guild details
- `POST /guilds/declare-war` - Declare war
- `GET /guilds/territories` - Get controlled territories

### Quests
- `GET /quests/available` - Get available quests
- `GET /quests/active` - Get active quests
- `POST /quests/accept` - Accept quest
- `POST /quests/complete` - Complete quest
- `GET /quests/campaign` - Get campaign quests

### Market
- `GET /market/stocks` - Get stock prices
- `POST /market/stocks/buy` - Buy stocks
- `POST /market/stocks/sell` - Sell stocks
- `GET /market/items` - Browse item marketplace

### Social
- `GET /social/nearby` - Get nearby players
- `POST /social/message` - Send message
- `POST /social/alliance` - Form alliance
- `POST /social/rival/declare` - Declare rival
- `POST /social/marry` - Propose marriage

### Leaderboards
- `GET /leaderboards/karma` - Karma leaderboard
- `GET /leaderboards/wealth` - Wealth leaderboard
- `GET /leaderboards/combat` - Combat leaderboard
- `GET /leaderboards/guilds` - Guild leaderboard

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('wss://api.karmanexus.com/ws');

// Authenticate
ws.send(JSON.stringify({
  type: 'authenticate',
  token: 'your_jwt_token'
}));
```

### Events

**Server → Client:**
- `player_joined` - Player entered area
- `action_performed` - Action occurred nearby
- `karma_changed` - Your karma changed
- `trait_updated` - Trait level changed
- `event_triggered` - World event occurred
- `combat_update` - Combat state changed
- `notification` - System notification

**Client → Server:**
- `join_room` - Join a room/area
- `chat_message` - Send chat message
- `location_update` - Update position

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per user
- **WebSocket**: 50 messages per second

Headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password",
    "details": {}
  }
}
```

### Common Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Pagination

For list endpoints:

```http
GET /quests/available?page=1&limit=20
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

## Examples

See individual endpoint documentation:
- [Authentication](./authentication.md)
- [Player Endpoints](./player.md)
- [Combat System](./combat.md)
- [Guild Endpoints](./guilds.md)
- [WebSocket Events](./websocket.md)

## SDKs

- **JavaScript/TypeScript**: `npm install @karmanexus/sdk`
- **Python**: `pip install karmanexus-sdk`
- **More coming soon**

## Support

- **Documentation Issues**: [GitHub Issues](https://github.com/karmanexus/docs/issues)
- **API Support**: [api-support@karmanexus.com](mailto:api-support@karmanexus.com)
- **Discord**: [Join our community](https://discord.gg/karmanexus)
