#!/usr/bin/env python3
"""Test WebSocket connection with JWT authentication"""
import asyncio
import websockets
import sys
import json

async def test_websocket(token):
    """Test WebSocket connection"""
    uri = f"ws://localhost:8001/ws?token={token}"
    
    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Wait for initial connection message
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            data = json.loads(response)
            print(f"✅ Connection data: {json.dumps(data, indent=2)}")
            
            # Send a test message
            test_message = {
                "type": "player",
                "event": "ping",
                "data": {"message": "Hello from test"}
            }
            await websocket.send(json.dumps(test_message))
            print(f"📤 Sent: {test_message}")
            
            # Wait for response
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            print("✅ WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_websocket.py <JWT_TOKEN>")
        print("\nFirst, get a token by registering or logging in:")
        print("curl -X POST http://localhost:8001/api/auth/login \\")
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"email":"test@example.com","password":"testpassword"}\'')
        sys.exit(1)
    
    token = sys.argv[1]
    asyncio.run(test_websocket(token))
