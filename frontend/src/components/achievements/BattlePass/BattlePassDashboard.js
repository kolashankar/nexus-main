import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Alert, AlertDescription } from '../../ui/alert';
import { Trophy, Calendar, Users } from 'lucide-react';
import { useBattlePass } from '../../../hooks/useBattlePass';
import BattlePassTrack from './BattlePassTrack';
import { toast } from 'sonner';
const BattlePassDashboard = () => {
    const { battlePass, progress, loading, error, claimRewards, purchasePremium, refreshProgress } = useBattlePass();
    useEffect(() => {
        refreshProgress();
    }, []);
    const handleClaimRewards = async (tier) => {
        try {
            const result = await claimRewards(tier);
            toast.success(`Claimed rewards for Tier ${tier}!`, {
                description: `${result.rewards_claimed.length} rewards added to your inventory`
            });
            await refreshProgress();
        }
        catch (error) {
            toast.error('Failed to claim rewards', {
                description: error.message || 'Please try again'
            });
        }
    };
    const handlePurchasePremium = async () => {
        try {
            await purchasePremium();
            toast.success('Premium Battle Pass activated!', {
                description: 'You now have access to all premium rewards'
            });
            await refreshProgress();
        }
        catch (error) {
            toast.error('Failed to purchase premium', {
                description: error.message || 'Please try again'
            });
        }
    };
    const calculateDaysRemaining = () => {
        if (!battlePass)
            return 0;
        const end = new Date(battlePass.end_date);
        const now = new Date();
        const diff = end.getTime() - now.getTime();
        return Math.ceil(diff / (1000 * 60 * 60 * 24));
    };
    if (loading) {
        return (_jsx("div", { className: "flex items-center justify-center py-12", children: _jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary" }) }));
    }
    if (error || !battlePass || !progress) {
        return (_jsx(Alert, { variant: "destructive", children: _jsx(AlertDescription, { children: error || 'No active battle pass found. Check back later!' }) }));
    }
    const daysRemaining = calculateDaysRemaining();
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs(Card, { children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-sm font-medium text-muted-foreground", children: "Current Tier" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Trophy, { className: "h-8 w-8 text-primary" }), _jsx("span", { className: "text-3xl font-bold", children: progress.current_tier }), _jsxs("span", { className: "text-muted-foreground", children: ["/ ", battlePass.total_tiers] })] }) })] }), _jsxs(Card, { children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-sm font-medium text-muted-foreground", children: "Time Remaining" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Calendar, { className: "h-8 w-8 text-primary" }), _jsx("span", { className: "text-3xl font-bold", children: daysRemaining }), _jsx("span", { className: "text-muted-foreground", children: "days" })] }) })] }), _jsxs(Card, { children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-sm font-medium text-muted-foreground", children: "Total XP Earned" }) }), _jsx(CardContent, { children: _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Users, { className: "h-8 w-8 text-primary" }), _jsx("span", { className: "text-3xl font-bold", children: progress.total_xp_earned.toLocaleString() })] }) })] })] }), _jsx(BattlePassTrack, { tiers: battlePass.tiers, currentTier: progress.current_tier, currentXp: progress.current_xp, hasPremium: progress.has_premium, claimedFree: progress.claimed_free_rewards, claimedPremium: progress.claimed_premium_rewards, onClaimRewards: handleClaimRewards, onPurchasePremium: handlePurchasePremium })] }));
};
export default BattlePassDashboard;