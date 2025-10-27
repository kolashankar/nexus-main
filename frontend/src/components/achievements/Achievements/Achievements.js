import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Input } from '../../ui/input';
import achievementsService from '../../../services/achievements/achievementsService';
import AchievementCard from './AchievementCard';
import { Progress } from '../../ui/progress';

const AchievementCategory = {
    TRAITS: 'traits',
    POWERS: 'powers',
    KARMA: 'karma',
    SOCIAL: 'social',
    ECONOMIC: 'economic',
    COMBAT: 'combat',
    QUESTS: 'quests',
    EXPLORATION: 'exploration',
    COLLECTION: 'collection',
    HIDDEN: 'hidden'
};

const Achievements = () => {
    const [achievements, setAchievements] = useState(null);
    const [allAchievements, setAllAchievements] = useState([]);
    const [filteredAchievements, setFilteredAchievements] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchAchievements();
        fetchAllAchievements();
    }, []);
    useEffect(() => {
        filterAchievements();
    }, [searchTerm, selectedCategory, allAchievements]);
    const fetchAchievements = async () => {
        try {
            const data = await achievementsService.getAchievements();
            setAchievements(data);
        }
        catch (error) {
            console.error('Failed to fetch achievements:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const fetchAllAchievements = async () => {
        try {
            const data = await achievementsService.getAchievementDefinitions();
            setAllAchievements(data);
        }
        catch (error) {
            console.error('Failed to fetch achievement definitions:', error);
        }
    };
    const filterAchievements = () => {
        let filtered = allAchievements;
        if (selectedCategory) {
            filtered = filtered.filter((a) => a.category === selectedCategory);
        }
        if (searchTerm) {
            filtered = filtered.filter((a) => a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                a.description.toLowerCase().includes(searchTerm.toLowerCase()));
        }
        setFilteredAchievements(filtered);
    };
    const isUnlocked = (achievementId) => {
        return achievements?.unlocked_achievements.some((a) => a.achievement_id === achievementId);
    };
    const getProgress = (achievementId) => {
        return achievements?.achievement_progress[achievementId];
    };
    if (loading) {
        return _jsx("div", { className: "flex justify-center items-center h-64", children: "Loading achievements..." });
    }
    return (_jsx("div", { className: "container mx-auto py-6", children: _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-3xl", children: "Achievements" }), achievements && (_jsxs("div", { className: "flex gap-2", children: [_jsxs(Badge, { variant: "secondary", children: [achievements.unlocked_achievements.length, "/", allAchievements.length] }), _jsxs(Badge, { children: ["Points: ", achievements.total_points] })] }))] }), achievements && (_jsxs("div", { className: "mt-4", children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { children: "Completion" }), _jsxs("span", { children: [achievements.completion_percentage.toFixed(1), "%"] })] }), _jsx(Progress, { value: achievements.completion_percentage, className: "h-2" })] }))] }), _jsxs(CardContent, { children: [_jsxs("div", { className: "mb-6 space-y-4", children: [_jsx(Input, { placeholder: "Search achievements...", value: searchTerm, onChange: (e) => setSearchTerm(e.target.value) }), _jsxs("div", { className: "flex flex-wrap gap-2", children: [_jsx(Badge, { variant: !selectedCategory ? 'default' : 'outline', className: "cursor-pointer", onClick: () => setSelectedCategory(null), children: "All" }), Object.values(AchievementCategory).map((category) => (_jsx(Badge, { variant: selectedCategory === category ? 'default' : 'outline', className: "cursor-pointer capitalize", onClick: () => setSelectedCategory(category), children: category.replace('_', ' ') }, category)))] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filteredAchievements.map((achievement) => (_jsx(AchievementCard, { achievement: achievement, unlocked: isUnlocked(achievement.achievement_id), progress: getProgress(achievement.achievement_id) }, achievement.achievement_id))) }), filteredAchievements.length === 0 && (_jsx("div", { className: "text-center py-12 text-muted-foreground", children: "No achievements found matching your criteria" }))] })] }) }));
};
export default Achievements;