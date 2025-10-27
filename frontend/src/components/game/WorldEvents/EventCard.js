import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Clock, Globe, Users } from 'lucide-react';
export const EventCard = ({ event, onViewDetails, getSeverityColor, getImpactIcon }) => {
    const formatDate = (date) => {
        return new Date(date).toLocaleString();
    };
    const getStatusBadge = (status) => {
        switch (status) {
            case 'active':
                return _jsx(Badge, { variant: "default", children: "Active" });
            case 'ended':
                return _jsx(Badge, { variant: "secondary", children: "Ended" });
            case 'scheduled':
                return _jsx(Badge, { variant: "outline", children: "Scheduled" });
            default:
                return _jsx(Badge, { variant: "outline", children: status });
        }
    };
    return (_jsxs(Card, { className: "hover:shadow-md transition-shadow cursor-pointer", onClick: onViewDetails, children: [_jsx(CardHeader, { children: _jsx("div", { className: "flex items-start justify-between", children: _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center gap-2 mb-2", children: [getImpactIcon(event.estimated_impact), _jsx(Badge, { variant: getSeverityColor(event.severity), children: event.severity }), getStatusBadge(event.status), event.is_global && (_jsxs(Badge, { variant: "outline", children: [_jsx(Globe, { className: "w-3 h-3 mr-1" }), "Global"] }))] }), _jsx(CardTitle, { className: "text-xl", children: event.name }), _jsx(CardDescription, { className: "mt-1", children: event.description })] }) }) }), _jsxs(CardContent, { children: [_jsxs("div", { className: "flex items-center justify-between text-sm text-muted-foreground", children: [_jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-4 h-4" }), _jsxs("span", { children: [event.duration_hours, "h"] })] }), event.requires_participation && (_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Users, { className: "w-4 h-4" }), _jsxs("span", { children: [event.total_participants, " participants"] })] }))] }), event.started_at && (_jsx("span", { className: "text-xs", children: formatDate(event.started_at) }))] }), _jsx("div", { className: "mt-3", children: _jsx(Button, { variant: "outline", size: "sm", className: "w-full", children: "View Details" }) })] })] }));
};
