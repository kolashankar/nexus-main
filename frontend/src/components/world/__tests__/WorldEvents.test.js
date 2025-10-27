import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import WorldEventsPanel from '../WorldEventsPanel';
const mockEvents = [
    {
        id: 'event1',
        name: 'Golden Age',
        type: 'positive',
        description: 'Double XP for all players',
        active: true,
        ends_at: '2024-12-31T23:59:59Z',
    },
    {
        id: 'event2',
        name: 'Economic Crash',
        type: 'negative',
        description: 'Market prices unstable',
        active: false,
        started_at: '2024-01-01T00:00:00Z',
    },
];
describe('WorldEventsPanel Component', () => {
    test('renders active events', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        expect(screen.getByText('Golden Age')).toBeInTheDocument();
    });
    test('displays event descriptions', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        expect(screen.getByText(/Double XP/i)).toBeInTheDocument();
    });
    test('shows active event badge', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        expect(screen.getByText(/active/i)).toBeInTheDocument();
    });
    test('displays event countdown timer', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        expect(screen.getByText(/ends in/i)).toBeInTheDocument();
    });
    test('categorizes events by type', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        const positiveEvent = screen.getByRole('listitem', { name: /golden age/i });
        expect(positiveEvent).toHaveClass(/positive/i);
    });
    test('shows event history', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents, showHistory: true }));
        expect(screen.getByText('Economic Crash')).toBeInTheDocument();
    });
    test('filters events by type', () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        const filterButton = screen.getByText(/positive/i);
        fireEvent.click(filterButton);
        expect(screen.getByText('Golden Age')).toBeInTheDocument();
    });
    test('displays event effects', () => {
        const eventWithEffects = {
            ...mockEvents[0],
            effects: { xp_multiplier: 2, credit_multiplier: 2 },
        };
        render(_jsx(WorldEventsPanel, { events: [eventWithEffects] }));
        expect(screen.getByText(/2x/i)).toBeInTheDocument();
    });
    test('shows empty state when no events', () => {
        render(_jsx(WorldEventsPanel, { events: [] }));
        expect(screen.getByText(/no active events/i)).toBeInTheDocument();
    });
    test('updates countdown in real-time', async () => {
        render(_jsx(WorldEventsPanel, { events: mockEvents }));
        // Timer should update
        await new Promise(resolve => setTimeout(resolve, 1000));
    });
});