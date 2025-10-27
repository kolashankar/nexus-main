import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Trophy, Clock } from 'lucide-react';
export const WeeklyQuests = () => {
    const [quests, setQuests] = useState([]);
    const [resetTime, setResetTime] = useState('');
    useEffect(() => {
        fetchWeeklyQuests();
    }, []);
    const fetchWeeklyQuests = async () => {
        try {
            const response = await fetch('/api/quests/weekly', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setQuests(data.quests || []);
            setResetTime(data.reset_time);
        }
        catch (error) {
            console.error('Failed to fetch weekly quests:', error);
        }
    };
    const getDifficultyColor = (difficulty) => {
        const colors = {
            medium: 'bg-yellow-500',
            hard: 'bg-orange-500',
            legendary: 'bg-purple-500'
        };
        return colors[difficulty] || 'bg-gray-500';
    };
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h2", { className: "text-2xl font-bold flex items-center gap-2", children: [_jsx(Trophy, { className: "h-6 w-6" }), "Weekly Challenges"] }), _jsxs("div", { className: "text-sm text-muted-foreground flex items-center gap-1", children: [_jsx(Clock, { className: "h-4 w-4" }), "Resets: ", resetTime] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: quests.map(quest => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold", children: quest.title }), _jsx(Badge, { className: getDifficultyColor(quest.difficulty), children: quest.difficulty })] }), _jsx(Trophy, { className: "h-5 w-5 text-yellow-500" })] }), _jsx("p", { className: "text-sm text-muted-foreground", children: quest.description }), _jsx("div", { className: "space-y-2", children: quest.objectives.map((obj, idx) => (_jsxs("div", { className: "text-sm", children: [_jsxs("div", { className: "flex justify-between mb-1", children: [_jsx("span", { children: obj.description }), _jsxs("span", { className: "font-medium", children: [obj.current, "/", obj.required] })] }), _jsx(Progress, { value: (obj.current / obj.required) * 100 })] }, idx))) }), _jsxs("div", { className: "flex justify-between text-sm border-t pt-2", children: [_jsxs("span", { className: "font-medium", children: ["\uD83D\uDCB0 ", quest.rewards.credits] }), _jsxs("span", { className: "font-medium", children: ["\u2B50 ", quest.rewards.xp, " XP"] }), quest.rewards.karma !== 0 && (_jsxs("span", { className: "font-medium", children: ["\u2728 ", quest.rewards.karma > 0 ? '+' : '', quest.rewards.karma] }))] }), quest.status === 'available' && (_jsx(Button, { className: "w-full", children: "Accept Challenge" }))] }) }, quest.id))) })] }));
};
