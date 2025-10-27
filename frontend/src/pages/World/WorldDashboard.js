import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Globe, MapPin } from 'lucide-react';
import WorldEventsPanel from '../../components/world/WorldEventsPanel';
import RegionalEventsPanel from '../../components/world/RegionalEventsPanel';
const WorldDashboard = () => {
    const [activeTab, setActiveTab] = useState('global');
    const [selectedTerritory, setSelectedTerritory] = useState(1);
    return (_jsxs("div", { className: "container mx-auto p-6 space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-4xl font-bold mb-2", children: "World Events" }), _jsx("p", { className: "text-muted-foreground", children: "Global and regional events affecting the game world" })] }), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { className: "grid w-full grid-cols-2", children: [_jsxs(TabsTrigger, { value: "global", className: "gap-2", children: [_jsx(Globe, { className: "h-4 w-4" }), "Global Events"] }), _jsxs(TabsTrigger, { value: "regional", className: "gap-2", children: [_jsx(MapPin, { className: "h-4 w-4" }), "Regional Events"] })] }), _jsx(TabsContent, { value: "global", className: "mt-6", children: _jsx(WorldEventsPanel, {}) }), _jsx(TabsContent, { value: "regional", className: "mt-6", children: _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1", children: _jsxs("div", { className: "space-y-2", children: [_jsx("h3", { className: "text-lg font-semibold mb-4", children: "Select Territory" }), [1, 2, 3, 4, 5].map((id) => (_jsxs("button", { onClick: () => setSelectedTerritory(id), className: `w-full p-3 rounded-lg border text-left transition-colors ${selectedTerritory === id
                                                    ? 'border-primary bg-primary/10'
                                                    : 'border-border hover:border-primary/50'}`, children: [_jsxs("p", { className: "font-semibold", children: ["Territory ", id] }), _jsx("p", { className: "text-xs text-muted-foreground", children: "View regional events" })] }, id)))] }) }), _jsx("div", { className: "lg:col-span-2", children: _jsx(RegionalEventsPanel, { territoryId: selectedTerritory }) })] }) })] })] }));
};
export default WorldDashboard;
