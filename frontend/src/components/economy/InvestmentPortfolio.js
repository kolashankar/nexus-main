import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { TrendingUp, PieChart, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';
export const InvestmentPortfolio = () => {
    const [portfolio, setPortfolio] = useState(null);
    const [opportunities, setOpportunities] = useState([]);
    const [activeTab, setActiveTab] = useState('portfolio');
    useEffect(() => {
        fetchPortfolio();
        fetchOpportunities();
    }, []);
    const fetchPortfolio = async () => {
        try {
            const response = await fetch('/api/investments/portfolio', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setPortfolio(data);
        }
        catch (error) {
            console.error('Failed to fetch portfolio:', error);
        }
    };
    const fetchOpportunities = async () => {
        try {
            const response = await fetch('/api/investments/opportunities', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setOpportunities(data.opportunities || []);
        }
        catch (error) {
            console.error('Failed to fetch opportunities:', error);
        }
    };
    const makeInvestment = async (investmentId, amount) => {
        try {
            const response = await fetch('/api/investments/invest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ investment_id: investmentId, amount })
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Investment successful!', {
                    description: `Invested in ${data.investment_name}`
                });
                fetchPortfolio();
            }
            else {
                toast.error('Investment failed', {
                    description: data.error
                });
            }
        }
        catch (error) {
            toast.error('Investment failed');
        }
    };
    const getRiskColor = (risk) => {
        const colors = {
            low: 'bg-green-500',
            medium: 'bg-yellow-500',
            high: 'bg-orange-500',
            very_high: 'bg-red-500'
        };
        return colors[risk] || 'bg-gray-500';
    };
    const formatCurrency = (value) => {
        return new Intl.NumberFormat().format(value);
    };
    return (_jsxs("div", { className: "p-6 space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(PieChart, { className: "h-8 w-8" }), "Investment Portfolio"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Grow your wealth through strategic investments" })] }) }), portfolio && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-1", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Total Invested" }), _jsx("p", { className: "text-2xl font-bold", children: formatCurrency(portfolio.total_invested) })] }) }), _jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-1", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Current Value" }), _jsx("p", { className: "text-2xl font-bold", children: formatCurrency(portfolio.current_value) })] }) }), _jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-1", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "Profit/Loss" }), _jsxs("p", { className: `text-2xl font-bold ${portfolio.total_profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`, children: [portfolio.total_profit_loss >= 0 ? '+' : '', formatCurrency(portfolio.total_profit_loss)] })] }) }), _jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-1", children: [_jsx("p", { className: "text-sm text-muted-foreground", children: "ROI" }), _jsxs("p", { className: `text-2xl font-bold ${portfolio.roi_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`, children: [portfolio.roi_percentage >= 0 ? '+' : '', portfolio.roi_percentage.toFixed(2), "%"] })] }) })] })), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "portfolio", children: "My Investments" }), _jsx(TabsTrigger, { value: "opportunities", children: "Opportunities" })] }), _jsx(TabsContent, { value: "portfolio", className: "space-y-4", children: portfolio && portfolio.investments.length > 0 ? (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: portfolio.investments.map(investment => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold", children: investment.name }), _jsxs(Badge, { className: getRiskColor(investment.risk_level), children: [investment.risk_level, " risk"] })] }), _jsx(TrendingUp, { className: "h-5 w-5 text-muted-foreground" })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-sm", children: [_jsxs("div", { children: [_jsx("p", { className: "text-muted-foreground", children: "Invested" }), _jsx("p", { className: "font-medium", children: formatCurrency(investment.amount_invested) })] }), _jsxs("div", { children: [_jsx("p", { className: "text-muted-foreground", children: "Current" }), _jsx("p", { className: "font-medium", children: formatCurrency(investment.current_value) })] }), _jsxs("div", { children: [_jsx("p", { className: "text-muted-foreground", children: "P/L" }), _jsxs("p", { className: `font-medium ${investment.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`, children: [investment.profit_loss >= 0 ? '+' : '', formatCurrency(investment.profit_loss)] })] }), _jsxs("div", { children: [_jsx("p", { className: "text-muted-foreground", children: "Return" }), _jsxs("p", { className: `font-medium ${investment.profit_loss_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`, children: [investment.profit_loss_percentage >= 0 ? '+' : '', investment.profit_loss_percentage.toFixed(2), "%"] })] })] }), _jsx(Button, { variant: "outline", className: "w-full", size: "sm", children: "Withdraw" })] }) }, investment.id))) })) : (_jsxs(Card, { className: "p-8 text-center", children: [_jsx(PieChart, { className: "h-12 w-12 mx-auto text-muted-foreground mb-4" }), _jsx("p", { className: "text-muted-foreground", children: "No active investments" }), _jsx(Button, { className: "mt-4", onClick: () => setActiveTab('opportunities'), children: "Browse Opportunities" })] })) }), _jsx(TabsContent, { value: "opportunities", className: "space-y-4", children: _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: opportunities.map(opp => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold", children: opp.name }), _jsxs(Badge, { className: getRiskColor(opp.risk_level), children: [opp.risk_level, " risk"] })] }), _jsx(AlertTriangle, { className: "h-5 w-5 text-yellow-500" })] }), _jsx("p", { className: "text-sm text-muted-foreground", children: opp.description }), _jsxs("div", { className: "space-y-2 text-sm", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Min. Investment:" }), _jsx("span", { className: "font-medium", children: formatCurrency(opp.min_investment) })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Expected Return:" }), _jsxs("span", { className: "font-medium text-green-600", children: ["+", opp.expected_return, "%"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Duration:" }), _jsxs("span", { className: "font-medium", children: [opp.duration_days, " days"] })] })] }), _jsx(Button, { className: "w-full", onClick: () => makeInvestment(opp.id, opp.min_investment), children: "Invest" })] }) }, opp.id))) }) })] })] }));
};