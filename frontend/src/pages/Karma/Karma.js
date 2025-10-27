import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import KarmaDisplay from '../../components/karma/KarmaDisplay/KarmaDisplay';
import KarmaHistory from '../../components/karma/KarmaDisplay/KarmaHistory';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { useKarma } from '../../hooks/useKarma';
export const Karma = () => {
    const { karmaScore, karmaHistory, loading } = useKarma();
    if (loading) {
        return _jsx("div", { className: "container mx-auto p-6", children: "Loading karma data..." });
    }
    return (_jsxs("div", { className: "container mx-auto p-6 space-y-6", children: [_jsx("h1", { className: "text-3xl font-bold", children: "Karma System" }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsx(KarmaDisplay, {}), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Karma Insights" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Current Score" }), _jsx("p", { className: "text-3xl font-bold", children: karmaScore })] }), _jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Total Events" }), _jsx("p", { className: "text-2xl font-semibold", children: karmaHistory.length })] }), _jsxs("div", { children: [_jsx("p", { className: "text-sm text-gray-600", children: "Moral Alignment" }), _jsx("p", { className: "text-xl font-medium", children: karmaScore > 500 ? '😇 Good' : karmaScore < -500 ? '😈 Bad' : '⚖️ Neutral' })] })] }) })] })] }), _jsx(KarmaHistory, {})] }));
};