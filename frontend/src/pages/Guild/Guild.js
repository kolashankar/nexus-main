import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import guildsService from '../../services/guilds/guildsService';
import { useAuth } from '../../hooks/useAuth';
const Guild = () => {
    const { user } = useAuth();
    const [guild, setGuild] = useState(null);
    const [members, setMembers] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadGuildData();
    }, []);
    const loadGuildData = async () => {
        try {
            const guildId = user?.guild_id;
            if (guildId) {
                const guildData = await guildsService.getGuild(guildId);
                setGuild(guildData);
                const membersData = await guildsService.getGuildMembers(guildId);
                setMembers(membersData);
            }
        }
        catch (error) {
            console.error('Failed to load guild:', error);
        }
        finally {
            setLoading(false);
        }
    };
    if (loading) {
        return _jsx("div", { className: "p-8", children: "Loading guild..." });
    }
    if (!guild) {
        return (_jsx("div", { className: "p-8", children: _jsxs(Card, { className: "p-6", children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "No Guild" }), _jsx("p", { className: "mb-4", children: "You are not in a guild yet." }), _jsx(Button, { onClick: () => window.location.href = '/guilds/list', children: "Browse Guilds" })] }) }));
    }
    return (_jsxs("div", { className: "p-8", children: [_jsxs("h1", { className: "text-4xl font-bold mb-8", children: [guild.name, " [", guild.tag, "]"] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-6", children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Guild Info" }), _jsxs("div", { className: "space-y-2", children: [_jsxs("p", { children: [_jsx("strong", { children: "Level:" }), " ", guild.level] }), _jsxs("p", { children: [_jsx("strong", { children: "Members:" }), " ", guild.total_members, "/", guild.max_members] }), _jsxs("p", { children: [_jsx("strong", { children: "Karma:" }), " ", guild.guild_karma] }), _jsxs("p", { children: [_jsx("strong", { children: "Reputation:" }), " ", guild.reputation] }), _jsxs("p", { children: [_jsx("strong", { children: "Territories:" }), " ", guild.controlled_territories.length] })] }), _jsx("p", { className: "mt-4 text-gray-600", children: guild.description })] }), _jsxs(Card, { className: "p-6", children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Guild Bank" }), _jsx("div", { className: "space-y-2", children: _jsxs("p", { children: [_jsx("strong", { children: "Credits:" }), " ", guild.guild_bank.credits] }) }), _jsx(Button, { className: "mt-4", onClick: () => {
                                    const amount = prompt('Enter amount to contribute:');
                                    if (amount) {
                                        guildsService.contributeToBank(parseInt(amount))
                                            .then(() => loadGuildData())
                                            .catch(console.error);
                                    }
                                }, children: "Contribute Credits" })] })] }), _jsxs(Card, { className: "p-6 mt-6", children: [_jsxs("h2", { className: "text-2xl font-bold mb-4", children: ["Members (", members.length, ")"] }), _jsx("div", { className: "space-y-2", children: members.map((member) => (_jsxs("div", { className: "flex justify-between items-center p-2 border-b", children: [_jsxs("div", { children: [_jsx("span", { className: "font-medium", children: member.username }), _jsxs("span", { className: "text-sm text-gray-500 ml-2", children: ["Level ", member.level] })] }), _jsx("span", { className: "text-sm", children: member.guild_rank })] }, member._id))) })] })] }));
};
export default Guild;
