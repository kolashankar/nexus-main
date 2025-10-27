import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../../ui/dialog';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { useToast } from '../../../hooks/useToast';
import { actionsService } from '../../../services/actions/actionsService';
export const DonateModal = ({ open, onClose, onSuccess }) => {
    const [targetId, setTargetId] = useState('');
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const { toast } = useToast();
    const handleDonate = async () => {
        if (!targetId || !amount) {
            toast({ title: 'Error', description: 'Please fill all fields', variant: 'destructive' });
            return;
        }
        const donationAmount = parseInt(amount);
        if (isNaN(donationAmount) || donationAmount <= 0) {
            toast({ title: 'Error', description: 'Invalid amount', variant: 'destructive' });
            return;
        }
        setLoading(true);
        try {
            const result = await actionsService.donate(targetId, donationAmount);
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
    return (_jsx(Dialog, { open: open, onOpenChange: onClose, children: _jsxs(DialogContent, { children: [_jsxs(DialogHeader, { children: [_jsx(DialogTitle, { children: "\uD83D\uDC9D Donate Credits" }), _jsx(DialogDescription, { children: "Make a charitable donation to another player. This will significantly boost your karma." })] }), _jsxs("div", { className: "space-y-4 mt-4", children: [_jsx(Input, { placeholder: "Enter target player ID", value: targetId, onChange: (e) => setTargetId(e.target.value) }), _jsx(Input, { type: "number", placeholder: "Amount to donate", value: amount, onChange: (e) => setAmount(e.target.value) }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { onClick: handleDonate, disabled: loading, className: "flex-1", children: loading ? 'Donating...' : 'Donate' }), _jsx(Button, { onClick: onClose, variant: "outline", children: "Cancel" })] })] })] }) }));
};
