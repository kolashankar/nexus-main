import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ProfileCard from '../ProfileCard/ProfileCard';
import { BrowserRouter } from 'react-router-dom';
const mockPlayer = {
    _id: 'player123',
    username: 'TestPlayer',
    level: 25,
    xp: 15000,
    karma_points: 500,
    economic_class: 'middle',
    moral_class: 'good',
    currencies: {
        credits: 10000,
        karma_tokens: 50,
    },
    stats: {
        total_actions: 150,
        pvp_wins: 10,
        quests_completed: 30,
    },
};
describe('ProfileCard Component', () => {
    const renderComponent = (player = mockPlayer) => {
        return render(_jsx(BrowserRouter, { children: _jsx(ProfileCard, { player: player }) }));
    };
    test('renders player username', () => {
        renderComponent();
        expect(screen.getByText('TestPlayer')).toBeInTheDocument();
    });
    test('displays player level', () => {
        renderComponent();
        expect(screen.getByText(/Level 25/i)).toBeInTheDocument();
    });
    test('shows karma points', () => {
        renderComponent();
        expect(screen.getByText(/500/)).toBeInTheDocument();
    });
    test('displays credits correctly', () => {
        renderComponent();
        expect(screen.getByText(/10,?000/)).toBeInTheDocument();
    });
    test('shows economic class badge', () => {
        renderComponent();
        expect(screen.getByText(/middle/i)).toBeInTheDocument();
    });
    test('displays moral class', () => {
        renderComponent();
        expect(screen.getByText(/good/i)).toBeInTheDocument();
    });
    test('shows player stats', () => {
        renderComponent();
        expect(screen.getByText(/150/)).toBeInTheDocument(); // total actions
        expect(screen.getByText(/30/)).toBeInTheDocument(); // quests completed
    });
    test('renders with different karma (negative)', () => {
        const negativeKarmaPlayer = { ...mockPlayer, karma_points: -300 };
        renderComponent(negativeKarmaPlayer);
        expect(screen.getByText(/-300/)).toBeInTheDocument();
    });
    test('handles missing stats gracefully', () => {
        const playerWithoutStats = { ...mockPlayer, stats: undefined };
        renderComponent(playerWithoutStats);
        expect(screen.getByText('TestPlayer')).toBeInTheDocument();
    });
    test('displays XP progress bar', () => {
        renderComponent();
        const progressBars = screen.getAllByRole('progressbar');
        expect(progressBars.length).toBeGreaterThan(0);
    });
});
