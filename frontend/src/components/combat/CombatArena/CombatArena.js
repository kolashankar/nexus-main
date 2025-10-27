import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import combatService from '../../../services/combat/combatService';
import ActionBar from '../ActionBar/ActionBar';
import HealthBar from '../HealthBar/HealthBar';
import { Card } from '../../ui/card';
import { Button } from '../../ui/button';
import { AlertCircle, Shield, Zap } from 'lucide-react';
import './CombatArena.css';
const CombatArena = ({ battleId, playerId }) => {
    const [battle, setBattle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [combatLog, setCombatLog] = useState([]);
    const [isMyTurn, setIsMyTurn] = useState(false);
    useEffect(() => {
        loadBattle();
        // Poll for updates every 2 seconds
        const interval = setInterval(loadBattle, 2000);
        return () => clearInterval(interval);
    }, [battleId]);
    useEffect(() => {
        if (battle) {
            setIsMyTurn(battle.active_participant_id === playerId);
        }
    }, [battle, playerId]);
    const loadBattle = async () => {
        try {
            const data = await combatService.getBattleState(battleId);
            setBattle(data);
            setLoading(false);
        }
        catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };
    const handleAction = async (actionType, targetId, abilityName) => {
        try {
            const result = await combatService.executeAction(battleId, playerId, actionType, targetId, abilityName);
            // Add to combat log
            setCombatLog(prev => [...prev, result.description]);
            // Reload battle state
            await loadBattle();
        }
        catch (err) {
            setError(err.message);
        }
    };
    const handleFlee = async () => {
        if (window.confirm('Are you sure you want to flee? This will count as a loss.')) {
            try {
                await combatService.fleeBattle(battleId, playerId);
                await loadBattle();
            }
            catch (err) {
                setError(err.message);
            }
        }
    };
    if (loading) {
        return (_jsx("div", { className: "combat-arena-loading", children: _jsx("div", { className: "spinner", children: "Loading battle..." }) }));
    }
    if (error) {
        return (_jsxs("div", { className: "combat-arena-error", children: [_jsx(AlertCircle, { className: "error-icon" }), _jsx("p", { children: error })] }));
    }
    if (!battle) {
        return _jsx("div", { children: "Battle not found" });
    }
    const player = battle.participants.find(p => p.player_id === playerId);
    const opponent = battle.participants.find(p => p.player_id !== playerId);
    if (!player || !opponent) {
        return _jsx("div", { children: "Invalid battle state" });
    }
    const isBattleOver = battle.status === 'completed';
    const isWinner = battle.winner_id === playerId;
    return (_jsxs("div", { className: "combat-arena", children: [_jsxs("div", { className: "battle-header", children: [_jsxs("h2", { className: "battle-title", children: [battle.battle_type.toUpperCase(), " - Turn ", battle.current_turn] }), _jsx("div", { className: "battle-status", children: isBattleOver ? (_jsx("span", { className: `status-badge ${isWinner ? 'winner' : 'loser'}`, children: isWinner ? '🏆 VICTORY!' : '💀 DEFEATED' })) : (_jsx("span", { className: `status-badge ${isMyTurn ? 'active' : 'waiting'}`, children: isMyTurn ? '⚡ YOUR TURN' : '⏳ OPPONENT\'S TURN' })) })] }), _jsxs("div", { className: "battle-arena", children: [_jsx("div", { className: "participant player-side", children: _jsxs(Card, { className: "participant-card", children: [_jsxs("div", { className: "participant-header", children: [_jsx("h3", { children: player.username }), _jsxs("span", { className: "ap-badge", children: [_jsx(Zap, { size: 16 }), " ", player.action_points, "/", player.max_action_points, " AP"] })] }), _jsx(HealthBar, { current: player.hp, max: player.max_hp, label: "HP" }), _jsxs("div", { className: "participant-stats", children: [_jsxs("div", { className: "stat", children: [_jsx(Shield, { size: 16 }), _jsxs("span", { children: ["ATK: ", player.combat_stats.attack] })] }), _jsxs("div", { className: "stat", children: [_jsx(Shield, { size: 16 }), _jsxs("span", { children: ["DEF: ", player.combat_stats.defense] })] })] }), player.status_effects.length > 0 && (_jsx("div", { className: "status-effects", children: player.status_effects.map((effect, i) => (_jsx("span", { className: "effect-badge", children: effect.type }, i))) }))] }) }), _jsx("div", { className: "vs-divider", children: _jsx("span", { className: "vs-text", children: "VS" }) }), _jsx("div", { className: "participant opponent-side", children: _jsxs(Card, { className: "participant-card", children: [_jsxs("div", { className: "participant-header", children: [_jsx("h3", { children: opponent.username }), _jsxs("span", { className: "ap-badge", children: [_jsx(Zap, { size: 16 }), " ", opponent.action_points, "/", opponent.max_action_points, " AP"] })] }), _jsx(HealthBar, { current: opponent.hp, max: opponent.max_hp, label: "HP" }), _jsxs("div", { className: "participant-stats", children: [_jsxs("div", { className: "stat", children: [_jsx(Shield, { size: 16 }), _jsxs("span", { children: ["ATK: ", opponent.combat_stats.attack] })] }), _jsxs("div", { className: "stat", children: [_jsx(Shield, { size: 16 }), _jsxs("span", { children: ["DEF: ", opponent.combat_stats.defense] })] })] }), opponent.status_effects.length > 0 && (_jsx("div", { className: "status-effects", children: opponent.status_effects.map((effect, i) => (_jsx("span", { className: "effect-badge", children: effect.type }, i))) }))] }) })] }), _jsxs(Card, { className: "combat-log", children: [_jsx("h4", { children: "Combat Log" }), _jsx("div", { className: "log-entries", children: combatLog.length === 0 ? (_jsx("p", { className: "log-empty", children: "Battle start! Prepare for combat..." })) : (combatLog.map((entry, i) => (_jsx("div", { className: "log-entry", children: entry }, i)))) })] }), !isBattleOver && isMyTurn && (_jsx(ActionBar, { participant: player, opponent: opponent, onAction: handleAction, onFlee: handleFlee })), isBattleOver && (_jsxs(Card, { className: "battle-results", children: [_jsx("h3", { children: isWinner ? '🏆 Victory!' : '💀 Defeat' }), battle.rewards && (_jsxs("div", { className: "rewards", children: [_jsx("h4", { children: "Rewards:" }), _jsx("ul", { children: Object.entries(battle.rewards).map(([key, value]) => (_jsxs("li", { children: [key, ": ", value] }, key))) })] })), _jsx(Button, { onClick: () => window.location.href = '/dashboard', children: "Return to Dashboard" })] }))] }));
};
export default CombatArena;
