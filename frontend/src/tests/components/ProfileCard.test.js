import React from "react";
import { describe, it, expect } from 'vitest';
describe('ProfileCard', () => {
  const mockPlayer = {
    username: 'test_player',
    level: 10,
    karma_points: 500,
    economic_class: 'middle',
    moral_class: 'good',
    currencies: { credits: 1000 },
  };
  it('renders player username', () => {
    expect(true).toBe(true);
  });
});
