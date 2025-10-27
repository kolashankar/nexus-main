import React from "react";
import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { Link } from 'react-router-dom';
import { Button } from '../../ui/button';
import useStore from '../../../store';
const Header = () => {
    const { isAuthenticated, logout, player } = useStore();
    const handleLogout = async () => {
        await logout();
        window.location.href = '/login';
    };
    return (_jsx("header", { className: "bg-slate-900 border-b border-purple-500/30 sticky top-0 z-50", children: _jsx("div", { className: "container mx-auto px-4", children: _jsxs("div", { className: "flex items-center justify-between h-16", children: [_jsx(Link, { to: "/", className: "flex items-center space-x-2", children: _jsx("span", { className: "text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600", children: "KARMA NEXUS" }) }), _jsx("nav", { className: "hidden md:flex items-center space-x-6", children: isAuthenticated ? (_jsxs(_Fragment, { children: [_jsx(Link, { to: "/dashboard", className: "text-gray-300 hover:text-white transition", children: "Dashboard" }), _jsx(Link, { to: "/profile", className: "text-gray-300 hover:text-white transition", children: "Profile" }), _jsx(Link, { to: "/play", className: "text-gray-300 hover:text-white transition", children: "Play" }), _jsxs("div", { className: "flex items-center space-x-4", children: [player && (_jsx("span", { className: "text-sm text-gray-400", children: player.username })), _jsx(Button, { variant: "outline", size: "sm", onClick: handleLogout, children: "Logout" })] })] })) : (_jsxs(_Fragment, { children: [_jsx(Link, { to: "/login", children: _jsx(Button, { variant: "ghost", children: "Login" }) }), _jsx(Link, { to: "/register", children: _jsx(Button, { children: "Get Started" }) })] })) })] }) }) }));
};
export default Header;
