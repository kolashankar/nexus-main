import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import TraitBar from './TraitBar';
const TraitItem = ({ name, value, category }) => {
    // Format trait name for display
    const formatName = (str) => {
        return str
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    };
    // Get color based on category
    const getCategoryColor = () => {
        switch (category) {
            case 'virtue':
                return 'text-green-600';
            case 'vice':
                return 'text-red-600';
            case 'skill':
                return 'text-blue-600';
            case 'meta':
                return 'text-purple-600';
            default:
                return 'text-gray-600';
        }
    };
    return (_jsx("div", { className: "flex items-center gap-3 p-3 bg-white rounded-lg border hover:shadow-md transition-shadow", children: _jsxs("div", { className: "flex-1", children: [_jsxs("div", { className: "flex justify-between items-center mb-1", children: [_jsx("span", { className: `font-medium ${getCategoryColor()}`, children: formatName(name) }), _jsx("span", { className: "text-sm font-bold text-gray-700", children: Math.round(value) })] }), _jsx(TraitBar, { value: value, category: category })] }) }));
};
export default TraitItem;
