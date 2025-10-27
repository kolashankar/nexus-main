import React from "react";
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_FRONTEND_URL || 'http://localhost:3000';

test.describe('Gameplay E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
  });

  test('should view player profile', async ({ page }) => {
    await page.goto(`${BASE_URL}/profile`);

    // Verify profile elements
    await expect(page.locator('h1')).toContainText(/Profile/i);
    await expect(page.locator('[data-testid="karma-score"]')).toBeVisible();
    await expect(page.locator('[data-testid="player-level"]')).toBeVisible();
  });

  test('should view and filter traits', async ({ page }) => {
    await page.goto(`${BASE_URL}/profile`);

    // Navigate to traits section
    await page.click('button:text("Traits")');

    // Wait for traits to load
    await page.waitForSelector('[data-testid="trait-item"]');

    // Filter by virtues
    await page.click('[data-testid="filter-virtues"]');
    const virtueTraits = await page.locator('[data-testid="trait-item"]').all();
    expect(virtueTraits.length).toBeGreaterThan(0);

    // Each visible trait should be a virtue
    for (const trait of virtueTraits) {
      const category = await trait.getAttribute('data-category');
      expect(category).toBe('virtue');
    }
  });

  test('should perform a game action (help)', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);

    // Click on actions menu
    await page.click('[data-testid="actions-menu"]');

    // Select help action
    await page.click('button:text("Help")');

    // Wait for target selection dialog
    await page.waitForSelector('[data-testid="target-selector"]');

    // Select first available player
    await page.click('[data-testid="player-target"]:first-child');

    // Confirm action
    await page.click('button:text("Confirm")');

    // Wait for success notification
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText(/success|helped/i);
  });

  test('should view skill tree', async ({ page }) => {
    await page.goto(`${BASE_URL}/skill-trees`);

    // Select a trait
    await page.click('[data-testid="trait-selector"]');
    await page.click('button:text("Empathy")');

    // Verify skill tree is displayed
    await expect(page.locator('[data-testid="skill-tree-canvas"]')).toBeVisible();
    await expect(page.locator('[data-testid="skill-node"]').first()).toBeVisible();
  });

  test('should view superpowers', async ({ page }) => {
    await page.goto(`${BASE_URL}/superpowers`);

    // Verify superpowers list
    await expect(page.locator('h1')).toContainText(/Superpowers/i);

    // Check if any powers are unlocked
    const unlockedPowers = await page.locator('[data-testid="power-unlocked"]').all();
    const lockedPowers = await page.locator('[data-testid="power-locked"]').all();

    expect(unlockedPowers.length + lockedPowers.length).toBeGreaterThan(0);
  });

  test('should view quests', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);

    // Verify quest sections
    await expect(page.locator('[data-testid="active-quests"]')).toBeVisible();
    await expect(page.locator('[data-testid="available-quests"]')).toBeVisible();

    // Click on a quest to view details
    const firstQuest = page.locator('[data-testid="quest-card"]').first();
    await expect(firstQuest).toBeVisible();
    await firstQuest.click();

    // Verify quest details modal
    await expect(page.locator('[data-testid="quest-details"]')).toBeVisible();
  });

  test('should navigate to marketplace', async ({ page }) => {
    await page.goto(`${BASE_URL}/marketplace`);

    // Verify marketplace tabs
    await expect(page.locator('button:text("Robots")')).toBeVisible();
    await expect(page.locator('button:text("Stocks")')).toBeVisible();
    await expect(page.locator('button:text("Properties")')).toBeVisible();

    // Switch to robots tab
    await page.click('button:text("Robots")');
    await expect(page.locator('[data-testid="robot-card"]').first()).toBeVisible();
  });

  test('should view leaderboards', async ({ page }) => {
    await page.goto(`${BASE_URL}/leaderboards`);

    // Verify leaderboard categories
    await expect(page.locator('button:text("Karma")')).toBeVisible();
    await expect(page.locator('button:text("Wealth")')).toBeVisible();
    await expect(page.locator('button:text("Power")')).toBeVisible();

    // Check karma leaderboard
    await page.click('button:text("Karma")');
    const leaderboardEntries = await page.locator('[data-testid="leaderboard-entry"]').all();
    expect(leaderboardEntries.length).toBeGreaterThan(0);
  });

  test('should view world events', async ({ page }) => {
    await page.goto(`${BASE_URL}/world`);

    // Verify world events panel
    await expect(page.locator('[data-testid="world-events-panel"]')).toBeVisible();

    // Check for active events
    const activeEvents = await page.locator('[data-testid="active-event"]').all();
    console.log(`Active events: ${activeEvents.length}`);
  });

  test('should access inventory', async ({ page }) => {
    await page.goto(`${BASE_URL}/profile`);

    // Navigate to inventory
    await page.click('button:text("Inventory")');

    // Verify inventory grid
    await expect(page.locator('[data-testid="inventory-grid"]')).toBeVisible();
  });
});