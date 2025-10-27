import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { BookOpen, Lock, CheckCircle2, Play } from 'lucide-react';
import { toast } from 'sonner';
export const CampaignViewer = () => {
    const [activeCampaign, setActiveCampaign] = useState(null);
    const [availableCampaigns, setAvailableCampaigns] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchActiveCampaign();
        fetchAvailableCampaigns();
    }, []);
    const fetchActiveCampaign = async () => {
        try {
            const response = await fetch('/api/quests/campaigns/active', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                if (data) {
                    // Fetch progress
                    const progressResponse = await fetch('/api/quests/campaigns/progress', {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                    const progressData = await progressResponse.json();
                    setActiveCampaign(progressData);
                }
            }
        }
        catch (error) {
            console.error('Failed to fetch campaign:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const fetchAvailableCampaigns = async () => {
        try {
            const response = await fetch('/api/quests/campaigns/available', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setAvailableCampaigns(data.campaigns || []);
        }
        catch (error) {
            console.error('Failed to fetch available campaigns:', error);
        }
    };
    const startCampaign = async (campaignType) => {
        try {
            const response = await fetch('/api/quests/campaigns/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ campaign_type: campaignType })
            });
            const data = await response.json();
            if (data.success) {
                toast.success('Campaign started!', {
                    description: data.campaign.title
                });
                fetchActiveCampaign();
            }
            else {
                toast.error('Failed to start campaign', {
                    description: data.error
                });
            }
        }
        catch (error) {
            toast.error('Failed to start campaign');
        }
    };
    if (loading) {
        return _jsx("div", { className: "p-6", children: "Loading..." });
    }
    return (_jsxs("div", { className: "p-6 space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-3xl font-bold flex items-center gap-2", children: [_jsx(BookOpen, { className: "h-8 w-8" }), "Story Campaigns"] }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Epic storylines with lasting consequences" })] }) }), activeCampaign ? (_jsxs("div", { className: "space-y-6", children: [_jsx(Card, { className: "p-6", children: _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold", children: activeCampaign.title }), _jsxs("p", { className: "text-muted-foreground", children: ["Chapter ", activeCampaign.current_chapter, " of ", activeCampaign.total_chapters] })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-sm", children: [_jsx("span", { children: "Overall Progress" }), _jsxs("span", { children: [activeCampaign.completion_percentage.toFixed(0), "%"] })] }), _jsx(Progress, { value: activeCampaign.completion_percentage })] })] }) }), _jsxs("div", { children: [_jsx("h3", { className: "text-xl font-bold mb-4", children: "Chapters" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: activeCampaign.chapters.map(chapter => (_jsx(Card, { className: `p-4 ${!chapter.unlocked ? 'opacity-50' : ''}`, children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("h4", { className: "font-bold", children: chapter.title }), _jsxs("p", { className: "text-sm text-muted-foreground", children: ["Chapter ", chapter.chapter_number] })] }), chapter.completed ? (_jsx(CheckCircle2, { className: "h-5 w-5 text-green-600" })) : chapter.unlocked ? (_jsx(Play, { className: "h-5 w-5 text-blue-600" })) : (_jsx(Lock, { className: "h-5 w-5 text-muted-foreground" }))] }), _jsx("p", { className: "text-sm text-muted-foreground", children: chapter.description }), chapter.unlocked && !chapter.completed && (_jsx(Button, { className: "w-full", size: "sm", children: "Continue" }))] }) }, chapter.chapter_number))) })] })] })) : (_jsxs("div", { className: "space-y-6", children: [_jsxs(Card, { className: "p-8 text-center", children: [_jsx(BookOpen, { className: "h-12 w-12 mx-auto text-muted-foreground mb-4" }), _jsx("p", { className: "text-muted-foreground mb-4", children: "Start an epic campaign to experience a unique story" })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-xl font-bold mb-4", children: "Available Campaigns" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: availableCampaigns.map(campaign => (_jsx(Card, { className: "p-6", children: _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("h4", { className: "text-xl font-bold", children: campaign.title }), _jsx("p", { className: "text-sm text-muted-foreground mt-1", children: campaign.description })] }), _jsxs("div", { className: "space-y-2 text-sm", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Chapters:" }), _jsx("span", { children: campaign.total_chapters })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Duration:" }), _jsx("span", { children: campaign.estimated_duration })] })] }), _jsx(Button, { className: "w-full", onClick: () => startCampaign(campaign.campaign_type), children: "Start Campaign" })] }) }, campaign.id))) })] })] }))] }));
};