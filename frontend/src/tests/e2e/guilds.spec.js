import React from "react";
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_FRONTEND_URL || 'http://localhost:3000';

test.describe('Guilds E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'guild_member');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
  });

  test('should view guild list', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds`);

    // Verify guilds page
    await expect(page.locator('h1')).toContainText(/Guilds/i);

    // Check for guild cards
    const guildCards = await page.locator('[data-testid="guild-card"]').all();
    expect(guildCards.length).toBeGreaterThan(0);
  });

  test('should view guild details', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds`);

    // Click on first guild
    const firstGuild = page.locator('[data-testid="guild-card"]').first();
    await firstGuild.click();

    // Verify guild details page
    await expect(page.locator('[data-testid="guild-name"]')).toBeVisible();
    await expect(page.locator('[data-testid="guild-description"]')).toBeVisible();
    await expect(page.locator('[data-testid="member-list"]')).toBeVisible();
  });

  test('should create a new guild', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds`);

    // Click create guild button
    await page.click('button:text("Create Guild")');

    // Fill guild creation form
    const timestamp = Date.now();
    await page.fill('input[name="name"]', `E2E Guild ${timestamp}`);
    await page.fill('input[name="tag"]', `E2E${timestamp.toString().slice(-3)}`);
    await page.fill('textarea[name="description"]', 'Test guild created by E2E tests');

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for success notification
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
    await expect(notification).toContainText(/created|success/i);
  });

  test('should join a guild', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds`);

    // Find a guild with open recruitment
    const openGuild = page
      .locator('[data-testid="guild-card"]')
      .filter({ hasText: 'Open' })
      .first();

    await expect(openGuild).toBeVisible();
    await openGuild.click();

    // Click join button
    await page.click('button:text("Join")');

    // Confirm join
    await page.click('button:text("Confirm")');

    // Wait for confirmation
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
  });

  test('should view guild members', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Navigate to members tab
    await page.click('button:text("Members")');

    // Verify member list
    await expect(page.locator('[data-testid="member-list"]')).toBeVisible();

    const members = await page.locator('[data-testid="member-item"]').all();
    expect(members.length).toBeGreaterThan(0);
  });

  test('should view guild territories', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Navigate to territories tab
    await page.click('button:text("Territories")');

    // Verify territory map
    await expect(page.locator('[data-testid="territory-map"]')).toBeVisible();
  });

  test('should view guild wars', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Navigate to wars tab
    await page.click('button:text("Wars")');

    // Verify wars section
    await expect(page.locator('[data-testid="guild-wars"]')).toBeVisible();

    // Check for active wars
    const activeWars = await page.locator('[data-testid="active-war"]').all();
    console.log(`Active wars: ${activeWars.length}`);
  });

  test('should contribute to guild bank', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Navigate to bank tab
    await page.click('button:text("Bank")');

    // Click contribute button
    await page.click('button:text("Contribute")');

    // Enter contribution amount
    await page.fill('input[name="amount"]', '1000');

    // Submit contribution
    await page.click('button[type="submit"]');

    // Wait for confirmation
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
  });

  test('should view guild quests', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Navigate to quests tab
    await page.click('button:text("Quests")');

    // Verify guild quests
    await expect(page.locator('[data-testid="guild-quests"]')).toBeVisible();

    // Check for available quests
    const availableQuests = await page.locator('[data-testid="guild-quest-card"]').all();
    console.log(`Guild quests available: ${availableQuests.length}`);
  });

  test('should leave guild', async ({ page }) => {
    await page.goto(`${BASE_URL}/guilds/my-guild`);

    // Open guild settings
    await page.click('[data-testid="guild-settings"]');

    // Click leave guild
    await page.click('button:text("Leave Guild")');

    // Confirm leaving
    await page.click('button:text("Confirm")');

    // Wait for confirmation
    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
    await expect(notification).toContainText(/left|departed/i);
  });
});