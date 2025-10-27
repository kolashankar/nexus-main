import React from "react";
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MarketStocks from '../StockMarket/MarketStocks';

const mockStocks = [
  { ticker: 'ROBOT', name: 'Robot Corp', price: 150.5, change_24h: 5.2 },
  { ticker: 'CYBER', name: 'Cyber Security Inc', price: 89.75, change_24h: -2.1 },
  { ticker: 'MED', name: 'MediTech', price: 210.0, change_24h: 0 },
];

describe('MarketStocks Component', () => {
  test('renders stock list', () => {
    render(<MarketStocks stocks={mockStocks} />);
    expect(screen.getByText('Robot Corp')).toBeInTheDocument();
    expect(screen.getByText('Cyber Security Inc')).toBeInTheDocument();
  });

  test('displays stock tickers', () => {
    render(<MarketStocks stocks={mockStocks} />);
    expect(screen.getByText('ROBOT')).toBeInTheDocument();
    expect(screen.getByText('CYBER')).toBeInTheDocument();
  });

  test('shows stock prices', () => {
    render(<MarketStocks stocks={mockStocks} />);
    expect(screen.getByText(/150\.50/)).toBeInTheDocument();
    expect(screen.getByText(/89\.75/)).toBeInTheDocument();
  });

  test('displays positive change in green', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const positiveChange = screen.getByText(/\+5\.2/i);
    expect(positiveChange).toHaveClass(/positive|green|up/i);
  });

  test('displays negative change in red', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const negativeChange = screen.getByText(/-2\.1/i);
    expect(negativeChange).toHaveClass(/negative|red|down/i);
  });

  test('shows buy button for each stock', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const buyButtons = screen.getAllByText(/buy/i);
    expect(buyButtons.length).toBe(mockStocks.length);
  });

  test('opens buy modal on buy button click', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const buyButton = screen.getAllByText(/buy/i)[0];
    fireEvent.click(buyButton);
    
    expect(screen.getByText(/purchase/i)).toBeInTheDocument();
  });

  test('displays stock chart on click', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const stockRow = screen.getByRole('row', { name: /Robot Corp/i });
    fireEvent.click(stockRow);
    
    expect(screen.getByTestId('stock-chart')).toBeInTheDocument();
  });

  test('shows portfolio if user owns stocks', () => {
    const portfolio = [{ ticker: 'ROBOT', shares: 10, avg_price: 145.0 }];
    render(<MarketStocks stocks={mockStocks} portfolio={portfolio} />);
    
    expect(screen.getByText(/portfolio/i)).toBeInTheDocument();
    expect(screen.getByText(/10 shares/i)).toBeInTheDocument();
  });

  test('calculates profit/loss', () => {
    const portfolio = [{ ticker: 'ROBOT', shares: 10, avg_price: 145.0 }];
    render(<MarketStocks stocks={mockStocks} portfolio={portfolio} />);
    
    // Profit = (150.50 - 145.00) * 10 = 55.00
    expect(screen.getByText(/\+55/)).toBeInTheDocument();
  });

  test('sorts stocks by change', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const sortButton = screen.getByText(/sort/i);
    fireEvent.click(sortButton);
    
    // Should re-render in sorted order
  });

  test('filters stocks by search', () => {
    render(<MarketStocks stocks={mockStocks} />);
    const searchInput = screen.getByPlaceholderText(/search/i);
    fireEvent.change(searchInput, { target: { value: 'Robot' } });
    
    expect(screen.getByText('Robot Corp')).toBeInTheDocument();
    expect(screen.queryByText('Cyber Security Inc')).not.toBeInTheDocument();
  });
});
