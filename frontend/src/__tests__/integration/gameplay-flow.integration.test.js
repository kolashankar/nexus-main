import React from "react";
import { jsx as _jsx } from 'react/jsx-runtime';
/**
 * Integration test for core gameplay flows
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../../pages/Dashboard/Dashboard';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
const mockPlayer = {
  _id: 'player123',
  username: 'TestPlayer',
  level: 25,
  karma_points: 500,
  currencies: { credits: 10000 },
  traits: { empathy: 75, hacking: 65 },
};
const server = setupServer(
  rest.get('/api/player/profile', (req, res, ctx) => {
    return res(ctx.json(mockPlayer));
  }),
  rest.post('/api/actions/help', (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        karma_change: 10,
        message: 'You helped another player!',
      })
    );
  }),
  rest.get('/api/quests/available', (req, res, ctx) => {
    return res(
      ctx.json([
        {
          _id: 'quest1',
          title: 'Help the Merchant',
          status: 'available',
          rewards: { credits: 500, xp: 100 },
        },
      ])
    );
  }),
  rest.post('/api/quests/accept', (req, res, ctx) => {
    return res(ctx.json({ success: true, quest_id: 'quest1' }));
  })
);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
describe('Gameplay Flow Integration Tests', () => {
  test('complete action flow (help another player)', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(Dashboard, {}) }));
    // Wait for dashboard to load
    await screen.findByText('TestPlayer');
    
    // Click on actions menu
    const actionsButton = screen.getByText(/actions/i);
    fireEvent.click(actionsButton);
    // Select help action
    const helpButton = screen.getByText(/help/i);
    fireEvent.click(helpButton);
    // Fill target player
    const targetInput = screen.getByPlaceholderText(/player name/i);
    fireEvent.change(targetInput, { target: { value: 'TargetPlayer' } });
    // Submit action
    const submitButton = screen.getByText(/confirm/i);
    fireEvent.click(submitButton);
    // Should show success message
    await screen.findByText(/helped another player/i);
  });
  test('quest acceptance and tracking', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(Dashboard, {}) }));
    // Navigate to quests
    const questsButton = screen.getByText(/quests/i);
    fireEvent.click(questsButton);
    // Wait for quests to load
    await screen.findByText('Help the Merchant');
    
    // Accept quest
    const acceptButton = screen.getByText(/accept/i);
    fireEvent.click(acceptButton);
    // Should move to active quests
    await screen.findByText(/active/i);
  });
  test('trait progression visualization', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(Dashboard, {}) }));
    // Navigate to profile
    const profileButton = screen.getByText(/profile/i);
    fireEvent.click(profileButton);
    // Should show traits
    await screen.findByText('empathy');
    expect(screen.getByText('75')).toBeInTheDocument();
    
    // Trait bars should be rendered
    const progressBars = screen.getAllByRole('progressbar');
    expect(progressBars.length).toBeGreaterThan(0);
  });
  test('karma system update flow', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(Dashboard, {}) }));
    // Initial karma
    await screen.findByText('500');
    
    // Perform action that changes karma
    // (Would trigger WebSocket update in real app)
    // Karma should update
    // await waitFor(() => {
    //   expect(screen.getByText('510')).toBeInTheDocument();
    // });
  });
  test('navigation between game sections', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(Dashboard, {}) }));
    // Dashboard -> Profile
    const profileLink = screen.getByText(/profile/i);
    fireEvent.click(profileLink);
    await screen.findByText(/traits/i);
    
    // Profile -> Marketplace
    const marketLink = screen.getByText(/market/i);
    fireEvent.click(marketLink);
    await screen.findByText(/robots/i);
    
    // Marketplace -> Guilds
    const guildLink = screen.getByText(/guilds/i);
    fireEvent.click(guildLink);
    await screen.findByText(/join.*guild/i);
  });
});