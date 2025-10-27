import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Calendar, Trophy } from 'lucide-react';
import LeaderboardPanel from '../Leaderboard/LeaderboardPanel';
import axios from 'axios';
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const SeasonalLeaderboard = () => {
    const [season, setSeason] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchCurrentSeason();
    }, []);
    const fetchCurrentSeason = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/api/seasonal/season/current`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setSeason(response.data);
        }
        catch (error) {
            console.error('Error fetching current season:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const calculateDaysRemaining = () => {
        if (!season)
            return 0;
        const end = new Date(season.end_date);
        const now = new Date();
        const diff = end.getTime() - now.getTime();
        return Math.ceil(diff / (1000 * 60 * 60 * 24));
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center py-12", children: _jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary" }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [season && (_jsxs(Card, { className: "border-primary/50", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs(CardTitle, { className: "flex items-center gap-2", children: [_jsx(Trophy, { className: "h-6 w-6 text-primary" }), season.name] }), _jsx(CardDescription, { children: season.description })] }), _jsxs(Badge, { variant: "default", className: "text-lg px-4 py-2", children: ["Season ", season.season_number] })] }) }), _jsx(CardContent, { children: _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm text-muted-foreground mb-1", children: "Days Remaining" }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Calendar, { className: "h-5 w-5 text-primary" }), _jsx("p", { className: "text-2xl font-bold", children: calculateDaysRemaining() })] })] }), _jsxs("div", { children: [_jsx("p", { className: "text-sm text-muted-foreground mb-1", children: "Active Players" }), _jsx("p", { className: "text-2xl font-bold", children: season.active_players.toLocaleString() })] }), _jsxs("div", { children: [_jsx("p", { className: "text-sm text-muted-foreground mb-1", children: "Total Players" }), _jsx("p", { className: "text-2xl font-bold", children: season.total_players.toLocaleString() })] })] }) })] })), _jsx(LeaderboardPanel, {})] }));
};
export default SeasonalLeaderboard;
