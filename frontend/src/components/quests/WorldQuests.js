import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Globe, Users } from 'lucide-react';
import { toast } from 'sonner';
export const WorldQuests = () => {
    const [quests, setQuests] = useState([]);
    useEffect(() => {
        fetchWorldQuests();
        const interval = setInterval(fetchWorldQuests, 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, []);
    const fetchWorldQuests = async () => {
        try {
            const response = await fetch('/api/quests/world', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setQuests(data.quests || []);
        }
        catch (error) {
            console.error('Failed to fetch world quests:', error);
        }
    };
    const participate = async (questId) => {
        try {
            const response = await fetch(`/api/quests/world/participate/${questId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Joined world quest!');
                fetchWorldQuests();
            }
            else {
                toast.error('Failed to join');
            }
        }
        catch (error) {
            toast.error('Failed to join quest');
        }
    };
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-2xl font-bold flex items-center gap-2", children: [_jsx(Globe, { className: "h-6 w-6" }), "World Quests"] }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Limited-time events open to all players" })] }), quests.length === 0 ? (_jsxs(Card, { className: "p-8 text-center", children: [_jsx(Globe, { className: "h-12 w-12 mx-auto text-muted-foreground mb-4" }), _jsx("p", { className: "text-muted-foreground", children: "No active world quests at the moment" })] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: quests.map(quest => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold text-lg", children: quest.title }), _jsxs(Badge, { variant: "secondary", children: [_jsx(Users, { className: "h-3 w-3 mr-1" }), quest.participants?.length || 0, " participating"] })] }), _jsx(Globe, { className: "h-6 w-6 text-blue-500" })] }), _jsx("p", { className: "text-sm text-muted-foreground", children: quest.description }), _jsxs("div", { className: "space-y-1 text-sm", children: [_jsx("div", { className: "font-medium", children: "Objectives:" }), quest.objectives.slice(0, 2).map((obj, idx) => (_jsxs("div", { children: ["\u2022 ", obj.description] }, idx)))] }), _jsxs("div", { className: "flex items-center justify-between text-sm border-t pt-2", children: [_jsxs("div", { className: "flex gap-3", children: [_jsxs("span", { children: ["\uD83D\uDCB0 ", quest.rewards.credits] }), _jsxs("span", { children: ["\u2B50 ", quest.rewards.xp, " XP"] })] }), quest.expires_at && (_jsxs("span", { className: "text-xs text-muted-foreground", children: ["Expires: ", new Date(quest.expires_at).toLocaleDateString()] }))] }), _jsx(Button, { className: "w-full", onClick: () => participate(quest.id), children: "Participate" })] }) }, quest.id))) }))] }));
};