# Production Notes — Planwrit Quick Ad, Version A

## How this video was produced

No Pexels API key or stock-footage-download connector was available in this
environment, so the video was generated end-to-end with the **Blotato "AI
Story Video"** pipeline (AI-generated + animated scenes, ElevenLabs
voiceover, burned-in captions) instead of the manual Canva/CapCut + Pexels
workflow described in `script.md`. Each of the script's 6 scenes was mapped
to one or more AI-generated scenes, with Scene 4's five stock-footage cuts
split into five individual scenes:

| Script scene | AI scenes | Voiceover / caption text |
|---|---|---|
| 1 — Hook | 1 | "Most business plans answer the wrong question." |
| 2 — Agitate | 1 | "The person reading your plan has one question. Most plans never answer it. We build plans that do." |
| 3 — Solution | 1 | "At Planwrit, we write immigration and business plans built to the exact standard of the person reviewing them." |
| 4 — Services | 5 (one per cut) | "C11 owner-operator plans." / "PNP entrepreneur streams." / "E2 investor visa." / "Pitch decks." / "Canadian grants." |
| 5 — Trust signal | 1 | "Every client starts with a free five minute eligibility assessment, honest feedback, no commitment." |
| 6 — CTA | 1 | "Visit Planwrit dot com and claim your free assessment today." |

**Voice:** Sarah (American, soft) — closest available match to the
Rachel/Bella-style warm, professional voice recommended in the original
script.

**Captions:** center position, gold highlight (`#C9A84C`) matching the
brand accent color specified in `script.md`.

**Transition:** fade between scenes (matches the "subtle cinematic"
direction).

**Motion:** AI-generated scene images were animated (`animateAiImages:
true`) rather than static, to approximate the stock-footage motion in the
original brief.

**Exports:**
- `assets/planwrit-quick-ad-version-a-16x9.mp4` — 1920×1080, for YouTube
- `assets/planwrit-quick-ad-version-a-9x16.mp4` — 1080×1920, for Reels/TikTok/Shorts

## If you want the original manual-footage version instead

`script.md` retains the full original brief (Pexels search terms, Canva/
CapCut steps, ElevenLabs voiceover instructions) if you'd rather hand-build
the ad from real stock footage — nothing here overwrites that workflow.
