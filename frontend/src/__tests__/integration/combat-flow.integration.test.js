import React from "react";
import { jsx as _jsx } from 'react/jsx-runtime';
/**
 * Integration test for combat system flow
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import CombatPage from '../../pages/Combat/Combat';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
const mockCombatState = {
  battle_id: 'battle123',
  player1: {
    id: 'player123',
    username: 'TestPlayer',
    hp: 100,
    max_hp: 100,
    ap: 4,
  },
  player2: {
    id: 'opponent123',
    username: 'Opponent',
    hp: 100,
    max_hp: 100,
    ap: 4,
  },
  current_turn: 'player123',
  turn_number: 1,
  status: 'active',
  log: [],
};
const server = setupServer(
  rest.post('/api/combat/challenge', (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        battle_id: 'battle123',
        message: 'Challenge sent!',
      })
    );
  }),
  rest.get('/api/combat/state', (req, res, ctx) => {
    return res(ctx.json(mockCombatState));
  }),
  rest.post('/api/combat/action', (req, res, ctx) => {
    const updatedState = {
      ...mockCombatState,
      player2: { ...mockCombatState.player2, hp: 75 },
      current_turn: 'opponent123',
      turn_number: 2,
      log: ['TestPlayer attacks for 25 damage!'],
    };
    return res(ctx.json(updatedState));
  })
);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
describe('Combat Flow Integration Tests', () => {
  test('challenge another player flow', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, {}) }));
    // Click challenge button
    const challengeButton = screen.getByText(/challenge player/i);
    fireEvent.click(challengeButton);
    // Enter opponent name
    const opponentInput = screen.getByPlaceholderText(/player name/i);
    fireEvent.change(opponentInput, { target: { value: 'Opponent' } });
    // Send challenge
    const sendButton = screen.getByText(/send challenge/i);
    fireEvent.click(sendButton);
    // Should show success
    await waitFor(() => {
      expect(screen.getByText(/challenge sent/i)).toBeInTheDocument();
    });
  });
  test('complete combat turn flow', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, { battleId: 'battle123' }) }));
    // Wait for combat to load
    await screen.findByText('TestPlayer');
    expect(screen.getByText('Opponent')).toBeInTheDocument();
    
    // Player's turn - attack
    const attackButton = screen.getByText(/attack/i);
    fireEvent.click(attackButton);
    // Should update combat state
    await screen.findByText(/attacks for 25 damage/i);
    
    // Turn should change
    expect(screen.getByText(/Opponent's turn/i)).toBeInTheDocument();
  });
  test('display action points correctly', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, { battleId: 'battle123' }) }));
    await waitFor(() => {
      expect(screen.getByText(/AP: 4/i)).toBeInTheDocument();
    });
  });
  test('use special ability', async () => {
    server.use(
      rest.post('/api/combat/action', (req, res, ctx) => {
        return res(
          ctx.json({
            ...mockCombatState,
            player1: { ...mockCombatState.player1, ap: 2 },
            player2: { ...mockCombatState.player2, hp: 65 },
            log: ['TestPlayer uses Heavy Attack for 35 damage!'],
          })
        );
      })
    );
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, { battleId: 'battle123' }) }));
    await screen.findByText(/attack/i);
    
    // Open abilities menu
    const abilitiesButton = screen.getByText(/abilities/i);
    fireEvent.click(abilitiesButton);
    // Use heavy attack
    const heavyAttack = screen.getByText(/heavy attack/i);
    fireEvent.click(heavyAttack);
    // Should consume AP and deal damage
    await screen.findByText(/AP: 2/i);
    expect(screen.getByText(/Heavy Attack/i)).toBeInTheDocument();
  });
  test('combat victory flow', async () => {
    server.use(
      rest.get('/api/combat/state', (req, res, ctx) => {
        return res(
          ctx.json({
            ...mockCombatState,
            status: 'ended',
            winner: 'player123',
            player2: { ...mockCombatState.player2, hp: 0 },
          })
        );
      })
    );
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, { battleId: 'battle123' }) }));
    // Should show victory screen
    await screen.findByText(/victory/i);
    // Should display rewards
    expect(screen.getByText(/rewards/i)).toBeInTheDocument();
  });
  test('flee from combat', async () => {
    server.use(
      rest.post('/api/combat/flee', (req, res, ctx) => {
        return res(
          ctx.json({
            success: true,
            message: 'You fled from combat!',
          })
        );
      })
    );
    render(_jsx(BrowserRouter, { children: _jsx(CombatPage, { battleId: 'battle123' }) }));
    await waitFor(() => {
      expect(screen.getByText(/flee/i)).toBeInTheDocument();
    });
    const fleeButton = screen.getByText(/flee/i);
    fireEvent.click(fleeButton);
    // Confirm flee
    const confirmButton = screen.getByText(/confirm/i);
    fireEvent.click(confirmButton);
    await waitFor(() => {
      expect(screen.getByText(/fled from combat/i)).toBeInTheDocument();
    });
  });
});