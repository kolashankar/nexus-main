import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import guildsService from '../../services/guilds/guildsService';
import { useAuth } from '../../hooks/useAuth';
const Territories = () => {
    const { user } = useAuth();
    const [territories, setTerritories] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadTerritories();
    }, []);
    const loadTerritories = async () => {
        try {
            const data = await guildsService.getAllTerritories();
            setTerritories(data);
        }
        catch (error) {
            console.error('Failed to load territories:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const handleAttack = async (territoryId) => {
        if (!user?.guild_id) {
            alert('You must be in a guild to attack territories');
            return;
        }
        if (!['leader', 'officer'].includes(user?.guild_rank || '')) {
            alert('Only guild leaders and officers can attack territories');
            return;
        }
        try {
            const result = await guildsService.attackTerritory(territoryId);
            alert(result.message);
            loadTerritories();
        }
        catch (error) {
            alert(error.response?.data?.detail || 'Failed to attack territory');
        }
    };
    if (loading) {
        return _jsx("div", { className: "p-8", children: "Loading territories..." });
    }
    return (_jsxs("div", { className: "p-8", children: [_jsx("h1", { className: "text-4xl font-bold mb-8", children: "Territories" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: territories.map((territory) => (_jsxs(Card, { className: "p-4", children: [_jsx("h3", { className: "text-xl font-bold mb-2", children: territory.name }), _jsx("p", { className: "text-sm text-gray-600 mb-2", children: territory.description }), _jsxs("div", { className: "space-y-1 text-sm", children: [_jsxs("p", { children: [_jsx("strong", { children: "Income:" }), " ", territory.passive_income, " credits/day"] }), _jsxs("p", { children: [_jsx("strong", { children: "Defense:" }), " Level ", territory.defense_level] }), territory.controlling_guild_id ? (_jsxs("p", { className: "text-green-600", children: [_jsx("strong", { children: "Controlled by:" }), " ", territory.controlling_guild_id] })) : (_jsx("p", { className: "text-gray-500", children: "Unclaimed" })), territory.contested && (_jsx("p", { className: "text-red-600 font-bold", children: "CONTESTED!" }))] }), territory.controlling_guild_id !== user?.guild_id && (_jsx(Button, { className: "mt-4 w-full", size: "sm", onClick: () => handleAttack(territory.territory_id), children: "Attack" }))] }, territory.territory_id))) })] }));
};
export default Territories;
