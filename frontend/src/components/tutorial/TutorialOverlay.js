import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { X, ArrowRight, CheckCircle, SkipForward } from 'lucide-react';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Progress } from '../ui/progress';
const TutorialOverlay = ({ onClose }) => {
    const [progress, setProgress] = useState(null);
    const [currentStep, setCurrentStep] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchTutorialData();
    }, []);
    const fetchTutorialData = async () => {
        try {
            // Fetch progress
            const progressRes = await fetch('/api/tutorial/progress', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            const progressData = await progressRes.json();
            setProgress(progressData);
            // Fetch current step if in progress
            if (progressData.status === 'in_progress') {
                const stepRes = await fetch('/api/tutorial/current', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const stepData = await stepRes.json();
                setCurrentStep(stepData);
            }
        }
        catch (error) {
            console.error('Error fetching tutorial data:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const handleCompleteStep = async () => {
        if (!currentStep)
            return;
        try {
            await fetch('/api/tutorial/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ step_id: currentStep.step_id })
            });
            // Refresh tutorial data
            await fetchTutorialData();
        }
        catch (error) {
            console.error('Error completing step:', error);
        }
    };
    const handleSkipStep = async () => {
        if (!currentStep)
            return;
        try {
            await fetch('/api/tutorial/skip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ step_id: currentStep.step_id })
            });
            // Refresh tutorial data
            await fetchTutorialData();
        }
        catch (error) {
            console.error('Error skipping step:', error);
        }
    };
    const handleSkipTutorial = async () => {
        try {
            await fetch('/api/tutorial/skip-all', {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            onClose();
        }
        catch (error) {
            console.error('Error skipping tutorial:', error);
        }
    };
    if (loading) {
        return (_jsx("div", { className: "fixed inset-0 bg-black/50 flex items-center justify-center z-50", children: _jsxs(Card, { className: "p-8", children: [_jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" }), _jsx("p", { className: "mt-4 text-center", children: "Loading tutorial..." })] }) }));
    }
    if (!progress || progress.status === 'not_started') {
        return null;
    }
    if (progress.status === 'completed' || progress.status === 'skipped') {
        return (_jsx("div", { className: "fixed inset-0 bg-black/50 flex items-center justify-center z-50", children: _jsxs(Card, { className: "max-w-md w-full p-8 text-center", children: [_jsx(CheckCircle, { className: "w-16 h-16 text-green-500 mx-auto mb-4" }), _jsx("h2", { className: "text-2xl font-bold mb-2", children: "Tutorial Complete!" }), _jsx("p", { className: "text-muted-foreground mb-6", children: "You've mastered the basics. Your journey in Karma Nexus begins now!" }), _jsx(Button, { onClick: onClose, className: "w-full", children: "Start Playing" })] }) }));
    }
    if (!currentStep) {
        return null;
    }
    return (_jsx("div", { className: "fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4", children: _jsxs(Card, { className: "max-w-2xl w-full p-6 relative", children: [_jsx(Button, { variant: "ghost", size: "icon", className: "absolute top-4 right-4", onClick: handleSkipTutorial, children: _jsx(X, { className: "h-4 w-4" }) }), _jsxs("div", { className: "mb-6", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-sm text-muted-foreground", children: "Tutorial Progress" }), _jsxs("span", { className: "text-sm font-medium", children: [progress.progress_percent, "%"] })] }), _jsx(Progress, { value: progress.progress_percent, className: "h-2" })] }), _jsxs("div", { className: "mb-6", children: [_jsx("h2", { className: "text-2xl font-bold mb-2", children: currentStep.title }), _jsx("p", { className: "text-muted-foreground mb-4", children: currentStep.description }), _jsxs("div", { className: "bg-secondary/20 p-4 rounded-lg mb-4", children: [_jsx("h3", { className: "font-semibold mb-2", children: "Your Task:" }), _jsx("p", { children: currentStep.task })] }), _jsxs("div", { className: "bg-accent/20 p-4 rounded-lg", children: [_jsx("h3", { className: "font-semibold mb-2", children: "Rewards:" }), _jsxs("div", { className: "flex gap-4 flex-wrap", children: [currentStep.reward.credits && (_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-yellow-500", children: "\uD83D\uDCB0" }), _jsxs("span", { children: [currentStep.reward.credits, " Credits"] })] })), currentStep.reward.xp && (_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-blue-500", children: "\u2B50" }), _jsxs("span", { children: [currentStep.reward.xp, " XP"] })] })), currentStep.reward.items && currentStep.reward.items.length > 0 && (_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-purple-500", children: "\uD83C\uDF81" }), _jsx("span", { children: currentStep.reward.items.join(', ') })] }))] })] })] }), _jsxs("div", { className: "flex gap-3", children: [currentStep.skippable && (_jsxs(Button, { variant: "outline", onClick: handleSkipStep, className: "flex-1", children: [_jsx(SkipForward, { className: "w-4 h-4 mr-2" }), "Skip Step"] })), _jsxs(Button, { onClick: handleCompleteStep, className: "flex-1", children: ["Continue", _jsx(ArrowRight, { className: "w-4 h-4 ml-2" })] })] }), _jsx("button", { onClick: handleSkipTutorial, className: "w-full text-center text-sm text-muted-foreground hover:text-foreground mt-4", children: "Skip entire tutorial" })] }) }));
};
export default TutorialOverlay;
