# Planwrit Quick Ad — Version A — Generated Video

| Format | Use case | Status | Source |
|---|---|---|---|
| 16:9 (1920x1080) | YouTube | Done | Blotato "AI Story Video" pipeline (AI voiceover + AI-generated scenes). See "16:9 render" below for the link and known pronunciation issue. |
| 9:16 (1080x1920) | Reels / TikTok / Shorts | Done | Built locally — `assets/planwrit-quick-ad-version-a-9x16.mp4` (committed to this repo). See "9:16 render" below. |

## 16:9 render (Blotato)

Generated via the Blotato "AI Story Video" pipeline (see `production-notes.md`
for how the script maps to scenes/voice/captions). This link points to the
hosted render on Blotato's media storage — review/download it from the
Blotato platform (my.blotato.com) or the direct link below.

https://database.blotato.io/storage/v1/object/public/public_media/e8685257-d3de-42f3-8e37-5d22e4352bbd/videogen2-render-9cec2e03-dd3d-4c5b-8913-1e009097bf47.mp4

**Known issue:** AI voiceover mispronounces "Planwrit" inconsistently
(should be "plan-rayt"). See the pronunciation section in
`production-notes.md`. Not yet corrected in this render.

## 9:16 render (built locally, no AI voiceover/generation)

`assets/planwrit-quick-ad-version-a-9x16.mp4` — committed directly to this
repo (no blocked external host involved, since it's rendered locally).

Built entirely in Python (Pillow + ffmpeg) instead of via Blotato, because:
- The Blotato account ran out of credits after the 16:9 render.
- This avoids the AI-voiceover pronunciation problem entirely — this
  version is silent/text-only (matches the "TEXT-ONLY VERSION" already
  described in `script.md`), so there's no "Planwrit" mispronunciation risk.

Uses real assets instead of AI-generated ones:
- 15 Pexels stock photos (client-sourced, uploaded to Google Drive, matching
  the original search-term table in `script.md`)
- 2 personal Toronto landmark photos (CN Tower, Front St W office tower)
- The actual Planwrit logo (background removed, composited transparently)

Full asset mapping, code, and how to re-render are in `production-notes.md`
and `render_9x16.py`.
