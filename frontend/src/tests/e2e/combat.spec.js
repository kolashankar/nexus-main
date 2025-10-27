import React from "react";
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_FRONTEND_URL || 'http://localhost:3000';

test.describe('Combat E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'fighter_test');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
  });

  test('should navigate to combat arena', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat`);

    // Verify combat page elements
    await expect(page.locator('h1')).toContainText(/Combat|Arena/i);
    await expect(page.locator('[data-testid="combat-stats"]')).toBeVisible();
  });

  test('should view combat stats', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat`);

    // Check combat stats display
    await expect(page.locator('[data-testid="hp-display"]')).toBeVisible();
    await expect(page.locator('[data-testid="attack-display"]')).toBeVisible();
    await expect(page.locator('[data-testid="defense-display"]')).toBeVisible();

    // Verify stats have numeric values
    const hpText = await page.locator('[data-testid="hp-display"]').textContent();
    expect(hpText).toMatch(/\d+/);
  });

  test('should challenge another player', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat`);

    // Click challenge button
    await page.click('button:text("Challenge")');

    // Wait for player list
    await page.waitForSelector('[data-testid="player-list"]');

    // Select first available player
    const firstPlayer = page.locator('[data-testid="challenge-target"]').first();
    await expect(firstPlayer).toBeVisible();
    await firstPlayer.click();

    // Confirm challenge
    await page.click('button:text("Confirm")');

    // Wait for confirmation
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
  });

  test('should display action bar during combat', async ({ page }) => {
    // This test assumes an active combat session exists at this URL
    await page.goto(`${BASE_URL}/combat/active`);

    // Verify action bar and buttons are visible
    await expect(page.locator('[data-testid="action-bar"]')).toBeVisible();
    await expect(page.locator('button:text("Attack")')).toBeVisible();
    await expect(page.locator('button:text("Defend")')).toBeVisible();
  });

  test('should perform attack action', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/active`);

    // Click attack button
    await page.click('button:text("Attack")');

    // Wait for combat log update and verify its content
    const latestLogEntry = page.locator('[data-testid="combat-log-entry"]').first();
    await expect(latestLogEntry).toContainText(/attack|hit|damage/i, { timeout: 5000 });
  });

  test('should use superpower in combat', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/active`);
    
    // Open powers menu
    await page.click('button:text("Powers")');

    // Select first available power
    const firstPower = page.locator('[data-testid="combat-power"]').first();
    await expect(firstPower).toBeVisible();
    await firstPower.click();

    // Confirm power usage
    await page.click('button:text("Use Power")');

    // Verify power was used
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
  });

  test('should display health bars', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/active`);
    
    // Verify player and opponent health bars are visible
    await expect(page.locator('[data-testid="player-health-bar"]')).toBeVisible();
    await expect(page.locator('[data-testid="opponent-health-bar"]')).toBeVisible();
  });

  test('should view combat history', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/history`);

    // Verify combat history page
    await expect(page.locator('h1')).toContainText(/History|Past Battles/i);

    // Check for battle records
    const firstRecord = page.locator('[data-testid="battle-record"]').first();
    await expect(firstRecord).toBeVisible();

    // Click on first battle to view details
    await firstRecord.click();

    // Verify battle details
    await expect(page.locator('[data-testid="battle-details"]')).toBeVisible();
  });

  test('should join arena queue', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/arena`);

    // Click join queue button
    await page.click('button:text("Join Queue")');

    // Verify in queue
    const queueStatus = await page.locator('[data-testid="queue-status"]');
    await expect(queueStatus).toContainText(/queue|waiting/i, { timeout: 5000 });
  });

  test('should display arena rankings', async ({ page }) => {
    await page.goto(`${BASE_URL}/combat/arena`);

    // Navigate to rankings tab
    await page.click('button:text("Rankings")');

    // Verify rankings list
    await expect(page.locator('[data-testid="arena-rankings"]')).toBeVisible();

    const rankings = await page.locator('[data-testid="rank-entry"]').all();
    expect(rankings.length).toBeGreaterThan(0);
  });
});