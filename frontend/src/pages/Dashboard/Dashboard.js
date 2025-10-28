import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Dashboard page component
 */
import { useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import useStore from '../../store';
import CharacterPreview3D from '../../components/3d/CharacterPreview3D/CharacterPreview3D';
import CharacterCustomizer from '../../components/character/CharacterCustomizer';
import TraitToggleIcon from '../../components/traits/TraitToggleIcon/TraitToggleIcon';
const Dashboard = () => {
    const { player, fetchPlayer, isLoadingPlayer } = useStore();
    useEffect(() => {
        if (!player) {
            fetchPlayer();
        }
    }, []);
    if (isLoadingPlayer) {
        return (_jsx("div", { className: "min-h-screen flex items-center justify-center", children: _jsx("div", { className: "text-xl", children: "Loading..." }) }));
    }
    if (!player) {
        return (_jsx("div", { className: "min-h-screen flex items-center justify-center", children: _jsx("div", { className: "text-xl text-white", children: "No player data available. Please try refreshing." }) }));
    }
    return (_jsx("div", { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6", children: _jsxs("div", { className: "container mx-auto", children: [_jsx("h1", { className: "text-4xl font-bold text-white mb-8", children: "Dashboard" }), _jsxs("div", { className: "grid md:grid-cols-3 gap-6 mb-8", children: [_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Player Info" }), _jsx(CardDescription, { children: "Your character details" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Username:" }), " ", player?.username || 'Unknown'] }), _jsxs("p", { children: [_jsx("strong", { children: "Level:" }), " ", player?.level || 1] }), _jsxs("p", { children: [_jsx("strong", { children: "XP:" }), " ", player?.xp || 0] })] }) })] }), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Karma & Class" }), _jsx(CardDescription, { children: "Your moral standing" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Karma:" }), " ", player?.karma_points || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Moral Class:" }), " ", player?.moral_class || 'Neutral'] }), _jsxs("p", { children: [_jsx("strong", { children: "Economic Class:" }), " ", player?.economic_class || 'Middle'] })] }) })] }), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Currencies" }), _jsx(CardDescription, { children: "Your wealth" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Credits:" }), " ", player?.currencies?.credits || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Karma Tokens:" }), " ", player?.currencies?.karma_tokens || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Dark Matter:" }), " ", player?.currencies?.dark_matter || 0] })] }) })] })] }), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "3D World Preview" }), _jsx(CardDescription, { children: "Your character in Karma Nexus" })] }), _jsx(CardContent, { children: _jsx("div", { className: "h-96", children: _jsx(Scene, {}) }) })] })] }) }));
};
export default Dashboard;
