# browser-agent

Raw-Playwright browser automation for this sandbox, where the official
`@playwright/mcp` server (configured in `.mcp.json`) fails to connect
because it looks for a system Chrome binary that doesn't exist here.
Uses the Chromium already vendored at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome` instead.

## gmail-search.mjs

Replicates the "search Gmail for X" demo (as seen in the Playwright MCP
promo reel) without going through MCP.

**Setup (once, on your own machine — never in this sandbox):**
```
npx playwright open --save-storage=state.json https://mail.google.com
```
Log into Gmail normally in the window that opens, close it, then copy
the generated `state.json` into this folder.

**Why not automate the login too?** Google actively detects and blocks
automated/headless sign-in on its own login form as suspicious activity.
This script never touches your password — it only replays a session you
created yourself in a real browser. `state.json` and `profile/` are
gitignored; never commit them, they're equivalent to a logged-in session.

**Run:**
```
node gmail-search.mjs "contractor invoice receipt renovation"
```
Prints the top 20 matching messages as JSON (subject/sender/snippet).

**For an unattended pipeline** (no human login step, ever) use the
Gmail API with OAuth instead of scraping the web UI — that's the
supported, ToS-compliant way to search mail programmatically.
