#!/usr/bin/env node
// Browser automation replicating the "Playwright MCP" Gmail-search demo,
// using the raw `playwright` npm package instead of the MCP wrapper
// (the MCP server needs a system Chrome binary this sandbox doesn't have,
// and this sandbox has no display for a human to log in interactively).
//
// Setup (once, on YOUR OWN machine, not in this sandbox):
//   npx playwright open --save-storage=state.json https://mail.google.com
//   -> log into Gmail normally in the window that opens, then close it.
//   -> copy the resulting state.json into tools/browser-agent/state.json
//
// Google actively flags automated/headless sign-in on its own login form
// as suspicious. This tool never touches your password — it only replays
// a session you created yourself in a real browser, then automates the
// search. For an unattended pipeline with no human login step at all, use
// the Gmail API with OAuth instead of scraping the web UI.
//
// Usage:
//   node gmail-search.mjs "contractor invoice receipt renovation"

import { chromium } from 'playwright';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_FILE = path.join(__dirname, 'state.json');
const CHROMIUM_PATH = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const query = process.argv[2];
if (!query) {
  console.error('Usage: node gmail-search.mjs "<search query>"');
  process.exit(1);
}

if (!existsSync(STATE_FILE)) {
  console.error(
    `Missing ${STATE_FILE}.\n` +
    'On your own machine, run:\n' +
    '  npx playwright open --save-storage=state.json https://mail.google.com\n' +
    'log into Gmail in the window that opens, close it, then copy the\n' +
    'generated state.json into tools/browser-agent/state.json here.'
  );
  process.exit(1);
}

const browser = await chromium.launch({
  executablePath: CHROMIUM_PATH,
  headless: true,
  args: ['--no-sandbox'],
});
const context = await browser.newContext({ storageState: STATE_FILE });
const page = await context.newPage();

await page.goto('https://mail.google.com/mail/u/0/#inbox', { waitUntil: 'domcontentloaded' });

const loggedIn = await page
  .locator('input[aria-label="Search mail"]')
  .first()
  .isVisible({ timeout: 10_000 })
  .catch(() => false);

if (!loggedIn) {
  console.error('Session expired or invalid — regenerate state.json (see setup above).');
  await browser.close();
  process.exit(1);
}

await page.fill('input[aria-label="Search mail"]', query);
await page.keyboard.press('Enter');
await page.waitForSelector('tr.zA', { timeout: 15_000 }).catch(() => {});

const results = await page.$$eval('tr.zA', (rows) =>
  rows.slice(0, 20).map((row) => ({
    subject: row.querySelector('.bog')?.textContent?.trim() ?? '',
    sender: row.querySelector('.yX.xY, .yW span[email]')?.textContent?.trim() ?? '',
    snippet: row.querySelector('.y2')?.textContent?.trim() ?? '',
  }))
);

console.log(JSON.stringify(results, null, 2));

await browser.close();
