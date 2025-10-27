import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../ui/card';
import { Button } from '../../ui/button';
import { X, Zap } from 'lucide-react';
import './AbilityMenu.css';
// Mock ability data - In real app, fetch from API
const ABILITY_DATA = {
    'emp_blast': { name: 'EMP Blast', cost: 2, description: 'Disables enemy robots' },
    'mercy': { name: 'Mercy', cost: 2, description: 'Spare enemy, gain karma' },
    'berserker_rage': { name: 'Berserker Rage', cost: 3, description: 'Double damage, no defense' },
    'tactical_advantage': { name: 'Tactical Advantage', cost: 2, description: 'Gain +2 AP' },
    'inner_peace': { name: 'Inner Peace', cost: 2, description: 'Restore 30% HP' },
    'shadow_strike': { name: 'Shadow Strike', cost: 3, description: 'Guaranteed critical' },
    'power_strike': { name: 'Power Strike', cost: 2, description: 'Triple damage attack' },
};
const AbilityMenu = ({ abilities, onSelect, onClose, availableAP }) => {
    return (_jsx("div", { className: "ability-menu-overlay", children: _jsxs(Card, { className: "ability-menu", children: [_jsxs("div", { className: "ability-menu-header", children: [_jsxs("h4", { children: [_jsx(Zap, { size: 20 }), " Select Ability"] }), _jsx(Button, { onClick: onClose, variant: "ghost", size: "icon", children: _jsx(X, { size: 20 }) })] }), _jsx("div", { className: "ability-list", children: abilities.length === 0 ? (_jsx("p", { className: "no-abilities", children: "No abilities equipped" })) : (abilities.map((abilityId) => {
                        const ability = ABILITY_DATA[abilityId] || {
                            name: abilityId,
                            cost: 2,
                            description: 'Unknown ability'
                        };
                        const canUse = availableAP >= ability.cost;
                        return (_jsxs("div", { className: `ability-item ${!canUse ? 'disabled' : ''}`, children: [_jsxs("div", { className: "ability-info", children: [_jsx("h5", { children: ability.name }), _jsx("p", { children: ability.description })] }), _jsxs("div", { className: "ability-actions", children: [_jsxs("span", { className: "ability-cost", children: [_jsx(Zap, { size: 14 }), " ", ability.cost, " AP"] }), _jsx(Button, { onClick: () => onSelect(abilityId), disabled: !canUse, size: "sm", children: "Use" })] })] }, abilityId));
                    })) })] }) }));
};
export default AbilityMenu;
