import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import GuildCard from '../GuildDashboard/GuildCard';
const mockGuild = {
    _id: 'guild123',
    name: 'Shadow Warriors',
    tag: 'SHDW',
    description: 'Elite combat guild',
    leader_id: 'leader123',
    total_members: 45,
    max_members: 100,
    level: 15,
    guild_karma: 1500,
    controlled_territories: [1, 3, 5],
    recruitment_open: true,
};
describe('GuildCard Component', () => {
    test('renders guild name', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText('Shadow Warriors')).toBeInTheDocument();
    });
    test('displays guild tag', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText('[SHDW]')).toBeInTheDocument();
    });
    test('shows guild description', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/Elite combat guild/i)).toBeInTheDocument();
    });
    test('displays member count', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/45\/100/)).toBeInTheDocument();
    });
    test('shows guild level', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/Level 15/i)).toBeInTheDocument();
    });
    test('displays guild karma', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/1,?500/)).toBeInTheDocument();
    });
    test('shows territory count', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/3 territories/i)).toBeInTheDocument();
    });
    test('displays recruitment status', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByText(/recruiting/i)).toBeInTheDocument();
    });
    test('shows join button when recruitment is open', () => {
        render(_jsx(GuildCard, { guild: mockGuild, mode: "browse" }));
        expect(screen.getByText(/join/i)).toBeInTheDocument();
    });
    test('hides join button when recruitment is closed', () => {
        const closedGuild = { ...mockGuild, recruitment_open: false };
        render(_jsx(GuildCard, { guild: closedGuild, mode: "browse" }));
        expect(screen.queryByText(/join/i)).not.toBeInTheDocument();
    });
    test('displays manage button for guild members', () => {
        render(_jsx(GuildCard, { guild: mockGuild, mode: "owned" }));
        expect(screen.getByText(/manage/i)).toBeInTheDocument();
    });
    test('shows member at capacity badge', () => {
        const fullGuild = { ...mockGuild, total_members: 100 };
        render(_jsx(GuildCard, { guild: fullGuild }));
        expect(screen.getByText(/full/i)).toBeInTheDocument();
    });
    test('handles join action', () => {
        const onJoin = jest.fn();
        render(_jsx(GuildCard, { guild: mockGuild, mode: "browse", onJoin: onJoin }));
        const joinButton = screen.getByText(/join/i);
        fireEvent.click(joinButton);
        expect(onJoin).toHaveBeenCalledWith(mockGuild._id);
    });
    test('displays guild emblem', () => {
        render(_jsx(GuildCard, { guild: mockGuild }));
        expect(screen.getByTestId('guild-emblem')).toBeInTheDocument();
    });
});
