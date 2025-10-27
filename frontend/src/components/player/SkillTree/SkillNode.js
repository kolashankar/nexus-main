import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Button } from '../../ui/button';
import { Lock, Unlock, Star } from 'lucide-react';
const SkillNode = ({ node, onUnlock, canUnlock }) => {
    const isUnlocked = node.unlocked;
    const isMilestone = node.node_id % 5 === 0;
    return (_jsx("div", { className: "relative", children: _jsxs(Button, { variant: isUnlocked ? 'default' : 'outline', size: "lg", className: `w-full h-24 flex flex-col items-center justify-center gap-2 ${isMilestone ? 'border-2 border-yellow-500' : ''}`, onClick: onUnlock, disabled: isUnlocked || !canUnlock, children: [isUnlocked ? (_jsx(Unlock, { className: "h-6 w-6" })) : (_jsx(Lock, { className: "h-6 w-6 text-muted-foreground" })), _jsxs("span", { className: "text-sm font-semibold", children: ["Node ", node.node_id] }), isMilestone && _jsx(Star, { className: "h-4 w-4 text-yellow-500 absolute top-1 right-1" }), node.level > 0 && (_jsxs("span", { className: "text-xs text-muted-foreground", children: ["Lvl ", node.level] }))] }) }));
};
export default SkillNode;
