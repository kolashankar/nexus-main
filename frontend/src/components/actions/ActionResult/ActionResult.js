import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent } from '../../ui/card';
import { Badge } from '../../ui/badge';
export const ActionResult = ({ success, message, karmaChange, creditsChange }) => {
    return (_jsx(Card, { className: success ? 'border-green-500' : 'border-red-500', children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center space-y-4", children: [_jsx("div", { className: "text-4xl", children: success ? '✅' : '❌' }), _jsx("p", { className: "text-lg font-medium", children: message }), _jsxs("div", { className: "flex gap-4 justify-center", children: [karmaChange !== undefined && (_jsxs(Badge, { variant: karmaChange > 0 ? 'default' : 'destructive', children: [karmaChange > 0 ? '+' : '', karmaChange, " Karma"] })), creditsChange !== undefined && (_jsxs(Badge, { variant: "outline", children: [creditsChange > 0 ? '+' : '', creditsChange, " Credits"] }))] })] }) }) }));
};
