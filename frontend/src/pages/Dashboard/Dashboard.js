import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import useStore from '../../store';
import CharacterCustomizer from '../../components/character/CharacterCustomizer';
import CharacterPreview3D from '../../components/3d/CharacterPreview3D/CharacterPreview3D';
import TraitToggleIcon from '../../components/traits/TraitToggleIcon/TraitToggleIcon';
import InitialTasksModal from '../../components/tasks/InitialTasksModal/InitialTasksModal';
import { getAllTraitsArray, isNewPlayer } from '../../utils/traitsHelper';
import { Button } from '../../components/ui/button';
const Dashboard = () => {
    const navigate = useNavigate();
    const { player, fetchPlayer, isLoadingPlayer } = useStore();
    const [showInitialTasks, setShowInitialTasks] = useState(false);
    useEffect(() => {
        fetchPlayer();
    }, [fetchPlayer]);
    useEffect(() => {
        // Check if player is new and should see initial tasks
        if (player && isNewPlayer(player.traits)) {
            setShowInitialTasks(true);
        }
    }, [player]);
    const handleTaskCompleted = (result) => {
        // Refresh player data after task completion
        fetchPlayer();
    };
    const handleCloseInitialTasks = () => {
        setShowInitialTasks(false);
    };
    if (isLoadingPlayer) {
        return (_jsx("div", { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center", children: _jsx("div", { className: "text-white text-2xl", children: "Loading..." }) }));
    }
    if (!player) {
        return (_jsx("div", { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center", children: _jsx("div", { className: "text-white text-2xl", children: "Unable to load player data. Please try refreshing." }) }));
    }
    // Convert traits object to array for TraitToggleIcon
    const traitsArray = getAllTraitsArray(player?.traits, player?.meta_traits);
    return (_jsxs("div", { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6", children: [_jsxs("div", { className: "container mx-auto", children: [_jsxs("div", { className: "flex items-center justify-between mb-8", children: [_jsx("h1", { className: "text-4xl font-bold text-white", children: "Dashboard" }), _jsxs("div", { className: "flex items-center gap-4", children: [traitsArray.length === 0 && (_jsx(Button, { onClick: () => setShowInitialTasks(true), className: "bg-purple-600 hover:bg-purple-700", children: "Start Initial Tasks" })), _jsx(TraitToggleIcon, { traits: traitsArray, playerName: player?.username || 'Player' })] })] }), _jsxs("div", { className: "grid md:grid-cols-3 gap-6 mb-8", children: [_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Player Info" }), _jsx(CardDescription, { children: "Your character details" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Username:" }), " ", player?.username || 'Unknown'] }), _jsxs("p", { children: [_jsx("strong", { children: "Level:" }), " ", player?.level || 1] }), _jsxs("p", { children: [_jsx("strong", { children: "XP:" }), " ", player?.xp || 0] })] }) })] }), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Karma & Class" }), _jsx(CardDescription, { children: "Your moral standing" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Karma:" }), " ", player?.karma_points || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Moral Class:" }), " ", player?.moral_class || 'Neutral'] }), _jsxs("p", { children: [_jsx("strong", { children: "Economic Class:" }), " ", player?.economic_class || 'Middle'] })] }) })] }), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Currencies" }), _jsx(CardDescription, { children: "Your wealth" })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Credits:" }), " ", player?.currencies?.credits || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Karma Tokens:" }), " ", player?.currencies?.karma_tokens || 0] }), _jsxs("p", { children: [_jsx("strong", { children: "Dark Matter:" }), " ", player?.currencies?.dark_matter || 0] })] }) })] })] }), _jsxs("div", { className: "grid md:grid-cols-2 gap-6", children: [_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Character Preview" }), _jsx(CardDescription, { children: "Your customized character" })] }), _jsx(CardContent, { children: _jsx("div", { className: "h-96", children: _jsx(CharacterPreview3D, { characterModel: player?.appearance?.model || player?.character_model || 'male_base', skinTone: player?.appearance?.skin_tone || player?.skin_tone || 'default', hairColor: player?.appearance?.hair_color || player?.hair_color || 'brown' }) }) })] }), _jsx(CharacterCustomizer, {})] })] }), _jsx(InitialTasksModal, { isOpen: showInitialTasks, onClose: handleCloseInitialTasks, onTaskCompleted: handleTaskCompleted })] }));
};
export default Dashboard;
