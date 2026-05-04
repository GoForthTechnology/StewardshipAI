# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: verify-styles.spec.ts >> Stewardship Portal Branding >> should apply diocese-blue background to sidebar
- Location: verify-styles.spec.ts:4:7

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: "rgb(26, 58, 90)"
Received: "rgba(0, 0, 0, 0)"
```

# Page snapshot

```yaml
- generic [ref=e5]:
  - generic [ref=e6]:
    - heading "🕊️ Stewardship Portal" [level=1] [ref=e7]
    - paragraph [ref=e8]: Catholic Diocese of Wichita
  - button "Google Sign in with Google" [ref=e9]:
    - img "Google" [ref=e10]
    - text: Sign in with Google
  - paragraph [ref=e12]: Please sign in with your authorized account.
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Stewardship Portal Branding', () => {
  4  |   test('should apply diocese-blue background to sidebar', async ({ page }) => {
  5  |     // We assume the app is running on localhost:8080 (Docker default)
  6  |     // If not running, this will fail, which is expected for verification.
  7  |     await page.goto('http://localhost:8080');
  8  |     
  9  |     // Wait for the login screen or portal to load
  10 |     await page.waitForSelector('body');
  11 | 
  12 |     // Check for the diocese-blue color on a known element
  13 |     // The sidebar in PortalComponent has class "bg-diocese-blue"
  14 |     // The login button in LoginComponent has class "bg-diocese-blue"
  15 |     
  16 |     const loginButton = page.locator('button:has-text("Sign in with Google")');
  17 |     if (await loginButton.isVisible()) {
  18 |       const bgColor = await loginButton.evaluate((el) => window.getComputedStyle(el).backgroundColor);
  19 |       // #1a3a5a in RGB is rgb(26, 58, 90)
> 20 |       expect(bgColor).toBe('rgb(26, 58, 90)');
     |                       ^ Error: expect(received).toBe(expected) // Object.is equality
  21 |     } else {
  22 |       const sidebar = page.locator('aside');
  23 |       const bgColor = await sidebar.evaluate((el) => window.getComputedStyle(el).backgroundColor);
  24 |       expect(bgColor).toBe('rgb(26, 58, 90)');
  25 |     }
  26 |   });
  27 | 
  28 |   test('should apply diocese-cream background to main content', async ({ page }) => {
  29 |     await page.goto('http://localhost:8080');
  30 |     const body = page.locator('body');
  31 |     const bgColor = await body.evaluate((el) => window.getComputedStyle(el).backgroundColor);
  32 |     // #fcfaf5 in RGB is rgb(252, 250, 245)
  33 |     expect(bgColor).toBe('rgb(252, 250, 245)');
  34 |   });
  35 | });
  36 | 
```