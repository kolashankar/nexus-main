import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MapPin, Shield, Swords, TrendingUp, Users } from 'lucide-react';
import { worldService } from '@/services/api/worldService';
import './WorldMap.css';
export const WorldMap = () => {
    const [territories, setTerritories] = useState([]);
    const [selectedTerritory, setSelectedTerritory] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchTerritories();
    }, []);
    const fetchTerritories = async () => {
        try {
            const data = await worldService.getAllTerritories();
            setTerritories(data.territories);
            if (data.territories.length > 0) {
                setSelectedTerritory(data.territories[0]);
            }
        }
        catch (error) {
            console.error('Error fetching territories:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const getStatusColor = (status) => {
        switch (status) {
            case 'controlled': return 'bg-blue-500';
            case 'contested': return 'bg-red-500';
            case 'neutral': return 'bg-gray-500';
            default: return 'bg-gray-500';
        }
    };
    const getRegionColor = (region) => {
        switch (region) {
            case 'north': return 'from-blue-400 to-blue-600';
            case 'south': return 'from-green-400 to-green-600';
            case 'east': return 'from-yellow-400 to-yellow-600';
            case 'west': return 'from-purple-400 to-purple-600';
            case 'central': return 'from-red-400 to-red-600';
            default: return 'from-gray-400 to-gray-600';
        }
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center h-96", children: _jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary" }) }));
    }
    return (_jsx("div", { className: "world-map-container p-6", children: _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1", children: _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "flex items-center gap-2", children: [_jsx(MapPin, { className: "w-5 h-5" }), "Territories"] }) }), _jsx(CardContent, { className: "p-0", children: _jsx(ScrollArea, { className: "h-[700px]", children: _jsx("div", { className: "space-y-2 p-4", children: territories.map((territory) => (_jsxs("div", { className: `p-3 rounded-lg border cursor-pointer transition-all hover:shadow-md ${selectedTerritory?.territory_id === territory.territory_id
                                                ? 'border-primary bg-primary/5'
                                                : 'border-border'}`, onClick: () => setSelectedTerritory(territory), children: [_jsxs("div", { className: "flex items-start justify-between mb-2", children: [_jsxs("div", { className: "flex-1", children: [_jsx("div", { className: "font-semibold", children: territory.name }), _jsxs("div", { className: "text-xs text-muted-foreground capitalize", children: [territory.region, " Region"] })] }), _jsx("div", { className: `w-3 h-3 rounded-full ${getStatusColor(territory.status)}` })] }), territory.contested && (_jsxs(Badge, { variant: "destructive", className: "text-xs", children: [_jsx(Swords, { className: "w-3 h-3 mr-1" }), "Contested"] })), territory.controlling_guild_name && (_jsxs("div", { className: "text-xs text-muted-foreground mt-1", children: ["Controlled by: ", territory.controlling_guild_name] })), _jsxs("div", { className: "flex items-center gap-3 mt-2 text-xs", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Users, { className: "w-3 h-3" }), territory.total_residents] }), _jsxs("div", { className: "text-muted-foreground", children: ["Karma: ", territory.local_karma.toFixed(0)] })] })] }, territory.territory_id))) }) }) })] }) }), _jsx("div", { className: "lg:col-span-2", children: selectedTerritory ? (_jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx("div", { className: `h-32 -mx-6 -mt-6 mb-4 rounded-t-lg bg-gradient-to-br ${getRegionColor(selectedTerritory.region)} flex items-center justify-center`, children: _jsxs("div", { className: "text-center text-white", children: [_jsx("h2", { className: "text-3xl font-bold", children: selectedTerritory.name }), _jsxs("p", { className: "text-sm opacity-90 capitalize", children: [selectedTerritory.region, " Region"] })] }) }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Badge, { variant: "outline", className: "capitalize", children: selectedTerritory.status }), selectedTerritory.contested && (_jsxs(Badge, { variant: "destructive", children: [_jsx(Swords, { className: "w-3 h-3 mr-1" }), "Under Siege"] }))] })] }), _jsxs(CardContent, { className: "space-y-6", children: [_jsx("p", { className: "text-muted-foreground", children: selectedTerritory.description }), selectedTerritory.controlling_guild_name && (_jsxs("div", { className: "bg-muted/50 p-4 rounded-lg", children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsx(Shield, { className: "w-4 h-4 text-primary" }), _jsx("span", { className: "font-semibold", children: "Controlled Territory" })] }), _jsxs("p", { className: "text-sm text-muted-foreground", children: ["Under control of ", _jsx("span", { className: "font-semibold", children: selectedTerritory.controlling_guild_name })] })] })), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center", children: [_jsx(Users, { className: "w-8 h-8 mx-auto mb-2 text-primary" }), _jsx("div", { className: "text-2xl font-bold", children: selectedTerritory.total_residents }), _jsx("div", { className: "text-sm text-muted-foreground", children: "Total Residents" }), _jsxs("div", { className: "text-xs text-muted-foreground mt-1", children: [selectedTerritory.online_players, " online"] })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center", children: [_jsx(TrendingUp, { className: "w-8 h-8 mx-auto mb-2 text-green-500" }), _jsx("div", { className: "text-2xl font-bold", children: selectedTerritory.local_karma.toFixed(0) }), _jsx("div", { className: "text-sm text-muted-foreground", children: "Local Karma" })] }) }) })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { className: "font-medium", children: "Prosperity Level" }), _jsxs("span", { className: "font-bold", children: [selectedTerritory.prosperity_level.toFixed(0), "%"] })] }), _jsx("div", { className: "h-2 bg-muted rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-green-500 transition-all", style: { width: `${selectedTerritory.prosperity_level}%` } }) })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { className: "font-medium", children: "Conflict Level" }), _jsxs("span", { className: "font-bold", children: [selectedTerritory.conflict_level.toFixed(0), "%"] })] }), _jsx("div", { className: "h-2 bg-muted rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-red-500 transition-all", style: { width: `${selectedTerritory.conflict_level}%` } }) })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2 text-sm", children: [_jsx("span", { className: "font-medium", children: "Strategic Value" }), _jsxs("span", { className: "font-bold", children: [selectedTerritory.strategic_value, "/100"] })] }), _jsx("div", { className: "h-2 bg-muted rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-purple-500 transition-all", style: { width: `${selectedTerritory.strategic_value}%` } }) })] })] }), selectedTerritory.active_events.length > 0 && (_jsxs("div", { children: [_jsx("h3", { className: "font-semibold mb-3", children: "Active Regional Events" }), _jsx("div", { className: "space-y-2", children: selectedTerritory.active_events.map((event, idx) => (_jsxs("div", { className: "bg-primary/10 p-3 rounded-lg border border-primary/20", children: [_jsx("div", { className: "font-medium", children: event.name }), _jsx("div", { className: "text-sm text-muted-foreground capitalize", children: event.event_type })] }, idx))) })] }))] })] })) : (_jsx(Card, { children: _jsxs(CardContent, { className: "py-12 text-center", children: [_jsx(MapPin, { className: "w-16 h-16 mx-auto mb-4 text-muted-foreground" }), _jsx("p", { className: "text-muted-foreground", children: "Select a territory to view details" })] }) })) })] }) }));
};
