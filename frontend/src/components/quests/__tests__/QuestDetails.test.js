import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent } from '@testing-library/react';
import { QuestDetails } from '../QuestDetails';
import '@testing-library/jest-dom';
const mockQuest = {
    _id: '1',
    title: 'Test Quest',
    description: 'A test quest description',
    lore: 'Ancient lore about the quest',
    quest_type: 'daily',
    difficulty: 'medium',
    objectives: [
        {
            description: 'Complete objective 1',
            type: 'collect',
            current: 5,
            required: 10,
            completed: false
        },
        {
            description: 'Complete objective 2',
            type: 'defeat',
            current: 3,
            required: 3,
            completed: true
        }
    ],
    rewards: {
        credits: 500,
        xp: 100,
        karma: 10,
        items: ['item1'],
        trait_boosts: { hacking: 5 }
    },
    status: 'available'
};
describe('QuestDetails', () => {
    it('renders quest information', () => {
        render(_jsx(QuestDetails, { quest: mockQuest }));
        expect(screen.getByText('Test Quest')).toBeInTheDocument();
        expect(screen.getByText('A test quest description')).toBeInTheDocument();
        expect(screen.getByText('Ancient lore about the quest')).toBeInTheDocument();
    });
    it('displays quest objectives', () => {
        render(_jsx(QuestDetails, { quest: mockQuest }));
        expect(screen.getByText('Complete objective 1')).toBeInTheDocument();
        expect(screen.getByText('Complete objective 2')).toBeInTheDocument();
        expect(screen.getByText('5/10')).toBeInTheDocument();
        expect(screen.getByText('3/3')).toBeInTheDocument();
    });
    it('displays rewards correctly', () => {
        render(_jsx(QuestDetails, { quest: mockQuest }));
        expect(screen.getByText('500')).toBeInTheDocument();
        expect(screen.getByText('100 XP')).toBeInTheDocument();
        expect(screen.getByText('+10')).toBeInTheDocument();
    });
    it('calls onAccept when accept button is clicked', () => {
        const mockOnAccept = jest.fn();
        render(_jsx(QuestDetails, { quest: mockQuest, onAccept: mockOnAccept }));
        const acceptButton = screen.getByText('Accept Quest');
        fireEvent.click(acceptButton);
        expect(mockOnAccept).toHaveBeenCalledWith('1');
    });
    it('calls onAbandon when abandon button is clicked', () => {
        const mockOnAbandon = jest.fn();
        const activeQuest = { ...mockQuest, status: 'active' };
        render(_jsx(QuestDetails, { quest: activeQuest, onAbandon: mockOnAbandon }));
        const abandonButton = screen.getByText('Abandon Quest');
        fireEvent.click(abandonButton);
        expect(mockOnAbandon).toHaveBeenCalledWith('1');
    });
    it('shows overall progress', () => {
        render(_jsx(QuestDetails, { quest: mockQuest }));
        // 1 out of 2 objectives completed = 50%
        expect(screen.getByText('50%')).toBeInTheDocument();
    });
    it('displays difficulty badge', () => {
        render(_jsx(QuestDetails, { quest: mockQuest }));
        expect(screen.getByText('medium')).toBeInTheDocument();
    });
});
