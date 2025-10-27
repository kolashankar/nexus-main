# 🚀 QUICK START - Fix WebSocket in 3 Steps

## 🎯 THE FASTEST WAY (For Web Users)

### Step 1: Clear Your Browser Cache
**Press F12** on your keyboard → Console tab → Copy this line and press Enter:

```javascript
localStorage.clear(); sessionStorage.clear(); alert('Storage cleared! Now reload the page.'); location.reload();
```

### Step 2: Login Again
Go to: **http://localhost:3000/login**

Enter your email and password, click Login

✅ **Done!** Token is automatically created and WebSocket connects!

---

## 🧪 FOR TESTING (Command Line)

### Get a Token:
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}' \
  | jq -r '.access_token'
```

### Test WebSocket with Token:
```bash
python /app/test_websocket.py "PASTE_YOUR_TOKEN_HERE"
```

---

## 📋 COPY-PASTE COMMANDS

### Check if Backend is Running:
```bash
curl http://localhost:8001/health
```
Expected: `{"status":"healthy"}`

### Create New Test User + Get Token:
```bash
curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"quicktest",
    "email":"quicktest@example.com",
    "password":"testpass123",
    "economic_class":"middle",
    "moral_class":"average"
  }' | jq -r '.access_token'
```

This will print your token. **Copy it.**

### Test the Token:
```bash
# Replace TOKEN_HERE with the token from above
python /app/test_websocket.py "TOKEN_HERE"
```

Expected output:
```
✅ WebSocket connected successfully!
```

---

## 🔍 CHECK YOUR CURRENT TOKEN

**Open browser console (F12)** and paste:

```javascript
// Quick check
const stored = JSON.parse(localStorage.getItem('karma-nexus-storage') || '{}');
console.log('Token:', stored.state?.accessToken);
console.log('Valid?', stored.state?.accessToken?.length > 100);
```

**Valid token** = Shows long string (100+ characters)
**Invalid token** = Shows short string or null

---

## ⚡ ONE-LINE FIX

If you just want to fix it **RIGHT NOW**:

### In Browser:
1. Press **F12**
2. Paste this:
```javascript
localStorage.clear(); location.href = '/login';
```
3. Login again
4. ✅ **Fixed!**

### In Terminal:
```bash
# Test with a fresh token
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test'$(date +%s)'","email":"test'$(date +%s)'@example.com","password":"testpass123","economic_class":"middle","moral_class":"average"}' \
  | jq -r '.access_token')

python /app/test_websocket.py "$TOKEN"
```

---

## 📺 VISUAL GUIDE

### How to Open Browser Console:

**Windows/Linux:**
- Press `F12` OR
- Press `Ctrl + Shift + I` OR
- Right-click anywhere → "Inspect" → "Console" tab

**Mac:**
- Press `Cmd + Option + I` OR
- Safari: Enable Developer Menu in Preferences first

### What You'll See:

```
╔══════════════════════════════════════╗
║  🌐 Browser Window                   ║
╠══════════════════════════════════════╣
║                                      ║
║  Your Website Content Here           ║
║                                      ║
╠══════════════════════════════════════╣
║  📟 Console (Press F12)              ║
║  ┌──────────────────────────────┐   ║
║  │ > Type commands here         │   ║
║  │                              │   ║
║  └──────────────────────────────┘   ║
╚══════════════════════════════════════╝
```

---

## 🎓 WHAT IS HAPPENING?

### The Problem:
Your browser has an **old/broken token** stored.

### The Solution:
1. **Clear** the old token
2. **Login** to get a fresh token
3. **WebSocket connects** automatically ✅

### Why It Happens:
- Browser stores tokens in localStorage
- Old tokens can be invalid/expired
- Backend correctly rejects invalid tokens with 403

### How We Fixed It:
- ✅ WebSocket endpoint is working (`/ws`)
- ✅ JWT authentication is working
- ✅ Backend tested and verified
- 👉 **You just need a fresh token!**

---

## 🆘 STILL NOT WORKING?

### Quick Diagnostics:

```bash
# Run all these commands:
echo "=== Checking Backend ==="
sudo supervisorctl status backend
curl -s http://localhost:8001/health

echo -e "\n=== Checking Frontend ==="
sudo supervisorctl status frontend

echo -e "\n=== Testing Fresh Token ==="
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"diag'$(date +%s)'","email":"diag'$(date +%s)'@example.com","password":"testpass123","economic_class":"middle","moral_class":"average"}' \
  | jq -r '.access_token')

if [ ! -z "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
  echo "✅ Token obtained: ${TOKEN:0:50}..."
  python /app/test_websocket.py "$TOKEN"
else
  echo "❌ Failed to get token"
fi
```

**If this test passes** → Your backend is fine, just login via web!
**If this test fails** → Check the error messages above

---

## 📚 More Details?

- **Full Guide**: `/app/TOKEN_GUIDE.md`
- **Troubleshooting**: `/app/WEBSOCKET_TROUBLESHOOTING.md`
- **Technical Docs**: `/app/WEBSOCKET_FIX_SUMMARY.md`

---

**🎉 Ready to Go! Just clear browser storage and login!**
