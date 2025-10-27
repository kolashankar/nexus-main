import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, Minus, Users, Zap } from 'lucide-react';
import { worldService } from '@/services/api/worldService';
export const KarmaDisplay = ({ worldState }) => {
    const [karmaStats, setKarmaStats] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchKarmaStats();
    }, []);
    const fetchKarmaStats = async () => {
        try {
            const stats = await worldService.getKarmaStatistics();
            setKarmaStats(stats);
        }
        catch (error) {
            console.error('Error fetching karma stats:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const getTrendIcon = (trend) => {
        switch (trend) {
            case 'rising':
                return _jsx(TrendingUp, { className: "w-5 h-5 text-green-500" });
            case 'falling':
                return _jsx(TrendingDown, { className: "w-5 h-5 text-red-500" });
            default:
                return _jsx(Minus, { className: "w-5 h-5 text-gray-500" });
        }
    };
    const getKarmaColor = (karma) => {
        if (karma > 10000)
            return 'text-purple-500';
        if (karma > 5000)
            return 'text-blue-500';
        if (karma > 0)
            return 'text-green-500';
        if (karma > -5000)
            return 'text-yellow-500';
        if (karma > -10000)
            return 'text-orange-500';
        return 'text-red-500';
    };
    const getKarmaLevel = (karma) => {
        if (karma > 15000)
            return 'Golden Age';
        if (karma > 10000)
            return 'Enlightened';
        if (karma > 5000)
            return 'Virtuous';
        if (karma > 0)
            return 'Balanced (Positive)';
        if (karma > -5000)
            return 'Balanced (Negative)';
        if (karma > -10000)
            return 'Corrupt';
        if (karma > -15000)
            return 'Dark Times';
        return 'Apocalyptic';
    };
    if (loading) {
        return (_jsx(Card, { children: _jsx(CardContent, { className: "py-12", children: _jsx("div", { className: "flex items-center justify-center", children: _jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-primary" }) }) }) }));
    }
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Collective Karma Status" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "text-center space-y-2", children: [_jsx("div", { className: `text-5xl font-bold ${getKarmaColor(worldState.collective_karma)}`, children: worldState.collective_karma.toLocaleString() }), _jsxs("div", { className: "flex items-center justify-center gap-2", children: [getTrendIcon(worldState.karma_trend), _jsx("span", { className: "text-lg font-semibold capitalize", children: worldState.karma_trend })] }), _jsx(Badge, { variant: "outline", className: "text-sm", children: getKarmaLevel(worldState.collective_karma) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4 pt-4", children: [_jsxs("div", { className: "text-center p-4 bg-muted/50 rounded-lg", children: [_jsx("div", { className: "text-sm text-muted-foreground mb-1", children: "Average Karma" }), _jsx("div", { className: "text-2xl font-bold", children: worldState.average_karma.toFixed(1) })] }), _jsxs("div", { className: "text-center p-4 bg-muted/50 rounded-lg", children: [_jsx("div", { className: "text-sm text-muted-foreground mb-1", children: "Total Players" }), _jsxs("div", { className: "text-2xl font-bold flex items-center justify-center gap-2", children: [_jsx(Users, { className: "w-5 h-5" }), worldState.total_players.toLocaleString()] })] })] })] })] }), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Recent Activity (24h)" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { className: "text-green-600 font-medium", children: "Positive Actions" }), _jsxs("span", { className: "font-bold", children: [worldState.positive_actions_24h.toLocaleString(), "(", ((worldState.positive_actions_24h / worldState.total_actions_24h) * 100).toFixed(1), "%)"] })] }), _jsx(Progress, { value: (worldState.positive_actions_24h / worldState.total_actions_24h) * 100, className: "h-2 bg-green-100" })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { className: "text-red-600 font-medium", children: "Negative Actions" }), _jsxs("span", { className: "font-bold", children: [worldState.negative_actions_24h.toLocaleString(), "(", ((worldState.negative_actions_24h / worldState.total_actions_24h) * 100).toFixed(1), "%)"] })] }), _jsx(Progress, { value: (worldState.negative_actions_24h / worldState.total_actions_24h) * 100, className: "h-2 bg-red-100" })] })] }), _jsxs("div", { className: "flex items-center justify-between pt-2 border-t", children: [_jsxs("div", { className: "flex items-center gap-2 text-sm text-muted-foreground", children: [_jsx(Zap, { className: "w-4 h-4" }), _jsx("span", { children: "Total Actions" })] }), _jsx("span", { className: "text-lg font-bold", children: worldState.total_actions_24h.toLocaleString() })] })] })] }), karmaStats && karmaStats.distribution && (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Player Distribution" }) }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-2", children: Object.entries(karmaStats.distribution).map(([level, count]) => (_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { className: "capitalize", children: level.replace('_', ' ') }), _jsxs("span", { className: "font-semibold", children: [count, " players"] })] }, level))) }) })] })), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Event Thresholds" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-3 text-sm", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-purple-600 font-medium", children: "Golden Age" }), _jsx("span", { children: "+15,000" })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-blue-600 font-medium", children: "Enlightened Era" }), _jsx("span", { children: "+10,000" })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-green-600 font-medium", children: "Virtuous Period" }), _jsx("span", { children: "+5,000" })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-gray-600 font-medium", children: "Balanced World" }), _jsx("span", { children: "0" })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-orange-600 font-medium", children: "Dark Times" }), _jsx("span", { children: "-5,000" })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-red-600 font-medium", children: "Apocalyptic" }), _jsx("span", { children: "-10,000" })] })] }) })] })] }));
};
