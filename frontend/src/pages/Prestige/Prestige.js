import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Progress } from '../../components/ui/progress';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '../../components/ui/alert-dialog';
import prestigeService from '../../services/prestige/prestigeService';
import { toast } from 'sonner';
import { Crown, Sparkles } from 'lucide-react';
const Prestige = () => {
    const [prestige, setPrestige] = useState(null);
    const [eligibility, setEligibility] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchPrestige();
        checkEligibility();
    }, []);
    const fetchPrestige = async () => {
        try {
            const data = await prestigeService.getPrestige();
            setPrestige(data);
        }
        catch (error) {
            console.error('Failed to fetch prestige:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const checkEligibility = async () => {
        try {
            const data = await prestigeService.checkPrestigeEligibility();
            setEligibility(data);
        }
        catch (error) {
            console.error('Failed to check eligibility:', error);
        }
    };
    const handlePrestige = async () => {
        try {
            const result = await prestigeService.performPrestige();
            toast.success(result.message);
            fetchPrestige();
            checkEligibility();
        }
        catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to prestige');
        }
    };
    if (loading) {
        return _jsx("div", { className: "flex justify-center items-center h-64", children: "Loading prestige..." });
    }
    return (_jsx("div", { className: "container mx-auto py-6", children: _jsxs(Card, { className: "bg-gradient-to-br from-purple-900/20 to-blue-900/20", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs(CardTitle, { className: "text-3xl flex items-center gap-2", children: [_jsx(Crown, { className: "h-8 w-8 text-yellow-500" }), "Prestige System"] }), prestige && (_jsxs(Badge, { variant: "secondary", className: "text-lg px-4 py-2", children: ["Level ", prestige.current_prestige_level] }))] }) }), _jsxs(CardContent, { className: "space-y-6", children: [prestige && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Prestige Level" }), _jsxs("p", { className: "text-3xl font-bold", children: [prestige.current_prestige_level, "/10"] })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Total Prestiges" }), _jsx("p", { className: "text-3xl font-bold", children: prestige.total_prestiges })] }) }) }), _jsx(Card, { children: _jsx(CardContent, { className: "pt-6", children: _jsxs("div", { className: "text-center", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Prestige Points" }), _jsx("p", { className: "text-3xl font-bold", children: prestige.prestige_points })] }) }) })] })), eligibility && (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Prestige Requirements" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { children: "Level 100" }), _jsxs(Badge, { variant: eligibility.current_level >= 100 ? 'default' : 'secondary', children: [eligibility.current_level, "/100"] })] }), _jsx(Progress, { value: (eligibility.current_level / 100) * 100 })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { children: "Karma" }), _jsxs(Badge, { variant: eligibility.current_karma >= 1000 ? 'default' : 'secondary', children: [eligibility.current_karma, "/1000"] })] }), _jsx(Progress, { value: (eligibility.current_karma / 1000) * 100 })] }), eligibility.requirements.achievements > 0 && (_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { children: "Achievements" }), _jsxs(Badge, { variant: eligibility.current_achievements >= eligibility.requirements.achievements
                                                                ? 'default'
                                                                : 'secondary', children: [eligibility.current_achievements, "/", eligibility.requirements.achievements] })] }), _jsx(Progress, { value: (eligibility.current_achievements / eligibility.requirements.achievements) *
                                                        100 })] })), _jsx("div", { className: "pt-4", children: eligibility.eligible ? (_jsxs(AlertDialog, { children: [_jsx(AlertDialogTrigger, { asChild: true, children: _jsxs(Button, { className: "w-full", size: "lg", children: [_jsx(Sparkles, { className: "mr-2 h-5 w-5" }), "Prestige Now"] }) }), _jsxs(AlertDialogContent, { children: [_jsxs(AlertDialogHeader, { children: [_jsx(AlertDialogTitle, { children: "Are you sure?" }), _jsx(AlertDialogDescription, { children: "Prestiging will reset your level and traits, but you'll keep 10% of your trait progress and gain permanent bonuses. This action cannot be undone." })] }), _jsxs(AlertDialogFooter, { children: [_jsx(AlertDialogCancel, { children: "Cancel" }), _jsx(AlertDialogAction, { onClick: handlePrestige, children: "Prestige" })] })] })] })) : (_jsx(Button, { className: "w-full", size: "lg", disabled: true, children: eligibility.message })) })] })] })), prestige && Object.keys(prestige.permanent_bonuses).length > 0 && (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Permanent Bonuses" }) }), _jsx(CardContent, { children: _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: Object.entries(prestige.permanent_bonuses).map(([bonus, value]) => (_jsxs("div", { className: "flex items-center justify-between p-3 bg-primary/10 rounded-lg", children: [_jsx("span", { className: "capitalize", children: bonus.replace('_', ' ') }), _jsxs(Badge, { variant: "secondary", children: ["x", value.toFixed(2)] })] }, bonus))) }) })] }))] })] }) }));
};
export default Prestige;