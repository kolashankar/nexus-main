import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import KarmaDisplay from '../KarmaDisplay/KarmaDisplay';
describe('KarmaDisplay Component', () => {
    test('renders positive karma correctly', () => {
        render(_jsx(KarmaDisplay, { karma: 500 }));
        expect(screen.getByText(/500/)).toBeInTheDocument();
    });
    test('renders negative karma correctly', () => {
        render(_jsx(KarmaDisplay, { karma: -300 }));
        expect(screen.getByText(/-300/)).toBeInTheDocument();
    });
    test('shows zero karma', () => {
        render(_jsx(KarmaDisplay, { karma: 0 }));
        expect(screen.getByText('0')).toBeInTheDocument();
    });
    test('displays positive karma with green color', () => {
        render(_jsx(KarmaDisplay, { karma: 500 }));
        const karmaElement = screen.getByRole('status', {name: /karma score/i});
        expect(karmaElement).toHaveClass(/positive/i);
    });
    test('displays negative karma with red color', () => {
        render(_jsx(KarmaDisplay, { karma: -300 }));
        const karmaElement = screen.getByRole('status', {name: /karma score/i});
        expect(karmaElement).toHaveClass(/negative/i);
    });
    test('shows karma change indicator', () => {
        render(_jsx(KarmaDisplay, { karma: 500, change: 50 }));
        expect(screen.getByText(/\+50/)).toBeInTheDocument();
    });
    test('displays karma tier label', () => {
        render(_jsx(KarmaDisplay, { karma: 1000, showTier: true }));
        expect(screen.getByText(/virtuous/i)).toBeInTheDocument();
    });
    test('shows karma as percentage', () => {
        render(_jsx(KarmaDisplay, { karma: 5000, max: 10000, showPercentage: true }));
        expect(screen.getByText(/50%/)).toBeInTheDocument();
    });
    test('renders karma history link', () => {
        render(_jsx(KarmaDisplay, { karma: 500, showHistory: true }));
        expect(screen.getByText(/history/i)).toBeInTheDocument();
    });
    test('handles very large karma values', () => {
        render(_jsx(KarmaDisplay, { karma: 999999 }));
        expect(screen.getByText(/999,?999/)).toBeInTheDocument();
    });
});