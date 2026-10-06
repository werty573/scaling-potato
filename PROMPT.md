# Claude Code prompt — "Soda" ad-grade landing page

Copy everything below the line into Claude Code (run it inside this repo).

Before you run it:
1. Save the full original "Recreate this site as a single HTML file: Soda" spec as `reference/spec.md`. The copy pasted in chat was cut off partway through section 4, so the **Assets** section (the URLs for `LEAVES_GLB`, `CHERRY_GLB`, `DEIT_SODA2_GLB`, `GREEN_SODA_PNG`, `BLUE_SODA_PNG`, the bubble PNGs and the blueberry GLB) and the JavaScript section are missing.
2. Download the reference reel yourself (for example with a reel-downloader site, or by saving it from the Instagram app) and commit it as `reference/reel.mp4`. Instagram blocks most cloud and server downloads, so Claude Code probably won't be able to fetch it on its own.

---

You are building a premium, ad-quality product landing page for a fictional drink called **"Soda" (Diet Soda)**. The finished page will be screen-recorded and cut into an **Instagram Reel ad (9:16)**, so it has to look good both as a desktop website and as a vertical video. Go all out: this should look like an award-winning brand site, not a template.

## Inputs (read them all before writing any code)

1. **`reference/spec.md`**: a detailed spec of a base site (a full-viewport hero with a 3D can in `<model-viewer>`, cherry and leaf GLB models with parallax and cursor repulsion, rising PNG bubbles, a glass header, and a flavor carousel that switches between a teal "Classic" theme and a blue "Zero Lime" theme with a 720° can spin, a texture swap and a berry implode/explode). Treat it as the **minimum baseline**. Every layout, CSS value, interaction and asset URL in it must be kept unless this prompt says to go further.
   - If `reference/spec.md` is missing or has no Assets section, stop and ask me for it. Don't invent asset URLs. If I tell you to continue without it, use free CC0 GLB models (for example from Poly Pizza or the Khronos glTF samples) and generated PNGs, save them under `assets/`, and list where each one came from in the README.

2. **Reference Instagram reel** (the ad style I want): https://www.instagram.com/reel/DdAgrCAO4km/
   - First look for `reference/reel.mp4`. If it isn't there, try to download the reel with `yt-dlp` (`pip install yt-dlp`). If Instagram blocks the download (it usually does from servers), tell me and ask me to commit the file. Don't guess what the reel looks like.
   - **Analyze the video.** Use `ffmpeg` to pull frames: one every 0.5s, plus scene-change frames with `-vf "select='gt(scene,0.3)',showinfo"`. Look at those frames and write `reference/reel-analysis.md` covering: the shot-by-shot structure with timestamps, the camera moves, the transitions, typography (font style, size, how text animates on and off), the colour palette (hex values), how the product is staged, the pacing, and the visual tricks to copy.
   - **Analyze the music.** Extract the audio (`ffmpeg -i reel.mp4 -vn audio.wav`). Use `librosa` (`pip install librosa`) to get the BPM, the beat timestamps, the onsets and strong drops/accents, and the energy curve over time. Add a "Music" section to the analysis: BPM, genre and mood, key moments (intro, build, drop) with timestamps, and a beat grid that the page's animations can lock to. Save the beat timestamps as `reference/beats.json`.

## What to build

A single self-contained **`index.html`** at the repo root. Use plain HTML, CSS and JS, with no build step and no framework. Load libraries only from CDNs (GSAP 3.12 from cdnjs, including ScrollTrigger only if you use it, and `@google/model-viewer` from unpkg). Local assets go in `assets/`.

### 1. Keep the whole baseline from the spec
Everything in `reference/spec.md` must work exactly as described:
- the can tilts toward the cursor
- berries are pushed away by the pointer
- leaves and berries move with layered parallax
- bubbles rise endlessly
- the flavor transition plays as choreographed: background morph, 720° spin with motion blur, texture swap at the peak, berries implode, swap model, then explode to new positions
- the glass nav, CTA and award badge are all present
- the accent colour is `#fbcfe8`, and the fonts are Galada, Inter, Manrope and Outfit

### 2. Upgrade it to match the reel
Use `reel-analysis.md` to raise the site to ad quality:
- **Cinematic intro sequence** (about 3–5s, skippable): a GSAP timeline that mirrors the reel's opening. The can drops or rotates into frame, the headline reveals letter by letter or with a mask, and the berries burst outward. Time the key hits to the beat grid in `beats.json`.
- **Typography and colour**: if the reel's type treatment or palette is stronger than the spec's, adopt it, but keep the Soda brand identity.
- **Transitions**: copy the reel's transition style (whip pans, zoom punches, colour flashes, liquid wipes — whatever it uses) for the flavor switch, layered on top of the spec's choreography.
- **Extra polish**: the can rotates slowly on its own when idle, the can catches a specular/light sweep, a subtle film grain/noise overlay, a soft vignette, and magnetic hover on the buttons. Add any other polish from the reel that fits.
- **Optional music**: add a mute/unmute toggle (muted by default, since browsers block autoplay). Don't ship the reel's copyrighted track. Put an `assets/music.mp3` slot in the code with a short note in the README telling me to add a royalty-free track with a similar BPM and mood (name 2–3 suitable search terms).

### 3. Ad / recording mode
- `index.html?ad=1` gives a **1080×1920 (9:16) vertical layout** built for screen-recording the Instagram ad. It stacks the layout vertically (headline on top, can in the middle, flavor cards at the bottom), hides the nav, and **auto-plays a scripted sequence**: intro → hero hold → flavor switch → second flavor hold → end card with "Soda — Pure Zero" and a CTA. Time the whole sequence to the beat grid, and keep it 15–20s long, matching the reel's length.
- Normal mode stays fully interactive on desktop, and must also look good on mobile.

### 4. Quality bar
- Hold 60fps: use `transform` and `opacity` only for animation, use `requestAnimationFrame` for cursor-driven motion, and don't cause layout thrash. Use `will-change` sparingly.
- Respect `prefers-reduced-motion`: switch the intro, spins and bubbles to simple fades.
- Before claiming the work is done, test it with Playwright (Chromium is pre-installed). Load the page in both modes, wait for the models to load, take screenshots at 1440×900, 390×844 and 1080×1920 (`?ad=1`), check the console for errors, and fix anything broken. Commit the screenshots to `screenshots/`.

## Deliverables
- `index.html`, plus `assets/` for any local files
- `reference/reel-analysis.md` and `reference/beats.json`
- `screenshots/` with desktop, mobile and ad-mode screenshots
- `README.md` covering how to open the page, how to record the ad (open `?ad=1` in Chrome at 1080×1920, record with OBS or the browser's screen recorder, add the music track in CapCut or Premiere), and asset credits

## Git
When everything works and the screenshots look right:
- commit with clear messages (one commit per logical step is fine)
- push to the current branch with `git push -u origin <current-branch>`
- don't open a pull request unless I ask
- tell me which branch you pushed and summarize what you built, including anything you couldn't do (for example, if the reel download was blocked)
