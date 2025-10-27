import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../ui/card';
import './TournamentBracket.css';
const TournamentBracket = ({ bracket, currentRound }) => {
    const renderMatch = (match) => {
        return (_jsxs("div", { className: `match match-status-${match.status}`, children: [_jsx("div", { className: `player ${match.winner_id === match.player1_id ? 'winner' : ''}`, children: match.player1_id || 'TBD' }), _jsx("div", { className: "match-vs", children: "VS" }), _jsx("div", { className: `player ${match.winner_id === match.player2_id ? 'winner' : ''}`, children: match.player2_id || 'TBD' })] }, match.match_id));
    };
    const renderRound = (roundNumber) => {
        const roundMatches = bracket[`round_${roundNumber}`] || [];
        return (_jsxs("div", { className: "round", children: [_jsx("h4", { className: "round-title", children: roundNumber === Math.ceil(Math.log2(32)) ? 'Finals' :
                        roundNumber === Math.ceil(Math.log2(32)) - 1 ? 'Semi-Finals' :
                            roundNumber === Math.ceil(Math.log2(32)) - 2 ? 'Quarter-Finals' :
                                `Round ${roundNumber}` }), _jsx("div", { className: "matches", children: roundMatches.map((match) => renderMatch(match)) })] }, roundNumber));
    };
    const totalRounds = Object.keys(bracket).length;
    return (_jsxs(Card, { className: "tournament-bracket", children: [_jsx("h3", { children: "Tournament Bracket" }), _jsx("div", { className: "bracket-container", children: Array.from({ length: totalRounds }, (_, i) => i + 1).map(round => renderRound(round)) })] }));
};
export default TournamentBracket;
