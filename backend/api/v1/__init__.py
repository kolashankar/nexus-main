"""API v1 package - Import all routers."""

from .auth import router as auth_router
from .player import router as player_router
from .actions import router as actions_router

# Combat
try:
    from .combat import router as combat_router
except ImportError:
    combat_router = None

# Robots
try:
    from .robots import router as robots_router
except ImportError:
    robots_router = None

# Guilds
try:
    from .guilds import router as guilds_router
except ImportError:
    guilds_router = None

# Quests
try:
    from .quests import router as quests_router
except ImportError:
    quests_router = None

# Market
try:
    from .market import router as market_router
except ImportError:
    market_router = None

# Social
try:
    from .social import router as social_router
except ImportError:
    social_router = None

# Karma
try:
    from .karma import router as karma_router
except ImportError:
    karma_router = None

# Leaderboards
try:
    from .leaderboards import router as leaderboards_router
except ImportError:
    leaderboards_router = None

# Tournaments
try:
    from .tournaments import router as tournaments_router
except ImportError:
    tournaments_router = None

# Achievements
try:
    from .achievements import router as achievements_router
except ImportError:
    achievements_router = None

# AI Companion
try:
    from .ai import router as ai_companion_router
except ImportError:
    ai_companion_router = None

# World
try:
    from .world import router as world_router
except ImportError:
    world_router = None

# Seasonal
try:
    from .seasonal import router as seasonal_router
except ImportError:
    seasonal_router = None


# Create module-level exports
auth = type('AuthModule', (), {'router': auth_router})()
player = type('PlayerModule', (), {'router': player_router})()
actions = type('ActionsModule', (), {'router': actions_router})()
combat = type('CombatModule', (), {
              'router': combat_router})() if combat_router else None
robots = type('RobotsModule', (), {
              'router': robots_router})() if robots_router else None
guilds = type('GuildsModule', (), {
              'router': guilds_router})() if guilds_router else None
quests = type('QuestsModule', (), {
              'router': quests_router})() if quests_router else None
market = type('MarketModule', (), {
              'router': market_router})() if market_router else None
social = type('SocialModule', (), {
              'router': social_router})() if social_router else None
karma = type('KarmaModule', (), {'router': karma_router})(
) if karma_router else None
leaderboards = type('LeaderboardsModule', (), {
                    'router': leaderboards_router})() if leaderboards_router else None
tournaments = type('TournamentsModule', (), {
                   'router': tournaments_router})() if tournaments_router else None
achievements = type('AchievementsModule', (), {
                    'router': achievements_router})() if achievements_router else None
ai_companion = type('AICompanionModule', (), {
                    'router': ai_companion_router})() if ai_companion_router else None
world = type('WorldModule', (), {'router': world_router})(
) if world_router else None
seasonal = type('SeasonalModule', (), {
                'router': seasonal_router})() if seasonal_router else None

__all__ = [
    'auth',
    'player',
    'actions',
    'combat',
    'robots',
    'guilds',
    'quests',
    'market',
    'social',
    'karma',
    'leaderboards',
    'tournaments',
    'achievements',
    'ai_companion',
    'world',
    'seasonal'
]
