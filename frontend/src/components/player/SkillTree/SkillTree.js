import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { Progress } from '../../ui/progress';
import skillTreesService from '../../../services/skillTrees/skillTreesService';
import SkillNode from './SkillNode';
import { toast } from 'sonner';
const SkillTree = () => {
    const [skillTrees, setSkillTrees] = useState(null);
    const [selectedTrait, setSelectedTrait] = useState('');
    const [selectedTree, setSelectedTree] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchSkillTrees();
    }, []);
    const fetchSkillTrees = async () => {
        try {
            const data = await skillTreesService.getSkillTrees();
            setSkillTrees(data);
        }
        catch (error) {
            console.error('Failed to fetch skill trees:', error);
            toast.error('Failed to load skill trees');
        }
        finally {
            setLoading(false);
        }
    };
    const handleSelectTrait = async (traitName) => {
        setSelectedTrait(traitName);
        if (skillTrees?.skill_trees[traitName]) {
            setSelectedTree(skillTrees.skill_trees[traitName]);
        }
    };
    const handleUnlockNode = async (nodeId) => {
        if (!selectedTrait)
            return;
        try {
            await skillTreesService.unlockNode({
                trait_name: selectedTrait,
                node_id: nodeId,
            });
            toast.success('Node unlocked!');
            fetchSkillTrees();
        }
        catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to unlock node');
        }
    };
    const handleChooseBranch = async (branch) => {
        if (!selectedTrait)
            return;
        try {
            await skillTreesService.chooseBranch({
                trait_name: selectedTrait,
                branch,
            });
            toast.success(`Branch ${branch} selected!`);
            fetchSkillTrees();
        }
        catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to choose branch');
        }
    };
    if (loading) {
        return _jsx("div", { className: "flex justify-center items-center h-64", children: "Loading skill trees..." });
    }
    return (_jsx("div", { className: "container mx-auto py-6", children: _jsxs(Card, { children: [_jsxs(CardHeader, { children: [_jsx(CardTitle, { className: "text-3xl", children: "Skill Trees" }), skillTrees && (_jsxs("div", { className: "flex gap-4 mt-4", children: [_jsxs(Badge, { variant: "secondary", children: ["Available Points: ", skillTrees.available_points] }), _jsxs(Badge, { variant: "outline", children: ["Total Invested: ", skillTrees.total_points_spent] })] }))] }), _jsx(CardContent, { children: _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-4 gap-6", children: [_jsxs("div", { className: "lg:col-span-1 space-y-2 max-h-[600px] overflow-y-auto", children: [_jsx("h3", { className: "font-semibold mb-3", children: "Select Trait" }), skillTrees &&
                                        Object.keys(skillTrees.skill_trees).map((traitName) => {
                                            const tree = skillTrees.skill_trees[traitName];
                                            return (_jsxs(Button, { variant: selectedTrait === traitName ? 'default' : 'outline', className: "w-full justify-between", onClick: () => handleSelectTrait(traitName), children: [_jsx("span", { className: "capitalize", children: traitName.replace('_', ' ') }), _jsx(Badge, { variant: "secondary", children: tree.total_points_invested })] }, traitName));
                                        })] }), _jsx("div", { className: "lg:col-span-3", children: selectedTree ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("h2", { className: "text-2xl font-bold capitalize", children: selectedTrait.replace('_', ' ') }), _jsxs("div", { className: "space-x-2", children: [_jsxs(Badge, { children: ["Points: ", selectedTree.total_points_invested, "/20"] }), selectedTree.active_branch && (_jsxs(Badge, { variant: "outline", children: ["Branch: ", selectedTree.active_branch] }))] })] }), _jsx(Progress, { value: (selectedTree.total_points_invested / 20) * 100, className: "h-2" }), _jsx("div", { className: "grid grid-cols-4 gap-4 mt-6", children: selectedTree.nodes.map((node) => (_jsx(SkillNode, { node: node, onUnlock: () => handleUnlockNode(node.node_id), canUnlock: skillTrees?.available_points > 0 }, node.node_id))) }), selectedTree.nodes[9]?.unlocked && !selectedTree.active_branch && (_jsxs(Card, { className: "mt-6 p-4 bg-blue-50 dark:bg-blue-900/20", children: [_jsx("h3", { className: "font-semibold mb-3", children: "Choose Your Path" }), _jsxs("div", { className: "flex gap-4", children: [_jsx(Button, { onClick: () => handleChooseBranch('A'), children: "Branch A" }), _jsx(Button, { onClick: () => handleChooseBranch('B'), children: "Branch B" })] })] }))] })) : (_jsx("div", { className: "flex items-center justify-center h-64 text-muted-foreground", children: "Select a trait to view its skill tree" })) })] }) })] }) }));
};
export default SkillTree;