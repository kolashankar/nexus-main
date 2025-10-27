import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
const KarmaScore = ({ karmaData }) => {
    if (!karmaData)
        return null;
    const getMoralClassColor = (moralClass) => {
        switch (moralClass) {
            case 'good':
                return 'bg-green-500';
            case 'bad':
                return 'bg-red-500';
            default:
                return 'bg-gray-500';
        }
    };
    const getKarmaLevelColor = (level) => {
        const positiveLevels = ['saint', 'virtuous', 'good', 'neutral_good'];
        const negativeLevels = ['demon', 'evil', 'bad', 'neutral_bad'];
        if (positiveLevels.includes(level))
            return 'text-green-600';
        if (negativeLevels.includes(level))
            return 'text-red-600';
        return 'text-gray-600';
    };
    // Calculate progress to next milestone
    const calculateProgress = () => {
        if (!karmaData.next_milestone)
            return 100;
        const current = karmaData.karma_points;
        const next = karmaData.next_milestone;
        if (next > 0) {
            const previous = next === 100 ? 0 : next === 500 ? 100 : next === 1000 ? 500 : next === 2000 ? 1000 : 0;
            return ((current - previous) / (next - previous)) * 100;
        }
        else {
            const previous = next === -100 ? 0 : next === -500 ? -100 : next === -1000 ? -500 : next === -2000 ? -1000 : 0;
            return ((current - previous) / (next - previous)) * 100;
        }
    };
    return (_jsxs(Card, { className: "w-full shadow-lg", children: [_jsx(CardHeader, { className: "bg-gradient-to-r from-orange-400 to-yellow-400 text-white", children: _jsxs(CardTitle, { className: "text-2xl flex items-center justify-between", children: [_jsx("span", { children: "Karma Score" }), _jsx(Badge, { className: getMoralClassColor(karmaData.moral_class), children: karmaData.moral_class.toUpperCase() })] }) }), _jsxs(CardContent, { className: "p-6", children: [_jsxs("div", { className: "text-center mb-6", children: [_jsx("div", { className: "text-6xl font-bold text-orange-600", children: karmaData.karma_points }), _jsx("div", { className: `text-xl font-semibold mt-2 ${getKarmaLevelColor(karmaData.karma_level)}`, children: karmaData.karma_level.replace('_', ' ').toUpperCase() })] }), karmaData.next_milestone && (_jsxs("div", { className: "mt-4", children: [_jsxs("div", { className: "flex justify-between text-sm mb-2", children: [_jsx("span", { className: "text-gray-600", children: "Next Milestone" }), _jsx("span", { className: "font-semibold", children: karmaData.next_milestone })] }), _jsx(Progress, { value: calculateProgress(), className: "h-3" })] })), _jsx("div", { className: "mt-6 p-4 bg-gray-50 rounded-lg", children: _jsxs("p", { className: "text-sm text-gray-700", children: [karmaData.karma_points >= 2000 && 'You are a beacon of virtue in this world. Your actions inspire others.', karmaData.karma_points >= 500 && karmaData.karma_points < 2000 && 'You are known for your good deeds and positive influence.', karmaData.karma_points > -500 && karmaData.karma_points < 500 && 'You walk the line between good and evil. Your choices will define you.', karmaData.karma_points > -2000 && karmaData.karma_points <= -500 && 'Your reputation has been tarnished by your actions.', karmaData.karma_points <= -2000 && 'You are feared and reviled. Redemption seems distant.'] }) })] })] }));
};
export default KarmaScore;
