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

## ⚠ Known issue in the 16:9 render — pronunciation

The AI voiceover said "Planwrit" inconsistently across scenes (correctly in
some, mispronounced as "plan-writ" in the Scene 6 CTA line "Visit
Planwrit.com..."). **The correct pronunciation is "plan-rayt," as in "plan
write."** "Planwrit" is an invented brand word, so the TTS engine guesses at
it and isn't reliable given plain-text input alone.

**Client decision: option (b).** Keep the exact "Planwrit.com" spelling
on-screen — do not hyphenate or otherwise alter the visible brand spelling.
The AI voice must still say "plan-rayt" correctly.

**Constraint:** the Blotato `ai-story-video` template exposes no
phoneme/IPA/pronunciation-dictionary override — captions are burned in
directly from the literal `script` text per scene, and audio pronunciation
of an invented word is entirely up to the TTS engine's own guess. There is
no dial in this tool to decouple "what's displayed" from "how it's said."
Guaranteeing correct pronunciation while keeping the exact spelling is
therefore not 100% controllable through this pipeline — it needs empirical
testing, not a text trick.

**Test plan for next regeneration (before spending credits on the full
video):** run 2–3 cheap single-scene test clips of just the CTA line
("Visit Planwrit.com and claim your free assessment today.") with different
*formatting-only* variants that don't change the visible brand spelling —
e.g. casing changes (`PLANWRIT.com`, `Planwrit.COM`), spacing
(`Planwrit .com`), or punctuation around it — and listen for which one the
voice (Sarah) reads as "plan-rayt." Lock in whichever phrasing works for
both the corrected 16:9 CTA/Scene 3 lines and the pending 9:16
regeneration. If no variant reliably produces the correct pronunciation,
report that plainly rather than shipping an unverified guess.

Apply the winning phrasing to every scene where "Planwrit" is spoken
(Scene 3 and Scene 6 in the current script), not just the CTA.

## If you want the original manual-footage version instead

`script.md` retains the full original brief (Pexels search terms, Canva/
CapCut steps, ElevenLabs voiceover instructions) if you'd rather hand-build
the ad from real stock footage — nothing here overwrites that workflow.
