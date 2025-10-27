import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Calendar, RefreshCw, Clock } from 'lucide-react';
import { toast } from 'sonner';
export const DailyQuests = () => {
    const [quests, setQuests] = useState([]);
    const [resetTime, setResetTime] = useState('');
    const [canRefresh, setCanRefresh] = useState(true);
    useEffect(() => {
        fetchDailyQuests();
    }, []);
    const fetchDailyQuests = async () => {
        try {
            const response = await fetch('/api/quests/daily', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setQuests(data.quests || []);
            setResetTime(data.reset_time);
        }
        catch (error) {
            console.error('Failed to fetch daily quests:', error);
        }
    };
    const refreshQuests = async () => {
        try {
            const response = await fetch('/api/quests/daily/refresh', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Daily quests refreshed!');
                fetchDailyQuests();
                setCanRefresh(false);
            }
            else {
                toast.error('Cannot refresh', {
                    description: data.error
                });
            }
        }
        catch (error) {
            toast.error('Failed to refresh quests');
        }
    };
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h2", { className: "text-2xl font-bold flex items-center gap-2", children: [_jsx(Calendar, { className: "h-6 w-6" }), "Daily Quests"] }), _jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("div", { className: "text-sm text-muted-foreground flex items-center gap-1", children: [_jsx(Clock, { className: "h-4 w-4" }), "Resets in: ", resetTime] }), _jsxs(Button, { variant: "outline", size: "sm", onClick: refreshQuests, disabled: !canRefresh, children: [_jsx(RefreshCw, { className: "h-4 w-4 mr-2" }), "Refresh"] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: quests.map(quest => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold", children: quest.title }), _jsx("p", { className: "text-sm text-muted-foreground", children: quest.description })] }), _jsx("div", { className: "space-y-2", children: quest.objectives.map((obj, idx) => (_jsxs("div", { className: "text-sm", children: [_jsxs("div", { className: "flex justify-between mb-1", children: [_jsx("span", { children: obj.description }), _jsxs("span", { children: [obj.current, "/", obj.required] })] }), _jsx(Progress, { value: (obj.current / obj.required) * 100 })] }, idx))) }), _jsxs("div", { className: "flex justify-between text-sm border-t pt-2", children: [_jsxs("span", { children: ["\uD83D\uDCB0 ", quest.rewards.credits] }), _jsxs("span", { children: ["\u2B50 ", quest.rewards.xp, " XP"] })] }), quest.status === 'available' && (_jsx(Button, { className: "w-full", size: "sm", children: "Accept" }))] }) }, quest.id))) })] }));
};