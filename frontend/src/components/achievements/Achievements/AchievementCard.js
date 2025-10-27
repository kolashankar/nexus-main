import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardHeader, CardTitle, CardContent } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Progress } from '../../ui/progress';
import { Trophy, Lock } from 'lucide-react';
const rarityColors = {
    common: 'bg-gray-500',
    uncommon: 'bg-green-500',
    rare: 'bg-blue-500',
    epic: 'bg-purple-500',
    legendary: 'bg-yellow-500',
};
const AchievementCard = ({ achievement, unlocked, progress }) => {
    return (_jsxs(Card, { className: unlocked ? 'border-2 border-primary' : 'opacity-75', children: [_jsx(CardHeader, { children: _jsx("div", { className: "flex items-start justify-between", children: _jsxs("div", { className: "flex items-center gap-2", children: [unlocked ? (_jsx(Trophy, { className: "h-6 w-6 text-yellow-500" })) : (_jsx(Lock, { className: "h-6 w-6 text-muted-foreground" })), _jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: achievement.name }), _jsx("p", { className: "text-sm text-muted-foreground", children: achievement.description })] })] }) }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { className: `${rarityColors[achievement.rarity]} text-white capitalize`, children: achievement.rarity }), _jsxs(Badge, { variant: "outline", children: [achievement.points, " pts"] })] }), progress && !unlocked && (_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-sm mb-1", children: [_jsx("span", { children: "Progress" }), _jsxs("span", { children: [progress.current_progress, "/", progress.required_progress] })] }), _jsx(Progress, { value: progress.percentage, className: "h-2" })] })), _jsx(Badge, { variant: "secondary", className: "text-xs capitalize", children: achievement.category.replace('_', ' ') })] })] }));
};
export default AchievementCard;
