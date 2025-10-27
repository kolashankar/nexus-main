import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { Link, useLocation } from 'react-router-dom';
import { cn } from '../../../lib/utils';
const navItems = [
    { title: 'Dashboard', href: '/dashboard' },
    { title: 'Profile', href: '/profile' },
    { title: 'Game World', href: '/game' },
    { title: 'Combat', href: '/combat' },
    { title: 'Guilds', href: '/guilds' },
    { title: 'Marketplace', href: '/marketplace' },
    { title: 'Quests', href: '/quests' },
    { title: 'Leaderboards', href: '/leaderboards' },
];
const Sidebar = () => {
    const location = useLocation();
    return (_jsx("aside", { className: "w-64 bg-slate-900 border-r border-purple-500/30 min-h-screen", children: _jsx("div", { className: "p-6", children: _jsx("nav", { className: "space-y-2", children: navItems.map((item) => {
                    const isActive = location.pathname === item.href;
                    return (_jsx(Link, { to: item.href, className: cn('block px-4 py-2 rounded-lg transition', isActive
                            ? 'bg-purple-600 text-white'
                            : 'text-gray-300 hover:bg-slate-800 hover:text-white'), children: item.title }, item.href));
                }) }) }) }));
};
export default Sidebar;
