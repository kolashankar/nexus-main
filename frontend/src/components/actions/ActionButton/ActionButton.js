import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Button } from '../../ui/button';
export const ActionButton = ({ icon, label, description, onClick, variant = 'default' }) => {
    return (_jsxs(Button, { variant: variant, onClick: onClick, className: "h-auto py-4 px-6 flex flex-col items-center gap-2 w-full", children: [_jsx("span", { className: "text-3xl", children: icon }), _jsxs("div", { className: "text-center", children: [_jsx("p", { className: "font-bold", children: label }), _jsx("p", { className: "text-xs opacity-80", children: description })] })] }));
};
