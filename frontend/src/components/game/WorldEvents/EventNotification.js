import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { X, Sparkles, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './EventNotification.css';
export const EventNotification = ({ event, onClose, onViewDetails }) => {
    const [show, setShow] = useState(true);
    useEffect(() => {
        // Auto-dismiss after 10 seconds
        const timer = setTimeout(() => {
            handleClose();
        }, 10000);
        return () => clearTimeout(timer);
    }, []);
    const handleClose = () => {
        setShow(false);
        setTimeout(onClose, 300); // Wait for animation
    };
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'critical': return 'border-red-500 bg-red-50';
            case 'high': return 'border-orange-500 bg-orange-50';
            case 'medium': return 'border-yellow-500 bg-yellow-50';
            case 'low': return 'border-green-500 bg-green-50';
            default: return 'border-gray-500 bg-gray-50';
        }
    };
    return (_jsx(AnimatePresence, { children: show && (_jsx(motion.div, { initial: { opacity: 0, y: -20, scale: 0.95 }, animate: { opacity: 1, y: 0, scale: 1 }, exit: { opacity: 0, y: -20, scale: 0.95 }, transition: { duration: 0.3 }, className: "event-notification", children: _jsx(Card, { className: `border-2 shadow-lg ${getSeverityColor(event.severity)}`, children: _jsx(CardContent, { className: "p-4", children: _jsxs("div", { className: "flex items-start gap-3", children: [_jsx("div", { className: "flex-shrink-0", children: event.severity === 'critical' ? (_jsx(AlertTriangle, { className: "w-6 h-6 text-red-600" })) : (_jsx(Sparkles, { className: "w-6 h-6 text-primary" })) }), _jsxs("div", { className: "flex-1 min-w-0", children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsx(Badge, { variant: "outline", children: event.event_type }), _jsx(Badge, { children: event.severity })] }), _jsx("h4", { className: "font-bold text-lg mb-1", children: event.name }), _jsx("p", { className: "text-sm text-muted-foreground", children: event.description }), _jsxs("div", { className: "flex gap-2 mt-3", children: [_jsx(Button, { size: "sm", onClick: onViewDetails, children: "View Details" }), _jsx(Button, { size: "sm", variant: "outline", onClick: handleClose, children: "Dismiss" })] })] }), _jsx(Button, { variant: "ghost", size: "icon", className: "flex-shrink-0 h-6 w-6", onClick: handleClose, children: _jsx(X, { className: "w-4 h-4" }) })] }) }) }) })) }));
};
