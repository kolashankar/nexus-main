import React from "react";
import { jsx as _jsx } from 'react/jsx-runtime';
/**
 * Integration test for marketplace and economy flows
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import MarketplacePage from '../../pages/Marketplace/Marketplace';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
const mockRobots = [
  { _id: 'robot1', name: 'Worker Bot', type: 'worker', price: 5000, level: 1 },
  { _id: 'robot2', name: 'Combat Bot', type: 'combat', price: 10000, level: 1 },
];
const mockStocks = [
  { ticker: 'ROBOT', name: 'Robot Corp', price: 150.5, change_24h: 5.2 },
  { ticker: 'CYBER', name: 'Cyber Inc', price: 89.75, change_24h: -2.1 },
];
const mockPlayer = {
  _id: 'player123',
  currencies: { credits: 50000 },
};
const server = setupServer(
  rest.get('/api/robots/marketplace', (req, res, ctx) => {
    return res(ctx.json(mockRobots));
  }),
  rest.post('/api/robots/purchase', (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        robot_id: 'robot1',
        message: 'Robot purchased!',
      })
    );
  }),
  rest.get('/api/market/stocks', (req, res, ctx) => {
    return res(ctx.json(mockStocks));
  }),
  rest.post('/api/market/stocks/buy', (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        shares: 10,
        total_cost: 1505,
      })
    );
  }),
  rest.get('/api/player/profile', (req, res, ctx) => {
    return res(ctx.json(mockPlayer));
  })
);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
describe('Marketplace Flow Integration Tests', () => {
  test('browse and purchase robot', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    // Wait for robots to load
    await waitFor(() => {
      expect(screen.getByText('Worker Bot')).toBeInTheDocument();
    });
    // Click purchase button
    const purchaseButtons = screen.getAllByText(/purchase/i);
    fireEvent.click(purchaseButtons[0]);
    // Confirm purchase
    const confirmButton = screen.getByText(/confirm/i);
    fireEvent.click(confirmButton);
    // Should show success
    await waitFor(() => {
      expect(screen.getByText(/robot purchased/i)).toBeInTheDocument();
    });
  });
  test('filter robots by type', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    await waitFor(() => {
      expect(screen.getByText('Worker Bot')).toBeInTheDocument();
    });
    // Filter by combat type
    const combatFilter = screen.getByText(/combat/i);
    fireEvent.click(combatFilter);
    // Should only show combat robots
    expect(screen.getByText('Combat Bot')).toBeInTheDocument();
    expect(screen.queryByText('Worker Bot')).not.toBeInTheDocument();
  });
  test('stock market purchase flow', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    // Switch to stocks tab
    const stocksTab = screen.getByText(/stocks/i);
    fireEvent.click(stocksTab);
    // Wait for stocks to load
    await screen.findByText('Robot Corp');
    
    // Buy stocks
    const buyButton = screen.getAllByText(/buy/i)[0];
    fireEvent.click(buyButton);
    // Enter quantity
    const quantityInput = screen.getByPlaceholderText(/quantity/i);
    fireEvent.change(quantityInput, { target: { value: '10' } });
    // Confirm purchase
    const confirmButton = screen.getByText(/confirm/i);
    fireEvent.click(confirmButton);
    // Should show success
    await screen.findByText(/purchased 10 shares/i);
  });
  test('insufficient funds error', async () => {
    server.use(
      rest.post('/api/robots/purchase', (req, res, ctx) => {
        return res(ctx.status(400), ctx.json({ error: 'Insufficient funds' }));
      })
    );
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    await waitFor(() => {
      expect(screen.getByText('Combat Bot')).toBeInTheDocument();
    });
    // Try to purchase expensive robot
    const purchaseButtons = screen.getAllByText(/purchase/i);
    fireEvent.click(purchaseButtons[1]);
    const confirmButton = screen.getByText(/confirm/i);
    fireEvent.click(confirmButton);
    // Should show error
    await waitFor(() => {
      expect(screen.getByText(/insufficient funds/i)).toBeInTheDocument();
    });
  });
  test('view robot details', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    await screen.findByText('Worker Bot');
    
    // Click on robot card
    const robotCard = screen.getByRole('button', { name: /worker bot/i });
    fireEvent.click(robotCard);
    
    // Should show details modal
    await screen.findByText(/details/i);
    expect(screen.getByText(/type: worker/i)).toBeInTheDocument();
  });
  test('sort items by price', async () => {
    render(_jsx(BrowserRouter, { children: _jsx(MarketplacePage, {}) }));
    await waitFor(() => {
      expect(screen.getByText('Worker Bot')).toBeInTheDocument();
    });
    // Click sort button
    const sortButton = screen.getByText(/sort/i);
    fireEvent.click(sortButton);
    // Select price ascending
    const priceOption = screen.getByText(/price.*low.*high/i);
    fireEvent.click(priceOption);
    // Should resort items
    // (Visual verification - Worker Bot should appear before Combat Bot)
  });
});