import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { VisibilityToggle } from './VisibilityToggle';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { usePrivacy } from '../../../hooks/usePrivacy';
export const PrivacySettings = () => {
    const { settings, loading, updateSettings, changeTier } = usePrivacy();
    if (loading || !settings) {
        return _jsx("div", { children: "Loading privacy settings..." });
    }
    const handleToggle = async (key, value) => {
        await updateSettings({ [key]: value });
    };
    const handleTierChange = async (tier) => {
        await changeTier(tier);
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "\uD83D\uDD12 Privacy Settings" }) }), _jsxs(CardContent, { className: "space-y-6", children: [_jsxs("div", { children: [_jsx("label", { className: "text-sm font-semibold mb-2 block", children: "Privacy Tier" }), _jsxs(Select, { value: settings.privacy_tier, onValueChange: handleTierChange, children: [_jsx(SelectTrigger, { children: _jsx(SelectValue, {}) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "public", children: "Public (Free)" }), _jsx(SelectItem, { value: "selective", children: "Selective (Small cost)" }), _jsx(SelectItem, { value: "private", children: "Private (Moderate cost)" }), _jsx(SelectItem, { value: "ghost", children: "Ghost (High cost)" }), _jsx(SelectItem, { value: "phantom", children: "Phantom (Very high cost)" })] })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("h3", { className: "text-sm font-semibold", children: "Visible Information" }), _jsx(VisibilityToggle, { label: "Cash Amount", checked: settings.cash, onChange: (v) => handleToggle('cash', v) }), _jsx(VisibilityToggle, { label: "Economic Class", checked: settings.economic_class, onChange: (v) => handleToggle('economic_class', v) }), _jsx(VisibilityToggle, { label: "Moral Class", checked: settings.moral_class, onChange: (v) => handleToggle('moral_class', v) }), _jsx(VisibilityToggle, { label: "Superpowers", checked: settings.superpowers, onChange: (v) => handleToggle('superpowers', v) }), _jsx(VisibilityToggle, { label: "Karma Score", checked: settings.karma_score, onChange: (v) => handleToggle('karma_score', v) }), _jsx(VisibilityToggle, { label: "Guild Membership", checked: settings.guild, onChange: (v) => handleToggle('guild', v) }), _jsx(VisibilityToggle, { label: "Location", checked: settings.location, onChange: (v) => handleToggle('location', v) })] })] })] }));
};
