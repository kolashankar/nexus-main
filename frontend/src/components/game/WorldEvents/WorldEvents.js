import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Sparkles, Zap, AlertTriangle, Globe, Clock, Users } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { EventCard } from './EventCard';
import { EventDetails } from './EventDetails';
import { KarmaDisplay } from './KarmaDisplay';
import { worldService } from '@/services/api/worldService';
import './WorldEvents.css';
export const WorldEvents = () => {
    const [activeEvent, setActiveEvent] = useState(null);
    const [recentEvents, setRecentEvents] = useState([]);
    const [worldState, setWorldState] = useState(null);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const { toast } = useToast();
    useEffect(() => {
        fetchData();
        // Poll for updates every 30 seconds
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);
    const fetchData = async () => {
        try {
            const [eventData, eventsData, stateData] = await Promise.all([
                worldService.getActiveEvent(),
                worldService.getRecentEvents(10),
                worldService.getWorldState()
            ]);
            setActiveEvent(eventData);
            setRecentEvents(eventsData.events);
            setWorldState(stateData);
        }
        catch (error) {
            console.error('Error fetching world data:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const handleParticipate = async (eventId) => {
        try {
            const result = await worldService.participateInEvent(eventId);
            if (result.success) {
                toast({
                    title: "Participation Recorded!",
                    description: result.message,
                });
                // Refresh data
                fetchData();
            }
        }
        catch (error) {
            toast({
                title: "Participation Failed",
                description: error.message || "Could not record participation",
                variant: "destructive"
            });
        }
    };
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'critical': return 'destructive';
            case 'high': return 'orange';
            case 'medium': return 'yellow';
            case 'low': return 'green';
            default: return 'secondary';
        }
    };
    const getImpactIcon = (impact) => {
        switch (impact) {
            case 'world_changing': return _jsx(Sparkles, { className: "w-5 h-5 text-purple-500" });
            case 'high': return _jsx(Zap, { className: "w-5 h-5 text-yellow-500" });
            case 'medium': return _jsx(AlertTriangle, { className: "w-5 h-5 text-orange-500" });
            default: return _jsx(Globe, { className: "w-5 h-5 text-blue-500" });
        }
    };
    const calculateTimeRemaining = (endsAt) => {
        const end = new Date(endsAt);
        const now = new Date();
        const diff = end.getTime() - now.getTime();
        if (diff <= 0)
            return 'Ending soon';
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        if (hours > 0) {
            return `${hours}h ${minutes}m remaining`;
        }
        return `${minutes}m remaining`;
    };
    if (loading) {
        return (_jsx("div", { className: "world-events-container", children: _jsx("div", { className: "flex items-center justify-center h-64", children: _jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary" }) }) }));
    }
    return (_jsxs("div", { className: "world-events-container p-6 space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(Globe, { className: "w-8 h-8 text-primary" }), "World Events"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Dynamic events triggered by collective karma" })] }), worldState && (_jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-sm text-muted-foreground", children: "Collective Karma" }), _jsx("div", { className: "text-2xl font-bold", children: worldState.collective_karma.toLocaleString() }), _jsx(Badge, { variant: worldState.karma_trend === 'rising' ? 'default' : worldState.karma_trend === 'falling' ? 'destructive' : 'secondary', children: worldState.karma_trend })] }))] }), activeEvent && (_jsxs(Card, { className: "active-event-card border-2 border-primary shadow-lg", children: [_jsx(CardHeader, { className: "pb-4", children: _jsx("div", { className: "flex items-start justify-between", children: _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center gap-2 mb-2", children: [getImpactIcon(activeEvent.estimated_impact), _jsx(Badge, { variant: getSeverityColor(activeEvent.severity), children: activeEvent.severity }), activeEvent.is_global && (_jsxs(Badge, { variant: "outline", children: [_jsx(Globe, { className: "w-3 h-3 mr-1" }), "Global"] }))] }), _jsx(CardTitle, { className: "text-2xl", children: activeEvent.name }), _jsx(CardDescription, { className: "text-base mt-2", children: activeEvent.description })] }) }) }), _jsxs(CardContent, { className: "space-y-4", children: [activeEvent.ends_at && (_jsxs("div", { className: "flex items-center gap-2 text-muted-foreground", children: [_jsx(Clock, { className: "w-4 h-4" }), _jsx("span", { className: "font-semibold", children: calculateTimeRemaining(activeEvent.ends_at) })] })), _jsx("div", { className: "bg-muted/50 p-4 rounded-lg", children: _jsx("p", { className: "text-sm leading-relaxed", children: activeEvent.lore }) }), _jsxs("div", { className: "space-y-2", children: [_jsx("h4", { className: "font-semibold", children: "Active Effects:" }), _jsx("div", { className: "grid gap-2", children: activeEvent.effects.map((effect, idx) => (_jsxs("div", { className: "flex items-center justify-between bg-muted/30 p-3 rounded", children: [_jsx("span", { className: "text-sm", children: effect.description }), _jsxs(Badge, { variant: "outline", children: [effect.duration_hours, "h"] })] }, idx))) })] }), activeEvent.requires_participation && (_jsx("div", { className: "bg-primary/10 p-4 rounded-lg border border-primary/20", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("h4", { className: "font-semibold mb-1", children: "Participation Required" }), _jsxs("p", { className: "text-sm text-muted-foreground", children: [activeEvent.total_participants, " players participating"] })] }), _jsxs(Button, { onClick: () => handleParticipate(activeEvent.event_id), children: [_jsx(Users, { className: "w-4 h-4 mr-2" }), "Participate"] })] }) })), _jsx(Button, { variant: "outline", className: "w-full", onClick: () => setSelectedEvent(activeEvent), children: "View Full Details" })] })] })), !activeEvent && (_jsx(Card, { children: _jsxs(CardContent, { className: "py-12 text-center", children: [_jsx(Globe, { className: "w-16 h-16 mx-auto mb-4 text-muted-foreground" }), _jsx("h3", { className: "text-xl font-semibold mb-2", children: "No Active Events" }), _jsx("p", { className: "text-muted-foreground", children: "The Architect is watching... Events are triggered by collective player karma." })] }) })), _jsxs(Tabs, { defaultValue: "recent", className: "w-full", children: [_jsxs(TabsList, { className: "grid w-full grid-cols-2", children: [_jsx(TabsTrigger, { value: "recent", children: "Recent Events" }), _jsx(TabsTrigger, { value: "karma", children: "World Karma" })] }), _jsx(TabsContent, { value: "recent", className: "space-y-4 mt-4", children: recentEvents.length > 0 ? (_jsx(ScrollArea, { className: "h-[600px]", children: _jsx("div", { className: "space-y-3 pr-4", children: recentEvents.map((event) => (_jsx(EventCard, { event: event, onViewDetails: () => setSelectedEvent(event), getSeverityColor: getSeverityColor, getImpactIcon: getImpactIcon }, event.event_id))) }) })) : (_jsx(Card, { children: _jsx(CardContent, { className: "py-12 text-center", children: _jsx("p", { className: "text-muted-foreground", children: "No recent events" }) }) })) }), _jsx(TabsContent, { value: "karma", className: "mt-4", children: worldState && _jsx(KarmaDisplay, { worldState: worldState }) })] }), selectedEvent && (_jsx(EventDetails, { event: selectedEvent, onClose: () => setSelectedEvent(null), onParticipate: handleParticipate }))] }));
};
