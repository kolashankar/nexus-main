import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Progress } from '@/components/ui/progress';
const TraitBar = ({ value, category }) => {
    // Get color class based on category
    const getBarColor = () => {
        switch (category) {
            case 'virtue':
                return 'bg-green-500';
            case 'vice':
                return 'bg-red-500';
            case 'skill':
                return 'bg-blue-500';
            case 'meta':
                return 'bg-purple-500';
            default:
                return 'bg-gray-500';
        }
    };
    return (_jsxs("div", { className: "relative", children: [_jsx(Progress, { value: value, className: "h-2" }), _jsx("style", { children: `
        .${getBarColor()} {
          background-color: currentColor;
        }
      ` })] }));
};
export default TraitBar;
