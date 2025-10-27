import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Zap, Lock, Clock, Star, Info } from 'lucide-react';
export const SuperpowerDisplay = ({ superpowers, onActivate, onViewDetails }) => {
    const [selectedTier, setSelectedTier] = useState(1);
    const getTierColor = (tier) => {
        const colors = {
            1: 'bg-gray-500',
            2: 'bg-green-500',
            3: 'bg-blue-500',
            4: 'bg-purple-500',
            5: 'bg-yellow-500'
        };
        return colors[tier] || 'bg-gray-500';
    };
    const getTierName = (tier) => {
        const names = {
            1: 'Basic',
            2: 'Intermediate',
            3: 'Advanced',
            4: 'Master',
            5: 'Legendary'
        };
        return names[tier] || 'Unknown';
    };
    const filteredPowers = superpowers.filter(p => p.tier === selectedTier);
    const unlockedCount = superpowers.filter(p => p.unlocked).length;
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Unlocked Powers" }), _jsxs("p", { className: "text-3xl font-bold", children: [unlockedCount, " / ", superpowers.length] })] }), _jsx(Zap, { className: "w-10 h-10 text-yellow-500" })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600 mb-2", children: "Completion" }), _jsx(Progress, { value: (unlockedCount / superpowers.length) * 100 }), _jsxs("p", { className: "text-xs text-gray-500 mt-1", children: [((unlockedCount / superpowers.length) * 100).toFixed(1), "%"] })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Highest Tier" }), _jsx("p", { className: "text-3xl font-bold", children: Math.max(...superpowers.filter(p => p.unlocked).map(p => p.tier), 0) })] }) }) })] }), _jsxs(Tabs, { value: selectedTier.toString(), onValueChange: (v) => setSelectedTier(Number(v)), children: [_jsx(TabsList, { className: "grid w-full grid-cols-5", children: [1, 2, 3, 4, 5].map((tier) => (_jsxs(TabsTrigger, { value: tier.toString(), children: [_jsx(Star, { className: `w-4 h-4 mr-1 ${superpowers.some(p => p.tier === tier && p.unlocked) ? 'text-yellow-500' : ''}` }), "Tier ", tier] }, tier))) }), _jsx("div", { className: "mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4", children: filteredPowers.map((power) => (_jsxs(Card, { className: `transition-all ${power.unlocked
                                ? 'border-2 hover:shadow-lg'
                                : 'opacity-60'}`, style: {
                                borderColor: power.unlocked ? getTierColor(power.tier).replace('bg-', '#') : undefined
                            }, children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex-1", children: [_jsxs(CardTitle, { className: "flex items-center gap-2 text-lg", children: [power.unlocked ? (_jsx(Zap, { className: `w-5 h-5 ${getTierColor(power.tier).replace('bg-', 'text-')}` })) : (_jsx(Lock, { className: "w-5 h-5 text-gray-400" })), power.name] }), _jsx("p", { className: "text-sm text-gray-600 mt-1", children: power.description })] }), _jsx(Badge, { className: getTierColor(power.tier), children: getTierName(power.tier) })] }) }), _jsx(CardContent, { children: power.unlocked ? (_jsxs("div", { className: "space-y-4", children: [power.currentCooldown > 0 ? (_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-sm mb-2", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-4 h-4" }), "On Cooldown"] }), _jsxs("span", { className: "font-semibold", children: [power.currentCooldown, "s"] })] }), _jsx(Progress, { value: ((power.cooldown - power.currentCooldown) / power.cooldown) * 100 })] })) : (_jsxs("div", { className: "flex items-center gap-2 text-sm text-green-600", children: [_jsx(Zap, { className: "w-4 h-4" }), _jsx("span", { className: "font-semibold", children: "Ready to Use" })] })), _jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { className: "text-gray-600", children: "Times Used" }), _jsx("span", { className: "font-semibold", children: power.usageCount })] }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-gray-600 mb-1", children: "Effects:" }), _jsx("div", { className: "flex flex-wrap gap-1", children: Object.entries(power.effects).slice(0, 3).map(([key, value]) => (_jsxs(Badge, { variant: "outline", className: "text-xs", children: [key, ": ", typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value] }, key))) })] }), _jsxs("div", { className: "flex gap-2", children: [_jsxs(Button, { className: "flex-1", disabled: power.currentCooldown > 0, onClick: () => onActivate(power.id), children: [_jsx(Zap, { className: "w-4 h-4 mr-2" }), "Activate"] }), _jsx(Button, { variant: "outline", size: "icon", onClick: () => onViewDetails(power.id), children: _jsx(Info, { className: "w-4 h-4" }) })] })] })) : (_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm font-semibold mb-2", children: "Unlock Requirements:" }), _jsx("div", { className: "space-y-1", children: Object.entries(power.unlock_conditions).map(([trait, value]) => (_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { className: "text-gray-600", children: trait.replace(/_/g, ' ') }), _jsxs("span", { className: "font-semibold", children: [value, "%"] })] }, trait))) })] }), _jsxs(Button, { variant: "outline", className: "w-full", onClick: () => onViewDetails(power.id), children: [_jsx(Info, { className: "w-4 h-4 mr-2" }), "View Details"] })] })) })] }, power.id))) })] })] }));
};
