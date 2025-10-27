import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardHeader, CardTitle, CardContent } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { Progress } from '../../ui/progress';
import { Zap, Clock } from 'lucide-react';
const SuperpowerCard = ({ power, isEquipped, onEquip, onUse, }) => {
    const isOnCooldown = power.cooldown_until
        ? new Date(power.cooldown_until) > new Date()
        : false;
    return (_jsxs(Card, { className: isEquipped ? 'border-2 border-primary' : '', children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "flex items-center justify-between text-lg", children: [_jsx("span", { children: power.power_id.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') }), isEquipped && _jsx(Badge, { children: "Equipped" })] }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsxs("span", { className: "text-muted-foreground", children: ["Level ", power.level] }), _jsxs("span", { className: "text-muted-foreground", children: ["Uses: ", power.usage_count] })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-sm mb-1", children: [_jsx("span", { children: "Mastery" }), _jsxs("span", { children: [power.mastery.toFixed(1), "%"] })] }), _jsx(Progress, { value: power.mastery, className: "h-2" })] }), isOnCooldown && (_jsxs("div", { className: "flex items-center gap-2 text-sm text-muted-foreground", children: [_jsx(Clock, { className: "h-4 w-4" }), _jsx("span", { children: "On cooldown" })] })), _jsxs("div", { className: "flex gap-2", children: [!isEquipped && (_jsx(Button, { variant: "outline", size: "sm", className: "flex-1", onClick: onEquip, children: "Equip" })), isEquipped && (_jsxs(Button, { size: "sm", className: "flex-1", onClick: onUse, disabled: isOnCooldown, children: [_jsx(Zap, { className: "h-4 w-4 mr-1" }), "Use Power"] }))] })] })] }));
};
export default SuperpowerCard;
