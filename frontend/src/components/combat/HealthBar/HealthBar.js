import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import './HealthBar.css';
const HealthBar = ({ current, max, label = 'HP', showNumbers = true }) => {
    const percentage = (current / max) * 100;
    const getHealthColor = () => {
        if (percentage > 60)
            return 'health-high';
        if (percentage > 30)
            return 'health-medium';
        return 'health-low';
    };
    return (_jsxs("div", { className: "health-bar-container", children: [_jsxs("div", { className: "health-bar-header", children: [_jsx("span", { className: "health-label", children: label }), showNumbers && (_jsxs("span", { className: "health-numbers", children: [current, " / ", max] }))] }), _jsxs("div", { className: `health-bar-wrapper ${getHealthColor()}`, children: [_jsx("div", { className: "health-bar-fill", style: { width: `${percentage}%` }, children: _jsx("div", { className: "health-bar-glow" }) }), _jsxs("span", { className: "health-percentage", children: [Math.round(percentage), "%"] })] })] }));
};
export default HealthBar;
