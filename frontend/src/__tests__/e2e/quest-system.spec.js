import React from "react";
/**
 * E2E tests for quest system
 * Tests the complete quest workflow from a user perspective
 */

import { test, expect } from '@playwright/test';

test.describe('Quest System E2E', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('should display available quests', async ({ page }) => {
    await page.goto('/quests');

    // Wait for quests to load
    await page.waitForSelector('[data-testid="quest-card"]', { timeout: 5000 });

    // Check that quests are displayed
    const quests = await page.locator('[data-testid="quest-card"]').count();
    expect(quests).toBeGreaterThan(0);
  });

  test('should accept a quest', async ({ page }) => {
    await page.goto('/quests');
    await page.waitForSelector('[data-testid="quest-card"]');

    // Click on first quest
    await page.click('[data-testid="quest-card"]:first-child');

    // Wait for quest details
    await page.waitForSelector('[data-testid="quest-details"]');

    // Accept quest
    await page.click('button:text("Accept")');

    // Check for success message
    await expect(page.locator('text=Quest Accepted')).toBeVisible();

    // Verify quest is in active tab
    await page.click('[data-testid="active-quests-tab"]');
    await page.waitForSelector('[data-testid="active-quest-card"]');
  });

  test('should display daily quests', async ({ page }) => {
    await page.goto('/quests');

    // Click daily quests tab
    await page.click('[data-testid="daily-quests-tab"]');

    // Wait for daily quests
    await page.waitForSelector('[data-testid="daily-quest-card"]', { timeout: 5000 });

    // Check that daily quests are displayed
    const dailyQuests = await page.locator('[data-testid="daily-quest-card"]').count();
    expect(dailyQuests).toBeGreaterThanOrEqual(0);
  });

  test('should show quest progress', async ({ page }) => {
    await page.goto('/quests');
    await page.click('[data-testid="active-quests-tab"]');

    // Wait for active quest
    const activeQuest = page.locator('[data-testid="active-quest-card"]').first();
    await activeQuest.waitFor({ timeout: 5000 });

    // Check for progress bar
    await expect(activeQuest.locator('[role="progressbar"]')).toBeVisible();

    // Check for objective counts
    await expect(activeQuest.locator('text=/\d+\/\d+/')).toBeVisible();
  });

  test('should abandon a quest', async ({ page }) => {
    await page.goto('/quests');
    await page.click('[data-testid="active-quests-tab"]');

    // Click on first active quest
    await page.click('[data-testid="active-quest-card"]:first-child');

    // Wait for quest details
    await page.waitForSelector('[data-testid="quest-details"]');

    // Abandon quest
    await page.click('button:text("Abandon")');

    // Confirm abandonment (if dialog appears)
    if (await page.locator('button:text("Confirm")').isVisible()) {
      await page.click('button:text("Confirm")');
    }

    // Check for success message
    await expect(page.locator('text=Quest Abandoned')).toBeVisible();
  });

  test('should display hidden quests', async ({ page }) => {
    await page.goto('/quests');

    // Click hidden quests tab
    await page.click('[data-testid="hidden-quests-tab"]');

    // Check for hints section
    await expect(page.locator('text=Cryptic Hints')).toBeVisible();
  });

  test('should start a campaign', async ({ page }) => {
    await page.goto('/quests');

    // Click campaigns tab
    await page.click('[data-testid="campaigns-tab"]');

    // Wait for campaigns
    await page.waitForSelector('[data-testid="campaign-card"]', { timeout: 5000 });

    // Click on first campaign
    await page.click('[data-testid="campaign-card"]:first-child');

    // Start campaign
    await page.click('button:text("Start Campaign")');

    // Check that campaign started
    await expect(page.locator('text=Campaign Started')).toBeVisible();
  });

  test('should filter quests by type', async ({ page }) => {
    await page.goto('/quests');

    // Check tabs are present
    await expect(page.locator('text=Active')).toBeVisible();
    await expect(page.locator('text=Daily')).toBeVisible();
    await expect(page.locator('text=Weekly')).toBeVisible();
    await expect(page.locator('text=World')).toBeVisible();
    await expect(page.locator('text=Hidden')).toBeVisible();
    await expect(page.locator('text=Guild')).toBeVisible();
  });

  test('should display quest rewards', async ({ page }) => {
    await page.goto('/quests');
    await page.waitForSelector('[data-testid="quest-card"]');

    // Click on first quest
    await page.click('[data-testid="quest-card"]:first-child');

    // Wait for quest details
    await page.waitForSelector('[data-testid="quest-details"]');

    // Check for rewards section
    await expect(page.locator('text=Rewards')).toBeVisible();

    // Check for reward types
    const rewardsSection = page.locator('[data-testid="quest-rewards"]');
    await expect(rewardsSection).toBeVisible();
  });
});
