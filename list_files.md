# 📋 KARMA NEXUS - FILES TO CREATE & MODIFY

## 📊 Overview
This document lists all files that need to be created or modified for completing the remaining features of Karma Nexus.

---

## 🆕 NEW FILES TO CREATE

### 🎨 UI/UX Documentation
- [x] `/app/ui_preview.md` - Complete UI architecture and scene documentation

### 🤖 Robot Trading Enhancement (Step 6)

#### Backend Files
- [ ] `/app/backend/services/robots/enhanced_trading.py` - Enhanced robot trading logic
- [ ] `/app/backend/services/marketplace/robot_marketplace.py` - Robot marketplace with coin economy
- [ ] `/app/backend/api/v1/robots/trading_router.py` - Enhanced trading endpoints

#### Frontend Files
- [ ] `/app/frontend/src/components/game/RobotMarket/RobotMarket.jsx` - Robot marketplace UI
- [ ] `/app/frontend/src/components/game/RobotMarket/RobotMarket.css` - Marketplace styles
- [ ] `/app/frontend/src/components/game/RobotMarket/RobotCard.jsx` - Individual robot display card
- [ ] `/app/frontend/src/components/game/RobotMarket/RobotFilters.jsx` - Filter robots by type/price
- [ ] `/app/frontend/src/components/game/RobotInventory/RobotInventory.jsx` - Player's robot inventory
- [ ] `/app/frontend/src/components/game/RobotInventory/RobotInventory.css` - Inventory styles
- [ ] `/app/frontend/src/hooks/useRobotTrading.js` - Robot trading hook

### 🎮 Game Tabs System (Fix Non-Working Tabs)

#### Tab Components
- [ ] `/app/frontend/src/components/game/GameTabs/GameTabs.jsx` - Main tab navigation
- [ ] `/app/frontend/src/components/game/GameTabs/GameTabs.css` - Tab styles
- [ ] `/app/frontend/src/components/game/GameTabs/QuestsTab.jsx` - Quests tab content
- [ ] `/app/frontend/src/components/game/GameTabs/InventoryTab.jsx` - Inventory tab content
- [ ] `/app/frontend/src/components/game/GameTabs/SettingsTab.jsx` - Settings tab content
- [ ] `/app/frontend/src/components/game/GameTabs/MapTab.jsx` - Map/Territory tab
- [ ] `/app/frontend/src/components/game/GameTabs/SocialTab.jsx` - Social/Friends tab
- [ ] `/app/frontend/src/components/game/GameTabs/AchievementsTab.jsx` - Achievements tab

### 📦 Asset Management (Step 8)

#### Asset Loading System
- [ ] `/app/frontend/src/utils/AssetLoader.js` - Centralized asset loading utility
- [ ] `/app/frontend/src/utils/AssetFallbacks.js` - Fallback procedural models
- [ ] `/app/frontend/src/utils/AssetValidator.js` - Validate asset integrity

#### Asset Lists
- [ ] `/app/asset_status.md` - Current status of all 93 assets
- [ ] `/app/asset_replacement_plan.md` - Detailed replacement strategy
- [ ] `/app/asset_sources.md` - Sources for replacement assets

### 🏗️ Level Unlock System (From plan_of_action.md)

#### Backend
- [ ] `/app/backend/services/progression/level_system.py` - Level-based unlock system
- [ ] `/app/backend/services/progression/unlock_manager.py` - Manage feature unlocks
- [ ] `/app/backend/api/v1/progression/unlocks_router.py` - Unlock API endpoints

#### Frontend
- [ ] `/app/frontend/src/components/game/UnlockNotification/UnlockNotification.jsx` - Unlock popup
- [ ] `/app/frontend/src/components/game/ProgressionTree/ProgressionTree.jsx` - Visual unlock tree

### 🔄 Upgrade Management System

#### Backend
- [ ] `/app/backend/services/upgrades/trait_upgrader.py` - Trait upgrade logic
- [ ] `/app/backend/services/upgrades/robot_upgrader.py` - Robot upgrade logic
- [ ] `/app/backend/services/upgrades/ornament_upgrader.py` - Ornament upgrade logic
- [ ] `/app/backend/services/upgrades/chip_upgrader.py` - Chip upgrade logic
- [ ] `/app/backend/api/v1/upgrades/upgrades_router.py` - Upgrade API endpoints

#### Frontend
- [ ] `/app/frontend/src/components/game/UpgradeStation/UpgradeStation.jsx` - Main upgrade UI
- [ ] `/app/frontend/src/components/game/UpgradeStation/UpgradeStation.css` - Upgrade styles
- [ ] `/app/frontend/src/components/game/UpgradeStation/TraitUpgrader.jsx` - Trait upgrades
- [ ] `/app/frontend/src/components/game/UpgradeStation/RobotUpgrader.jsx` - Robot upgrades
- [ ] `/app/frontend/src/components/game/UpgradeStation/OrnamentUpgrader.jsx` - Ornament upgrades
- [ ] `/app/frontend/src/components/game/UpgradeStation/ChipUpgrader.jsx` - Chip upgrades
- [ ] `/app/frontend/src/hooks/useUpgrades.js` - Upgrade management hook

---

## 🔧 EXISTING FILES TO MODIFY

### 🎮 Core Game Files

#### GameWorld Component (Asset Loading Fixes)
- [x] `/app/frontend/src/components/game/GameWorld/GameWorld.jsx`
  - **Changes Needed:**
    - ✅ Add GLB model loader alongside procedural models
    - ✅ Add model loading error handling and fallbacks
    - ✅ Add asset preloading with progress indicator
    - ✅ Add character animation system
    - ✅ Add building models loading
    - ✅ Fix asset paths to public folder

#### GameWorld CSS (Visual Improvements)
- [ ] `/app/frontend/src/components/game/GameWorld/GameWorld.css`
  - **Changes Needed:**
    - Add loading screen styles
    - Add asset error display styles
    - Add progress bar styles

### 🤖 Robot System Enhancement

#### Existing Robot Service
- [ ] `/app/backend/services/robots/robot_service.py`
  - **Changes Needed:**
    - Add enhanced trading methods
    - Add coin-based pricing
    - Add robot upgrade functionality
    - Add robot level system (1-10)
    - Add robot stat calculations

#### Robot API Router
- [ ] `/app/backend/api/v1/robots/router.py`
  - **Changes Needed:**
    - Add buy/sell with coins endpoints
    - Add upgrade endpoints
    - Add marketplace listing endpoints
    - Add robot inventory management

### 💎 Marketplace System

#### Existing Marketplace Service
- [ ] `/app/backend/services/marketplace/marketplace.py`
  - **Changes Needed:**
    - Add robot trading to marketplace
    - Add chip trading system
    - Add price fluctuation logic
    - Add supply/demand mechanics

#### Marketplace API
- [ ] `/app/backend/api/v1/marketplace/router.py`
  - **Changes Needed:**
    - Add robot marketplace endpoints
    - Add chip marketplace endpoints
    - Add market statistics endpoints

### 🎯 Task System Integration

#### Task Manager
- [ ] `/app/backend/services/tasks/task_manager.py`
  - **Changes Needed:**
    - Integrate with ornament bonus system
    - Add coin reward calculations
    - Add task expiration handling
    - Add task refresh logic

#### Task Generator
- [ ] `/app/backend/services/ai/task_generator.py`
  - **Changes Needed:**
    - Ensure Gemini API integration is working
    - Add task variety based on player level
    - Add task difficulty scaling
    - Add special event tasks

### 📊 Player Profile

#### Player Model
- [ ] `/app/backend/models/player/player.py`
  - **Changes Needed:**
    - Add ornament inventory
    - Add robot inventory
    - Add chip inventory
    - Add upgrade levels tracking
    - Add unlock status tracking

#### Player Service
- [ ] `/app/backend/services/player/profile.py`
  - **Changes Needed:**
    - Add ornament management methods
    - Add robot management methods
    - Add upgrade tracking methods
    - Add unlock checking methods

### 🎨 UI Components

#### Main Game Page
- [ ] `/app/frontend/src/pages/Game/Game.jsx` or `/app/frontend/src/pages/GameWorld/GameWorld.jsx`
  - **Changes Needed:**
    - Add tab navigation system
    - Add TaskPanel integration
    - Add Marketplace integration
    - Add RobotMarket integration
    - Add proper layout with all panels

#### ProceduralModels Utility
- [ ] `/app/frontend/src/utils/ProceduralModels.js`
  - **Changes Needed:**
    - Enhance character models with animations
    - Add ornament attachment points
    - Improve building models
    - Add robot model variations

### 🗺️ Navigation & Routing

#### App Router
- [ ] `/app/frontend/src/App.js`
  - **Changes Needed:**
    - Add routes for new pages (upgrade station, robot market)
    - Update navigation links
    - Add route guards for locked features

### 🎨 Styling

#### Global Styles
- [ ] `/app/frontend/src/index.css`
  - **Changes Needed:**
    - Add tab navigation styles
    - Add marketplace theme colors
    - Add upgrade station styles

#### Theme Configuration
- [ ] `/app/frontend/tailwind.config.js`
  - **Changes Needed:**
    - Add custom colors for new features
    - Add animation classes
    - Add responsive breakpoints

---

## 📚 DOCUMENTATION FILES TO UPDATE

### Core Documentation
- [x] `/app/plan_of_action.md`
  - **Changes Needed:**
    - ✅ Add detailed architecture for all 20 karma screens
    - ✅ Add detailed architecture for all 10 upgrade screens
    - ✅ Add implementation specs for each screen
    - ✅ Add currency flow diagrams

### Project Status
- [ ] `/app/phases.md`
  - **Changes Needed:**
    - Update Phase 11 completion status
    - Add new sub-phases for remaining 50 test files
    - Add asset replacement phases
    - Update overall progress percentage

- [ ] `/app/implementation_status.md`
  - **Changes Needed:**
    - Update feature completion checklist
    - Add asset status section
    - Add tab system status
    - Update API endpoint list

### New Documentation
- [x] `/app/ui_preview.md`
  - **Content:**
    - Complete UI/UX architecture
    - All game scenes with screenshots/mockups
    - Tab system architecture
    - Component hierarchy
    - User flow diagrams
    - Control reference

- [ ] `/app/asset_documentation.md`
  - **Content:**
    - Complete asset inventory (all 93 files)
    - Asset status (working/placeholder/missing)
    - Replacement plan
    - Asset sources and licenses
    - Loading strategy

---

## 🔢 FILE COUNT SUMMARY

### New Files to Create: 58
- Backend: 12 files
- Frontend Components: 28 files
- Utilities: 6 files
- Documentation: 5 files
- Asset Management: 7 files

### Existing Files to Modify: 18
- Backend: 6 files
- Frontend: 8 files
- Configuration: 2 files
- Documentation: 2 files

### **Total Files Affected: 76**

---

## 🎯 PRIORITY ORDER

### High Priority (Must Complete First)
1. ✅ `/app/ui_preview.md` - Complete UI architecture documentation
2. ✅ Fix GLB asset loading in `GameWorld.jsx`
3. ✅ Create asset status documentation (`asset_status.md`)
4. ✅ Fix non-working tabs (create GameTabs components)
5. ✅ Enhance robot trading system

### Medium Priority (Next Phase)
6. Create upgrade station UI and backend
7. Implement level unlock system
8. Replace placeholder assets
9. Add all 93 assets to asset loader

### Low Priority (Polish Phase)
10. Optimize asset loading performance
11. Add asset compression
12. Add loading animations
13. Complete test coverage

---

## 📝 NOTES

### Asset Files
The 93 assets in `/app/frontend/public/` include:
- **Models:** `models/characters/`, `models/robots/`, `models/environment/`, `models/buildings/`
- **Textures:** `textures/characters/`, `textures/environment/`, `textures/effects/`
- **Sounds:** `sounds/combat/`, `sounds/ui/`, `sounds/music/`
- **Icons:** `icons/traits/`, `icons/superpowers/`, `icons/items/`
- **Images:** `images/backgrounds/`, `images/ui/`
- **Fonts:** `fonts/`

### Tab System Features
The tab system should include:
- **Quests Tab:** Active quests, daily tasks, quest log
- **Inventory Tab:** Items, robots, chips, ornaments
- **Settings Tab:** Graphics, audio, controls, privacy
- **Map Tab:** Territory map, guild locations, fast travel
- **Social Tab:** Friends, alliances, chat
- **Achievements Tab:** Unlocked achievements, progress

### Integration Points
Files that need integration:
1. **TaskPanel** → GameWorld (right side panel)
2. **Marketplace** → Main navigation
3. **RobotMarket** → Marketplace tab
4. **GameTabs** → GameWorld (overlay tabs)
5. **UpgradeStation** → Main navigation

---

**Last Updated:** Current Development Session  
**Status:** 🚀 Ready for Implementation  
**Estimated Completion:** 3-4 development sessions
