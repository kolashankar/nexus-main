import React from "react";
/**
 * Custom hook for WebSocket
 */
import { useEffect, useCallback } from 'react';
import websocketService from '../services/websocket/websocketService';
import useStore from '../store';

export const useWebSocket = () => {
  const { accessToken, isAuthenticated } = useStore();

  useEffect(() => {
    if (isAuthenticated && accessToken) {
      websocketService.connect(accessToken);
    }

    return () => {
      if (!isAuthenticated) {
        websocketService.disconnect();
      }
    };
  }, [isAuthenticated, accessToken]);

  const send = useCallback((eventType, data) => {
    websocketService.send(eventType, data);
  }, []);

  const on = useCallback((eventType, handler) => {
    websocketService.on(eventType, handler);
  }, []);

  const off = useCallback((eventType, handler) => {
    websocketService.off(eventType, handler);
  }, []);

  return {
    send,
    on,
    off,
  };
};

export default useWebSocket;
