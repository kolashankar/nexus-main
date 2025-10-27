import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Eye, Lock, MapPin, Clock } from 'lucide-react';
import { toast } from 'sonner';
export const HiddenQuests = () => {
    const [discoveredQuests, setDiscoveredQuests] = useState([]);
    const [hints, setHints] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHiddenQuests();
        fetchHints();
    }, []);
    const fetchHiddenQuests = async () => {
        try {
            const response = await fetch('/api/quests/hidden/discovered', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setDiscoveredQuests(data.quests || []);
        }
        catch (error) {
            console.error('Failed to fetch hidden quests:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const fetchHints = async () => {
        try {
            const response = await fetch('/api/quests/hidden/hints', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setHints(data.hints || []);
        }
        catch (error) {
            console.error('Failed to fetch hints:', error);
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
            if (response.ok) {
                toast.success('Quest Accepted', {
                    description: 'Hidden quest added to your quest log',
                });
                fetchHiddenQuests();
            }
        }
        catch (error) {
            toast.error('Error', {
                description: 'Failed to accept quest'
            });
        }
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center h-64", children: _jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500" }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-2xl font-bold mb-4 flex items-center gap-2", children: [_jsx(Eye, { className: "h-6 w-6 text-purple-500" }), "Discovered Hidden Quests"] }), discoveredQuests.length === 0 ? (_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsx("p", { className: "text-gray-400 text-center", children: "No hidden quests discovered yet. Explore the world to find them!" }) }) })) : (_jsx("div", { className: "grid gap-4", children: discoveredQuests.map((quest) => (_jsxs(Card, { className: "border-purple-500/30 bg-gradient-to-r from-purple-900/20 to-transparent", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs(CardTitle, { className: "flex items-center gap-2", children: [quest.title, _jsx(Badge, { variant: "outline", className: "ml-2", children: quest.difficulty })] }), _jsx(CardDescription, { className: "mt-2", children: quest.description })] }), quest.status === 'available' && (_jsx(Button, { onClick: () => acceptQuest(quest._id), size: "sm", className: "bg-purple-600 hover:bg-purple-700", children: "Accept" }))] }) }), quest.discovered_at && (_jsx(CardContent, { children: _jsxs("div", { className: "flex items-center gap-2 text-sm text-gray-400", children: [_jsx(Clock, { className: "h-4 w-4" }), "Discovered: ", new Date(quest.discovered_at).toLocaleDateString()] }) }))] }, quest._id))) }))] }), _jsxs("div", { children: [_jsxs("h2", { className: "text-2xl font-bold mb-4 flex items-center gap-2", children: [_jsx(Lock, { className: "h-6 w-6 text-yellow-500" }), "Cryptic Hints"] }), hints.length === 0 ? (_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsx("p", { className: "text-gray-400 text-center", children: "No hints available at this time." }) }) })) : (_jsx("div", { className: "grid gap-4 sm:grid-cols-2 lg:grid-cols-3", children: hints.map((hint, index) => (_jsxs(Card, { className: "border-yellow-500/30 bg-gradient-to-br from-yellow-900/10 to-transparent", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-lg flex items-center gap-2", children: [_jsx(MapPin, { className: "h-5 w-5 text-yellow-500" }), "Mystery Quest"] }) }), _jsxs(CardContent, { children: [_jsxs("p", { className: "text-sm text-gray-300 italic", children: ["\"", hint.hint, "\""] }), _jsxs("div", { className: "mt-3 flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", className: "text-xs", children: hint.difficulty }), _jsx(Badge, { variant: "outline", className: "text-xs", children: hint.category })] })] })] }, index))) }))] })] }));
};