import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../../ui/dialog';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { useToast } from '../../../hooks/useToast';
import { actionsService } from '../../../services/actions/actionsService';
export const StealModal = ({ open, onClose, onSuccess }) => {
    const [targetId, setTargetId] = useState('');
    const [loading, setLoading] = useState(false);
    const { toast } = useToast();
    const handleSteal = async () => {
        if (!targetId) {
            toast({ title: 'Error', description: 'Please enter a target ID', variant: 'destructive' });
            return;
        }
        setLoading(true);
        try {
            const result = await actionsService.steal(targetId);
            toast({
                title: result.success ? 'Success!' : 'Caught!',
                description: result.message,
                variant: result.success ? 'default' : 'destructive'
            });
            if (result.success && onSuccess)
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
    return (_jsx(Dialog, { open: open, onOpenChange: onClose, children: _jsxs(DialogContent, { children: [_jsxs(DialogHeader, { children: [_jsx(DialogTitle, { children: "\uD83D\uDCB0 Steal from Player" }), _jsx(DialogDescription, { children: "Attempt to steal credits from another player. Risky! Success depends on your stealth vs their perception." })] }), _jsxs("div", { className: "space-y-4 mt-4", children: [_jsx(Input, { placeholder: "Enter target player ID", value: targetId, onChange: (e) => setTargetId(e.target.value) }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { onClick: handleSteal, disabled: loading, variant: "destructive", className: "flex-1", children: loading ? 'Stealing...' : 'Attempt Steal' }), _jsx(Button, { onClick: onClose, variant: "outline", children: "Cancel" })] })] })] }) }));
};
