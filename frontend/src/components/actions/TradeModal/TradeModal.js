import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../../ui/dialog';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { useToast } from '../../../hooks/useToast';
import { actionsService } from '../../../services/actions/actionsService';
export const TradeModal = ({ open, onClose, onSuccess }) => {
    const [targetId, setTargetId] = useState('');
    const [offerAmount, setOfferAmount] = useState('');
    const [requestAmount, setRequestAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const { toast } = useToast();
    const handleTrade = async () => {
        if (!targetId || !offerAmount || !requestAmount) {
            toast({ title: 'Error', description: 'Please fill all fields', variant: 'destructive' });
            return;
        }
        setLoading(true);
        try {
            const result = await actionsService.trade(targetId, {
                credits: parseInt(offerAmount)
            }, {
                credits: parseInt(requestAmount)
            });
            toast({
                title: 'Success!',
                description: result.message,
                variant: 'default'
            });
            if (onSuccess)
                onSuccess();
            onClose();
        }
        catch (error) {
            toast({ title: 'Error', description: error.message, variant: 'destructive' });
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx(Dialog, { open: open, onOpenChange: onClose, children: _jsxs(DialogContent, { children: [_jsxs(DialogHeader, { children: [_jsx(DialogTitle, { children: "\uD83E\uDD1D Trade Proposal" }), _jsx(DialogDescription, { children: "Propose a trade with another player. Both parties must agree for the trade to complete." })] }), _jsxs("div", { className: "space-y-4 mt-4", children: [_jsx(Input, { placeholder: "Enter target player ID", value: targetId, onChange: (e) => setTargetId(e.target.value) }), _jsx(Input, { type: "number", placeholder: "Credits you offer", value: offerAmount, onChange: (e) => setOfferAmount(e.target.value) }), _jsx(Input, { type: "number", placeholder: "Credits you request", value: requestAmount, onChange: (e) => setRequestAmount(e.target.value) }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { onClick: handleTrade, disabled: loading, className: "flex-1", children: loading ? 'Proposing...' : 'Propose Trade' }), _jsx(Button, { onClick: onClose, variant: "outline", children: "Cancel" })] })] })] }) }));
};
