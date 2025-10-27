/**
 * WebSocket service for real-time communication
 */

class WebSocketService {
  constructor() {
    this.ws = null;
    this.handlers = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.reconnectTimer = null;
    this.currentToken = null;
    // Get base WS URL from env or construct from window location
    // Support both Vite (import.meta.env) and Create React App (process.env) patterns
    let wsUrl = import.meta.env?.VITE_WS_URL || 
                process.env.REACT_APP_WS_URL;
    if (!wsUrl) {
      // Use window location to construct WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      wsUrl = `${protocol}//${host}/ws`;
    }
    this.url = wsUrl;
  }

  connect(token) {
    if (!token) {
      console.error('WebSocket: No token provided');
      return;
    }

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket: Already connected');
      return;
    }

    // Store token for reconnection
    this.currentToken = token;

    // Clear any pending reconnection
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    try {
      // Construct WebSocket URL with token as query parameter
      this.ws = new WebSocket(`${this.url}?token=${token}`);

      this.ws.onopen = () => {
        console.log('WebSocket: Connected successfully');
        this.reconnectAttempts = 0;
        // Notify handlers that connection is established
        this.handleMessage({ type: 'connected', data: {} });
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('WebSocket: Failed to parse message', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket: Error occurred', error);
      };

      this.ws.onclose = (event) => {
        console.log(`WebSocket: Disconnected (code: ${event.code}, reason: ${event.reason})`);
        this.ws = null;
        
        // Don't reconnect if it was a clean closure or auth failure
        if (event.code === 1000 || event.code === 403 || event.code === 401) {
          console.log('WebSocket: Not attempting reconnect (clean close or auth failure)');
          this.handleMessage({ type: 'disconnected', data: { code: event.code } });
          return;
        }
        
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('WebSocket: Failed to create connection', error);
    }
  }

  disconnect() {
    console.log('WebSocket: Disconnecting...');
    
    // Clear reconnection timer
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    
    // Reset reconnection attempts
    this.reconnectAttempts = this.maxReconnectAttempts;
    
    if (this.ws) {
      // Close with normal closure code
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    
    this.currentToken = null;
  }

  send(eventType, data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: eventType, data }));
    } else {
      console.error('WebSocket: Cannot send message - not connected');
      return false;
    }
    return true;
  }

  on(eventType, handler) {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType).push(handler);
  }

  off(eventType, handler) {
    const handlers = this.handlers.get(eventType);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  handleMessage(message) {
    const { type, data } = message;
    const handlers = this.handlers.get(type);

    if (handlers) {
      handlers.forEach((handler) => {
        try {
          handler(data);
        } catch (error) {
          console.error(`WebSocket: Error in handler for ${type}`, error);
        }
      });
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('WebSocket: Max reconnection attempts reached');
      this.handleMessage({ 
        type: 'reconnect_failed', 
        data: { attempts: this.reconnectAttempts } 
      });
      return;
    }

    if (!this.currentToken) {
      console.error('WebSocket: Cannot reconnect - no token available');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.min(this.reconnectAttempts, 3);
    
    console.log(
      `WebSocket: Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`
    );

    this.reconnectTimer = setTimeout(() => {
      this.connect(this.currentToken);
    }, delay);
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }

  getReadyState() {
    if (!this.ws) return 'CLOSED';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING: return 'CONNECTING';
      case WebSocket.OPEN: return 'OPEN';
      case WebSocket.CLOSING: return 'CLOSING';
      case WebSocket.CLOSED: return 'CLOSED';
      default: return 'UNKNOWN';
    }
  }
}

export default new WebSocketService();