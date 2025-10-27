import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card, CardContent, CardHeader } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Button } from '../../ui/button';
import { Progress } from '../../ui/progress';
import { Lock, Check, Crown, Gift } from 'lucide-react';
const BattlePassTrack = ({ tiers, currentTier, currentXp, hasPremium, claimedFree, claimedPremium, onClaimRewards, onPurchasePremium }) => {
    const [selectedTier, setSelectedTier] = useState(null);
    const getRarityColor = (rarity) => {
        const colors = {
            common: 'bg-gray-500',
            rare: 'bg-blue-500',
            epic: 'bg-purple-500',
            legendary: 'bg-yellow-500'
        };
        return colors[rarity] || 'bg-gray-500';
    };
    const calculateProgress = (tierIndex) => {
        if (tierIndex === 0)
            return 100;
        if (tierIndex > currentTier)
            return 0;
        if (tierIndex < currentTier)
            return 100;
        // Current tier - calculate partial progress
        const prevTier = tiers[tierIndex - 1];
        const currentTierData = tiers[tierIndex];
        const xpForThisTier = currentTierData.xp_required - prevTier.xp_required;
        const xpInThisTier = currentXp - prevTier.xp_required;
        return (xpInThisTier / xpForThisTier) * 100;
    };
    const canClaimRewards = (tier) => {
        return tier <= currentTier && !claimedFree.includes(tier);
    };
    const renderReward = (reward, index) => (_jsxs("div", { className: "flex flex-col items-center p-2 rounded-lg bg-secondary/20 hover:bg-secondary/40 transition-colors", children: [_jsx("div", { className: `w-12 h-12 rounded-lg ${getRarityColor(reward.rarity)} flex items-center justify-center mb-2`, children: _jsx(Gift, { className: "h-6 w-6 text-white" }) }), _jsx("p", { className: "text-xs text-center font-medium", children: reward.name }), reward.amount > 1 && (_jsxs("span", { className: "text-xs text-muted-foreground", children: ["x", reward.amount] }))] }, index));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold", children: "Battle Pass" }), _jsxs("p", { className: "text-sm text-muted-foreground", children: ["Tier ", currentTier, " / ", tiers.length] })] }), !hasPremium && (_jsxs(Button, { onClick: onPurchasePremium, className: "gap-2", children: [_jsx(Crown, { className: "h-4 w-4" }), "Upgrade to Premium"] }))] }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex justify-between text-sm", children: [_jsx("span", { children: "Overall Progress" }), _jsxs("span", { className: "font-bold", children: [currentXp.toLocaleString(), " XP"] })] }), _jsx(Progress, { value: (currentTier / tiers.length) * 100, className: "h-3" })] }) }) }), _jsx("div", { className: "space-y-4", children: tiers.map((tier, index) => {
                    const isUnlocked = tier.tier <= currentTier;
                    const freeClaimed = claimedFree.includes(tier.tier);
                    const premiumClaimed = claimedPremium.includes(tier.tier);
                    const progress = calculateProgress(index);
                    return (_jsxs(Card, { className: `relative ${isUnlocked ? 'border-primary/50' : 'opacity-50'}`, children: [_jsx(CardHeader, { className: "pb-3", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs(Badge, { variant: isUnlocked ? "default" : "secondary", children: ["Tier ", tier.tier] }), _jsxs("span", { className: "text-sm text-muted-foreground", children: [tier.xp_required.toLocaleString(), " XP"] })] }), !isUnlocked && _jsx(Lock, { className: "h-5 w-5 text-muted-foreground" }), isUnlocked && canClaimRewards(tier.tier) && (_jsxs(Button, { onClick: () => onClaimRewards(tier.tier), size: "sm", className: "gap-2", children: [_jsx(Gift, { className: "h-4 w-4" }), "Claim"] })), freeClaimed && (_jsx(Check, { className: "h-5 w-5 text-green-500" }))] }) }), _jsxs(CardContent, { children: [tier.tier === currentTier && (_jsx("div", { className: "mb-4", children: _jsx(Progress, { value: progress, className: "h-2" }) })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center gap-2 mb-2", children: [_jsx("h4", { className: "text-sm font-semibold", children: "Free Rewards" }), freeClaimed && (_jsx(Badge, { variant: "outline", className: "text-xs", children: "Claimed" }))] }), _jsx("div", { className: "grid grid-cols-3 gap-2", children: tier.free_rewards.map((reward, idx) => renderReward(reward, idx)) })] }), _jsxs("div", { className: "space-y-2 relative", children: [_jsxs("div", { className: "flex items-center gap-2 mb-2", children: [_jsx(Crown, { className: "h-4 w-4 text-yellow-500" }), _jsx("h4", { className: "text-sm font-semibold", children: "Premium Rewards" }), premiumClaimed && (_jsx(Badge, { variant: "outline", className: "text-xs", children: "Claimed" }))] }), !hasPremium && (_jsx("div", { className: "absolute inset-0 bg-black/50 backdrop-blur-sm rounded-lg flex items-center justify-center", children: _jsx(Lock, { className: "h-8 w-8 text-white" }) })), _jsx("div", { className: "grid grid-cols-3 gap-2", children: tier.premium_rewards.map((reward, idx) => renderReward(reward, idx)) })] })] })] })] }, tier.tier));
                }) })] }));
};
export default BattlePassTrack;
