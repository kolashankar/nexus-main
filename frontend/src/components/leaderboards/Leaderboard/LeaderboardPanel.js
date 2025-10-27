import React from "react";
import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { Badge } from '../../ui/badge';
import { Avatar, AvatarFallback } from '../../ui/avatar';
import { Trophy, TrendingUp, TrendingDown, Crown, Sword, DollarSign, Target } from 'lucide-react';
import { useLeaderboards } from '../../../hooks/useLeaderboards';
const LeaderboardPanel = () => {
    const { leaderboards, myRanks, loading, fetchLeaderboard, fetchMyRank } = useLeaderboards();
    const [activeTab, setActiveTab] = useState('karma');
    useEffect(() => {
        fetchLeaderboard('karma');
        fetchLeaderboard('wealth');
        fetchLeaderboard('combat');
        fetchLeaderboard('achievement');
        fetchMyRank('karma');
        fetchMyRank('wealth');
        fetchMyRank('combat');
        fetchMyRank('achievement');
    }, []);
    const getLeaderboardIcon = (type) => {
        const icons = {
            karma: _jsx(Target, { className: "h-5 w-5" }),
            wealth: _jsx(DollarSign, { className: "h-5 w-5" }),
            combat: _jsx(Sword, { className: "h-5 w-5" }),
            achievement: _jsx(Trophy, { className: "h-5 w-5" })
        };
        return icons[type] || _jsx(Trophy, { className: "h-5 w-5" });
    };
    const getRankColor = (rank) => {
        if (rank === 1)
            return 'text-yellow-500';
        if (rank === 2)
            return 'text-gray-400';
        if (rank === 3)
            return 'text-amber-700';
        return 'text-muted-foreground';
    };
    const getRankIcon = (rank) => {
        if (rank <= 3) {
            return _jsx(Crown, { className: `h-5 w-5 ${getRankColor(rank)}` });
        }
        return null;
    };
    const formatValue = (type, value) => {
        if (type === 'wealth') {
            return `$${value.toLocaleString()}`;
        }
        return value.toLocaleString();
    };
    const renderLeaderboardEntry = (entry, type) => (_jsxs("div", { className: "flex items-center justify-between p-3 rounded-lg hover:bg-secondary/20 transition-colors", children: [_jsxs("div", { className: "flex items-center gap-3 flex-1", children: [_jsxs("div", { className: "flex items-center gap-2 min-w-[60px]", children: [_jsxs("span", { className: `text-lg font-bold ${getRankColor(entry.rank)}`, children: ["#", entry.rank] }), getRankIcon(entry.rank)] }), _jsx(Avatar, { className: "h-10 w-10", children: _jsx(AvatarFallback, { children: entry.username.substring(0, 2).toUpperCase() }) }), _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("p", { className: "font-semibold", children: entry.username }), entry.title && (_jsx(Badge, { variant: "outline", className: "text-xs", children: entry.title }))] }), _jsxs("div", { className: "flex items-center gap-2 text-xs text-muted-foreground", children: [entry.level && _jsxs("span", { children: ["Level ", entry.level] }), entry.guild_name && (_jsxs(_Fragment, { children: [_jsx("span", { children: "\u2022" }), _jsx("span", { children: entry.guild_name })] }))] })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("div", { className: "text-right", children: [_jsx("p", { className: "font-bold text-lg", children: formatValue(type, entry.value) }), entry.change_24h !== undefined && entry.change_24h !== 0 && (_jsxs("div", { className: "flex items-center gap-1 text-xs", children: [entry.change_24h > 0 ? (_jsx(TrendingUp, { className: "h-3 w-3 text-green-500" })) : (_jsx(TrendingDown, { className: "h-3 w-3 text-red-500" })), _jsx("span", { className: entry.change_24h > 0 ? 'text-green-500' : 'text-red-500', children: Math.abs(entry.change_24h) })] }))] }) })] }, entry.player_id));
    const renderMyRank = (type) => {
        const rank = myRanks[type];
        if (!rank)
            return null;
        return (_jsx(Card, { className: "border-primary/50 bg-primary/5 mb-4", children: _jsx(CardContent, { className: "pt-4", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("div", { className: `text-2xl font-bold ${getRankColor(rank.rank)}`, children: ["#", rank.rank] }), _jsxs("div", { children: [_jsx("p", { className: "font-semibold", children: "Your Rank" }), _jsxs("p", { className: "text-sm text-muted-foreground", children: ["Top ", rank.percentile.toFixed(1), "%"] })] })] }), _jsxs("div", { className: "text-right", children: [_jsx("p", { className: "text-2xl font-bold", children: formatValue(type, rank.value) }), _jsxs("p", { className: "text-xs text-muted-foreground", children: [rank.total_players.toLocaleString(), " players"] })] })] }) }) }));
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center py-12", children: _jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary" }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-3xl font-bold", children: "Leaderboards" }), _jsx("p", { className: "text-muted-foreground", children: "Compete with players worldwide" })] }), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { className: "grid w-full grid-cols-4", children: [_jsxs(TabsTrigger, { value: "karma", className: "gap-2", children: [getLeaderboardIcon('karma'), "Karma"] }), _jsxs(TabsTrigger, { value: "wealth", className: "gap-2", children: [getLeaderboardIcon('wealth'), "Wealth"] }), _jsxs(TabsTrigger, { value: "combat", className: "gap-2", children: [getLeaderboardIcon('combat'), "Combat"] }), _jsxs(TabsTrigger, { value: "achievement", className: "gap-2", children: [getLeaderboardIcon('achievement'), "Achievements"] })] }), ['karma', 'wealth', 'combat', 'achievement'].map(type => (_jsxs(TabsContent, { value: type, className: "space-y-4", children: [renderMyRank(type), _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsxs(CardTitle, { className: "flex items-center gap-2", children: [getLeaderboardIcon(type), type.charAt(0).toUpperCase() + type.slice(1), " Leaderboard"] }), _jsxs(CardDescription, { children: ["Top players ranked by ", type] })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-2", children: [leaderboards[type]?.entries?.map((entry) => renderLeaderboardEntry(entry, type)), (!leaderboards[type] || leaderboards[type].entries?.length === 0) && (_jsx("p", { className: "text-center text-muted-foreground py-8", children: "No rankings available yet" }))] }) })] })] }, type)))] })] }));
};
export default LeaderboardPanel;
