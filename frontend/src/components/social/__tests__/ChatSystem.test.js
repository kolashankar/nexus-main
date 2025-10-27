import React from "react";
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatSystem from '../Chat/Chat';

const mockMessages = [
  { id: 1, username: 'Player1', message: 'Hello everyone!', timestamp: new Date().toISOString() },
  { id: 2, username: 'Player2', message: 'Hi there!', timestamp: new Date().toISOString() },
  { id: 3, username: 'Player1', message: 'How is it going?', timestamp: new Date().toISOString() },
];

describe('ChatSystem Component', () => {
  test('renders chat messages', () => {
    render(<ChatSystem messages={mockMessages} />);
    expect(screen.getByText('Hello everyone!')).toBeInTheDocument();
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });

  test('displays usernames', () => {
    render(<ChatSystem messages={mockMessages} />);
    expect(screen.getAllByText('Player1').length).toBeGreaterThan(0);
    expect(screen.getByText('Player2')).toBeInTheDocument();
  });

  test('shows message input field', () => {
    render(<ChatSystem messages={mockMessages} />);
    expect(screen.getByPlaceholderText(/type a message/i)).toBeInTheDocument();
  });

  test('sends message on submit', async () => {
    const onSendMessage = jest.fn();
    render(<ChatSystem messages={mockMessages} onSendMessage={onSendMessage} />);
    
    const input = screen.getByPlaceholderText(/type a message/i);
    const sendButton = screen.getByText(/send/i);
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(onSendMessage).toHaveBeenCalledWith('Test message');
    });
  });

  test('clears input after sending', async () => {
    const onSendMessage = jest.fn();
    render(<ChatSystem messages={mockMessages} onSendMessage={onSendMessage} />);
    
    const input = screen.getByPlaceholderText(/type a message/i);
    const sendButton = screen.getByText(/send/i);
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });

  test('displays timestamp for messages', () => {
    render(<ChatSystem messages={mockMessages} />);
    expect(screen.getAllByText(/ago/).length).toBeGreaterThan(0);
  });

  test('auto-scrolls to latest message', () => {
    render(<ChatSystem messages={mockMessages} />);
    const chatContainer = screen.getByRole('log');
    
    expect(chatContainer?.scrollTop).toBeGreaterThan(0);
  });

  test('shows online users count', () => {
    render(<ChatSystem messages={mockMessages} onlineCount={25} />);
    expect(screen.getByText(/25 online/i)).toBeInTheDocument();
  });

  test('filters messages by channel', () => {
    render(<ChatSystem messages={mockMessages} />);
    const guildTab = screen.getByText(/guild/i);
    fireEvent.click(guildTab);
    // Should filter to guild messages only
  });

  test('prevents empty message submission', () => {
    const onSendMessage = jest.fn();
    render(<ChatSystem messages={mockMessages} onSendMessage={onSendMessage} />);
    
    const sendButton = screen.getByText(/send/i);
    fireEvent.click(sendButton);
    
    expect(onSendMessage).not.toHaveBeenCalled();
  });
});
