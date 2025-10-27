import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Trophy, Crown, Award } from 'lucide-react';
import BattlePassDashboard from '../../components/achievements/BattlePass/BattlePassDashboard';
import SeasonalLeaderboard from '../../components/leaderboards/SeasonalLeaderboard/SeasonalLeaderboard';
import TournamentList from '../../components/tournaments/TournamentList';
const SeasonalDashboard = () => {
    const [activeTab, setActiveTab] = useState('battlepass');
    return (_jsxs("div", { className: "container mx-auto p-6 space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-4xl font-bold mb-2", children: "Seasonal Content" }), _jsx("p", { className: "text-muted-foreground", children: "Compete, progress, and earn exclusive rewards" })] }), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { className: "grid w-full grid-cols-3", children: [_jsxs(TabsTrigger, { value: "battlepass", className: "gap-2", children: [_jsx(Crown, { className: "h-4 w-4" }), "Battle Pass"] }), _jsxs(TabsTrigger, { value: "leaderboards", className: "gap-2", children: [_jsx(Trophy, { className: "h-4 w-4" }), "Leaderboards"] }), _jsxs(TabsTrigger, { value: "tournaments", className: "gap-2", children: [_jsx(Award, { className: "h-4 w-4" }), "Tournaments"] })] }), _jsx(TabsContent, { value: "battlepass", className: "mt-6", children: _jsx(BattlePassDashboard, {}) }), _jsx(TabsContent, { value: "leaderboards", className: "mt-6", children: _jsx(SeasonalLeaderboard, {}) }), _jsx(TabsContent, { value: "tournaments", className: "mt-6", children: _jsx(TournamentList, {}) })] })] }));
};
export default SeasonalDashboard;
