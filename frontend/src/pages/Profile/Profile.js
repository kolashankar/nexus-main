import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useParams } from 'react-router-dom';
import ProfileCard from '@/components/player/ProfileCard/ProfileCard';
import TraitsList from '@/components/player/TraitsList/TraitsList';
import { usePlayer } from '@/hooks/usePlayer';
const Profile = () => {
    const { playerId } = useParams();
    const { player, loading } = usePlayer();
    if (loading) {
        return (_jsx("div", { className: "container mx-auto px-4 py-8", children: _jsxs("div", { className: "animate-pulse space-y-4", children: [_jsx("div", { className: "h-48 bg-gray-300 rounded-lg" }), _jsx("div", { className: "h-96 bg-gray-300 rounded-lg" })] }) }));
    }
    if (!player) {
        return (_jsx("div", { className: "container mx-auto px-4 py-8", children: _jsx("div", { className: "text-center text-red-600", children: "Player not found" }) }));
    }
    return (_jsx("div", { className: "container mx-auto px-4 py-8", children: _jsxs("div", { className: "max-w-6xl mx-auto space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-4xl font-bold text-gray-900 mb-2", children: playerId ? 'Player Profile' : 'My Profile' }), _jsx("p", { className: "text-gray-600", children: "View and manage your character information" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1", children: _jsx(ProfileCard, { showActions: !playerId }) }), _jsx("div", { className: "lg:col-span-2", children: _jsx(TraitsList, {}) })] })] }) }));
};
export default Profile;
