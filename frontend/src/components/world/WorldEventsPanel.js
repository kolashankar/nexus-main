import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Sparkles, AlertTriangle, Activity, TrendingUp, TrendingDown } from 'lucide-react';
import { useWorldEvents } from '../../hooks/useWorldEvents';
import { Progress } from '../ui/progress';
const WorldEventsPanel = () => {
    const { worldState, activeEvents, loading } = useWorldEvents();
    const [selectedEvent, setSelectedEvent] = useState(null);
    const getKarmaTrendIcon = (trend) => {
        switch (trend) {
            case 'rising':
                return _jsx(TrendingUp, { className: "h-5 w-5 text-green-500" });
            case 'falling':
                return _jsx(TrendingDown, { className: "h-5 w-5 text-red-500" });
            default:
                return _jsx(Activity, { className: "h-5 w-5 text-blue-500" });
        }
    };
    const getEventTypeColor = (eventType) => {
        if (eventType.includes('blessing') || eventType.includes('golden')) {
            return 'bg-green-500';
        }
        if (eventType.includes('purge') || eventType.includes('collapse')) {
            return 'bg-red-500';
        }
        return 'bg-blue-500';
    };
    const calculateTimeRemaining = (endsAt) => {
        const end = new Date(endsAt);
        const now = new Date();
        const diff = end.getTime() - now.getTime();
        if (diff <= 0)
            return 'Ended';
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        return `${hours}h ${minutes}m remaining`;
    };
    if (loading) {
        return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "World Events" }) }), _jsx(CardContent, { children: _jsx("div", { className: "flex items-center justify-center py-8", children: _jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-primary" }) }) })] }));
    }
    return (_jsxs("div", { className: "space-y-4", children: [_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsxs(CardTitle, { className: "flex items-center justify-between", children: [_jsx("span", { children: "Global Karma Status" }), worldState && getKarmaTrendIcon(worldState.karma_trend)] }), _jsx(CardDescription, { children: "Collective karma across all players" })] }), _jsx(CardContent, { children: worldState ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-sm mb-2", children: [_jsx("span", { children: "Collective Karma" }), _jsx("span", { className: "font-bold", children: worldState.collective_karma.toFixed(0) })] }), _jsx(Progress, { value: Math.abs(worldState.collective_karma) % 100, className: "h-2" })] }), _jsxs("div", { className: "flex justify-between text-sm text-muted-foreground", children: [_jsxs("span", { children: ["Online: ", worldState.online_players] }), _jsxs("span", { children: ["Total: ", worldState.total_players] })] })] })) : (_jsx("p", { className: "text-sm text-muted-foreground", children: "No data available" })) })] }), worldState?.active_event && (_jsxs(Card, { className: "border-2 border-primary", children: [_jsxs(CardHeader, { children: [_jsxs(CardTitle, { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "h-5 w-5 text-yellow-500" }), worldState.active_event.name] }), _jsx(CardDescription, { children: worldState.active_event.description })] }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { className: getEventTypeColor(worldState.active_event.event_type), children: worldState.active_event.event_type.replace('_', ' ').toUpperCase() }), _jsx("span", { className: "text-sm text-muted-foreground", children: calculateTimeRemaining(worldState.active_event.ends_at) })] }), _jsxs("div", { className: "bg-secondary/20 rounded-lg p-3 space-y-1", children: [_jsx("p", { className: "text-sm font-semibold mb-2", children: "Active Effects:" }), Object.entries(worldState.active_event.effects).map(([key, value]) => (_jsxs("div", { className: "text-sm flex justify-between", children: [_jsxs("span", { className: "text-muted-foreground", children: [key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()), ":"] }), _jsx("span", { className: "font-medium", children: typeof value === 'number' ? `${value}x` : value.toString() })] }, key)))] }), _jsxs("p", { className: "text-sm text-muted-foreground", children: [worldState.active_event.participants, " players participating"] })] }) })] })), activeEvents && activeEvents.length > 0 && (_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { children: "Active Events" }), _jsx(CardDescription, { children: "Regional and special events currently happening" })] }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-3", children: activeEvents.map((event) => (_jsx("div", { className: "border rounded-lg p-3 hover:bg-secondary/20 cursor-pointer transition-colors", onClick: () => setSelectedEvent(event), children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex-1", children: [_jsx("h4", { className: "font-semibold text-sm", children: event.name }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: event.description })] }), _jsx(Badge, { variant: "outline", className: "ml-2", children: calculateTimeRemaining(event.ends_at) })] }) }, event.event_id))) }) })] })), (!worldState?.active_event && (!activeEvents || activeEvents.length === 0)) && (_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center py-8", children: [_jsx(AlertTriangle, { className: "h-12 w-12 text-muted-foreground mx-auto mb-4" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "No active world events at this time" }), _jsx("p", { className: "text-xs text-muted-foreground mt-2", children: "Collective karma actions will trigger new events" })] }) }) }))] }));
};
export default WorldEventsPanel;
