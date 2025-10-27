import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Users, Trophy, Clock, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';
export const GuildQuests = () => {
    const [quests, setQuests] = useState([]);
    const [activeQuests, setActiveQuests] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchGuildQuests();
    }, []);
    const fetchGuildQuests = async () => {
        try {
            const response = await fetch('/api/quests/guild', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setQuests(data.available || []);
            setActiveQuests(data.active || []);
        }
        catch (error) {
            console.error('Failed to fetch guild quests:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const joinQuest = async (questId) => {
        try {
            const response = await fetch(`/api/quests/guild/${questId}/join`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            if (response.ok) {
                toast.success('Joined Guild Quest', {
                    description: 'You have joined the guild quest',
                });
                fetchGuildQuests();
            }
        }
        catch (error) {
            toast.error('Error', {
                description: 'Failed to join guild quest'
            });
        }
    };
    const calculateProgress = (objectives) => {
        const completed = objectives.filter(obj => obj.completed).length;
        return (completed / objectives.length) * 100;
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center h-64", children: _jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [activeQuests.length > 0 && (_jsxs("div", { children: [_jsxs("h2", { className: "text-2xl font-bold mb-4 flex items-center gap-2", children: [_jsx(Users, { className: "h-6 w-6 text-blue-500" }), "Active Guild Quests"] }), _jsx("div", { className: "grid gap-4", children: activeQuests.map((quest) => (_jsxs(Card, { className: "border-blue-500/30", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex-1", children: [_jsx(CardTitle, { children: quest.title }), _jsx(CardDescription, { className: "mt-2", children: quest.description })] }), _jsxs(Badge, { variant: "outline", className: "bg-blue-500/20", children: [quest.participants.length, "/", quest.required_members, " Members"] })] }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsx("div", { className: "space-y-2", children: quest.objectives.map((objective, idx) => (_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsxs("span", { className: "flex items-center gap-2", children: [objective.completed && (_jsx(CheckCircle, { className: "h-4 w-4 text-green-500" })), objective.description] }), _jsxs("span", { className: "text-gray-400", children: [objective.current, "/", objective.required] })] }), _jsx(Progress, { value: (objective.current / objective.required) * 100, className: "h-2" })] }, idx))) }), _jsxs("div", { className: "pt-2 border-t border-gray-700", children: [_jsxs("div", { className: "flex items-center justify-between text-sm mb-2", children: [_jsx("span", { children: "Overall Progress" }), _jsxs("span", { className: "text-blue-400", children: [Math.round(calculateProgress(quest.objectives)), "%"] })] }), _jsx(Progress, { value: calculateProgress(quest.objectives), className: "h-3" })] }), _jsxs("div", { className: "flex items-center gap-4 text-sm bg-gray-800/50 p-3 rounded-lg", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Trophy, { className: "h-4 w-4 text-yellow-500" }), _jsxs("span", { children: [quest.rewards.guild_reputation, " Rep"] })] }), _jsxs("div", { className: "flex items-center gap-1", children: [_jsx("span", { className: "text-green-500", children: "\uD83D\uDCB0" }), _jsxs("span", { children: [quest.rewards.credits, " Credits"] })] }), _jsxs("div", { className: "flex items-center gap-1", children: [_jsx("span", { className: "text-blue-500", children: "\u2B50" }), _jsxs("span", { children: [quest.rewards.guild_xp, " Guild XP"] })] })] }), quest.expires_at && (_jsxs("div", { className: "flex items-center gap-2 text-sm text-gray-400", children: [_jsx(Clock, { className: "h-4 w-4" }), "Expires: ", new Date(quest.expires_at).toLocaleDateString()] }))] })] }, quest._id))) })] })), _jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Available Guild Quests" }), quests.length === 0 ? (_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsx("p", { className: "text-gray-400 text-center", children: "No guild quests available. Check back later!" }) }) })) : (_jsx("div", { className: "grid gap-4 sm:grid-cols-2", children: quests.map((quest) => (_jsxs(Card, { className: "border-gray-700", children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { className: "text-lg", children: quest.title }), _jsx(CardDescription, { children: quest.description })] }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { className: "text-gray-400", children: "Required Members:" }), _jsx("span", { className: "font-medium", children: quest.required_members })] }), _jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { className: "text-gray-400", children: "Current Participants:" }), _jsx("span", { className: "font-medium text-blue-400", children: quest.participants.length })] }), _jsx(Button, { onClick: () => joinQuest(quest._id), className: "w-full", variant: "outline", children: "Join Quest" })] })] }, quest._id))) }))] })] }));
};