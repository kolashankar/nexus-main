import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { GuildQuests } from '../GuildQuests';
import '@testing-library/jest-dom';

// Mock fetch
global.fetch = jest.fn();

const mockGuildQuests = {
  available: [
    {
      id: 'gq1',
      title: 'Guild Raid',
      description: 'Operation completed',
      guild_id: 'guild1',
      objectives: [],
      rewards: { guild_reputation: 100, guild_xp: 500 },
      participants: [],
      required_members: 5,
      status: 'available',
    },
  ],
  active: [
    {
      id: 'gq2',
      title: 'Territory Defense',
      description: 'Operation completed',
      guild_id: 'guild1',
      objectives: [
        { description: 'Defeat 10 invaders', current: 5, required: 10, completed: false },
      ],
      rewards: { guild_reputation: 150, guild_xp: 750 },
      participants: ['player1', 'player2'],
      required_members: 3,
      status: 'active',
    },
  ],
};

describe('GuildQuests Component', () => {
  beforeEach(() => {
    (global.fetch).mockClear();
  });

  it('renders guild quests', async () => {
    (global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockGuildQuests),
    });

    render(<GuildQuests />);

    await screen.findByText('Guild Raid');
    expect(screen.getByText('Territory Defense')).toBeInTheDocument();
  });

  it('displays quest progress', async () => {
    (global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockGuildQuests),
    });

    render(<GuildQuests />);

    await screen.findByText('5/10');
  });

  it('handles joining a guild quest', async () => {
    (global.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockGuildQuests),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      });

    render(<GuildQuests />);

    const joinButton = await screen.findByText('Join Quest');
    fireEvent.click(joinButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/join'),
        expect.any(Object)
      );
    });
  });
});
