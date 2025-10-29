import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Login page component
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../../components/ui/card';
import useStore from '../../store';
const Login = () => {
    const navigate = useNavigate();
    const { login, isLoading, error } = useStore();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(formData);
            navigate('/dashboard');
        }
        catch (err) {
            // Error is handled by the store and displayed below
        }
    };
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    return (_jsx("div", { className: "min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4", children: _jsxs(Card, { className: "w-full max-w-md", children: [_jsxs(CardHeader, { className: "space-y-1", children: [_jsx(CardTitle, { className: "text-2xl font-bold", children: "Login" }), _jsx(CardDescription, { children: "Enter your credentials to access your account" })] }), _jsxs("form", { onSubmit: handleSubmit, children: [_jsxs(CardContent, { className: "space-y-4", children: [error && (_jsx("div", { className: "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative", role: "alert", children: _jsx("span", { className: "block sm:inline", children: error }) })), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "email", className: "text-sm font-medium", children: "Email" }), _jsx(Input, { id: "email", name: "email", type: "email", placeholder: "Enter your email", value: formData.email, onChange: handleChange, required: true })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("label", { htmlFor: "password", className: "text-sm font-medium", children: "Password" }), _jsx(Input, { id: "password", name: "password", type: "password", placeholder: "Enter your password", value: formData.password, onChange: handleChange, required: true })] })] }), _jsxs(CardFooter, { className: "flex flex-col space-y-4", children: [_jsx(Button, { type: "submit", className: "w-full", disabled: isLoading, children: isLoading ? 'Logging in...' : 'Login' }), _jsxs("div", { className: "text-sm text-center text-gray-600", children: ["Don't have an account?", ' ', _jsx(Link, { to: "/register", className: "text-purple-600 hover:text-purple-700 font-medium", children: "Register here" })] })] })] })] }) }));
};
export default Login;
