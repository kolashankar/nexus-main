import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Progress } from '@/components/ui/progress';
const StatsDisplay = ({ player }) => {
    // Calculate XP progress
    const calculateXPProgress = () => {
        const xpForCurrentLevel = 100 * (player.level ** 2);
        const xpForNextLevel = 100 * ((player.level + 1) ** 2);
        const xpInLevel = player.xp - xpForCurrentLevel;
        const xpNeeded = xpForNextLevel - xpForCurrentLevel;
        return (xpInLevel / xpNeeded) * 100;
    };
    const xpProgress = calculateXPProgress();
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-sm mb-1", children: [_jsx("span", { className: "font-medium text-gray-700", children: "Experience" }), _jsxs("span", { className: "text-gray-600", children: [player.xp, " XP"] })] }), _jsx(Progress, { value: xpProgress, className: "h-3" }), _jsxs("div", { className: "text-xs text-gray-500 mt-1 text-right", children: [Math.round(xpProgress), "% to Level ", player.level + 1] })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3 mt-4", children: [_jsxs("div", { className: "p-3 bg-gray-50 rounded-lg", children: [_jsx("div", { className: "text-xs text-gray-600", children: "Total Actions" }), _jsx("div", { className: "text-xl font-bold text-gray-800", children: player.stats?.total_actions || 0 })] }), _jsxs("div", { className: "p-3 bg-gray-50 rounded-lg", children: [_jsx("div", { className: "text-xs text-gray-600", children: "PvP Wins" }), _jsx("div", { className: "text-xl font-bold text-gray-800", children: player.stats?.pvp_wins || 0 })] }), _jsxs("div", { className: "p-3 bg-gray-50 rounded-lg", children: [_jsx("div", { className: "text-xs text-gray-600", children: "Quests Done" }), _jsx("div", { className: "text-xl font-bold text-gray-800", children: player.stats?.quests_completed || 0 })] }), _jsxs("div", { className: "p-3 bg-gray-50 rounded-lg", children: [_jsx("div", { className: "text-xs text-gray-600", children: "Robots Owned" }), _jsx("div", { className: "text-xl font-bold text-gray-800", children: player.stats?.robots_owned || 0 })] })] }), player.prestige_level > 0 && (_jsx("div", { className: "mt-3 p-3 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-lg border-2 border-yellow-300", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-gray-800", children: "Prestige Level" }), _jsxs("span", { className: "text-2xl font-bold text-orange-600", children: ["\u2605 ", player.prestige_level] })] }) }))] }));
};
export default StatsDisplay;
