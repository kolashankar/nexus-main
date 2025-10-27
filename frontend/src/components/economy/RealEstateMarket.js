import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Home, Building2, DollarSign, TrendingUp, MapPin } from 'lucide-react';
import { toast } from 'sonner';
export const RealEstateMarket = () => {
    const [properties, setProperties] = useState([]);
    const [myProperties, setMyProperties] = useState([]);
    const [activeTab, setActiveTab] = useState('market');
    const [filter, setFilter] = useState('all');
    useEffect(() => {
        fetchProperties();
        fetchMyProperties();
    }, []);
    const fetchProperties = async () => {
        try {
            const response = await fetch('/api/real-estate/properties', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setProperties(data.properties || []);
        }
        catch (error) {
            console.error('Failed to fetch properties:', error);
        }
    };
    const fetchMyProperties = async () => {
        try {
            const response = await fetch('/api/real-estate/my-properties', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setMyProperties(data.properties || []);
        }
        catch (error) {
            console.error('Failed to fetch my properties:', error);
        }
    };
    const purchaseProperty = async (propertyId) => {
        try {
            const response = await fetch('/api/real-estate/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ property_id: propertyId })
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Property purchased!', {
                    description: `${data.property_name} - ${data.passive_income} credits/day`
                });
                fetchProperties();
                fetchMyProperties();
            }
            else {
                toast.error('Purchase failed', {
                    description: data.error || 'Unable to purchase property'
                });
            }
        }
        catch (error) {
            toast.error('Purchase failed');
        }
    };
    const getPropertyIcon = (type) => {
        switch (type) {
            case 'apartment':
                return _jsx(Home, { className: "h-6 w-6" });
            case 'house':
            case 'mansion':
                return _jsx(Building2, { className: "h-6 w-6" });
            default:
                return _jsx(Building2, { className: "h-6 w-6" });
        }
    };
    const formatPrice = (price) => {
        return new Intl.NumberFormat().format(price);
    };
    const filteredProperties = properties.filter(prop => filter === 'all' || prop.property_type === filter);
    return (_jsxs("div", { className: "p-6 space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(Building2, { className: "h-8 w-8" }), "Real Estate Market"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Invest in properties for passive income" })] }) }), _jsxs(Tabs, { value: activeTab, onValueChange: setActiveTab, children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "market", children: "Marketplace" }), _jsxs(TabsTrigger, { value: "portfolio", children: ["My Properties (", myProperties.length, ")"] })] }), _jsxs(TabsContent, { value: "market", className: "space-y-4", children: [_jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { variant: filter === 'all' ? 'default' : 'outline', size: "sm", onClick: () => setFilter('all'), children: "All" }), _jsx(Button, { variant: filter === 'apartment' ? 'default' : 'outline', size: "sm", onClick: () => setFilter('apartment'), children: "Apartments" }), _jsx(Button, { variant: filter === 'house' ? 'default' : 'outline', size: "sm", onClick: () => setFilter('house'), children: "Houses" }), _jsx(Button, { variant: filter === 'commercial' ? 'default' : 'outline', size: "sm", onClick: () => setFilter('commercial'), children: "Commercial" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filteredProperties.map(property => (_jsx(Card, { className: "p-4 hover:shadow-lg transition-all", children: _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold text-lg", children: property.name }), _jsx(Badge, { variant: "outline", children: property.property_type })] }), getPropertyIcon(property.property_type)] }), _jsx("p", { className: "text-sm text-muted-foreground", children: property.description }), _jsxs("div", { className: "space-y-2 text-sm", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(MapPin, { className: "h-4 w-4" }), "Territory ", property.territory_id] }), _jsxs("span", { children: [property.size, "m\u00B2"] })] }), _jsxs("div", { className: "flex items-center justify-between font-bold", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(DollarSign, { className: "h-4 w-4" }), "Price:"] }), _jsx("span", { children: formatPrice(property.price) })] }), _jsxs("div", { className: "flex items-center justify-between text-green-600", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(TrendingUp, { className: "h-4 w-4" }), "Income:"] }), _jsxs("span", { children: [formatPrice(property.passive_income), "/day"] })] })] }), _jsx(Button, { className: "w-full", onClick: () => purchaseProperty(property.id), children: "Purchase" })] }) }, property.id))) })] }), _jsx(TabsContent, { value: "portfolio", className: "space-y-4", children: myProperties.length === 0 ? (_jsxs(Card, { className: "p-8 text-center", children: [_jsx(Building2, { className: "h-12 w-12 mx-auto text-muted-foreground mb-4" }), _jsx("p", { className: "text-muted-foreground", children: "You don't own any properties yet" }), _jsx(Button, { className: "mt-4", onClick: () => setActiveTab('market'), children: "Browse Properties" })] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: myProperties.map(property => (_jsx(Card, { className: "p-4", children: _jsxs("div", { className: "space-y-3", children: [_jsx("h3", { className: "font-bold", children: property.name }), _jsxs("div", { className: "text-sm space-y-1", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Purchase Price:" }), _jsx("span", { children: formatPrice(property.purchase_price) })] }), _jsxs("div", { className: "flex justify-between text-green-600", children: [_jsx("span", { children: "Daily Income:" }), _jsx("span", { children: formatPrice(property.passive_income) })] })] })] }) }, property.property_id))) })) })] })] }));
};