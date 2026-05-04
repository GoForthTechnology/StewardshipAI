import { test, expect } from '@playwright/test';

test.describe('Stewardship Portal Branding', () => {
  test('should apply diocese-blue background to sidebar', async ({ page }) => {
    // We assume the app is running on localhost:8080 (Docker default)
    // If not running, this will fail, which is expected for verification.
    await page.goto('http://localhost:8080');
    
    // Wait for the login screen or portal to load
    await page.waitForSelector('body');

    // Check for the diocese-blue color on a known element
    // The sidebar in PortalComponent has class "bg-diocese-blue"
    // The login button in LoginComponent has class "bg-diocese-blue"
    
    const loginButton = page.locator('button:has-text("Sign in with Google")');
    if (await loginButton.isVisible()) {
      const bgColor = await loginButton.evaluate((el) => window.getComputedStyle(el).backgroundColor);
      // #1a3a5a in RGB is rgb(26, 58, 90)
      expect(bgColor).toBe('rgb(26, 58, 90)');
    } else {
      const sidebar = page.locator('aside');
      const bgColor = await sidebar.evaluate((el) => window.getComputedStyle(el).backgroundColor);
      expect(bgColor).toBe('rgb(26, 58, 90)');
    }
  });

  test('should apply diocese-cream background to main content', async ({ page }) => {
    await page.goto('http://localhost:8080');
    const body = page.locator('body');
    const bgColor = await body.evaluate((el) => window.getComputedStyle(el).backgroundColor);
    // #fcfaf5 in RGB is rgb(252, 250, 245)
    expect(bgColor).toBe('rgb(252, 250, 245)');
  });
});
