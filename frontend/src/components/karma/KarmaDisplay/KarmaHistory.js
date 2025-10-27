import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import apiClient from '@/services/api/client';
import { formatDistance } from 'date-fns';
const KarmaHistory = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchHistory();
    }, []);
    const fetchHistory = async () => {
        try {
            const response = await apiClient.get('/api/karma/history?limit=20');
            setHistory(response.data);
        }
        catch (error) {
            console.error('Failed to fetch karma history:', error);
        }
        finally {
            setLoading(false);
        }
    };
    if (loading) {
        return (_jsx(Card, { children: _jsx(CardContent, { className: "p-6", children: _jsx("div", { className: "animate-pulse space-y-3", children: [1, 2, 3].map(i => (_jsx("div", { className: "h-16 bg-gray-300 rounded" }, i))) }) }) }));
    }
    return (_jsxs(Card, { className: "w-full", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Karma History" }) }), _jsx(CardContent, { children: _jsx(ScrollArea, { className: "h-96", children: _jsx("div", { className: "space-y-3", children: history.length === 0 ? (_jsx("div", { className: "text-center text-gray-500 py-8", children: "No karma history yet. Perform actions to start building your karma!" })) : (history.map((entry, index) => (_jsxs("div", { className: "flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors", children: [_jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsx(Badge, { variant: entry.karma_change > 0 ? 'default' : 'destructive', children: entry.action_type.toUpperCase() }), _jsx("span", { className: "text-sm text-gray-600", children: formatDistance(new Date(entry.timestamp), new Date(), { addSuffix: true }) })] }), _jsx("p", { className: "text-sm text-gray-700", children: entry.message })] }), _jsxs("div", { className: "text-right", children: [_jsxs("div", { className: `text-2xl font-bold ${entry.karma_change > 0 ? 'text-green-600' : 'text-red-600'}`, children: [entry.karma_change > 0 ? '+' : '', entry.karma_change] }), _jsx("div", { className: "text-xs text-gray-500", children: "karma" })] })] }, index)))) }) }) })] }));
};
export default KarmaHistory;
