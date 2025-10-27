import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CombatArena from '../CombatArena/CombatArena';
const mockCombatState = {
    battle_id: 'battle123',
    player1: {
        id: 'player1',
        username: 'Warrior',
        hp: 80,
        max_hp: 100,
        ap: 4,
    },
    player2: {
        id: 'player2',
        username: 'Mage',
        hp: 60,
        max_hp: 100,
        ap: 4,
    },
    current_turn: 'player1',
    turn_number: 1,
    status: 'active',
};
describe('CombatArena Component', () => {
    test('renders both players', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState }));
        expect(screen.getByText('Warrior')).toBeInTheDocument();
        expect(screen.getByText('Mage')).toBeInTheDocument();
    });
    test('displays health bars for both players', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState }));
        const healthBars = screen.getAllByRole('progressbar');
        expect(healthBars.length).toBeGreaterThanOrEqual(2);
    });
    test('shows current turn indicator', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState }));
        expect(screen.getByText(/Turn 1/i)).toBeInTheDocument();
        expect(screen.getByText(/Warrior's turn/i)).toBeInTheDocument();
    });
    test('displays action buttons when it is player turn', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState, playerId: "player1" }));
        expect(screen.getByText(/attack/i)).toBeInTheDocument();
        expect(screen.getByText(/defend/i)).toBeInTheDocument();
    });
    test('disables actions when not player turn', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState, playerId: "player2" }));
        const attackButton = screen.getByText(/attack/i);
        expect(attackButton).toBeDisabled();
    });
    test('shows action points (AP)', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState, playerId: "player1" }));
        expect(screen.getByText(/AP: 4/i)).toBeInTheDocument();
    });
    test('displays combat log', () => {
        const stateWithLog = {
            ...mockCombatState,
            log: ['Warrior attacks Mage for 25 damage!']
        };
        render(_jsx(CombatArena, { combatState: stateWithLog }));
        expect(screen.getByText(/Warrior attacks Mage/i)).toBeInTheDocument();
    });
    test('handles attack action', async () => {
        const onAction = jest.fn();
        render(_jsx(CombatArena, { combatState: mockCombatState, playerId: "player1", onAction: onAction }));
        const attackButton = screen.getByText(/attack/i);
        fireEvent.click(attackButton);
        await waitFor(() => {
            expect(onAction).toHaveBeenCalledWith('attack');
        });
    });
    test('shows victory screen when battle ends', () => {
        const victoryState = { ...mockCombatState, status: 'ended', winner: 'player1' };
        render(_jsx(CombatArena, { combatState: victoryState, playerId: "player1" }));
        expect(screen.getByText(/victory/i)).toBeInTheDocument();
    });
    test('displays flee button', () => {
        render(_jsx(CombatArena, { combatState: mockCombatState, playerId: "player1" }));
        expect(screen.getByText(/flee/i)).toBeInTheDocument();
    });
});
