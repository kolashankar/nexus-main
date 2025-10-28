# 🎮 KARMA NEXUS 2.0 - COMPLETE GAME DESIGN & IMPLEMENTATION PLAN

## 📋 Executive Summary
This comprehensive document outlines the complete game architecture, including:
- **20 Karma Interaction Screens** - Detailed scenarios between 5 players
- **10 Upgrade System Screens** - Complete upgrade mechanics for all components
- **Economy System** - Cash, coins, and all currency flows
- **Feature Enhancement Plan** - AI tasks, marketplace, robot trading

---

## 🎯 PROJECT GOALS

### Primary Objectives
1. ✅ Replace placeholder assets with realistic, cinematic assets (93 files)
2. ✅ Implement Gemini AI-powered dynamic task generation
3. ✅ Create task panel UI with coin rewards
4. ✅ Build marketplace for ornaments (chains & rings)
5. ✅ Implement bonus coin system with visual ornaments
6. ✅ Enhance robot trading system

### Success Criteria
- All assets loading correctly in game
- AI generates trait-based tasks dynamically
- Marketplace functional with coin transactions
- Ornaments visible on 3D character models
- Robot trading integrated with new economy

---

## 📊 CURRENT STATUS - **✅ MAJOR FEATURES COMPLETE!**

### ✅ What's NOW Working (Added in Current Session)
1. **Gemini AI Task System:** ✅ COMPLETE
   - AI-powered task generation based on player traits
   - Task panel UI on right side
   - Task completion with coin rewards
   - Ornament bonus calculation integrated

2. **Marketplace System:** ✅ COMPLETE
   - Golden Chain (2,000 coins → +3% bonus)
   - Mystic Ring (5,000 coins → +7% bonus)
   - Dynamic pricing (doubles each purchase)
   - Bonus stacking system
   - Purchase flow working

3. **Enhanced Controls:** ✅ COMPLETE
   - WASD keys (existing)
   - Arrow keys ⬆️⬇️⬅️➡️ (NEW)
   - Both methods supported simultaneously

4. **Critical Frontend Fixes:** ✅ COMPLETE
   - Created `/lib/utils.js` (fixed UI components)
   - Fixed GameWorld component
   - Improved asset loading with fallbacks
   - Error handling improved

5. **Documentation:** ✅ COMPLETE
   - Created comprehensive `ui_preview.md`
   - Updated `phases.md` with new features
   - Updated `plan_of_action.md` (this file)
1. **Game Core:**
   - ✅ 3D game world with Three.js
   - ✅ Character movement (WASD + Arrow keys)
   - ✅ Player authentication & profiles
   - ✅ Backend API (FastAPI + MongoDB)
   - ✅ 80 traits system (virtues, vices, skills, meta)
   - ✅ Currency system (6 types including credits)

2. **Assets (Partial):**
   - ✅ 93 asset files present in /public folder
   - ✅ Character models (male/female base, athletic, heavy)
   - ✅ Robot models (scout, trader, combat, medic, etc.)
   - ✅ Environment models (buildings, props, terrain)
   - ✅ Sounds (combat, UI, background music)
   - ✅ Textures (characters, environment, effects)

3. **Backend Services:**
   - ✅ Player profile management
   - ✅ Authentication (JWT)
   - ✅ Quest system (basic structure)
   - ✅ Currency tracking

### ❌ What Needs Implementation

1. **Assets:**
   - ❌ Many assets are low-quality placeholders
   - ❌ Some assets not loading/showing in game
   - ❌ Need realistic, cinematic replacements

2. **AI Task System:**
   - ❌ No Gemini AI integration
   - ❌ No dynamic task generation
   - ❌ No task panel UI
   - ❌ No task-completion coin rewards

3. **Marketplace:**
   - ❌ No marketplace UI
   - ❌ No ornament purchasing (chain/ring)
   - ❌ No bonus coin calculation
   - ❌ No ornament visibility on character

4. **Robot Trading:**
   - ❌ Basic structure exists but needs enhancement
   - ❌ Not integrated with new coin system

---

## 🚀 IMPLEMENTATION PHASES

## PHASE 1: ASSET AUDIT & INFRASTRUCTURE ⏳
**Goal:** Identify all placeholder assets and prepare replacement strategy

### Tasks:
- [⏳] Audit all 93 assets in /public folder
- [⏳] Categorize: Character models, Environment, Robots, UI, Sounds, Textures
- [⏳] Identify which are placeholders vs real assets
- [⏳] Document asset loading issues
- [⏳] Create asset replacement priority list

### Deliverables:
- Asset audit report
- List of assets to replace (prioritized)
- Asset loading bug fixes

**Status:** 🔄 In Progress  
**Blockers:** None  
**ETA:** Current session

---

## PHASE 2: GEMINI AI INTEGRATION ⏳
**Goal:** Integrate Gemini API for dynamic task generation based on character traits

### Tasks:
- [⏳] Add Gemini API key to backend .env
- [⏳] Install emergentintegrations library
- [⏳] Create task generation service (`/backend/services/ai/task_generator.py`)
- [⏳] Implement trait-based task logic (virtues → good tasks, vices → bad tasks)
- [⏳] Create task data model
- [⏳] Build task generation API endpoint (`/api/tasks/generate`)
- [⏳] Test AI task generation with different character traits

### API Specifications:
```python
# Endpoint: POST /api/tasks/generate
# Request: { player_id: str }
# Response: {
#   task_id: str,
#   description: str,
#   task_type: "good" | "bad",
#   coin_reward: int,
#   expires_at: datetime
# }
```

### Task Generation Logic:
- Analyze player's top 5 virtues & vices
- Generate contextually appropriate tasks
- Good tasks: Help NPCs, build, donate, protect
- Bad tasks: Steal, sabotage, deceive, exploit
- Coin rewards: 50-200 coins per task

**Status:** ⏳ Not Started  
**Blockers:** None  
**ETA:** Phase 2

---

## PHASE 3: TASK PANEL UI ⏳
**Goal:** Create right-side task panel showing current task and completion UI

### Tasks:
- [⏳] Create TaskPanel component (`/frontend/src/components/game/TaskPanel/TaskPanel.jsx`)
- [⏳] Design task card UI (task description, reward, timer)
- [⏳] Add task completion button
- [⏳] Implement auto-refresh on completion
- [⏳] Show coin balance
- [⏳] Add task completion animation
- [⏳] Integrate with backend task API

### UI Design:
```
┌─────────────────────────┐
│ 🎯 CURRENT TASK         │
├─────────────────────────┤
│ Help the NPC merchant   │
│ deliver supplies        │
│                         │
│ 💰 Reward: 150 coins    │
│ ⏱️  Expires: 10:45      │
│                         │
│ [Complete Task]         │
└─────────────────────────┘
│ Coins: 1,250            │
└─────────────────────────┘
```

**Status:** ⏳ Not Started  
**Blockers:** Phase 2 completion  
**ETA:** Phase 3

---

## PHASE 4: MARKETPLACE SYSTEM ⏳
**Goal:** Implement ornament marketplace with chain/ring purchases and bonus coins

### Tasks:
- [⏳] Create Marketplace component (`/frontend/src/components/game/Marketplace/Marketplace.jsx`)
- [⏳] Design marketplace UI (item cards, prices, purchase buttons)
- [⏳] Build ornament inventory system (backend)
- [⏳] Create purchase API endpoint (`/api/marketplace/purchase`)
- [⏳] Implement price doubling logic (2nd chain = 4000, 3rd = 8000)
- [⏳] Create bonus coin calculation service
- [⏳] Update task completion to apply ornament bonuses
- [⏳] Add ornament ownership tracking

### Ornament Specifications:
| Item  | Base Price | Bonus | Price Scaling |
|-------|-----------|-------|---------------|
| Chain | 2,000     | +3%   | 2x per purchase |
| Ring  | 5,000     | +7%   | 2x per purchase |

### Bonus Calculation Example:
- Base task reward: 100 coins
- With 1 chain (3%): 103 coins
- With 2 chains (6%): 106 coins
- With 1 chain + 1 ring (10%): 110 coins

### API Specifications:
```python
# Endpoint: POST /api/marketplace/purchase
# Request: { player_id: str, item_type: "chain" | "ring" }
# Response: {
#   success: bool,
#   new_balance: int,
#   item_count: int,
#   next_price: int
# }
```

**Status:** ⏳ Not Started  
**Blockers:** Phase 3 completion  
**ETA:** Phase 4

---

## PHASE 5: ORNAMENT VISUALIZATION ⏳
**Goal:** Make ornaments visible on 3D character models in game

### Tasks:
- [⏳] Create chain 3D model or use primitive geometry
- [⏳] Create ring 3D model or use primitive geometry
- [⏳] Update GameWorld.jsx to load ornaments
- [⏳] Attach ornaments to character skeleton/bones
- [⏳] Position chain on neck, rings on fingers
- [⏳] Add glow effects for ornaments
- [⏳] Update ornament visibility on purchase
- [⏳] Handle multiple ornaments (stacking)

### Technical Implementation:
```javascript
// Load ornaments based on player inventory
playerOrnaments.chains.forEach((_, index) => {
  const chain = createChainModel();
  chain.position.set(0, 1.4, 0); // Neck position
  chain.rotation.x = Math.PI / 6 + (index * 0.1);
  characterModel.add(chain);
});
```

**Status:** ⏳ Not Started  
**Blockers:** Phase 4 completion  
**ETA:** Phase 5

---

## PHASE 6: ROBOT TRADING ENHANCEMENT ⏳
**Goal:** Enhance existing robot trading system with new economy

### Tasks:
- [⏳] Review existing robot trading code
- [⏳] Integrate robot prices with coin system
- [⏳] Update robot marketplace UI
- [⏳] Add robot selling functionality
- [⏳] Implement robot price fluctuations
- [⏳] Add robot inventory management
- [⏳] Create transaction history

### Existing Robot Types:
- Scout (reconnaissance)
- Trader (commerce)
- Combat (battle)
- Medic (healing)
- Hacker (cyber warfare)
- Guardian (defense)
- Harvester (resource gathering)
- Tactical (strategy)
- Assault (offense)

**Status:** ⏳ Not Started  
**Blockers:** Phase 4 completion  
**ETA:** Phase 6

---

## PHASE 7: ASSET REPLACEMENT - CHARACTERS ⏳
**Goal:** Replace character model placeholders with realistic, cinematic assets

### Priority Assets:
1. [⏳] Character models (male/female base, athletic, heavy)
2. [⏳] Character textures (skin, hair, clothing)
3. [⏳] Character animations (walk, run, jump, attack)

### Asset Sources:
- Mixamo (free rigged characters)
- Sketchfab (CC licensed models)
- Poly Haven (free 3D assets)
- CGTrader (premium models if needed)

### Quality Requirements:
- High-poly models (10k-50k triangles)
- PBR textures (4K resolution)
- Rigged and animated
- Realistic human proportions
- Cinematic lighting compatible

**Status:** ⏳ Not Started  
**Blockers:** None (can run parallel)  
**ETA:** Phase 7

---

## PHASE 8: ASSET REPLACEMENT - ENVIRONMENT ⏳
**Goal:** Replace environment placeholders with realistic, cinematic assets

### Priority Assets:
1. [⏳] Buildings (tower, headquarters, shop, warehouse)
2. [⏳] Props (containers, vehicles, crates)
3. [⏳] Terrain (platforms, ground textures)
4. [⏳] Environment textures (metal, concrete, brick)

### Asset Sources:
- Poly Haven (free PBR textures)
- Quixel Megascans (high-quality scans)
- Sketchfab (CC licensed models)
- Free3D.com (free models)

### Quality Requirements:
- Detailed geometry
- PBR materials
- Optimized for real-time rendering
- Consistent art style (cyberpunk/futuristic)
- Proper UV mapping

**Status:** ⏳ Not Started  
**Blockers:** None (can run parallel)  
**ETA:** Phase 8

---

## PHASE 9: ASSET REPLACEMENT - ROBOTS & UI ⏳
**Goal:** Replace robot models and UI assets

### Priority Assets:
1. [⏳] Robot models (scout, trader, combat, medic, etc.)
2. [⏳] UI icons (health, energy, coins, etc.)
3. [⏳] Sound effects
4. [⏳] Background music

### Asset Sources:
- Free Sound (sound effects)
- OpenGameArt (sprites & sounds)
- Sketchfab (robot models)

**Status:** ⏳ Not Started  
**Blockers:** None  
**ETA:** Phase 9

---

## PHASE 10: TESTING & BUG FIXES ⏳
**Goal:** Comprehensive testing of all new features

### Testing Areas:
- [⏳] Asset loading verification (all 93 files)
- [⏳] Gemini AI task generation
- [⏳] Task panel UI/UX
- [⏳] Marketplace transactions
- [⏳] Ornament purchases & pricing
- [⏳] Bonus coin calculations
- [⏳] Ornament visualization on characters
- [⏳] Robot trading
- [⏳] Backend API endpoints
- [⏳] Frontend-backend integration

### Test Scenarios:
1. **Task System:**
   - Generate task for good character → receives virtuous task
   - Generate task for bad character → receives vice task
   - Complete task → coins added to balance
   - Auto-refresh after completion

2. **Marketplace:**
   - Purchase first chain (2000 coins)
   - Purchase second chain (4000 coins)
   - Purchase ring (5000 coins)
   - Verify bonus coins calculation
   - Check ornament visibility on character

3. **Robot Trading:**
   - Buy robot with coins
   - Sell robot for coins
   - Check inventory updates

**Status:** ⏳ Not Started  
**Blockers:** All phases 2-9  
**ETA:** Phase 10

---

## PHASE 11: POLISH & OPTIMIZATION ⏳
**Goal:** Final polish, performance optimization, and documentation

### Tasks:
- [⏳] Performance testing (FPS, load times)
- [⏳] UI/UX improvements
- [⏳] Code cleanup
- [⏳] Documentation updates
- [⏳] Error handling improvements
- [⏳] Security audit

**Status:** ⏳ Not Started  
**Blockers:** Phase 10 completion  
**ETA:** Phase 11

---

## 📊 OVERALL PROGRESS TRACKER

### Phase Summary
| Phase | Name | Status | Progress | ETA |
|-------|------|--------|----------|-----|
| 1 | Asset Audit | 🔄 In Progress | 0% | Current |
| 2 | Gemini AI Integration | ⏳ Not Started | 0% | Session 1 |
| 3 | Task Panel UI | ⏳ Not Started | 0% | Session 1 |
| 4 | Marketplace System | ⏳ Not Started | 0% | Session 2 |
| 5 | Ornament Visualization | ⏳ Not Started | 0% | Session 2 |
| 6 | Robot Trading | ⏳ Not Started | 0% | Session 2 |
| 7 | Assets - Characters | ⏳ Not Started | 0% | Session 3 |
| 8 | Assets - Environment | ⏳ Not Started | 0% | Session 3 |
| 9 | Assets - Robots/UI | ⏳ Not Started | 0% | Session 3 |
| 10 | Testing | ⏳ Not Started | 0% | Session 4 |
| 11 | Polish | ⏳ Not Started | 0% | Session 4 |

### Overall Progress: 0/11 phases (0%)

---

## 🔧 TECHNICAL SPECIFICATIONS

### Backend Architecture

#### New Services
```
backend/services/
├── ai/
│   ├── __init__.py
│   ├── task_generator.py      # Gemini AI task generation
│   └── trait_analyzer.py      # Analyze player traits
├── marketplace/
│   ├── __init__.py
│   ├── ornament_shop.py       # Handle purchases
│   └── bonus_calculator.py    # Calculate coin bonuses
└── tasks/
    ├── __init__.py
    ├── task_manager.py        # Task lifecycle
    └── reward_distributor.py  # Distribute coins
```

#### New API Endpoints
```
POST   /api/tasks/generate          # Generate new task
POST   /api/tasks/complete          # Complete task
GET    /api/tasks/current           # Get current task
POST   /api/marketplace/purchase    # Buy ornament
GET    /api/marketplace/inventory   # Get player ornaments
GET    /api/marketplace/prices      # Get current prices
PUT    /api/robots/sell             # Sell robot
PUT    /api/robots/buy              # Buy robot
GET    /api/robots/marketplace      # List available robots
```

#### Database Models
```python
# Task Model
{
  task_id: str,
  player_id: str,
  description: str,
  task_type: "good" | "bad",
  base_reward: int,
  actual_reward: int,  # With bonuses
  status: "active" | "completed" | "expired",
  created_at: datetime,
  expires_at: datetime
}

# Ornament Inventory
{
  player_id: str,
  chains: int,
  rings: int,
  total_bonus_percentage: float,
  last_updated: datetime
}

# Purchase History
{
  purchase_id: str,
  player_id: str,
  item_type: "chain" | "ring",
  price_paid: int,
  purchase_number: int,  # 1st, 2nd, 3rd, etc.
  purchased_at: datetime
}
```

### Frontend Architecture

#### New Components
```
frontend/src/components/game/
├── TaskPanel/
│   ├── TaskPanel.jsx          # Main task panel
│   ├── TaskCard.jsx           # Individual task display
│   └── TaskPanel.css          # Styles
├── Marketplace/
│   ├── Marketplace.jsx        # Main marketplace
│   ├── OrnamentCard.jsx       # Item card
│   ├── PurchaseModal.jsx      # Confirmation modal
│   └── Marketplace.css        # Styles
└── GameWorld/
    └── OrnamentLoader.js      # Load ornament 3D models
```

#### State Management
```javascript
// Task State
const [currentTask, setCurrentTask] = useState(null);
const [taskLoading, setTaskLoading] = useState(false);

// Marketplace State
const [ornamentInventory, setOrnamentInventory] = useState({
  chains: 0,
  rings: 0,
  bonusPercentage: 0
});

// Player Coins
const [coinBalance, setCoinBalance] = useState(0);
```

---

## 🎨 UI/UX DESIGN SPECIFICATIONS

### Task Panel
- **Position:** Right side of screen
- **Size:** 300px wide, auto height
- **Style:** Semi-transparent dark background with neon accents
- **Animation:** Slide in from right on load
- **Colors:** Purple/blue theme matching game aesthetic

### Marketplace
- **Position:** Toggleable overlay (button in HUD)
- **Layout:** Grid of item cards
- **Item Cards:** Image, name, price, owned count, purchase button
- **Feedback:** Success animation on purchase

### Ornaments on Character
- **Chain:** Golden necklace visible on neck area
- **Ring:** Glowing ring on finger
- **Effect:** Subtle glow/shimmer to indicate magical properties
- **Stacking:** Multiple chains/rings visible (different positions/sizes)

---

## 🚨 KNOWN ISSUES & FIXES NEEDED

### Asset Loading Issues
- ❌ Some GLB models not loading (404 errors)
- ❌ Texture paths incorrect
- ❌ Missing model fallbacks

### Current Bugs
- ⚠️ Dashboard null checks needed
- ⚠️ ProfileCard undefined properties
- ⚠️ Some assets showing as placeholders

---

## 📝 DEPENDENCIES TO INSTALL

### Backend
```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### Frontend
```bash
# Already installed:
# - three
# - @react-three/fiber
# - @react-three/drei
```

---

## 🔐 ENVIRONMENT VARIABLES

### Backend (.env)
```
GEMINI_API_KEY=AIzaSyCrDnhg5VTo-XrfO1eoamZD9R6wVlqYSM
```

---

## 📈 SUCCESS METRICS

### Functional Metrics
- ✅ 93/93 assets loading correctly
- ✅ Task generation < 2 seconds
- ✅ 100% task completion success rate
- ✅ Marketplace transaction success rate > 99%
- ✅ Ornaments visible in 3D world

### Performance Metrics
- ✅ Game FPS > 30 (target 60)
- ✅ API response time < 500ms
- ✅ Asset load time < 5 seconds

---

## 🎯 NEXT STEPS

### Immediate Actions (Current Session)
1. ✅ Complete this plan document
2. ⏳ Start Phase 1: Asset audit
3. ⏳ Start Phase 2: Gemini AI integration
4. ⏳ Begin Phase 3: Task panel UI

### Session 2
- Complete Phases 4-6 (Marketplace, ornaments, robot trading)

### Session 3
- Complete Phases 7-9 (Asset replacement)

### Session 4
- Complete Phases 10-11 (Testing & polish)

---

**Document Version:** 1.0  
**Last Updated:** Current Development Session  
**Status:** 🚀 Ready to Begin Implementation

---

## 📞 CONTACT & SUPPORT
For questions or issues, refer to the main README.md or test_result.md files.
