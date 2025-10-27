import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import BattlePass from '../BattlePass/BattlePass';
const mockBattlePassData = {
    season: 2,
    current_tier: 15,
    max_tier: 100,
    xp: 15000,
    xp_to_next: 1000,
    premium: true,
    rewards: [
        { tier: 1, type: 'credits', amount: 500, unlocked: true },
        { tier: 5, type: 'cosmetic', item: 'Cool Skin', unlocked: true },
        { tier: 10, type: 'robot', item: 'Scout Bot', unlocked: true },
        { tier: 15, type: 'superpower', item: 'Mind Reading', unlocked: true },
        { tier: 20, type: 'credits', amount: 2000, unlocked: false },
    ],
};
describe('BattlePass Component', () => {
    test('renders season number', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        expect(screen.getByText(/Season 2/i)).toBeInTheDocument();
    });
    test('displays current tier', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        expect(screen.getByText(/Tier 15/i)).toBeInTheDocument();
    });
    test('shows XP progress', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        expect(screen.getByText(/15,?000/)).toBeInTheDocument();
    });
    test('displays progress bar', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const progressBar = screen.getByRole('progressbar');
        expect(progressBar).toBeInTheDocument();
    });
    test('shows premium badge', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        expect(screen.getByText(/premium/i)).toBeInTheDocument();
    });
    test('displays free tier rewards', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        expect(screen.getByText(/500/)).toBeInTheDocument(); // credits
    });
    test('shows locked rewards', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const lockedRewards = screen.getAllByTestId(/locked-reward/i);
        expect(lockedRewards.length).toBeGreaterThan(0);
    });
    test('displays unlocked rewards differently', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const unlockedReward = screen.getByText('Cool Skin');
        const rewardContainer = screen.getByRole('listitem', {name: /cool skin/i});
        expect(rewardContainer).not.toHaveClass(/locked/i);
    });
    test('shows upgrade to premium button for free users', () => {
        const freeData = { ...mockBattlePassData, premium: false };
        render(_jsx(BattlePass, { data: freeData }));
        expect(screen.getByText(/upgrade/i)).toBeInTheDocument();
    });
    test('displays tier track', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const tierTrack = screen.getByTestId('tier-track');
        expect(tierTrack).toBeInTheDocument();
    });
    test('highlights current tier on track', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const currentTier = screen.getByTestId('tier-15');
        expect(currentTier).toHaveClass(/current/i);
    });
    test('shows reward preview on hover', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        const reward = screen.getByText('Cool Skin');
        fireEvent.mouseEnter(reward);
        // Tooltip should appear
    });
    test('calculates percentage to next tier', () => {
        render(_jsx(BattlePass, { data: mockBattlePassData }));
        // Should show percentage based on xp and xp_to_next
        expect(screen.getByText(/93%|94%/)).toBeInTheDocument();
    });
});