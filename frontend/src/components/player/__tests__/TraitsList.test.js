import React from "react";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TraitsList from '../TraitsList/TraitsList';

const mockTraits = {
  empathy: 85,
  integrity: 75,
  greed: 20,
  hacking: 60,
  negotiation: 55,
  strength: 40,
};

describe('TraitsList Component', () => {
  test('renders all traits', () => {
    render(<TraitsList traits={mockTraits} />);
    expect(screen.getByText('empathy')).toBeInTheDocument();
    expect(screen.getByText('integrity')).toBeInTheDocument();
    expect(screen.getByText('greed')).toBeInTheDocument();
  });

  test('displays trait values correctly', () => {
    render(<TraitsList traits={mockTraits} />);
    expect(screen.getByText(/85/)).toBeInTheDocument();
    expect(screen.getByText(/75/)).toBeInTheDocument();
    expect(screen.getByText(/20/)).toBeInTheDocument();
  });

  test('shows trait progress bars', () => {
    render(<TraitsList traits={mockTraits} />);
    const progressBars = screen.getAllByRole('progressbar');
    expect(progressBars.length).toBe(Object.keys(mockTraits).length);
  });

  test('filters traits by category', () => {
    render(<TraitsList traits={mockTraits} categories={['virtues', 'vices']} />);

    const virtuesButton = screen.getByText(/virtues/i);
    fireEvent.click(virtuesButton);

    // Should show empathy and integrity (virtues)
    expect(screen.getByText('empathy')).toBeInTheDocument();
    expect(screen.getByText('integrity')).toBeInTheDocument();
  });

  test('sorts traits by value', () => {
    render(<TraitsList traits={mockTraits} />);

    const sortButton = screen.getByText(/sort/i);
    fireEvent.click(sortButton);

    const traitElements = screen.getAllByTestId(/trait-item/i);
    expect(traitElements.length).toBeGreaterThan(0);
  });

  test('highlights high traits (>80%)', () => {
    render(<TraitsList traits={mockTraits} />);
    const empathyElement = screen.getByRole('listitem', {name: /empathy/i});
    expect(empathyElement).toHaveClass(/high/i);
  });

  test('shows trait tooltips on hover', async () => {
    render(<TraitsList traits={mockTraits} />);
    const empathyElement = screen.getByText('empathy');
    fireEvent.mouseEnter(empathyElement);

    // Tooltip should appear
    await screen.findByText(/Feel others' emotions/i);
  });

  test('handles empty traits', () => {
    render(<TraitsList traits={{}} />);
    expect(screen.getByText(/No traits/i)).toBeInTheDocument();
  });

  test('calculates average trait value', () => {
    render(<TraitsList traits={mockTraits} />);
    // Average should be displayed
    expect(screen.getByText(/average/i)).toBeInTheDocument();
  });
});
