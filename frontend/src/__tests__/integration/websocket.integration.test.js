import React from "react";
/**
 * Integration tests for WebSocket connection
 */

import websocketService from '../../services/websocket/websocketService';
import WS from 'jest-websocket-mock';

let server;

beforeEach(() => {
  server = new WS('ws://localhost:8001/ws');
});

afterEach(() => {
  WS.clean();
});

describe('WebSocket Integration Tests', () => {
  describe('Connection', () => {
    test('connects to WebSocket server', async () => {
      websocketService.connect('test-token');
      await server.connected;

      expect(server).toHaveReceivedMessages([
        {
          type: 'auth',
          token: 'test-token',
        },
      ]);
    });

    test('reconnects on disconnect', async () => {
      websocketService.connect('test-token');
      await server.connected;

      server.close();

      // Should attempt reconnect
      await new Promise((resolve) => setTimeout(resolve, 1000));
    });
  });

  describe('Message Handling', () => {
    test('receives player_joined event', async () => {
      const handler = jest.fn();
      websocketService.on('player_joined', handler);

      websocketService.connect('test-token');
      await server.connected;

      server.send(
        JSON.stringify({
          type: 'player_joined',
          data: { username: 'newplayer' },
        })
      );

      expect(handler).toHaveBeenCalledWith({ username: 'newplayer' });
    });

    test('receives karma_changed event', async () => {
      const handler = jest.fn();
      websocketService.on('karma_changed', handler);

      websocketService.connect('test-token');
      await server.connected;

      server.send(
        JSON.stringify({
          type: 'karma_changed',
          data: { old_karma: 100, new_karma: 110 },
        })
      );

      expect(handler).toHaveBeenCalledWith({ old_karma: 100, new_karma: 110 });
    });
  });

  describe('Sending Messages', () => {
    test('sends chat message', async () => {
      websocketService.connect('test-token');
      await server.connected;

      websocketService.sendMessage('chat_message', {
        message: 'Hello',
        room: 'global',
      });

      await expect(server).toReceiveMessage(
        JSON.stringify({
          type: 'chat_message',
          data: { message: 'Hello', room: 'global' },
        })
      );
    });

    test('sends location update', async () => {
      websocketService.connect('test-token');
      await server.connected;

      websocketService.sendMessage('location_update', {
        x: 100,
        y: 200,
        z: 0,
      });

      await expect(server).toReceiveMessage(
        JSON.stringify({
          type: 'location_update',
          data: { x: 100, y: 200, z: 0 },
        })
      );
    });
  });

  describe('Room Management', () => {
    test('joins room', async () => {
      websocketService.connect('test-token');
      await server.connected;

      websocketService.joinRoom('guild-123');

      await expect(server).toReceiveMessage(
        JSON.stringify({
          type: 'join_room',
          data: { room: 'guild-123' },
        })
      );
    });

    test('leaves room', async () => {
      websocketService.connect('test-token');
      await server.connected;

      websocketService.leaveRoom('guild-123');

      await expect(server).toReceiveMessage(
        JSON.stringify({
          type: 'leave_room',
          data: { room: 'guild-123' },
        })
      );
    });
  });

  describe('Error Handling', () => {
    test('handles connection error', async () => {
      const errorHandler = jest.fn();
      websocketService.on('error', errorHandler);

      server.error();

      expect(errorHandler).toHaveBeenCalled();
    });

    test('handles malformed messages', async () => {
      websocketService.connect('test-token');
      await server.connected;

      server.send('invalid json');

      // Should not crash
    });
  });
});
