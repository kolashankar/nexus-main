import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Target, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';
import { questService } from '../../services/questService';
export const QuestTracker = () => {
    const [trackedQuests, setTrackedQuests] = useState([]);
    const [expanded, setExpanded] = useState([]);
    const [minimized, setMinimized] = useState(false);
    useEffect(() => {
        fetchTrackedQuests();
        const interval = setInterval(fetchTrackedQuests, 30000); // Refresh every 30s
        return () => clearInterval(interval);
    }, []);
    const fetchTrackedQuests = async () => {
        try {
            const quests = await questService.getActiveQuests();
            setTrackedQuests(quests.slice(0, 5)); // Track max 5 quests
        }
        catch (error) {
            console.error('Failed to fetch tracked quests:', error);
        }
    };
    const toggleExpanded = (questId) => {
        setExpanded(prev => prev.includes(questId)
            ? prev.filter(id => id !== questId)
            : [...prev, questId]);
    };
    const calculateProgress = (objectives) => {
        if (objectives.length === 0)
            return 0;
        const completed = objectives.filter(obj => obj.completed).length;
        return (completed / objectives.length) * 100;
    };
    if (minimized) {
        return (_jsx("div", { className: "fixed bottom-4 right-4 z-50", children: _jsxs(Button, { onClick: () => setMinimized(false), variant: "default", size: "sm", children: [_jsx(Target, { className: "h-4 w-4 mr-2" }), "Quests (", trackedQuests.length, ")"] }) }));
    }
    return (_jsx("div", { className: "fixed bottom-4 right-4 w-80 z-50", children: _jsx(Card, { className: "p-4 shadow-2xl border-2", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "font-bold flex items-center gap-2", children: [_jsx(Target, { className: "h-5 w-5" }), "Active Quests"] }), _jsx(Button, { variant: "ghost", size: "sm", onClick: () => setMinimized(true), children: "Minimize" })] }), trackedQuests.length === 0 ? (_jsx("p", { className: "text-sm text-muted-foreground text-center py-4", children: "No active quests" })) : (_jsx("div", { className: "space-y-2 max-h-96 overflow-y-auto", children: trackedQuests.map(quest => (_jsxs("div", { className: "border rounded p-2 hover:bg-accent/50 transition-colors", children: [_jsxs("div", { className: "cursor-pointer", onClick: () => toggleExpanded(quest.id), children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsxs("div", { className: "flex-1", children: [_jsx("div", { className: "font-medium text-sm truncate", children: quest.title }), _jsx(Badge, { variant: "outline", className: "text-xs mt-1", children: quest.quest_type })] }), expanded.includes(quest.id) ? (_jsx(ChevronUp, { className: "h-4 w-4" })) : (_jsx(ChevronDown, { className: "h-4 w-4" }))] }), _jsx(Progress, { value: calculateProgress(quest.objectives), className: "h-1" })] }), expanded.includes(quest.id) && (_jsx("div", { className: "mt-2 space-y-1 pl-2 border-l-2", children: quest.objectives.map((obj, idx) => (_jsxs("div", { className: "flex items-start gap-2 text-xs", children: [obj.completed ? (_jsx(CheckCircle2, { className: "h-3 w-3 text-green-600 mt-0.5 flex-shrink-0" })) : (_jsx(Target, { className: "h-3 w-3 text-muted-foreground mt-0.5 flex-shrink-0" })), _jsxs("div", { className: "flex-1", children: [_jsx("div", { className: obj.completed ? 'line-through text-muted-foreground' : '', children: obj.description }), _jsxs("div", { className: "text-muted-foreground", children: [obj.current, "/", obj.required] })] })] }, idx))) }))] }, quest.id))) }))] }) }) }));
};
