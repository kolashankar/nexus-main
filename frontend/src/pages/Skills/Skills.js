import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import SuperpowersList from '../../components/player/SuperpowersList/SuperpowersList';
import SkillTree from '../../components/player/SkillTree/SkillTree';
export const Skills = () => {
    const [selectedTrait, setSelectedTrait] = useState('hacking');
    const traitCategories = {
        skills: ['hacking', 'negotiation', 'stealth', 'leadership', 'technical_knowledge'],
        virtues: ['empathy', 'integrity', 'discipline', 'creativity', 'resilience'],
        vices: ['greed', 'arrogance', 'deceit', 'cruelty', 'selfishness']
    };
    return (_jsxs("div", { className: "container mx-auto p-6 space-y-6", children: [_jsx("h1", { className: "text-3xl font-bold", children: "Skills & Powers" }), _jsxs(Tabs, { defaultValue: "superpowers", children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "superpowers", children: "Superpowers" }), _jsx(TabsTrigger, { value: "skill-trees", children: "Skill Trees" })] }), _jsx(TabsContent, { value: "superpowers", className: "mt-6", children: _jsx(SuperpowersList, {}) }), _jsx(TabsContent, { value: "skill-trees", className: "mt-6", children: _jsxs("div", { className: "space-y-6", children: [_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Select a Trait" }) }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-4", children: Object.entries(traitCategories).map(([category, traits]) => (_jsxs("div", { children: [_jsx("p", { className: "text-sm font-semibold mb-2 capitalize", children: category }), _jsx("div", { className: "flex flex-wrap gap-2", children: traits.map((trait) => (_jsx("button", { onClick: () => setSelectedTrait(trait), className: `px-3 py-1 rounded text-sm ${selectedTrait === trait
                                                                    ? 'bg-blue-500 text-white'
                                                                    : 'bg-gray-200 text-gray-700'}`, children: trait.replace('_', ' ') }, trait))) })] }, category))) }) })] }), selectedTrait && _jsx(SkillTree, { traitName: selectedTrait })] }) })] })] }));
};