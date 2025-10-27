# 📁 KARMA NEXUS - COMPLETE PROJECT STRUCTURE

## 5-Level Nested Folder Architecture

This document provides the complete folder structure for Karma Nexus, organized for scalability and maintainability.

---

## 📂 Root Structure Overview

```
/app/
├── backend/                    # FastAPI backend (Python)
├── frontend/                   # React frontend (JavaScript/TypeScript)
├── shared/                     # Shared resources and configs
├── tests/                      # Test suites
├── scripts/                    # Utility scripts
├── docs/                       # Documentation
├── assets/                     # Raw assets (pre-build)
├── .gitignore
├── README.md
├── idea.md
├── implementation_status.md
└── questions.md
```

---

## 🔧 BACKEND STRUCTURE (/app/backend/)

```
backend/
│
├── server.py                   # Main FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .env.example               # Environment template
├── pyproject.toml             # Poetry config (optional)
├── pytest.ini                 # Pytest configuration
│
├── api/                        # API routes layer
│   ├── __init__.py
│   ├── deps.py                # Dependency injection utilities
│   │
│   ├── v1/                    # API version 1
│   │   ├── __init__.py
│   │   │
│   │   ├── auth/              # Authentication endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # Auth routes
│   │   │   ├── schemas.py     # Pydantic models for auth
│   │   │   └── utils.py       # Auth helpers (JWT, hashing)
│   │   │
│   │   ├── player/            # Player management endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── profile/       # Player profile sub-routes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── traits/        # Traits management
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── superpowers/   # Superpowers management
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   └── skill_trees/   # Skill trees
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── schemas.py
│   │   │
│   │   ├── actions/           # Game actions endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── hack.py        # Hacking actions
│   │   │   ├── help.py        # Helping actions
│   │   │   ├── steal.py       # Stealing actions
│   │   │   ├── donate.py      # Donation actions
│   │   │   └── trade.py       # Trading actions
│   │   │
│   │   ├── combat/            # Combat system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── duel/          # PvP duels
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── arena/         # Arena battles
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   └── abilities/     # Combat abilities
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── robots/            # Robot system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── marketplace/   # Robot marketplace
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── training/      # Robot training
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── battles/       # Robot battles
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   └── chips/         # Robot chips
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── guilds/            # Guild system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── management/    # Guild management
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── wars/          # Guild wars
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── territories/   # Territory control
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   └── quests/        # Guild quests
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── quests/            # Quest system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── personal/      # Personal quests
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── daily/         # Daily quests
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── weekly/        # Weekly quests
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── campaigns/     # Story campaigns
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   └── world/         # World quests
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── market/            # Market system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── stocks/        # Stock market
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── items/         # Item marketplace
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   └── real_estate/   # Real estate
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── social/            # Social features endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── alliances/     # Alliances
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── rivals/        # Rival system
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── marriage/      # Marriage system
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── mentorship/    # Mentor/apprentice
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   └── chat/          # Chat system
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── karma/             # Karma system endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── events/        # Karma events
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   └── world/         # World karma state
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   ├── leaderboards/      # Leaderboards endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── tournaments/       # Tournaments endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── achievements/      # Achievements endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── ai/                # AI interactions endpoints
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── companion/     # AI companion
│   │   │       ├── __init__.py
│   │   │       └── router.py
│   │   │
│   │   └── admin/             # Admin endpoints
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── schemas.py
│   │
│   └── websocket/             # WebSocket handlers
│       ├── __init__.py
│       ├── manager.py         # Connection manager
│       ├── handlers.py        # Event handlers
│       └── events/            # Event types
│           ├── __init__.py
│           ├── player.py      # Player events
│           ├── combat.py      # Combat events
│           ├── chat.py        # Chat events
│           └── world.py       # World events
│
├── core/                      # Core application components
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── security.py           # Security utilities
│   ├── database.py           # Database connection
│   └── constants.py          # Application constants
│
├── models/                    # Database models
│   ├── __init__.py
│   ├── base.py               # Base model class
│   │
│   ├── player/               # Player-related models
│   │   ├── __init__.py
│   │   ├── player.py         # Main player model
│   │   ├── traits.py         # Traits model
│   │   ├── superpowers.py    # Superpowers model
│   │   ├── skill_trees.py    # Skill trees model
│   │   └── appearance.py     # Appearance model
│   │
│   ├── actions/              # Action models
│   │   ├── __init__.py
│   │   ├── action.py         # Base action model
│   │   └── history.py        # Action history
│   │
│   ├── combat/               # Combat models
│   │   ├── __init__.py
│   │   ├── battle.py         # Battle model
│   │   └── stats.py          # Combat stats
│   │
│   ├── robots/               # Robot models
│   │   ├── __init__.py
│   │   ├── robot.py          # Robot model
│   │   └── chips.py          # Chip model
│   │
│   ├── guilds/               # Guild models
│   │   ├── __init__.py
│   │   ├── guild.py          # Guild model
│   │   ├── member.py         # Member model
│   │   └── territory.py      # Territory model
│   │
│   ├── quests/               # Quest models
│   │   ├── __init__.py
│   │   ├── quest.py          # Quest model
│   │   └── campaign.py       # Campaign model
│   │
│   ├── market/               # Market models
│   │   ├── __init__.py
│   │   ├── stock.py          # Stock model
│   │   └── listing.py        # Marketplace listing
│   │
│   ├── karma/                # Karma models
│   │   ├── __init__.py
│   │   ├── event.py          # Karma event model
│   │   └── world_state.py    # World state model
│   │
│   └── social/               # Social models
│       ├── __init__.py
│       ├── relationship.py   # Relationship model
│       └── message.py        # Message model
│
├── services/                  # Business logic services
│   ├── __init__.py
│   │
│   ├── ai/                   # AI services (The Pantheon)
│   │   ├── __init__.py
│   │   ├── base.py           # Base AI service
│   │   │
│   │   ├── karma_arbiter/    # The Karma Arbiter
│   │   │   ├── __init__.py
│   │   │   ├── arbiter.py    # Main arbiter logic
│   │   │   ├── prompts.py    # System prompts
│   │   │   ├── evaluator.py  # Action evaluation
│   │   │   └── cache.py      # Response caching
│   │   │
│   │   ├── oracle/           # The Oracle (Quest Generator)
│   │   │   ├── __init__.py
│   │   │   ├── oracle.py     # Main oracle logic
│   │   │   ├── prompts.py    # Quest prompts
│   │   │   ├── generator.py  # Quest generation
│   │   │   └── templates.py  # Quest templates
│   │   │
│   │   ├── economist/        # The Economist (Market AI)
│   │   │   ├── __init__.py
│   │   │   ├── economist.py  # Main economist logic
│   │   │   ├── market.py     # Market management
│   │   │   ├── pricing.py    # Price calculations
│   │   │   └── events.py     # Economic events
│   │   │
│   │   ├── warlord/          # The Warlord (Combat AI)
│   │   │   ├── __init__.py
│   │   │   ├── warlord.py    # Main warlord logic
│   │   │   ├── combat.py     # Combat management
│   │   │   ├── balance.py    # PvP balancing
│   │   │   └── guild_wars.py # Guild war logic
│   │   │
│   │   ├── architect/        # The Architect (World Events)
│   │   │   ├── __init__.py
│   │   │   ├── architect.py  # Main architect logic
│   │   │   ├── events.py     # Event generation
│   │   │   ├── triggers.py   # Event triggers
│   │   │   └── world.py      # World management
│   │   │
│   │   └── companion/        # AI Companions (Personal NPCs)
│   │       ├── __init__.py
│   │       ├── companion.py  # Main companion logic
│   │       ├── personality.py # Personality system
│   │       ├── dialogue.py   # Dialogue generation
│   │       └── advice.py     # Advice system
│   │
│   ├── player/               # Player services
│   │   ├── __init__.py
│   │   ├── profile.py        # Profile management
│   │   ├── traits.py         # Traits management
│   │   ├── progression.py    # Level/XP system
│   │   ├── superpowers.py    # Superpower unlocking
│   │   ├── skill_trees.py    # Skill tree logic
│   │   └── prestige.py       # Prestige system
│   │
│   ├── actions/              # Action services
│   │   ├── __init__.py
│   │   ├── handler.py        # Action handler
│   │   ├── validator.py      # Action validation
│   │   └── processor.py      # Action processing
│   │
│   ├── combat/               # Combat services
│   │   ├── __init__.py
│   │   ├── engine.py         # Combat engine
│   │   ├── calculator.py     # Damage calculation
│   │   ├── abilities.py      # Ability system
│   │   └── arena.py          # Arena management
│   │
│   ├── robots/               # Robot services
│   │   ├── __init__.py
│   │   ├── factory.py        # Robot creation
│   │   ├── training.py       # Training system
│   │   ├── marketplace.py    # Marketplace logic
│   │   └── fusion.py         # Robot fusion
│   │
│   ├── guilds/               # Guild services
│   │   ├── __init__.py
│   │   ├── management.py     # Guild management
│   │   ├── wars.py           # War system
│   │   ├── territories.py    # Territory control
│   │   └── quests.py         # Guild quests
│   │
│   ├── quests/               # Quest services
│   │   ├── __init__.py
│   │   ├── manager.py        # Quest management
│   │   ├── progression.py    # Quest progression
│   │   └── rewards.py        # Reward distribution
│   │
│   ├── market/               # Market services
│   │   ├── __init__.py
│   │   ├── stocks.py         # Stock market
│   │   ├── trading.py        # Trading logic
│   │   └── pricing.py        # Price management
│   │
│   ├── social/               # Social services
│   │   ├── __init__.py
│   │   ├── relationships.py  # Relationship management
│   │   ├── messaging.py      # Messaging system
│   │   └── reputation.py     # Reputation system
│   │
│   ├── karma/                # Karma services
│   │   ├── __init__.py
│   │   ├── calculator.py     # Karma calculation
│   │   ├── events.py         # Event management
│   │   └── world_state.py    # World state tracking
│   │
│   └── economy/              # Economy services
│       ├── __init__.py
│       ├── currency.py       # Currency management
│       ├── transactions.py   # Transaction handling
│       └── rewards.py        # Reward system
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── validators.py         # Data validators
│   ├── helpers.py            # Helper functions
│   ├── formatters.py         # Data formatters
│   ├── cache.py              # Caching utilities
│   └── logger.py             # Logging setup
│
├── middleware/                # Custom middleware
│   ├── __init__.py
│   ├── auth.py               # Auth middleware
│   ├── rate_limit.py         # Rate limiting
│   ├── logging.py            # Request logging
│   └── error_handler.py      # Error handling
│
├── tasks/                     # Background tasks
│   ├── __init__.py
│   ├── karma_processor.py    # Process karma evaluations
│   ├── quest_generator.py    # Generate quests
│   ├── market_updater.py     # Update market prices
│   ├── world_events.py       # Trigger world events
│   └── cleanup.py            # Cleanup tasks
│
└── tests/                     # Backend tests
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures
    │
    ├── unit/                 # Unit tests
    │   ├── __init__.py
    │   ├── test_karma.py
    │   ├── test_traits.py
    │   └── test_combat.py
    │
    ├── integration/          # Integration tests
    │   ├── __init__.py
    │   ├── test_actions.py
    │   └── test_quests.py
    │
    └── e2e/                  # End-to-end tests
        ├── __init__.py
        └── test_game_flow.py
```

---

## ⚛️ FRONTEND STRUCTURE (/app/frontend/)

```
frontend/
│
├── package.json              # Node dependencies
├── yarn.lock                 # Yarn lock file
├── tsconfig.json            # TypeScript config
├── tailwind.config.js       # Tailwind CSS config
├── postcss.config.js        # PostCSS config
├── vite.config.js           # Vite config (if using Vite)
├── .env                     # Environment variables
├── .env.example            # Environment template
│
├── public/                  # Static assets
│   ├── index.html
│   ├── favicon.ico
│   ├── manifest.json       # PWA manifest
│   ├── robots.txt
│   │
│   ├── models/             # 3D models (static)
│   │   ├── characters/
│   │   │   ├── base_male.glb
│   │   │   └── base_female.glb
│   │   ├── robots/
│   │   │   ├── worker_bot.glb
│   │   │   └── combat_bot.glb
│   │   └── environment/
│   │       └── city_block.glb
│   │
│   └── textures/           # Textures
│       ├── characters/
│       └── environment/
│
├── src/                    # Source code
│   ├── index.tsx          # Entry point
│   ├── App.tsx            # Root component
│   ├── App.css            # Global styles
│   ├── index.css          # Base styles
│   │
│   ├── components/        # Reusable components
│   │   ├── ui/           # Shadcn UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── toast.tsx
│   │   │   ├── sonner.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── slider.tsx
│   │   │   ├── tooltip.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── accordion.tsx
│   │   │   ├── alert.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── calendar.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── radio-group.tsx
│   │   │   ├── scroll-area.tsx
│   │   │   ├── separator.tsx
│   │   │   ├── sheet.tsx
│   │   │   ├── skeleton.tsx
│   │   │   └── switch.tsx
│   │   │
│   │   ├── layout/       # Layout components
│   │   │   ├── Header/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Header.css
│   │   │   │   ├── UserMenu.tsx
│   │   │   │   ├── Notifications.tsx
│   │   │   │   └── QuickStats.tsx
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Sidebar.css
│   │   │   │   ├── NavItem.tsx
│   │   │   │   └── OnlinePlayers.tsx
│   │   │   ├── Footer/
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Footer.css
│   │   │   └── Container/
│   │   │       ├── Container.tsx
│   │   │       └── Container.css
│   │   │
│   │   ├── player/       # Player-related components
│   │   │   ├── ProfileCard/
│   │   │   │   ├── ProfileCard.tsx
│   │   │   │   ├── ProfileCard.css
│   │   │   │   ├── Avatar3D.tsx
│   │   │   │   └── StatsDisplay.tsx
│   │   │   ├── TraitsList/
│   │   │   │   ├── TraitsList.tsx
│   │   │   │   ├── TraitsList.css
│   │   │   │   ├── TraitItem.tsx
│   │   │   │   ├── TraitBar.tsx
│   │   │   │   └── TraitFilters.tsx
│   │   │   ├── SuperpowersList/
│   │   │   │   ├── SuperpowersList.tsx
│   │   │   │   ├── SuperpowerCard.tsx
│   │   │   │   └── PowerActivation.tsx
│   │   │   ├── SkillTree/
│   │   │   │   ├── SkillTree.tsx
│   │   │   │   ├── SkillTree.css
│   │   │   │   ├── SkillNode.tsx
│   │   │   │   ├── SkillBranch.tsx
│   │   │   │   └── SkillTooltip.tsx
│   │   │   └── Inventory/
│   │   │       ├── Inventory.tsx
│   │   │       ├── InventoryGrid.tsx
│   │   │       └── ItemCard.tsx
│   │   │
│   │   ├── game/         # Game world components
│   │   │   ├── GameWorld/
│   │   │   │   ├── GameWorld.tsx
│   │   │   │   ├── GameWorld.css
│   │   │   │   ├── Scene3D.tsx
│   │   │   │   ├── Camera.tsx
│   │   │   │   ├── Lighting.tsx
│   │   │   │   └── Environment.tsx
│   │   │   ├── PlayerAvatar/
│   │   │   │   ├── PlayerAvatar.tsx
│   │   │   │   ├── Avatar3DModel.tsx
│   │   │   │   ├── AvatarAnimations.tsx
│   │   │   │   └── NameTag.tsx
│   │   │   ├── NPCs/
│   │   │   │   ├── AICompanion.tsx
│   │   │   │   ├── CompanionDialog.tsx
│   │   │   │   └── CompanionAvatar.tsx
│   │   │   └── WorldMap/
│   │   │       ├── WorldMap.tsx
│   │   │       ├── Territory.tsx
│   │   │       └── Minimap.tsx
│   │   │
│   │   ├── combat/       # Combat components
│   │   │   ├── CombatArena/
│   │   │   │   ├── CombatArena.tsx
│   │   │   │   ├── CombatArena.css
│   │   │   │   ├── BattleField3D.tsx
│   │   │   │   └── CombatHUD.tsx
│   │   │   ├── ActionBar/
│   │   │   │   ├── ActionBar.tsx
│   │   │   │   ├── ActionButton.tsx
│   │   │   │   └── CooldownTimer.tsx
│   │   │   ├── HealthBar/
│   │   │   │   ├── HealthBar.tsx
│   │   │   │   └── HealthBar.css
│   │   │   └── AbilityMenu/
│   │   │       ├── AbilityMenu.tsx
│   │   │       └── AbilityCard.tsx
│   │   │
│   │   ├── robots/       # Robot components
│   │   │   ├── RobotCard/
│   │   │   │   ├── RobotCard.tsx
│   │   │   │   ├── RobotCard.css
│   │   │   │   ├── Robot3DModel.tsx
│   │   │   │   └── RobotStats.tsx
│   │   │   ├── RobotMarketplace/
│   │   │   │   ├── RobotMarketplace.tsx
│   │   │   │   ├── MarketGrid.tsx
│   │   │   │   └── FilterBar.tsx
│   │   │   ├── RobotTraining/
│   │   │   │   ├── RobotTraining.tsx
│   │   │   │   ├── TrainingInterface.tsx
│   │   │   │   └── TrainingProgress.tsx
│   │   │   └── RobotBattles/
│   │   │       ├── RobotBattles.tsx
│   │   │       ├── BattleArena.tsx
│   │   │       └── BattleStats.tsx
│   │   │
│   │   ├── guilds/       # Guild components
│   │   │   ├── GuildDashboard/
│   │   │   │   ├── GuildDashboard.tsx
│   │   │   │   ├── GuildInfo.tsx
│   │   │   │   ├── MemberList.tsx
│   │   │   │   └── GuildStats.tsx
│   │   │   ├── GuildWars/
│   │   │   │   ├── GuildWars.tsx
│   │   │   │   ├── WarList.tsx
│   │   │   │   ├── WarDetails.tsx
│   │   │   │   └── WarMap.tsx
│   │   │   ├── Territories/
│   │   │   │   ├── TerritoryMap.tsx
│   │   │   │   ├── TerritoryCard.tsx
│   │   │   │   └── SiegeInterface.tsx
│   │   │   └── GuildQuests/
│   │   │       ├── GuildQuests.tsx
│   │   │       └── QuestCard.tsx
│   │   │
│   │   ├── quests/       # Quest components
│   │   │   ├── QuestLog/
│   │   │   │   ├── QuestLog.tsx
│   │   │   │   ├── QuestList.tsx
│   │   │   │   ├── QuestItem.tsx
│   │   │   │   └── QuestFilters.tsx
│   │   │   ├── QuestDetails/
│   │   │   │   ├── QuestDetails.tsx
│   │   │   │   ├── QuestDetails.css
│   │   │   │   ├── Objectives.tsx
│   │   │   │   ├── Rewards.tsx
│   │   │   │   └── QuestLore.tsx
│   │   │   ├── CampaignViewer/
│   │   │   │   ├── CampaignViewer.tsx
│   │   │   │   ├── ChapterList.tsx
│   │   │   │   ├── StoryView.tsx
│   │   │   │   └── ChoiceDialog.tsx
│   │   │   └── DailyQuests/
│   │   │       ├── DailyQuests.tsx
│   │   │       └── DailyQuestCard.tsx
│   │   │
│   │   ├── market/       # Market components
│   │   │   ├── Marketplace/
│   │   │   │   ├── Marketplace.tsx
│   │   │   │   ├── ItemGrid.tsx
│   │   │   │   └── SearchBar.tsx
│   │   │   ├── StockMarket/
│   │   │   │   ├── StockMarket.tsx
│   │   │   │   ├── StockChart.tsx
│   │   │   │   ├── StockList.tsx
│   │   │   │   └── TradingInterface.tsx
│   │   │   └── RealEstate/
│   │   │       ├── RealEstate.tsx
│   │   │       └── PropertyCard.tsx
│   │   │
│   │   ├── social/       # Social components
│   │   │   ├── Chat/
│   │   │   │   ├── Chat.tsx
│   │   │   │   ├── Chat.css
│   │   │   │   ├── MessageList.tsx
│   │   │   │   ├── MessageInput.tsx
│   │   │   │   └── ChatTabs.tsx
│   │   │   ├── FriendsList/
│   │   │   │   ├── FriendsList.tsx
│   │   │   │   ├── FriendCard.tsx
│   │   │   │   └── OnlineStatus.tsx
│   │   │   ├── AllianceManager/
│   │   │   │   ├── AllianceManager.tsx
│   │   │   │   └── AllianceCard.tsx
│   │   │   ├── RivalSystem/
│   │   │   │   ├── RivalSystem.tsx
│   │   │   │   └── RivalCard.tsx
│   │   │   └── MarriageSystem/
│   │   │       ├── MarriageSystem.tsx
│   │   │       ├── ProposalDialog.tsx
│   │   │       └── CoupleCard.tsx
│   │   │
│   │   ├── karma/        # Karma components
│   │   │   ├── KarmaDisplay/
│   │   │   │   ├── KarmaDisplay.tsx
│   │   │   │   ├── KarmaScore.tsx
│   │   │   │   └── KarmaHistory.tsx
│   │   │   ├── KarmaEvents/
│   │   │   │   ├── KarmaEvents.tsx
│   │   │   │   ├── EventCard.tsx
│   │   │   │   └── EventDialog.tsx
│   │   │   └── WorldKarma/
│   │   │       ├── WorldKarma.tsx
│   │   │       └── CollectiveStatus.tsx
│   │   │
│   │   ├── leaderboards/ # Leaderboard components
│   │   │   ├── Leaderboard/
│   │   │   │   ├── Leaderboard.tsx
│   │   │   │   ├── LeaderboardTabs.tsx
│   │   │   │   ├── RankingList.tsx
│   │   │   │   └── PlayerRank.tsx
│   │   │   └── Tournaments/
│   │   │       ├── Tournaments.tsx
│   │   │       ├── TournamentCard.tsx
│   │   │       └── Bracket.tsx
│   │   │
│   │   ├── achievements/ # Achievement components
│   │   │   ├── Achievements/
│   │   │   │   ├── Achievements.tsx
│   │   │   │   ├── AchievementGrid.tsx
│   │   │   │   ├── AchievementCard.tsx
│   │   │   │   └── CategoryFilter.tsx
│   │   │   └── BattlePass/
│   │   │       ├── BattlePass.tsx
│   │   │       ├── PassTrack.tsx
│   │   │       └── RewardItem.tsx
│   │   │
│   │   ├── customization/ # Customization components
│   │   │   ├── CharacterCreator/
│   │   │   │   ├── CharacterCreator.tsx
│   │   │   │   ├── CharacterCreator.css
│   │   │   │   ├── Preview3D.tsx
│   │   │   │   ├── FaceEditor.tsx
│   │   │   │   ├── BodyEditor.tsx
│   │   │   │   └── ColorPicker.tsx
│   │   │   ├── Wardrobe/
│   │   │   │   ├── Wardrobe.tsx
│   │   │   │   ├── OutfitGrid.tsx
│   │   │   │   └── OutfitCard.tsx
│   │   │   └── Housing/
│   │   │       ├── Housing.tsx
│   │   │       ├── RoomEditor.tsx
│   │   │       └── FurnitureList.tsx
│   │   │
│   │   ├── auth/         # Authentication components
│   │   │   ├── Login/
│   │   │   │   ├── Login.tsx
│   │   │   │   ├── Login.css
│   │   │   │   └── LoginForm.tsx
│   │   │   ├── Register/
│   │   │   │   ├── Register.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   └── ForgotPassword/
│   │   │       ├── ForgotPassword.tsx
│   │   │       └── ResetForm.tsx
│   │   │
│   │   ├── common/       # Common components
│   │   │   ├── Loading/
│   │   │   │   ├── Loading.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   └── Skeleton.tsx
│   │   │   ├── ErrorBoundary/
│   │   │   │   ├── ErrorBoundary.tsx
│   │   │   │   └── ErrorFallback.tsx
│   │   │   ├── Modal/
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── Modal.css
│   │   │   ├── Notification/
│   │   │   │   ├── Notification.tsx
│   │   │   │   └── NotificationItem.tsx
│   │   │   └── Tooltip/
│   │   │       ├── Tooltip.tsx
│   │   │       └── Tooltip.css
│   │   │
│   │   └── 3d/           # 3D-specific components
│   │       ├── Scene/
│   │       │   ├── Scene.tsx
│   │       │   └── SceneConfig.ts
│   │       ├── Models/
│   │       │   ├── CharacterModel.tsx
│   │       │   ├── RobotModel.tsx
│   │       │   └── EnvironmentModel.tsx
│   │       ├── Effects/
│   │       │   ├── ParticleSystem.tsx
│   │       │   ├── Glow.tsx
│   │       │   └── PostProcessing.tsx
│   │       └── Controls/
│   │           ├── OrbitControls.tsx
│   │           └── TouchControls.tsx
│   │
│   ├── pages/            # Page components
│   │   ├── Landing/
│   │   │   ├── Landing.tsx
│   │   │   ├── Landing.css
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   └── CallToAction.tsx
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Dashboard.css
│   │   │   ├── Overview.tsx
│   │   │   └── QuickActions.tsx
│   │   ├── Profile/
│   │   │   ├── Profile.tsx
│   │   │   └── Profile.css
│   │   ├── GameWorld/
│   │   │   ├── GameWorld.tsx
│   │   │   └── GameWorld.css
│   │   ├── Combat/
│   │   │   ├── Combat.tsx
│   │   │   └── Combat.css
│   │   ├── Guild/
│   │   │   ├── Guild.tsx
│   │   │   └── Guild.css
│   │   ├── Marketplace/
│   │   │   ├── Marketplace.tsx
│   │   │   └── Marketplace.css
│   │   ├── Leaderboards/
│   │   │   ├── Leaderboards.tsx
│   │   │   └── Leaderboards.css
│   │   └── Settings/
│   │       ├── Settings.tsx
│   │       ├── Settings.css
│   │       ├── Account.tsx
│   │       ├── Privacy.tsx
│   │       └── Graphics.tsx
│   │
│   ├── services/         # API services
│   │   ├── api/
│   │   │   ├── client.ts        # Axios client
│   │   │   ├── config.ts        # API config
│   │   │   └── interceptors.ts  # Request/response interceptors
│   │   │
│   │   ├── auth/
│   │   │   ├── authService.ts
│   │   │   └── tokenService.ts
│   │   │
│   │   ├── player/
│   │   │   ├── playerService.ts
│   │   │   ├── traitsService.ts
│   │   │   └── superpowersService.ts
│   │   │
│   │   ├── combat/
│   │   │   └── combatService.ts
│   │   │
│   │   ├── robots/
│   │   │   └── robotService.ts
│   │   │
│   │   ├── guilds/
│   │   │   └── guildService.ts
│   │   │
│   │   ├── quests/
│   │   │   └── questService.ts
│   │   │
│   │   ├── market/
│   │   │   └── marketService.ts
│   │   │
│   │   ├── social/
│   │   │   └── socialService.ts
│   │   │
│   │   └── websocket/
│   │       ├── websocketService.ts
│   │       └── eventHandlers.ts
│   │
│   ├── store/            # State management (Zustand)
│   │   ├── index.ts
│   │   │
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── playerSlice.ts
│   │   │   ├── gameSlice.ts
│   │   │   ├── combatSlice.ts
│   │   │   ├── socialSlice.ts
│   │   │   └── uiSlice.ts
│   │   │
│   │   └── selectors/
│   │       ├── authSelectors.ts
│   │       └── playerSelectors.ts
│   │
│   ├── hooks/            # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── usePlayer.ts
│   │   ├── useWebSocket.ts
│   │   ├── useCombat.ts
│   │   ├── useQuests.ts
│   │   ├── use3DScene.ts
│   │   ├── useToast.ts
│   │   └── useDebounce.ts
│   │
│   ├── utils/            # Utility functions
│   │   ├── formatters.ts      # Data formatters
│   │   ├── validators.ts      # Validation helpers
│   │   ├── calculations.ts    # Game calculations
│   │   ├── constants.ts       # Constants
│   │   ├── helpers.ts         # Helper functions
│   │   └── date.ts            # Date utilities
│   │
│   ├── types/            # TypeScript types
│   │   ├── index.ts
│   │   ├── player.ts
│   │   ├── combat.ts
│   │   ├── robot.ts
│   │   ├── guild.ts
│   │   ├── quest.ts
│   │   ├── market.ts
│   │   ├── social.ts
│   │   └── api.ts
│   │
│   ├── config/           # Configuration files
│   │   ├── routes.ts          # Route definitions
│   │   ├── game.ts            # Game config
│   │   ├── theme.ts           # Theme config
│   │   └── constants.ts       # App constants
│   │
│   ├── styles/           # Global styles
│   │   ├── globals.css        # Global CSS
│   │   ├── variables.css      # CSS variables
│   │   ├── animations.css     # Animations
│   │   └── fonts.css          # Font imports
│   │
│   └── assets/           # Local assets
│       ├── images/
│       │   ├── logos/
│       │   ├── icons/
│       │   └── backgrounds/
│       ├── sounds/
│       │   ├── effects/
│       │   └── music/
│       └── fonts/
│
└── tests/                # Frontend tests
    ├── unit/
    │   ├── components/
    │   └── hooks/
    ├── integration/
    │   └── services/
    └── e2e/
        └── flows/
```

---

## 📚 SHARED STRUCTURE (/app/shared/)

```
shared/
│
├── config/              # Shared configuration
│   ├── game_constants.json    # Game constants
│   ├── traits.json            # Trait definitions
│   ├── superpowers.json       # Superpower definitions
│   └── robots.json            # Robot types
│
├── types/               # Shared TypeScript types
│   ├── player.ts
│   ├── traits.ts
│   └── common.ts
│
└── utils/               # Shared utilities
    └── validation.ts
```

---

## 🧪 TESTS STRUCTURE (/app/tests/)

```
tests/
│
├── backend/             # Backend tests
│   ├── unit/
│   │   ├── services/
│   │   │   ├── test_karma_arbiter.py
│   │   │   ├── test_oracle.py
│   │   │   └── test_combat.py
│   │   └── models/
│   │       └── test_player_model.py
│   │
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_action_flow.py
│   │   └── test_quest_flow.py
│   │
│   └── e2e/
│       └── test_full_game_flow.py
│
├── frontend/            # Frontend tests
│   ├── unit/
│   │   ├── components/
│   │   └── hooks/
│   ├── integration/
│   │   └── api/
│   └── e2e/
│       ├── playwright/
│       │   ├── auth.spec.ts
│       │   ├── gameplay.spec.ts
│       │   └── combat.spec.ts
│       └── cypress/
│           └── e2e/
│
├── performance/         # Performance tests
│   ├── load_tests/
│   │   └── locustfile.py
│   └── stress_tests/
│
└── fixtures/            # Test fixtures
    ├── players.json
    ├── guilds.json
    └── quests.json
```

---

## 🔧 SCRIPTS STRUCTURE (/app/scripts/)

```
scripts/
│
├── setup/               # Setup scripts
│   ├── init_db.py              # Initialize database
│   ├── seed_data.py            # Seed test data
│   └── install_deps.sh         # Install dependencies
│
├── maintenance/         # Maintenance scripts
│   ├── backup_db.py            # Database backup
│   ├── clean_logs.sh           # Clean old logs
│   └── update_prices.py        # Update market prices
│
├── migration/           # Database migrations
│   ├── migrate_v1_to_v2.py
│   └── rollback_v2.py
│
├── deployment/          # Deployment scripts
│   ├── deploy.sh               # Deploy to production
│   ├── rollback.sh             # Rollback deployment
│   └── health_check.sh         # Health check
│
└── utils/               # Utility scripts
    ├── generate_traits.py      # Generate trait data
    ├── calculate_balance.py    # Balance calculations
    └── export_stats.py         # Export game stats
```

---

## 📖 DOCS STRUCTURE (/app/docs/)

```
docs/
│
├── api/                 # API documentation
│   ├── README.md
│   ├── authentication.md
│   ├── player.md
│   ├── combat.md
│   ├── guilds.md
│   └── websocket.md
│
├── game_design/         # Game design docs
│   ├── traits.md
│   ├── superpowers.md
│   ├── combat_system.md
│   ├── karma_system.md
│   └── economy.md
│
├── technical/           # Technical docs
│   ├── architecture.md
│   ├── database_schema.md
│   ├── ai_integration.md
│   └── deployment.md
│
├── guides/              # User guides
│   ├── quickstart.md
│   ├── gameplay.md
│   └── faq.md
│
└── assets/              # Documentation assets
    ├── diagrams/
    └── screenshots/
```

---

## 🎨 ASSETS STRUCTURE (/app/assets/)

```
assets/
│
├── 3d_models/           # 3D models (before processing)
│   ├── characters/
│   │   ├── male/
│   │   │   ├── base.fbx
│   │   │   ├── animations/
│   │   │   │   ├── idle.fbx
│   │   │   │   ├── walk.fbx
│   │   │   │   └── run.fbx
│   │   │   └── textures/
│   │   │       └── skin.png
│   │   └── female/
│   │       └── ...
│   │
│   ├── robots/
│   │   ├── worker_bot/
│   │   │   ├── model.fbx
│   │   │   └── textures/
│   │   ├── combat_bot/
│   │   └── ...
│   │
│   └── environment/
│       ├── buildings/
│       ├── props/
│       └── terrain/
│
├── textures/            # Texture files
│   ├── characters/
│   ├── robots/
│   └── environment/
│
├── audio/               # Audio files
│   ├── music/
│   │   ├── menu.mp3
│   │   ├── combat.mp3
│   │   └── ambient.mp3
│   ├── sfx/
│   │   ├── actions/
│   │   │   ├── hack.wav
│   │   │   └── powerup.wav
│   │   ├── ui/
│   │   │   ├── click.wav
│   │   │   └── notification.wav
│   │   └── combat/
│   │       ├── hit.wav
│   │       └── miss.wav
│   └── voice/
│       └── companion/
│
├── images/              # 2D images
│   ├── icons/
│   │   ├── traits/
│   │   │   ├── empathy.svg
│   │   │   └── ...
│   │   ├── superpowers/
│   │   └── items/
│   ├── ui/
│   │   ├── backgrounds/
│   │   └── frames/
│   └── marketing/
│       ├── logo.svg
│       └── banner.png
│
└── fonts/               # Custom fonts
    ├── Orbitron/
    ├── Inter/
    └── JetBrainsMono/
```

---

## 📝 ROOT CONFIG FILES

```
/app/
│
├── .gitignore           # Git ignore rules
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment template
├── README.md            # Project README
├── idea.md              # Game design document
├── implementation_status.md  # Technical blueprint
├── questions.md         # FAQ document
├── PROJECT_STRUCTURE.md # This file
├── LICENSE              # License file
├── CHANGELOG.md         # Change log
└── CONTRIBUTING.md      # Contribution guidelines
```

---

## 📊 SUMMARY STATISTICS

### Total Structure:

- **Backend Files:** ~200+ files
- **Frontend Files:** ~300+ files
- **Shared Files:** ~20 files
- **Test Files:** ~100+ files
- **Documentation Files:** ~50+ files
- **Asset Files:** ~500+ files (models, textures, audio)

**Total:** ~1,200+ files across 5-level nested structure

### Key Directories:

1. **Backend API Routes:** 15+ feature areas with 100+ endpoints
2. **AI Services:** 6 AI agents with dedicated logic
3. **Frontend Components:** 50+ reusable components
4. **3D Assets:** Characters, robots, environment models
5. **Services Layer:** Complete business logic separation
6. **State Management:** Organized Zustand slices
7. **Testing:** Comprehensive test coverage

---

## 🎯 DEVELOPMENT WORKFLOW

### File Organization Principles:

1. **Feature-Based Structure:** Group by feature, not file type
2. **5-Level Max Nesting:** Avoid deeper nesting for maintainability
3. **Clear Naming:** Self-documenting file names
4. **Separation of Concerns:** UI, Logic, Data layers separated
5. **Shared Resources:** Common code in shared/
6. **Type Safety:** TypeScript types alongside components

### Best Practices:

- **Backend:** Each API route has its own folder with router, schemas, and logic
- **Frontend:** Component folders contain all related files (tsx, css, tests)
- **Services:** Business logic separated from API routes
- **Models:** Database models organized by domain
- **Tests:** Mirror source structure for easy navigation

---

## ✅ STRUCTURE VERIFICATION

To verify this structure works:

```bash
# Backend
cd /app/backend
python -c "import server; print('Backend structure OK')"

# Frontend
cd /app/frontend
npm run build
# Should build successfully

# Tests
cd /app/tests
pytest
# Should discover and run tests
```

---

**This structure is production-ready and scales from MVP to full game launch! 🚀**

---

*Project Structure Document v1.0*  
*Complete 5-Level Nested Architecture*  
*1,200+ Files Organized for Success*