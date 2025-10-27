import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import TraitItem from './TraitItem';
import { usePlayer } from '@/hooks/usePlayer';
const TraitsList = () => {
    const { player } = usePlayer();
    const [filter, setFilter] = useState('all');
    if (!player)
        return null;
    const traits = player.traits || {};
    const metaTraits = player.meta_traits || {};
    // Categorize traits
    const virtues = [
        'empathy', 'integrity', 'discipline', 'creativity', 'resilience',
        'curiosity', 'kindness', 'courage', 'patience', 'adaptability',
        'wisdom', 'humility', 'vision', 'honesty', 'loyalty',
        'generosity', 'self_awareness', 'gratitude', 'optimism', 'loveability'
    ];
    const vices = [
        'greed', 'arrogance', 'deceit', 'cruelty', 'selfishness',
        'envy', 'wrath', 'cowardice', 'laziness', 'gluttony',
        'paranoia', 'impulsiveness', 'vengefulness', 'manipulation', 'prejudice',
        'betrayal', 'stubbornness', 'pessimism', 'recklessness', 'vanity'
    ];
    const skills = [
        'hacking', 'negotiation', 'stealth', 'leadership', 'technical_knowledge',
        'physical_strength', 'speed', 'intelligence', 'charisma', 'perception',
        'endurance', 'dexterity', 'memory', 'focus', 'networking',
        'strategy', 'trading', 'engineering', 'medicine', 'meditation'
    ];
    const getTraitsByCategory = (category) => {
        switch (category) {
            case 'virtues':
                return virtues.map(name => ({ name, value: traits[name] || 50 }));
            case 'vices':
                return vices.map(name => ({ name, value: traits[name] || 50 }));
            case 'skills':
                return skills.map(name => ({ name, value: traits[name] || 50 }));
            case 'meta':
                return Object.entries(metaTraits).map(([name, value]) => ({ name, value: value }));
            default:
                return Object.entries(traits).map(([name, value]) => ({ name, value: value }));
        }
    };
    const filterTraits = (traitsList) => {
        if (filter === 'top') {
            return [...traitsList].sort((a, b) => b.value - a.value).slice(0, 10);
        }
        else if (filter === 'bottom') {
            return [...traitsList].sort((a, b) => a.value - b.value).slice(0, 10);
        }
        return traitsList;
    };
    return (_jsxs(Card, { className: "w-full", children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { className: "text-2xl", children: "Character Traits" }), _jsxs("div", { className: "flex gap-2 mt-2", children: [_jsx("button", { onClick: () => setFilter('all'), className: `px-3 py-1 rounded ${filter === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`, children: "All" }), _jsx("button", { onClick: () => setFilter('top'), className: `px-3 py-1 rounded ${filter === 'top' ? 'bg-green-500 text-white' : 'bg-gray-200'}`, children: "Top 10" }), _jsx("button", { onClick: () => setFilter('bottom'), className: `px-3 py-1 rounded ${filter === 'bottom' ? 'bg-red-500 text-white' : 'bg-gray-200'}`, children: "Bottom 10" })] })] }), _jsx(CardContent, { children: _jsxs(Tabs, { defaultValue: "virtues", className: "w-full", children: [_jsxs(TabsList, { className: "grid w-full grid-cols-4", children: [_jsx(TabsTrigger, { value: "virtues", children: "Virtues (20)" }), _jsx(TabsTrigger, { value: "vices", children: "Vices (20)" }), _jsx(TabsTrigger, { value: "skills", children: "Skills (20)" }), _jsx(TabsTrigger, { value: "meta", children: "Meta (20)" })] }), _jsx(TabsContent, { value: "virtues", className: "space-y-2 mt-4", children: filterTraits(getTraitsByCategory('virtues')).map((trait) => (_jsx(TraitItem, { name: trait.name, value: trait.value, category: "virtue" }, trait.name))) }), _jsx(TabsContent, { value: "vices", className: "space-y-2 mt-4", children: filterTraits(getTraitsByCategory('vices')).map((trait) => (_jsx(TraitItem, { name: trait.name, value: trait.value, category: "vice" }, trait.name))) }), _jsx(TabsContent, { value: "skills", className: "space-y-2 mt-4", children: filterTraits(getTraitsByCategory('skills')).map((trait) => (_jsx(TraitItem, { name: trait.name, value: trait.value, category: "skill" }, trait.name))) }), _jsx(TabsContent, { value: "meta", className: "space-y-2 mt-4", children: filterTraits(getTraitsByCategory('meta')).map((trait) => (_jsx(TraitItem, { name: trait.name, value: trait.value, category: "meta" }, trait.name))) })] }) })] }));
};
export default TraitsList;
