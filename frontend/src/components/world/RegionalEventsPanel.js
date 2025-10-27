import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { MapPin, Zap, Shield, TrendingUp, AlertTriangle, PartyPopper } from 'lucide-react';
import axios from 'axios';
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const RegionalEventsPanel = ({ territoryId }) => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        if (territoryId) {
            fetchRegionalEvents(territoryId);
        }
    }, [territoryId]);
    const fetchRegionalEvents = async (territory) => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/api/world/events/regional/${territory}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setEvents(response.data);
        }
        catch (error) {
            console.error('Error fetching regional events:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const getEventIcon = (eventType) => {
        const icons = {
            resource_surge: _jsx(Zap, { className: "h-5 w-5 text-yellow-500" }),
            hostile_takeover: _jsx(Shield, { className: "h-5 w-5 text-red-500" }),
            market_boom: _jsx(TrendingUp, { className: "h-5 w-5 text-green-500" }),
            npc_raid: _jsx(AlertTriangle, { className: "h-5 w-5 text-orange-500" }),
            festival: _jsx(PartyPopper, { className: "h-5 w-5 text-purple-500" }),
            disaster: _jsx(AlertTriangle, { className: "h-5 w-5 text-red-600" })
        };
        return icons[eventType] || _jsx(MapPin, { className: "h-5 w-5" });
    };
    const getEventColor = (eventType) => {
        const colors = {
            resource_surge: 'border-yellow-500/50',
            hostile_takeover: 'border-red-500/50',
            market_boom: 'border-green-500/50',
            npc_raid: 'border-orange-500/50',
            festival: 'border-purple-500/50',
            disaster: 'border-red-600/50'
        };
        return colors[eventType] || '';
    };
    const calculateTimeRemaining = (endsAt) => {
        const end = new Date(endsAt);
        const now = new Date();
        const diff = end.getTime() - now.getTime();
        if (diff <= 0)
            return 'Ended';
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        }
        return `${minutes}m`;
    };
    const renderEffects = (effects) => {
        return Object.entries(effects).map(([key, value]) => {
            let displayValue = value;
            if (typeof value === 'number') {
                if (value > 1) {
                    displayValue = `${value}x`;
                }
                else if (value < 1) {
                    displayValue = `${(value * 100).toFixed(0)}%`;
                }
            }
            else if (typeof value === 'boolean') {
                displayValue = value ? 'Active' : 'Inactive';
            }
            return (_jsxs("div", { className: "text-xs", children: [_jsxs("span", { className: "text-muted-foreground", children: [key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), ":"] }), _jsx("span", { className: "ml-1 font-medium", children: displayValue.toString() })] }, key));
        });
    };
    if (!territoryId) {
        return (_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center py-8", children: [_jsx(MapPin, { className: "h-12 w-12 text-muted-foreground mx-auto mb-4" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Select a territory to view regional events" })] }) }) }));
    }
    if (loading) {
        return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Regional Events" }) }), _jsx(CardContent, { children: _jsx("div", { className: "flex items-center justify-center py-8", children: _jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-primary" }) }) })] }));
    }
    return (_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsxs(CardTitle, { className: "flex items-center gap-2", children: [_jsx(MapPin, { className: "h-5 w-5" }), "Regional Events"] }), _jsx(CardDescription, { children: "Active events in this territory" })] }), _jsx(CardContent, { children: events.length === 0 ? (_jsx("div", { className: "text-center py-8", children: _jsx("p", { className: "text-sm text-muted-foreground", children: "No active events in this territory" }) })) : (_jsx("div", { className: "space-y-3", children: events.map((event) => (_jsxs("div", { className: `border-2 rounded-lg p-4 ${getEventColor(event.event_type)}`, children: [_jsxs("div", { className: "flex items-start justify-between mb-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [getEventIcon(event.event_type), _jsxs("div", { children: [_jsx("h4", { className: "font-semibold", children: event.name }), _jsx("p", { className: "text-xs text-muted-foreground", children: event.territory_name })] })] }), _jsx(Badge, { variant: "outline", children: calculateTimeRemaining(event.ends_at) })] }), _jsx("p", { className: "text-sm text-muted-foreground mb-3", children: event.description }), _jsxs("div", { className: "space-y-1 bg-secondary/20 rounded p-2", children: [_jsx("p", { className: "text-xs font-semibold mb-1", children: "Effects:" }), renderEffects(event.effects)] })] }, event.event_id))) })) })] }));
};
export default RegionalEventsPanel;
