import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { CheckCircle, Circle, Trophy, Star, Coins } from 'lucide-react';
export const QuestDetails = ({ quest, onAccept, onAbandon }) => {
    const getDifficultyColor = (difficulty) => {
        switch (difficulty.toLowerCase()) {
            case 'easy':
                return 'text-green-500 border-green-500';
            case 'medium':
                return 'text-yellow-500 border-yellow-500';
            case 'hard':
                return 'text-red-500 border-red-500';
            case 'legendary':
                return 'text-purple-500 border-purple-500';
            default:
                return 'text-gray-500 border-gray-500';
        }
    };
    const getTypeColor = (type) => {
        switch (type.toLowerCase()) {
            case 'daily':
                return 'bg-blue-500/20 text-blue-400';
            case 'weekly':
                return 'bg-purple-500/20 text-purple-400';
            case 'guild':
                return 'bg-green-500/20 text-green-400';
            case 'world':
                return 'bg-orange-500/20 text-orange-400';
            case 'hidden':
                return 'bg-pink-500/20 text-pink-400';
            default:
                return 'bg-gray-500/20 text-gray-400';
        }
    };
    const calculateOverallProgress = () => {
        if (quest.objectives.length === 0)
            return 0;
        const completed = quest.objectives.filter(obj => obj.completed).length;
        return (completed / quest.objectives.length) * 100;
    };
    return (_jsxs(Card, { className: "max-w-3xl mx-auto", children: [_jsx(CardHeader, { children: _jsx("div", { className: "flex items-start justify-between", children: _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center gap-2 mb-2", children: [_jsx(CardTitle, { className: "text-2xl", children: quest.title }), _jsx(Badge, { variant: "outline", className: getDifficultyColor(quest.difficulty), children: quest.difficulty }), _jsx(Badge, { className: getTypeColor(quest.quest_type), children: quest.quest_type })] }), _jsx(CardDescription, { className: "text-base", children: quest.description })] }) }) }), _jsxs(CardContent, { className: "space-y-6", children: [quest.lore && (_jsxs("div", { className: "bg-gray-800/50 p-4 rounded-lg border border-gray-700", children: [_jsx("h3", { className: "font-semibold mb-2 text-amber-400", children: "Story" }), _jsx("p", { className: "text-sm text-gray-300 italic", children: quest.lore })] })), _jsxs("div", { children: [_jsx("h3", { className: "font-semibold mb-3 text-lg", children: "Objectives" }), _jsx("div", { className: "space-y-3", children: quest.objectives.map((objective, idx) => (_jsx("div", { className: "space-y-2", children: _jsxs("div", { className: "flex items-center gap-2", children: [objective.completed ? (_jsx(CheckCircle, { className: "h-5 w-5 text-green-500 flex-shrink-0" })) : (_jsx(Circle, { className: "h-5 w-5 text-gray-500 flex-shrink-0" })), _jsxs("div", { className: "flex-1", children: [_jsx("p", { className: `text-sm ${objective.completed ? 'text-gray-400 line-through' : 'text-gray-200'}`, children: objective.description }), _jsxs("div", { className: "flex items-center gap-2 mt-1", children: [_jsx(Progress, { value: (objective.current / objective.required) * 100, className: "h-2 flex-1" }), _jsxs("span", { className: "text-xs text-gray-400 min-w-[60px] text-right", children: [objective.current, "/", objective.required] })] })] })] }) }, idx))) }), _jsxs("div", { className: "mt-4 pt-4 border-t border-gray-700", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-sm font-medium", children: "Overall Progress" }), _jsxs("span", { className: "text-sm text-blue-400", children: [Math.round(calculateOverallProgress()), "%"] })] }), _jsx(Progress, { value: calculateOverallProgress(), className: "h-3" })] })] }), _jsxs("div", { children: [_jsx("h3", { className: "font-semibold mb-3 text-lg", children: "Rewards" }), _jsxs("div", { className: "grid grid-cols-2 gap-3", children: [quest.rewards.credits > 0 && (_jsxs("div", { className: "bg-gray-800/50 p-3 rounded-lg flex items-center gap-2", children: [_jsx(Coins, { className: "h-5 w-5 text-yellow-500" }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-gray-400", children: "Credits" }), _jsx("p", { className: "font-semibold text-yellow-500", children: quest.rewards.credits })] })] })), quest.rewards.xp > 0 && (_jsxs("div", { className: "bg-gray-800/50 p-3 rounded-lg flex items-center gap-2", children: [_jsx(Star, { className: "h-5 w-5 text-blue-500" }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-gray-400", children: "Experience" }), _jsxs("p", { className: "font-semibold text-blue-500", children: [quest.rewards.xp, " XP"] })] })] })), quest.rewards.karma !== 0 && (_jsxs("div", { className: "bg-gray-800/50 p-3 rounded-lg flex items-center gap-2", children: [_jsx(Trophy, { className: "h-5 w-5 text-purple-500" }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-gray-400", children: "Karma" }), _jsxs("p", { className: `font-semibold ${quest.rewards.karma > 0 ? 'text-green-500' : 'text-red-500'}`, children: [quest.rewards.karma > 0 ? '+' : '', quest.rewards.karma] })] })] })), quest.rewards.items && quest.rewards.items.length > 0 && (_jsxs("div", { className: "bg-gray-800/50 p-3 rounded-lg flex items-center gap-2", children: [_jsx("div", { className: "h-5 w-5 text-amber-500", children: "\uD83D\uDCE6" }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-gray-400", children: "Items" }), _jsxs("p", { className: "font-semibold text-amber-500", children: [quest.rewards.items.length, " items"] })] })] }))] }), quest.rewards.trait_boosts && Object.keys(quest.rewards.trait_boosts).length > 0 && (_jsxs("div", { className: "mt-3 bg-gradient-to-r from-purple-900/20 to-transparent p-3 rounded-lg", children: [_jsx("p", { className: "text-sm font-medium mb-2 text-purple-400", children: "Trait Bonuses" }), _jsx("div", { className: "flex flex-wrap gap-2", children: Object.entries(quest.rewards.trait_boosts).map(([trait, boost]) => (_jsxs(Badge, { variant: "outline", className: "text-xs", children: [trait, ": +", boost] }, trait))) })] }))] }), _jsxs("div", { className: "flex gap-3", children: [quest.status === 'available' && onAccept && (_jsx(Button, { onClick: () => onAccept(quest._id), className: "flex-1", children: "Accept Quest" })), quest.status === 'active' && onAbandon && (_jsx(Button, { onClick: () => onAbandon(quest._id), variant: "destructive", className: "flex-1", children: "Abandon Quest" }))] }), quest.expires_at && (_jsx("div", { className: "bg-red-900/20 border border-red-500/30 p-3 rounded-lg", children: _jsxs("p", { className: "text-sm text-red-400", children: ["\u26A0\uFE0F This quest expires on ", new Date(quest.expires_at).toLocaleString()] }) }))] })] }));
};
