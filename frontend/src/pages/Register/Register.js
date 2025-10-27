import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Register page component
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card';
import useStore from '../../store';
const Register = () => {
    const navigate = useNavigate();
    const { register, isLoading, error } = useStore();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
    });
    const [localError, setLocalError] = useState(null);
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLocalError(null);
        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
            setLocalError('Passwords do not match');
            return;
        }
        // Validate password length
        if (formData.password.length < 8) {
            setLocalError('Password must be at least 8 characters long');
            return;
        }
        try {
            await register({
                username: formData.username,
                email: formData.email,
                password: formData.password,
            });
            navigate('/dashboard');
        }
        catch (err) {
            // Error is handled by the store
        }
    };
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const displayError = localError || error;
    return (_jsx("div", { className: "min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4", children: _jsxs(Card, { className: "w-full max-w-md", children: [_jsxs(CardHeader, { className: "space-y-1", children: [_jsx(CardTitle, { className: "text-2xl font-bold", children: "Create Account" }), _jsx(CardDescription, { children: "Join Karma Nexus and begin your journey" })] }), _jsxs("form", { onSubmit: handleSubmit, children: [_jsxs(CardContent, { className: "space-y-4", children: [displayError && (_jsx("div", { className: "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative", children: displayError })), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "username", className: "text-sm font-medium", children: "Username" }), _jsx(Input, { id: "username", name: "username", type: "text", placeholder: "Choose a username", value: formData.username, onChange: handleChange, required: true, minLength: 3 })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "email", className: "text-sm font-medium", children: "Email" }), _jsx(Input, { id: "email", name: "email", type: "email", placeholder: "Enter your email", value: formData.email, onChange: handleChange, required: true })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "password", className: "text-sm font-medium", children: "Password" }), _jsx(Input, { id: "password", name: "password", type: "password", placeholder: "Create a password", value: formData.password, onChange: handleChange, required: true, minLength: 8 })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "confirmPassword", className: "text-sm font-medium", children: "Confirm Password" }), _jsx(Input, { id: "confirmPassword", name: "confirmPassword", type: "password", placeholder: "Confirm your password", value: formData.confirmPassword, onChange: handleChange, required: true })] })] }), _jsxs(CardFooter, { className: "flex flex-col space-y-4", children: [_jsx(Button, { type: "submit", className: "w-full", disabled: isLoading, children: isLoading ? 'Creating account...' : 'Create Account' }), _jsxs("div", { className: "text-sm text-center text-gray-600", children: ["Already have an account?", ' ', _jsx(Link, { to: "/login", className: "text-purple-600 hover:text-purple-700 font-medium", children: "Login here" })] })] })] })] }) }));
};
export default Register;
