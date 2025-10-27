import React from "react";
import { jsx as _jsx } from 'react/jsx-runtime';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SeasonalDashboard } from '../../pages/Seasonal/SeasonalDashboard';
// Mock API
jest.mock('../../services/api/client');
describe('SeasonalDashboard', () => {
  const mockSeasonData = {
    currentSeason: 3,
    seasonStart: new Date('2025-01-01').toISOString(),
    seasonEnd: new Date('2025-03-31').toISOString(),
    battlePassTier: 45,
    battlePassPremium: true,
    seasonRank: 127,
  };
  beforeEach(() => {
    jest.clearAllMocks();
  });
  it('renders seasonal dashboard correctly', async () => {
    render(_jsx(SeasonalDashboard, {}));
    await waitFor(() => {
      expect(screen.getByText(/Season 3/i)).toBeInTheDocument();
    });
  });
  it('displays current battle pass tier', async () => {
    render(_jsx(SeasonalDashboard, {}));
    await waitFor(() => {
      expect(screen.getByText(/Tier 45/i)).toBeInTheDocument();
    });
  });
  it('shows premium badge for premium users', async () => {
    render(_jsx(SeasonalDashboard, {}));
    await waitFor(() => {
      expect(screen.getByText(/Premium/i)).toBeInTheDocument();
    });
  });
  it('displays seasonal leaderboard position', async () => {
    render(_jsx(SeasonalDashboard, {}));
    await waitFor(() => {
      expect(screen.getByText(/Rank.*127/i)).toBeInTheDocument();
    });
  });
  it('handles season end countdown', async () => {
    render(_jsx(SeasonalDashboard, {}));
    await waitFor(() => {
      expect(screen.getByText(/Time Remaining/i)).toBeInTheDocument();
    });
  });
});
