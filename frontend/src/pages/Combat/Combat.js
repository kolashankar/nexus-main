import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CombatArena from '../../components/combat/CombatArena/CombatArena';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import combatService from '../../services/combat/combatService';
import tournamentsService from '../../services/tournaments/tournamentsService';
import TournamentCard from '../../components/tournaments/TournamentCard/TournamentCard';
import { Sword, Trophy, Users } from 'lucide-react';
import './Combat.css';
const Combat = () => {
    const navigate = useNavigate();
    const { battleId } = useParams();
    const [activeBattles, setActiveBattles] = useState([]);
    const [tournaments, setTournaments] = useState([]);
    const [loading, setLoading] = useState(true);
    // Get player ID from auth (mock for now)
    const playerId = 'current-player-id'; // TODO: Get from auth context
    useEffect(() => {
        loadData();
    }, []);
    const loadData = async () => {
        try {
            const [battlesData, tournamentsData] = await Promise.all([
                combatService.getActiveBattles(playerId),
                tournamentsService.getActiveTournaments()
            ]);
            setActiveBattles(battlesData.battles || []);
            setTournaments(tournamentsData || []);
        }
        catch (error) {
            console.error('Failed to load combat data:', error);
        }
        finally {
            setLoading(false);
        }
    };
    // If battleId is provided, show combat arena
    if (battleId) {
        return (_jsx("div", { className: "combat-page", children: _jsx(CombatArena, { battleId: battleId, playerId: playerId }) }));
    }
    const handleJoinArena = async (ranked) => {
        try {
            const result = await combatService.joinArenaQueue(playerId, ranked);
            if (result.battle_id) {
                navigate(`/combat/${result.battle_id}`);
            }
            else {
                alert('Searching for opponent...');
            }
        }
        catch (error) {
            alert(error.message || 'Failed to join arena');
        }
    };
    const handleRegisterTournament = async (tournamentId) => {
        try {
            await tournamentsService.registerForTournament(tournamentId, playerId);
            alert('Successfully registered!');
            loadData();
        }
        catch (error) {
            alert(error.message || 'Failed to register');
        }
    };
    return (_jsxs("div", { className: "combat-page", children: [_jsxs("div", { className: "combat-header", children: [_jsx("h1", { children: "Combat Arena" }), _jsx("p", { children: "Test your skills in PvP battles and tournaments" })] }), _jsxs(Tabs, { defaultValue: "arena", className: "combat-tabs", children: [_jsxs(TabsList, { children: [_jsxs(TabsTrigger, { value: "arena", children: [_jsx(Sword, { size: 16 }), " Arena"] }), _jsxs(TabsTrigger, { value: "duels", children: [_jsx(Users, { size: 16 }), " Duels"] }), _jsxs(TabsTrigger, { value: "tournaments", children: [_jsx(Trophy, { size: 16 }), " Tournaments"] })] }), _jsx(TabsContent, { value: "arena", children: _jsxs("div", { className: "arena-section", children: [_jsxs(Card, { className: "arena-card", children: [_jsx("h2", { children: "Arena Matchmaking" }), _jsx("p", { children: "Fight against players of similar skill level" }), _jsxs("div", { className: "arena-buttons", children: [_jsx(Button, { onClick: () => handleJoinArena(false), size: "lg", className: "casual-button", children: "Join Casual Match" }), _jsx(Button, { onClick: () => handleJoinArena(true), size: "lg", className: "ranked-button", children: "Join Ranked Match" })] })] }), activeBattles.length > 0 && (_jsxs(Card, { className: "active-battles-card", children: [_jsx("h3", { children: "Active Battles" }), _jsx("div", { className: "battles-list", children: activeBattles.map(battle => (_jsxs("div", { className: "battle-item", children: [_jsx("span", { children: battle.battle_type }), _jsx(Button, { onClick: () => navigate(`/combat/${battle.battle_id}`), size: "sm", children: "Continue" })] }, battle.battle_id))) })] }))] }) }), _jsx(TabsContent, { value: "duels", children: _jsxs(Card, { children: [_jsx("h2", { children: "Challenge Players" }), _jsx("p", { children: "Send duel challenges to other players" }), _jsx("div", { className: "duels-section", children: _jsx("p", { className: "coming-soon", children: "Coming soon: Player search and challenge system" }) })] }) }), _jsx(TabsContent, { value: "tournaments", children: _jsx("div", { className: "tournaments-grid", children: loading ? (_jsx("p", { children: "Loading tournaments..." })) : tournaments.length === 0 ? (_jsx(Card, { children: _jsx("p", { className: "no-tournaments", children: "No active tournaments" }) })) : (tournaments.map(tournament => (_jsx(TournamentCard, { tournament: tournament, onRegister: handleRegisterTournament, onView: (id) => navigate(`/tournaments/${id}`) }, tournament.tournament_id)))) }) })] })] }));
};
export default Combat;
