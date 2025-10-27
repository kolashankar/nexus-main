import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Trophy, Lock, Search, Star } from 'lucide-react';
export const AchievementGrid = ({ achievements, onAchievementClick }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const categories = useMemo(() => {
        const cats = new Set(achievements.map(a => a.category));
        return ['all', ...Array.from(cats)];
    }, [achievements]);
    const filteredAchievements = useMemo(() => {
        return achievements.filter(achievement => {
            // Filter hidden achievements that aren't unlocked
            if (achievement.hidden && !achievement.unlocked) {
                return false;
            }
            // Filter by category
            if (selectedCategory !== 'all' && achievement.category !== selectedCategory) {
                return false;
            }
            // Filter by search query
            if (searchQuery) {
                const query = searchQuery.toLowerCase();
                return (achievement.name.toLowerCase().includes(query) ||
                    achievement.description.toLowerCase().includes(query));
            }
            return true;
        });
    }, [achievements, selectedCategory, searchQuery]);
    const stats = useMemo(() => {
        const total = achievements.filter(a => !a.hidden).length;
        const unlocked = achievements.filter(a => a.unlocked).length;
        const percentage = total > 0 ? (unlocked / total) * 100 : 0;
        return { total, unlocked, percentage };
    }, [achievements]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Unlocked" }), _jsx("p", { className: "text-3xl font-bold", children: stats.unlocked })] }), _jsx(Trophy, { className: "w-10 h-10 text-yellow-500" })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Total" }), _jsx("p", { className: "text-3xl font-bold", children: stats.total })] }), _jsx(Star, { className: "w-10 h-10 text-blue-500" })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("p", { className: "text-sm text-gray-600", children: "Completion" }), _jsxs("p", { className: "text-sm font-semibold", children: [stats.percentage.toFixed(1), "%"] })] }), _jsx(Progress, { value: stats.percentage })] }) }) })] }), _jsx("div", { className: "flex gap-4", children: _jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" }), _jsx(Input, { placeholder: "Search achievements...", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), className: "pl-10" })] }) }), _jsxs(Tabs, { value: selectedCategory, onValueChange: setSelectedCategory, children: [_jsx(TabsList, { className: "grid w-full grid-cols-5 lg:grid-cols-11", children: categories.map((cat) => (_jsx(TabsTrigger, { value: cat, className: "text-xs", children: cat }, cat))) }), _jsx("div", { className: "mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filteredAchievements.map((achievement) => (_jsx(Card, { className: `cursor-pointer transition-all hover:shadow-lg ${achievement.unlocked
                                ? 'border-yellow-400 bg-yellow-50 dark:bg-yellow-950'
                                : 'opacity-75'}`, onClick: () => onAchievementClick(achievement.id), children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "flex items-start gap-3", children: [_jsx("div", { className: `p-3 rounded-full ${achievement.unlocked
                                                ? 'bg-yellow-500'
                                                : 'bg-gray-300 dark:bg-gray-700'}`, children: achievement.unlocked ? (_jsx(Trophy, { className: "w-6 h-6 text-white" })) : (_jsx(Lock, { className: "w-6 h-6 text-gray-500" })) }), _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center justify-between mb-1", children: [_jsx("h3", { className: "font-semibold text-sm", children: achievement.name }), achievement.hidden && (_jsx(Badge, { variant: "secondary", className: "text-xs", children: "Hidden" }))] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-400 mb-2", children: achievement.description }), !achievement.unlocked && achievement.progress !== undefined && achievement.total !== undefined && (_jsxs("div", { className: "mb-2", children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-gray-500", children: "Progress" }), _jsxs("span", { className: "text-gray-600 font-medium", children: [achievement.progress, " / ", achievement.total] })] }), _jsx(Progress, { value: (achievement.progress / achievement.total) * 100, className: "h-2" })] })), _jsx("div", { className: "flex flex-wrap gap-1 mt-2", children: Object.entries(achievement.rewards).map(([key, value]) => (_jsxs(Badge, { variant: "outline", className: "text-xs", children: ["+", value, " ", key] }, key))) }), _jsx(Badge, { variant: "secondary", className: "mt-2 text-xs", children: achievement.category })] })] }) }) }, achievement.id))) }), filteredAchievements.length === 0 && (_jsxs("div", { className: "text-center py-12", children: [_jsx(Lock, { className: "w-16 h-16 text-gray-400 mx-auto mb-4" }), _jsx("p", { className: "text-gray-600", children: "No achievements found" })] }))] })] }));
};
