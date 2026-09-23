# Open Generative AI -- vendored copy

Vendored from https://github.com/anil-matcha/open-generative-ai (MIT).
Open-source, self-hosted alternative to Higgsfield/Freepik/Krea/OpenArt --
image, video, lip-sync and "Cinema Studio" virtual-camera generation across
600+ models (Flux, Kling, Sora, Veo, etc.) via your own API keys, no
subscription.

**Note on content moderation:** this project positions itself as
"uncensored" / "no content filters" -- it does not apply its own content
moderation on top of whatever the underlying model provider does. Installed
and run here at explicit user request, verified working, but be aware of
that positioning before exposing it to end users or pointing it at anything
production-facing.

Not wired into reels_mvp.py or the Telegram bot -- installed and verified
as a standalone service, same as screenshot-to-code.

## Run it

```bash
cd open-generative-ai
npm run setup   # installs deps + builds workspace packages (studio, workflow, agents, design-agent)
npm run dev     # Next.js dev server -> http://localhost:3000 (redirects to /studio)
```

Verified in this session: `npm run setup` completed, `npm run dev` served
`/studio` with HTTP 200, screenshot confirmed the UI renders. You'll be
prompted for a Muapi (or per-model) API key on first generation; none is
configured here. Server was stopped after verification, not left running.

Desktop app alternative: `npm run electron:dev` (not tested here -- no
display server in this sandbox).
