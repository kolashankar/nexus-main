import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Button } from '../../ui/button';
import { Sword, Shield, Zap, Flag } from 'lucide-react';
import AbilityMenu from '../AbilityMenu/AbilityMenu';
import './ActionBar.css';
const ActionBar = ({ participant, opponent, onAction, onFlee }) => {
    const [showAbilities, setShowAbilities] = useState(false);
    const handleAttack = () => {
        onAction('attack', opponent.player_id);
    };
    const handleDefend = () => {
        onAction('defend');
    };
    const handleAbility = (abilityName) => {
        onAction('use_power', opponent.player_id, abilityName);
        setShowAbilities(false);
    };
    const canAct = (apCost) => {
        return participant.action_points >= apCost;
    };
    return (_jsxs("div", { className: "action-bar", children: [_jsxs("div", { className: "action-bar-header", children: [_jsx("h4", { children: "Choose Your Action" }), _jsxs("span", { className: "ap-display", children: [_jsx(Zap, { size: 16 }), " ", participant.action_points, "/", participant.max_action_points, " AP"] })] }), _jsxs("div", { className: "action-buttons", children: [_jsxs(Button, { onClick: handleAttack, disabled: !canAct(1), className: "action-button attack-button", size: "lg", children: [_jsx(Sword, { size: 20 }), _jsxs("div", { children: [_jsx("div", { className: "action-name", children: "Attack" }), _jsx("div", { className: "action-cost", children: "1 AP" })] })] }), _jsxs(Button, { onClick: handleDefend, disabled: !canAct(1), className: "action-button defend-button", size: "lg", children: [_jsx(Shield, { size: 20 }), _jsxs("div", { children: [_jsx("div", { className: "action-name", children: "Defend" }), _jsx("div", { className: "action-cost", children: "1 AP" })] })] }), _jsxs(Button, { onClick: () => setShowAbilities(!showAbilities), disabled: !canAct(2) || participant.equipped_abilities.length === 0, className: "action-button ability-button", size: "lg", children: [_jsx(Zap, { size: 20 }), _jsxs("div", { children: [_jsx("div", { className: "action-name", children: "Abilities" }), _jsx("div", { className: "action-cost", children: "Varies" })] })] }), _jsxs(Button, { onClick: onFlee, disabled: !canAct(3), className: "action-button flee-button", size: "lg", variant: "outline", children: [_jsx(Flag, { size: 20 }), _jsxs("div", { children: [_jsx("div", { className: "action-name", children: "Flee" }), _jsx("div", { className: "action-cost", children: "3 AP" })] })] })] }), showAbilities && (_jsx(AbilityMenu, { abilities: participant.equipped_abilities, onSelect: handleAbility, onClose: () => setShowAbilities(false), availableAP: participant.action_points }))] }));
};
export default ActionBar;
