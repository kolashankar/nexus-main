import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../ui/card';
import { Button } from '../../ui/button';
import { Trophy, Users, Calendar } from 'lucide-react';
import './TournamentCard.css';
const TournamentCard = ({ tournament, onRegister, onView, isRegistered = false }) => {
    const getStatusBadge = () => {
        switch (tournament.status) {
            case 'registration':
                return _jsx("span", { className: "status-badge registration", children: "Open for Registration" });
            case 'in_progress':
                return _jsx("span", { className: "status-badge in-progress", children: "In Progress" });
            case 'completed':
                return _jsx("span", { className: "status-badge completed", children: "Completed" });
            default:
                return null;
        }
    };
    return (_jsxs(Card, { className: "tournament-card", children: [_jsxs("div", { className: "tournament-header", children: [_jsx(Trophy, { className: "tournament-icon", size: 32 }), _jsxs("div", { children: [_jsx("h3", { children: tournament.name }), getStatusBadge()] })] }), _jsx("p", { className: "tournament-description", children: tournament.description }), _jsxs("div", { className: "tournament-info", children: [_jsxs("div", { className: "info-item", children: [_jsx(Users, { size: 16 }), _jsxs("span", { children: [tournament.participants.length, " / ", tournament.max_participants, " Players"] })] }), tournament.starts_at && (_jsxs("div", { className: "info-item", children: [_jsx(Calendar, { size: 16 }), _jsx("span", { children: new Date(tournament.starts_at).toLocaleString() })] }))] }), tournament.prize_pool && Object.keys(tournament.prize_pool).length > 0 && (_jsxs("div", { className: "prize-pool", children: [_jsx("h4", { children: "Prize Pool" }), _jsx("div", { className: "prizes", children: Object.entries(tournament.prize_pool).map(([place, prize]) => (_jsxs("div", { className: "prize-item", children: [_jsx("span", { className: "place", children: place }), _jsx("span", { className: "prize", children: prize })] }, place))) })] })), _jsxs("div", { className: "tournament-actions", children: [tournament.status === 'registration' && !isRegistered && (_jsx(Button, { onClick: () => onRegister(tournament.tournament_id), disabled: tournament.participants.length >= tournament.max_participants, className: "register-button", children: "Register Now" })), isRegistered && (_jsx("span", { className: "registered-badge", children: "\u2713 Registered" })), _jsx(Button, { onClick: () => onView(tournament.tournament_id), variant: "outline", children: "View Details" })] })] }));
};
export default TournamentCard;
