import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import socialService from '../../services/social/socialService';
import { useAuth } from '../../hooks/useAuth';
const SocialHub = () => {
    const { user } = useAuth();
    const [onlinePlayers, setOnlinePlayers] = useState([]);
    const [alliance, setAlliance] = useState(null);
    const [marriage, setMarriage] = useState(null);
    const [mentorship, setMentorship] = useState(null);
    const [proposals, setProposals] = useState([]);
    const [mentorshipRequests, setMentorshipRequests] = useState([]);
    useEffect(() => {
        loadSocialData();
    }, []);
    const loadSocialData = async () => {
        try {
            // Load online players
            const players = await socialService.getOnlinePlayers();
            setOnlinePlayers(players);
            // Load alliance
            try {
                const allianceData = await socialService.getMyAlliance();
                setAlliance(allianceData);
            }
            catch (error) {
                // Not in an alliance
            }
            // Load marriage
            try {
                const marriageData = await socialService.getMyMarriage();
                setMarriage(marriageData);
            }
            catch (error) {
                // Not married
            }
            // Load mentorship
            try {
                const mentorshipData = await socialService.getMyMentorship();
                setMentorship(mentorshipData);
            }
            catch (error) {
                // Not in mentorship
            }
            // Load proposals
            try {
                const proposalsData = await socialService.getPendingProposals();
                setProposals(proposalsData);
            }
            catch (error) {
                // No proposals
            }
            // Load mentorship requests
            try {
                const requestsData = await socialService.getPendingMentorshipRequests();
                setMentorshipRequests(requestsData);
            }
            catch (error) {
                // No requests
            }
        }
        catch (error) {
            console.error('Failed to load social data:', error);
        }
    };
    return (_jsxs("div", { className: "p-8", children: [_jsx("h1", { className: "text-4xl font-bold mb-8", children: "Social Hub" }), _jsxs(Tabs, { defaultValue: "players", className: "w-full", children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "players", children: "Online Players" }), _jsx(TabsTrigger, { value: "alliance", children: "Alliance" }), _jsx(TabsTrigger, { value: "marriage", children: "Marriage" }), _jsx(TabsTrigger, { value: "mentorship", children: "Mentorship" })] }), _jsx(TabsContent, { value: "players", children: _jsxs(Card, { className: "p-6", children: [_jsxs("h2", { className: "text-2xl font-bold mb-4", children: ["Online Players (", onlinePlayers.length, ")"] }), _jsx("div", { className: "space-y-2", children: onlinePlayers.map((player) => (_jsxs("div", { className: "flex justify-between items-center p-2 border-b", children: [_jsxs("div", { children: [_jsx("span", { className: "font-medium", children: player.username }), _jsxs("span", { className: "text-sm text-gray-500 ml-2", children: ["Level ", player.level] })] }), _jsx(Button, { size: "sm", variant: "outline", children: "View Profile" })] }, player._id))) })] }) }), _jsx(TabsContent, { value: "alliance", children: _jsx(Card, { className: "p-6", children: alliance ? (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Your Alliance" }), _jsxs("p", { children: [_jsx("strong", { children: "Name:" }), " ", alliance.alliance_name || 'Unnamed Alliance'] }), _jsxs("p", { children: [_jsx("strong", { children: "Members:" }), " ", alliance.members.length, "/3"] }), _jsx(Button, { className: "mt-4", variant: "destructive", onClick: async () => {
                                            await socialService.leaveAlliance();
                                            loadSocialData();
                                        }, children: "Leave Alliance" })] })) : (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "No Alliance" }), _jsx("p", { className: "mb-4", children: "You are not in an alliance yet." }), _jsx(Button, { onClick: async () => {
                                            const name = prompt('Enter alliance name (optional):');
                                            await socialService.createAlliance(name || undefined);
                                            loadSocialData();
                                        }, children: "Create Alliance" })] })) }) }), _jsx(TabsContent, { value: "marriage", children: _jsx(Card, { className: "p-6", children: marriage ? (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Marriage" }), _jsxs("p", { children: [_jsx("strong", { children: "Married Since:" }), " ", new Date(marriage.married_at).toLocaleDateString()] }), _jsxs("p", { children: [_jsx("strong", { children: "Joint Karma:" }), " ", marriage.joint_karma] }), _jsx(Button, { className: "mt-4", variant: "destructive", onClick: async () => {
                                            // eslint-disable-next-line no-restricted-globals
                                            if (confirm('Are you sure you want to divorce? (Karma penalty applies)')) {
                                                await socialService.divorce();
                                                loadSocialData();
                                            }
                                        }, children: "Divorce" })] })) : (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Not Married" }), proposals.length > 0 && (_jsxs("div", { className: "mb-4", children: [_jsx("h3", { className: "font-bold mb-2", children: "Pending Proposals" }), proposals.map((proposal) => (_jsxs("div", { className: "flex justify-between items-center p-2 border-b", children: [_jsxs("span", { children: ["Proposal from ", proposal.proposer_id] }), _jsxs("div", { className: "space-x-2", children: [_jsx(Button, { size: "sm", onClick: async () => {
                                                                    await socialService.acceptProposal(proposal._id);
                                                                    loadSocialData();
                                                                }, children: "Accept" }), _jsx(Button, { size: "sm", variant: "outline", onClick: async () => {
                                                                    await socialService.rejectProposal(proposal._id);
                                                                    loadSocialData();
                                                                }, children: "Reject" })] })] }, proposal._id)))] }))] })) }) }), _jsx(TabsContent, { value: "mentorship", children: _jsx(Card, { className: "p-6", children: mentorship ? (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "Mentorship" }), _jsxs("p", { children: [_jsx("strong", { children: "Lessons Completed:" }), " ", mentorship.lessons_completed] }), _jsxs("p", { children: [_jsx("strong", { children: "XP Bonus:" }), " ", mentorship.apprentice_xp_bonus * 100, "%"] }), _jsx(Button, { className: "mt-4", onClick: async () => {
                                            await socialService.completeLesson();
                                            loadSocialData();
                                        }, children: "Complete Lesson" })] })) : (_jsxs("div", { children: [_jsx("h2", { className: "text-2xl font-bold mb-4", children: "No Mentorship" }), mentorshipRequests.length > 0 && (_jsxs("div", { className: "mb-4", children: [_jsx("h3", { className: "font-bold mb-2", children: "Pending Requests" }), mentorshipRequests.map((request) => (_jsxs("div", { className: "flex justify-between items-center p-2 border-b", children: [_jsxs("span", { children: ["Request from ", request.apprentice_id] }), _jsxs("div", { className: "space-x-2", children: [_jsx(Button, { size: "sm", onClick: async () => {
                                                                    await socialService.acceptMentorshipRequest(request._id);
                                                                    loadSocialData();
                                                                }, children: "Accept" }), _jsx(Button, { size: "sm", variant: "outline", onClick: async () => {
                                                                    await socialService.rejectMentorshipRequest(request._id);
                                                                    loadSocialData();
                                                                }, children: "Reject" })] })] }, request._id)))] }))] })) }) })] })] }));
};
export default SocialHub;