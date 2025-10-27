import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent } from '@/components/ui/dialog';
import HackActionModal from '../modals/HackActionModal';
import HelpActionModal from '../modals/HelpActionModal';
import StealActionModal from '../modals/StealActionModal';
import DonateActionModal from '../modals/DonateActionModal';
import TradeActionModal from '../modals/TradeActionModal';
const ActionsDashboard = () => {
    const [selectedAction, setSelectedAction] = useState(null);
    const actions = [
        {
            id: 'hack',
            name: 'Hack',
            description: 'Hack another player to steal credits',
            icon: '💻',
            color: 'bg-blue-500 hover:bg-blue-600',
            karmaEffect: 'Negative'
        },
        {
            id: 'help',
            name: 'Help',
            description: 'Help another player with credits',
            icon: '❤️',
            color: 'bg-green-500 hover:bg-green-600',
            karmaEffect: 'Positive'
        },
        {
            id: 'steal',
            name: 'Steal',
            description: 'Steal credits from another player',
            icon: '👿',
            color: 'bg-red-500 hover:bg-red-600',
            karmaEffect: 'Very Negative'
        },
        {
            id: 'donate',
            name: 'Donate',
            description: 'Donate credits to another player',
            icon: '🌟',
            color: 'bg-yellow-500 hover:bg-yellow-600',
            karmaEffect: 'Very Positive'
        },
        {
            id: 'trade',
            name: 'Trade',
            description: 'Trade credits with another player',
            icon: '🤝',
            color: 'bg-purple-500 hover:bg-purple-600',
            karmaEffect: 'Neutral'
        }
    ];
    const renderActionModal = () => {
        switch (selectedAction) {
            case 'hack':
                return _jsx(HackActionModal, { onClose: () => setSelectedAction(null) });
            case 'help':
                return _jsx(HelpActionModal, { onClose: () => setSelectedAction(null) });
            case 'steal':
                return _jsx(StealActionModal, { onClose: () => setSelectedAction(null) });
            case 'donate':
                return _jsx(DonateActionModal, { onClose: () => setSelectedAction(null) });
            case 'trade':
                return _jsx(TradeActionModal, { onClose: () => setSelectedAction(null) });
            default:
                return null;
        }
    };
    return (_jsxs("div", { className: "w-full", children: [_jsxs("div", { className: "mb-6", children: [_jsx("h2", { className: "text-3xl font-bold text-gray-900 mb-2", children: "Game Actions" }), _jsx("p", { className: "text-gray-600", children: "Choose your actions wisely - they affect your karma, traits, and reputation" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: actions.map((action) => (_jsxs(Card, { className: "cursor-pointer hover:shadow-xl transition-all transform hover:-translate-y-1", onClick: () => setSelectedAction(action.id), children: [_jsx(CardHeader, { className: `${action.color} text-white`, children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-4xl", children: action.icon }), _jsx(CardTitle, { className: "text-2xl", children: action.name })] }) }), _jsxs(CardContent, { className: "p-4", children: [_jsx("p", { className: "text-gray-700 mb-3", children: action.description }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-gray-600", children: "Karma Effect:" }), _jsx("span", { className: `text-sm font-bold ${action.karmaEffect.includes('Positive')
                                                ? 'text-green-600'
                                                : action.karmaEffect.includes('Negative')
                                                    ? 'text-red-600'
                                                    : 'text-gray-600'}`, children: action.karmaEffect })] })] })] }, action.id))) }), selectedAction && (_jsx(Dialog, { open: !!selectedAction, onOpenChange: () => setSelectedAction(null), children: _jsx(DialogContent, { className: "max-w-2xl", children: renderActionModal() }) }))] }));
};
export default ActionsDashboard;
