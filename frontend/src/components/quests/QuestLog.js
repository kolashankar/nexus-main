import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Scroll, CheckCircle2, Clock, Target } from 'lucide-react';
import { toast } from 'sonner';
export const QuestLog = () => {
    const [activeQuests, setActiveQuests] = useState([]);
    const [availableQuests, setAvailableQuests] = useState([]);
    const [completedQuests, setCompletedQuests] = useState([]);
    const [selectedQuest, setSelectedQuest] = useState(null);
    const [activeTab, setActiveTab] = useState('active');
    useEffect(() => {
        fetchActiveQuests();
        fetchAvailableQuests();
        fetchCompletedQuests();
    }, []);
    const fetchActiveQuests = async () => {
        try {
            const response = await fetch('/api/quests/active', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setActiveQuests(data.quests || []);
        }
        catch (error) {
            console.error('Failed to fetch active quests:', error);
        }
    };
    const fetchAvailableQuests = async () => {
        try {
            const response = await fetch('/api/quests/available', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setAvailableQuests(data.quests || []);
        }
        catch (error) {
            console.error('Failed to fetch available quests:', error);
        }
    };
    const fetchCompletedQuests = async () => {
        try {
            const response = await fetch('/api/quests/completed', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setCompletedQuests(data.quests || []);
        }
        catch (error) {
            console.error('Failed to fetch completed quests:', error);
        }
    };
    const acceptQuest = async (questId) => {
        try {
            const response = await fetch('/api/quests/accept', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ quest_id: questId })
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Quest accepted!', {
                    description: data.quest_title
                });
                fetchActiveQuests();
                fetchAvailableQuests();
            }
            else {
                toast.error('Failed to accept quest', {
                    description: data.error
                });
            }
        }
        catch (error) {
            toast.error('Failed to accept quest');
        }
    };
    const completeQuest = async (questId) => {
        try {
            const response = await fetch('/api/quests/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ quest_id: questId })
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Quest completed!', {
                    description: `+${data.rewards.xp} XP, +${data.rewards.credits} credits`
                });
                fetchActiveQuests();
                fetchCompletedQuests();
            }
            else {
                toast.error('Failed to complete quest', {
                    description: data.error
                });
            }
        }
        catch (error) {
            toast.error('Failed to complete quest');
        }
    };
    const getDifficultyColor = (difficulty) => {
        const colors = {
            easy: 'bg-green-500',
            medium: 'bg-yellow-500',
            hard: 'bg-orange-500',
            legendary: 'bg-purple-500'
        };
        return colors[difficulty] || 'bg-gray-500';
    };
    const calculateProgress = (objectives) => {
        if (objectives.length === 0)
            return 0;
        const completed = objectives.filter(obj => obj.completed).length;
        return (completed / objectives.length) * 100;
    };
    const canComplete = (quest) => {
        return quest.objectives.every(obj => obj.completed);
    };
    const QuestCard = ({ quest, showAccept = false, showComplete = false }) => (_jsx(Card, { className: `p-4 cursor-pointer transition-all hover:shadow-lg ${selectedQuest?.id === quest.id ? 'ring-2 ring-primary' : ''}`, onClick: () => setSelectedQuest(quest), children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex-1", children: [_jsx("h3", { className: "font-bold text-lg", children: quest.title }), _jsxs("div", { className: "flex gap-2 mt-1", children: [_jsx(Badge, { className: getDifficultyColor(quest.difficulty), children: quest.difficulty }), _jsx(Badge, { variant: "outline", children: quest.quest_type })] })] }), _jsx(Scroll, { className: "h-6 w-6 text-muted-foreground" })] }), _jsx("p", { className: "text-sm text-muted-foreground", children: quest.description }), quest.status === 'active' && (_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { children: "Progress" }), _jsxs("span", { children: [calculateProgress(quest.objectives).toFixed(0), "%"] })] }), _jsx(Progress, { value: calculateProgress(quest.objectives) })] })), _jsxs("div", { className: "space-y-1 text-sm", children: [_jsx("div", { className: "font-medium", children: "Objectives:" }), quest.objectives.slice(0, 3).map((obj, index) => (_jsxs("div", { className: "flex items-center gap-2", children: [obj.completed ? (_jsx(CheckCircle2, { className: "h-4 w-4 text-green-600" })) : (_jsx(Target, { className: "h-4 w-4 text-muted-foreground" })), _jsxs("span", { className: obj.completed ? 'line-through text-muted-foreground' : '', children: [obj.description, " (", obj.current, "/", obj.required, ")"] })] }, index)))] }), _jsx("div", { className: "flex items-center justify-between text-sm border-t pt-2", children: _jsxs("div", { className: "flex gap-3", children: [_jsxs("span", { children: ["\uD83D\uDCB0 ", quest.rewards.credits] }), _jsxs("span", { children: ["\u2B50 ", quest.rewards.xp, " XP"] }), quest.rewards.karma !== 0 && (_jsxs("span", { children: ["\u2728 ", quest.rewards.karma > 0 ? '+' : '', quest.rewards.karma] }))] }) }), showAccept && (_jsx(Button, { className: "w-full", onClick: (e) => {
                        e.stopPropagation();
                        acceptQuest(quest.id);
                    }, children: "Accept Quest" })), showComplete && canComplete(quest) && (_jsx(Button, { className: "w-full", onClick: (e) => {
                        e.stopPropagation();
                        completeQuest(quest.id);
                    }, children: "Complete Quest" }))] }) }));
    return (_jsxs("div", { className: "p-6 space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(Scroll, { className: "h-8 w-8" }), "Quest Log"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Your adventure awaits" })] }) }), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { children: [_jsxs(TabsTrigger, { value: "active", children: ["Active (", activeQuests.length, ")"] }), _jsxs(TabsTrigger, { value: "available", children: ["Available (", availableQuests.length, ")"] }), _jsxs(TabsTrigger, { value: "completed", children: ["Completed (", completedQuests.length, ")"] })] }), _jsx(TabsContent, { value: "active", className: "space-y-4", children: activeQuests.length === 0 ? (_jsxs(Card, { className: "p-8 text-center", children: [_jsx(Clock, { className: "h-12 w-12 mx-auto text-muted-foreground mb-4" }), _jsx("p", { className: "text-muted-foreground", children: "No active quests. Check available quests!" }), _jsx(Button, { className: "mt-4", onClick: () => setActiveTab('available'), children: "Browse Quests" })] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: activeQuests.map(quest => (_jsx(QuestCard, { quest: quest, showComplete: true }, quest.id))) })) }), _jsx(TabsContent, { value: "available", className: "space-y-4", children: _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: availableQuests.map(quest => (_jsx(QuestCard, { quest: quest, showAccept: true }, quest.id))) }) }), _jsx(TabsContent, { value: "completed", className: "space-y-4", children: _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: completedQuests.map(quest => (_jsx(QuestCard, { quest: quest }, quest.id))) }) })] })] }));
};