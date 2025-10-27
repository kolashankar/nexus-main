import React from "react";
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_FRONTEND_URL || 'http://localhost:3000';

test.describe('Quests E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'quest_seeker');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
  });

  test('should navigate to quests page', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);
    await expect(page.locator('h1')).toContainText(/Quests/i);
  });

  test('should view available quests', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);

    await page.click('button:text("Available")');
    const quests = await page.locator('[data-testid="quest-card"]').all();
    console.log(`Available quests: ${quests.length}`);
  });

  test('should view active quests', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);

    await page.click('button:text("Active")');
    await expect(page.locator('[data-testid="active-quests"]')).toBeVisible();
  });

  test('should view quest details', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);

    const firstQuest = page.locator('[data-testid="quest-card"]').first();
    await expect(firstQuest).toBeVisible();
    await firstQuest.click();

    await expect(page.locator('[data-testid="quest-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="quest-description"]')).toBeVisible();
    await expect(page.locator('[data-testid="quest-objectives"]')).toBeVisible();
    await expect(page.locator('[data-testid="quest-rewards"]')).toBeVisible();
  });

  test('should accept a quest', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);
    await page.click('button:text("Available")');

    const firstQuest = page.locator('[data-testid="quest-card"]').first();
    await expect(firstQuest).toBeVisible();

    await firstQuest.click();
    await page.click('button:text("Accept")');

    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
    await expect(notification).toContainText(/accepted|started/i);
  });

  test('should view quest objectives progress', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);
    await page.click('button:text("Active")');

    const activeQuest = page.locator('[data-testid="quest-card"]').first();
    await expect(activeQuest).toBeVisible();
    await activeQuest.click();

    const objectives = await page.locator('[data-testid="objective-item"]').all();
    for (const obj of objectives) {
      await expect(obj).toHaveAttribute('data-progress');
    }
  });

  test('should view daily quests', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);
    await page.click('button:text("Daily")');

    await expect(page.locator('[data-testid="daily-quests"]')).toBeVisible();
    const dailyQuests = await page.locator('[data-testid="daily-quest-card"]').all();
    expect(dailyQuests.length).toBeLessThanOrEqual(3);
  });

  test('should view campaign', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests/campaign`);

    await expect(page.locator('[data-testid="campaign-viewer"]')).toBeVisible();
  });

  test('should abandon a quest', async ({ page }) => {
    await page.goto(`${BASE_URL}/quests`);
    await page.click('button:text("Active")');

    const activeQuest = page.locator('[data-testid="quest-card"]').first();
    await expect(activeQuest).toBeVisible();

    await activeQuest.click();
    await page.click('button:text("Abandon")');
    await page.click('button:text("Confirm")');

    const notification = await page.locator('[role="alert"]');
    await expect(notification).toBeVisible({ timeout: 5000 });
  });
});