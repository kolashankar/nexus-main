import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import CharacterCreator from '../CharacterCreator/CharacterCreator';
describe('CharacterCreator Component', () => {
    test('renders character creator interface', () => {
        render(_jsx(CharacterCreator, {}));
        expect(screen.getByText(/create character/i)).toBeInTheDocument();
    });
    test('displays gender selection', () => {
        render(_jsx(CharacterCreator, {}));
        expect(screen.getByText(/male/i)).toBeInTheDocument();
        expect(screen.getByText(/female/i)).toBeInTheDocument();
    });
    test('shows customization tabs', () => {
        render(_jsx(CharacterCreator, {}));
        expect(screen.getByText(/face/i)).toBeInTheDocument();
        expect(screen.getByText(/hair/i)).toBeInTheDocument();
        expect(screen.getByText(/body/i)).toBeInTheDocument();
    });
    test('displays 3D character preview', () => {
        render(_jsx(CharacterCreator, {}));
        expect(screen.getByTestId('character-preview')).toBeInTheDocument();
    });
    test('allows changing hair style', () => {
        render(_jsx(CharacterCreator, {}));
        const hairTab = screen.getByText(/hair/i);
        fireEvent.click(hairTab);
        const hairStyles = screen.getAllByRole('button', { name: /style/i });
        expect(hairStyles.length).toBeGreaterThan(0);
    });
    test('provides color picker for hair', () => {
        render(_jsx(CharacterCreator, {}));
        const hairTab = screen.getByText(/hair/i);
        fireEvent.click(hairTab);
        expect(screen.getByTestId('color-picker')).toBeInTheDocument();
    });
    test('displays face customization options', () => {
        render(_jsx(CharacterCreator, {}));
        const faceTab = screen.getByText(/face/i);
        fireEvent.click(faceTab);
        expect(screen.getByText(/eyes/i)).toBeInTheDocument();
        expect(screen.getByText(/nose/i)).toBeInTheDocument();
    });
    test('shows body type selection', () => {
        render(_jsx(CharacterCreator, {}));
        const bodyTab = screen.getByText(/body/i);
        fireEvent.click(bodyTab);
        expect(screen.getByText(/slim/i)).toBeInTheDocument();
        expect(screen.getByText(/athletic/i)).toBeInTheDocument();
    });
    test('validates character name input', () => {
        render(_jsx(CharacterCreator, {}));
        const nameInput = screen.getByPlaceholderText(/character name/i);
        fireEvent.change(nameInput, { target: { value: 'ab' } });
        expect(screen.getByText(/name too short/i)).toBeInTheDocument();
    });
    test('disables create button until customization complete', () => {
        render(_jsx(CharacterCreator, {}));
        const createButton = screen.getByText(/create/i);
        expect(createButton).toBeDisabled();
    });
    test('enables create button when valid', () => {
        render(_jsx(CharacterCreator, {}));
        const nameInput = screen.getByPlaceholderText(/character name/i);
        fireEvent.change(nameInput, { target: { value: 'ValidName' } });
        const createButton = screen.getByText(/create/i);
        expect(createButton).not.toBeDisabled();
    });
    test('rotates character preview', () => {
        render(_jsx(CharacterCreator, {}));
        const preview = screen.getByTestId('character-preview');
        fireEvent.mouseDown(preview, { clientX: 0 });
        fireEvent.mouseMove(preview, { clientX: 100 });
        fireEvent.mouseUp(preview);
        // Character should rotate
    });
});
