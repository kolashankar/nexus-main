import React from "react";
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import RobotCard from '../RobotCard/RobotCard';

const mockRobot = {
  _id: 'robot123',
  name: 'Worker Bot Alpha',
  type: 'worker',
  level: 5,
  stats: {
    efficiency: 75,
    durability: 80,
    speed: 60,
  },
  price: 5000,
  owner_id: 'player456',
};

describe('RobotCard Component', () => {
  test('renders robot name', () => {
    render(<RobotCard robot={mockRobot} />);
    expect(screen.getByText('Worker Bot Alpha')).toBeInTheDocument();
  });

  test('displays robot type', () => {
    render(<RobotCard robot={mockRobot} />);
    expect(screen.getByText(/worker/i)).toBeInTheDocument();
  });

  test('shows robot level', () => {
    render(<RobotCard robot={mockRobot} />);
    expect(screen.getByText(/Level 5/i)).toBeInTheDocument();
  });

  test('displays robot stats', () => {
    render(<RobotCard robot={mockRobot} />);
    expect(screen.getByText(/75/)).toBeInTheDocument(); // efficiency
    expect(screen.getByText(/80/)).toBeInTheDocument(); // durability
    expect(screen.getByText(/60/)).toBeInTheDocument(); // speed
  });

  test('shows price for marketplace', () => {
    render(<RobotCard robot={mockRobot} mode="marketplace" />);
    expect(screen.getByText(/5,?000/)).toBeInTheDocument();
  });

  test('displays purchase button in marketplace mode', () => {
    render(<RobotCard robot={mockRobot} mode="marketplace" />);
    expect(screen.getByText(/purchase/i)).toBeInTheDocument();
  });

  test('shows upgrade button for owned robots', () => {
    render(<RobotCard robot={mockRobot} mode="owned" />);
    expect(screen.getByText(/upgrade/i)).toBeInTheDocument();
  });

  test('handles click event', () => {
    const handleClick = jest.fn();
    render(<RobotCard robot={mockRobot} onClick={handleClick} />);
    
    const card = screen.getByRole('button');
    fireEvent.click(card);
    
    expect(handleClick).toHaveBeenCalled();
  });

  test('displays robot 3D model preview', () => {
    render(<RobotCard robot={mockRobot} />);
    expect(screen.getByTestId('robot-3d-model')).toBeInTheDocument();
  });

  test('shows training progress', () => {
    const trainingRobot = { ...mockRobot, training_progress: 50 };
    render(<RobotCard robot={trainingRobot} mode="owned" />);
    expect(screen.getByText(/training/i)).toBeInTheDocument();
  });
});
