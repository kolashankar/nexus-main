import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import KarmaScore from './KarmaScore';
import KarmaHistory from './KarmaHistory';
import apiClient from '@/services/api/client';
const KarmaDisplay = () => {
    const [karmaData, setKarmaData] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchKarmaData();
    }, []);
    const fetchKarmaData = async () => {
        try {
            const response = await apiClient.get('/api/karma/score');
            setKarmaData(response.data);
        }
        catch (error) {
            console.error('Failed to fetch karma data:', error);
        }
        finally {
            setLoading(false);
        }
    };
    if (loading) {
        return (_jsx(Card, { className: "w-full", children: _jsx(CardContent, { className: "p-6", children: _jsxs("div", { className: "animate-pulse space-y-4", children: [_jsx("div", { className: "h-24 bg-gray-300 rounded" }), _jsx("div", { className: "h-32 bg-gray-300 rounded" })] }) }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsx(KarmaScore, { karmaData: karmaData }), _jsx(KarmaHistory, {})] }));
};
export default KarmaDisplay;
