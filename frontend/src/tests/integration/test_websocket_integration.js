import React from "react";
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import io from 'socket.io-client';

const WS_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

describe('WebSocket Integration Tests', () => {
  let socket;
  const authToken = 'test_token_here';

  beforeAll((done) => {
    socket = io(WS_URL, {
      auth: { token: authToken },
      transports: ['websocket'],
    });

    socket.on('connect', () => {
      done();
    });
  });

  afterAll(() => {
    if (socket.connected) {
      socket.disconnect();
    }
  });

  it('should connect to WebSocket server', () => {
    expect(socket.connected).toBe(true);
  });

  it('should authenticate successfully', (done) => {
    socket.emit('authenticate', { token: authToken });

    socket.on('authenticated', (data) => {
      expect(data.success).toBe(true);
      done();
    });
  });

  it('should join a room', (done) => {
    socket.emit('join_room', { room: 'test_room' });

    socket.on('room_joined', (data) => {
      expect(data.room).toBe('test_room');
      done();
    });
  });

  it('should receive player updates', (done) => {
    socket.on('player_update', (data) => {
      expect(data).toHaveProperty('player_id');
      expect(data).toHaveProperty('update_type');
      done();
    });

    // Trigger an update
    socket.emit('request_update');
  });

  it('should receive karma change notifications', (done) => {
    socket.on('karma_changed', (data) => {
      expect(data).toHaveProperty('player_id');
      expect(data).toHaveProperty('old_karma');
      expect(data).toHaveProperty('new_karma');
      expect(data).toHaveProperty('change');
      done();
    });
  });

  it('should receive trait update notifications', (done) => {
    socket.on('trait_updated', (data) => {
      expect(data).toHaveProperty('trait_name');
      expect(data).toHaveProperty('old_value');
      expect(data).toHaveProperty('new_value');
      done();
    });
  });

  it('should broadcast chat messages', (done) => {
    const testMessage = 'Hello from test!';

    socket.on('chat_message', (data) => {
      if (data.message === testMessage) {
        expect(data).toHaveProperty('username');
        expect(data).toHaveProperty('timestamp');
        done();
      }
    });

    socket.emit('chat_message', { message: testMessage });
  });

  it('should handle disconnection gracefully', (done) => {
    socket.on('disconnect', () => {
      expect(socket.connected).toBe(false);
      done();
    });

    socket.disconnect();
  });
});