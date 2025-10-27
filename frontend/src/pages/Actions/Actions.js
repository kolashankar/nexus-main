import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { ActionButton } from '../../components/actions/ActionButton/ActionButton';
import { ActionHistory } from '../../components/actions/ActionHistory/ActionHistory';
import { HackModal } from '../../components/actions/HackModal/HackModal';
import { HelpModal } from '../../components/actions/HelpModal/HelpModal';
import { StealModal } from '../../components/actions/StealModal/StealModal';
import { DonateModal } from '../../components/actions/DonateModal/DonateModal';
import { TradeModal } from '../../components/actions/TradeModal/TradeModal';
export const Actions = () => {
    const [activeModal, setActiveModal] = useState(null);
    return (_jsxs("div", { className: "container mx-auto p-6 space-y-6", children: [_jsx("h1", { className: "text-3xl font-bold", children: "Game Actions" }), _jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Choose Your Action" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4", children: [_jsx(ActionButton, { icon: "\uD83D\uDD10", label: "Hack", description: "Infiltrate systems", onClick: () => setActiveModal('hack') }), _jsx(ActionButton, { icon: "\uD83E\uDD1D", label: "Help", description: "Assist others", onClick: () => setActiveModal('help') }), _jsx(ActionButton, { icon: "\uD83D\uDCB0", label: "Steal", description: "Take resources", onClick: () => setActiveModal('steal'), variant: "destructive" }), _jsx(ActionButton, { icon: "\uD83D\uDC9D", label: "Donate", description: "Give to others", onClick: () => setActiveModal('donate') }), _jsx(ActionButton, { icon: "\uD83E\uDD1D", label: "Trade", description: "Exchange goods", onClick: () => setActiveModal('trade'), variant: "outline" })] }) })] }), _jsx(ActionHistory, {}), _jsx(HackModal, { open: activeModal === 'hack', onClose: () => setActiveModal(null) }), _jsx(HelpModal, { open: activeModal === 'help', onClose: () => setActiveModal(null) }), _jsx(StealModal, { open: activeModal === 'steal', onClose: () => setActiveModal(null) }), _jsx(DonateModal, { open: activeModal === 'donate', onClose: () => setActiveModal(null) }), _jsx(TradeModal, { open: activeModal === 'trade', onClose: () => setActiveModal(null) })] }));
};
