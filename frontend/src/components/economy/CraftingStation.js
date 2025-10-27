import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Hammer, Package, Clock, TrendingUp } from 'lucide-react';
import { toast } from 'sonner';
export const CraftingStation = () => {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [crafting, setCrafting] = useState(false);
    const [craftingProgress, setCraftingProgress] = useState(0);
    const [activeCategory, setActiveCategory] = useState('all');
    useEffect(() => {
        fetchRecipes();
    }, []);
    const fetchRecipes = async () => {
        try {
            const response = await fetch('/api/crafting/recipes', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setRecipes(data.recipes || []);
        }
        catch (error) {
            console.error('Failed to fetch recipes:', error);
        }
    };
    const craftItem = async (recipeId, quantity = 1) => {
        setCrafting(true);
        setCraftingProgress(0);
        try {
            const response = await fetch('/api/crafting/craft', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ recipe_id: recipeId, quantity })
            });
            const data = await response.json();
            if (data.success) {
                // Simulate crafting progress
                const interval = setInterval(() => {
                    setCraftingProgress(prev => {
                        if (prev >= 100) {
                            clearInterval(interval);
                            toast.success(`Crafted ${data.item_name}!`, {
                                description: `+${data.xp_gained} XP`
                            });
                            setCrafting(false);
                            fetchRecipes(); // Refresh recipes
                            return 100;
                        }
                        return prev + 10;
                    });
                }, 100);
            }
            else {
                toast.error('Crafting failed', {
                    description: data.error || 'Unknown error'
                });
                setCrafting(false);
            }
        }
        catch (error) {
            toast.error('Crafting failed');
            setCrafting(false);
        }
    };
    const canCraft = (recipe) => {
        if (!recipe.unlocked)
            return false;
        return recipe.materials_required.every(mat => mat.owned >= mat.quantity);
    };
    const getRarityColor = (rarity) => {
        const colors = {
            common: 'bg-gray-500',
            uncommon: 'bg-green-500',
            rare: 'bg-blue-500',
            epic: 'bg-purple-500',
            legendary: 'bg-yellow-500'
        };
        return colors[rarity] || 'bg-gray-500';
    };
    const filteredRecipes = recipes.filter(recipe => activeCategory === 'all' || recipe.category === activeCategory);
    return (_jsxs("div", { className: "p-6 space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(Hammer, { className: "h-8 w-8" }), "Crafting Station"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Create items from materials" })] }) }), _jsxs(Tabs, { value: activeCategory, onValueChange: setActiveCategory, children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "all", children: "All" }), _jsx(TabsTrigger, { value: "robot_parts", children: "Robot Parts" }), _jsx(TabsTrigger, { value: "electronics", children: "Electronics" }), _jsx(TabsTrigger, { value: "power", children: "Power" }), _jsx(TabsTrigger, { value: "augmentation", children: "Augmentation" })] }), _jsxs(TabsContent, { value: activeCategory, className: "space-y-4", children: [crafting && (_jsx(Card, { className: "p-6", children: _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-medium", children: "Crafting in progress..." }), _jsxs("span", { children: [craftingProgress, "%"] })] }), _jsx(Progress, { value: craftingProgress })] }) })), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filteredRecipes.map(recipe => (_jsx(Card, { className: `p-4 cursor-pointer transition-all hover:shadow-lg ${!recipe.unlocked ? 'opacity-50' : ''} ${selectedRecipe?.id === recipe.id ? 'ring-2 ring-primary' : ''}`, onClick: () => setSelectedRecipe(recipe), children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold text-lg", children: recipe.name }), _jsx(Badge, { className: getRarityColor(recipe.result_item.rarity), children: recipe.result_item.rarity })] }), _jsx(Package, { className: "h-6 w-6 text-muted-foreground" })] }), _jsx("p", { className: "text-sm text-muted-foreground", children: recipe.description }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-medium", children: "Materials Required:" }), recipe.materials_required.map(mat => (_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { children: mat.name }), _jsxs("span", { className: mat.owned >= mat.quantity
                                                                    ? 'text-green-600'
                                                                    : 'text-red-600', children: [mat.owned, "/", mat.quantity] })] }, mat.material_id)))] }), _jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "h-4 w-4" }), recipe.crafting_time, "s"] }), _jsxs("div", { className: "flex items-center gap-1", children: [_jsx(TrendingUp, { className: "h-4 w-4" }), "+", recipe.xp_reward, " XP"] })] }), _jsx(Button, { className: "w-full", disabled: !canCraft(recipe) || crafting, onClick: (e) => {
                                                    e.stopPropagation();
                                                    craftItem(recipe.id);
                                                }, children: recipe.unlocked ? 'Craft' : `Unlock at Lv.${recipe.level_required}` })] }) }, recipe.id))) })] })] })] }));
};