import React from "react";
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_FRONTEND_URL || 'http://localhost:3000';

test.describe('Authentication E2E Tests', () => {
  test('should complete full registration flow', async ({ page }) => {
    await page.goto(`${BASE_URL}/register`);

    // Fill registration form
    const timestamp = Date.now();
    await page.fill('input[name="username"]', `e2e_user_${timestamp}`);
    await page.fill('input[name="email"]', `e2e${timestamp}@test.com`);
    await page.fill('input[name="password"]', 'SecurePass123!');
    await page.fill('input[name="confirmPassword"]', 'SecurePass123!');

    // Submit registration
    await page.click('button[type="submit"]');

    // Wait for redirect to character creation or dashboard
    await page.waitForURL(/\/(character-creation|dashboard)/);

    // Verify user is logged in
    const userMenu = await page.locator('[data-testid="user-menu"]');
    await expect(userMenu).toBeVisible();
  });

  test('should login with existing credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);

    // Fill login form
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');

    // Submit login
    await page.click('button[type="submit"]');

    // Wait for redirect to dashboard
    await page.waitForURL(`${BASE_URL}/dashboard`);

    // Verify dashboard elements
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);

    await page.fill('input[name="username"]', 'nonexistent');
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    // Check for error message
    const errorMessage = await page.locator('[role="alert"]');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText(/invalid|incorrect/i);
  });

  test('should logout successfully', async ({ page }) => {
    // First login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);

    // Then logout
    await page.click('[data-testid="user-menu"]');
    await page.click('button:text("Logout")');

    // Verify redirect to landing/login page
    await page.waitForURL(/\/(login|\/)$/);
  });

  test('should persist login after page refresh', async ({ page }) => {
    // Login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);

    // Refresh page
    await page.reload();

    // Verify still logged in
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
    await expect(page).toHaveURL(`${BASE_URL}/dashboard`);
  });

  test('should redirect to login when accessing protected route', async ({ page }) => {
    await page.goto(`${BASE_URL}/profile`);

    // Should redirect to login
    await page.waitForURL(/\/login/);
  });
});
