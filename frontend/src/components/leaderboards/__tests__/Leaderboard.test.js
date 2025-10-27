import React from "react";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Leaderboard from '../Leaderboard/Leaderboard';

const mockLeaderboardData = [
  { rank: 1, username: 'Player1', value: 10000, player_id: '1' },
  { rank: 2, username: 'Player2', value: 8500, player_id: '2' },
  { rank: 3, username: 'Player3', value: 7000, player_id: '3' },
  { rank: 4, username: 'Player4', value: 6000, player_id: '4' },
  { rank: 5, username: 'Player5', value: 5500, player_id: '5' },
];

describe('Leaderboard Component', () => {
  test('renders leaderboard title', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} />);
    expect(screen.getByText('Karma Leaders')).toBeInTheDocument();
  });

  test('displays all players in order', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} />);
    expect(screen.getByText('Player1')).toBeInTheDocument();
    expect(screen.getByText('Player2')).toBeInTheDocument();
    expect(screen.getByText('Player5')).toBeInTheDocument();
  });

  test('shows rank numbers', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} />);
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  test('displays player values', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} />);
    expect(screen.getByText(/10,?000/)).toBeInTheDocument();
    expect(screen.getByText(/8,?500/)).toBeInTheDocument();
  });

  test('highlights top 3 players differently', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} />);
    const firstPlace = screen.getByRole('listitem', { name: /Player1/i });
    expect(firstPlace).toHaveClass(/gold|first/i);
  });

  test('highlights current player', () => {
    render(<Leaderboard title="Karma Leaders" data={mockLeaderboardData} currentPlayerId="3" />);
    const currentPlayer = screen.getByRole('listitem', { name: /Player3/i });
    expect(currentPlayer).toHaveClass(/current|highlight/i);
  });

  test('shows empty state when no data', () => {
    render(<Leaderboard title="Karma Leaders" data={[]} />);
    expect(screen.getByText(/no players/i)).toBeInTheDocument();
  });

  test('displays category tabs', () => {
    render(
      <Leaderboard
        title="Karma Leaders"
        data={mockLeaderboardData}
        categories={['karma', 'wealth']}
      />
    );
    expect(screen.getByText(/karma/i)).toBeInTheDocument();
    expect(screen.getByText(/wealth/i)).toBeInTheDocument();
  });

  test('switches between categories', () => {
    const onCategoryChange = jest.fn();
    render(
      <Leaderboard
        title="Karma Leaders"
        data={mockLeaderboardData}
        categories={['karma', 'wealth']}
        onCategoryChange={onCategoryChange}
      />
    );
    
    const wealthTab = screen.getByText(/wealth/i);
    fireEvent.click(wealthTab);
    
    expect(onCategoryChange).toHaveBeenCalledWith('wealth');
  });

  test('shows player rank outside top 10', () => {
    render(
      <Leaderboard
        title="Karma Leaders"
        data={mockLeaderboardData}
        currentPlayerRank={{ rank: 25, value: 2000 }}
      />
    );
    expect(screen.getByText(/Your rank/i)).toBeInTheDocument();
  });

  test('displays pagination for large datasets', () => {
    const largeData = Array.from({ length: 50 }, (_, i) => ({
      rank: i + 1,
      username: `Player${i + 1}`,
      value: 10000 - i * 100,
      player_id: `${i + 1}`,
    }));
    
    render(<Leaderboard title="Karma Leaders" data={largeData} totalPages={5} currentPage={1} />);
    expect(screen.getByText(/1.*10.*50/)).toBeInTheDocument();
  });
});
