import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { actionsService } from '../../../services/actions/actionsService';
export const ActionHistory = () => {
    const [actions, setActions] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadHistory();
    }, []);
    const loadHistory = async () => {
        try {
            const history = await actionsService.getHistory();
            setActions(history);
        }
        catch (error) {
            console.error('Failed to load action history:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const getActionIcon = (type) => {
        const icons = {
            hack: '🔐',
            help: '🤝',
            steal: '💰',
            donate: '💝',
            trade: '🤝'
        };
        return icons[type] || '⚡';
    };
    const getActionColor = (type) => {
        const colors = {
            hack: 'bg-purple-500',
            help: 'bg-green-500',
            steal: 'bg-red-500',
            donate: 'bg-blue-500',
            trade: 'bg-yellow-500'
        };
        return colors[type] || 'bg-gray-500';
    };
    if (loading) {
        return _jsx("div", { className: "text-center py-8", children: "Loading history..." });
    }
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Recent Actions" }) }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-3", children: actions.length === 0 ? (_jsx("p", { className: "text-gray-500 text-center py-4", children: "No actions yet" })) : (actions.map((action) => (_jsxs("div", { className: "flex items-center justify-between p-3 bg-gray-50 rounded-lg", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-2xl", children: getActionIcon(action.action_type) }), _jsxs("div", { children: [_jsx("p", { className: "font-medium capitalize", children: action.action_type }), _jsx("p", { className: "text-sm text-gray-500", children: new Date(action.timestamp).toLocaleString() })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { className: getActionColor(action.action_type), children: [action.karma_changes?.actor_karma > 0 ? '+' : '', action.karma_changes?.actor_karma || 0, " Karma"] }) })] }, action._id)))) }) })] }));
};
