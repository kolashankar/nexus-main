import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Switch } from '../../ui/switch';
export const VisibilityToggle = ({ label, checked, onChange }) => {
    return (_jsxs("div", { className: "flex items-center justify-between py-2", children: [_jsx("span", { className: "text-sm", children: label }), _jsx(Switch, { checked: checked, onCheckedChange: onChange })] }));
};
