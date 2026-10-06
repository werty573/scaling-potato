# Claude Code prompt: mind-blowing animated website (for an Instagram ad)

Copy everything below the line into Claude Code and run it inside this repo.

---

Build a website with **mind-blowing, award-level animation**. It should be the kind of site that wins Awwwards Site of the Day and makes people stop scrolling. I'll screen-record it and post it as an **Instagram Reel ad (9:16)**, so it has to look incredible as a desktop site *and* as a vertical video.

The style, motion, pacing and mood all come from this reference reel:
**https://www.instagram.com/reel/DdAgrCAO4km/**

## Step 1: Get the reference reel (do this first)

1. Check whether `reference/reel.mp4` already exists in the repo. If it does, use it.
2. If it doesn't, try to download the reel:
   `pip install yt-dlp && yt-dlp -o "reference/reel.%(ext)s" "https://www.instagram.com/reel/DdAgrCAO4km/"`
3. Also check `~/Downloads` for a recently downloaded reel video.
4. **If the download fails for any reason** (blocked, login required, no video found, proxy error, anything else), **stop and ask me to download it for you.** Say exactly this:
   > "I couldn't download the reel. Please download it (from the Instagram app or a reel downloader site) and save it in this project folder as `reference/reel.mp4`, or just tell me where you saved it. Then tell me to continue."

   Then wait for my reply. **Don't guess what the reel looks like, and don't build anything until you've actually analysed the video.**

## Step 2: Analyse the reel (visuals and music)

Write your findings to `reference/reel-analysis.md`.

**Visuals.** Use `ffmpeg` to extract one frame every 0.5s, plus scene-change frames (`-vf "select='gt(scene,0.3)',showinfo"`). Look at every frame, then document:
- the shot-by-shot breakdown with timestamps
- camera moves (zooms, pans, rotations, parallax, depth)
- the transitions between shots and exactly how they work
- typography: font style, weight, size, and how text animates in and out
- the colour palette, with hex values
- what the subject or product is and how it's staged
- lighting, texture, grain and any effects
- pacing and rhythm
- the 5 most impressive moments, and how you'd recreate each one on the web

**Music.** Extract the audio (`ffmpeg -i reference/reel.mp4 -vn reference/audio.wav`) and analyse it with `librosa`:
- BPM and beat timestamps
- onsets and strong hits/drops
- the energy curve over time
- genre and mood
- intro, build and drop timestamps

Save the beats and hits as `reference/beats.json` so the animations can sync to them.

**Then ask me what the website is for:** the brand or product name, the tagline, and the colours, if they differ from the reel. Give me a 5–8 line summary of the concept you'd build from the analysis. **Wait for my answer before you start building.**

## Step 3: Build it, and go all out on the animation

Build a single self-contained `index.html` at the repo root, plus an `assets/` folder for local files.
- Plain HTML, CSS and JS, with no build step.
- Load libraries from CDNs only (cdnjs, jsDelivr or unpkg). Pick whatever the effects need: **GSAP** (with ScrollTrigger, SplitText or Flip, and CustomEase), **Three.js** (WebGL shaders, particles, post-processing), **Lenis** (smooth scroll), and `<model-viewer>` for 3D models.

The animation has to be the star. It should match the reel's style and go beyond it. The bar is techniques like these:
- **Cinematic intro.** A preloader that turns into a hero reveal. Text reveals letter by letter, or through masks or clip-paths, and the opening hits land on the music's beats.
- **WebGL/3D centrepiece.** A 3D object or shader scene that reacts to the cursor: it tilts, follows the pointer, ripples or distorts. Add particles and depth parallax.
- **Physics-feeling interactivity.** Elements are repelled by or attracted to the cursor, buttons are magnetic, there's a custom cursor, and things move with inertia and spring easing.
- **Scroll-driven storytelling.** Pinned sections, horizontal scroll, scrubbed timelines, zoom-through transitions, and layered parallax. If the reel has distinct scenes, each one becomes a section.
- **Choreographed transitions.** Reproduce the reel's transitions (whip pans, zoom punches, liquid or shader wipes, colour floods, morphs, implode/explode) between sections or states.
- **Finishing polish.** Film grain or noise, vignette, light sweeps, motion blur on fast moves, colour grading, and smooth idle motion so it never looks static.

Every motion should feel intentional and premium: custom easing, nothing linear, nothing janky.

### Ad / recording mode
`index.html?ad=1` is a **1080×1920 (9:16) vertical version** made for screen-recording the Instagram ad:
- no navigation and no scrolling needed
- it **auto-plays a scripted sequence** that runs intro → the 2–4 best moments → end card with brand name and CTA
- it's timed to `beats.json`, and its length matches the reel's (about 15–20s)

### Music
Add a mute/unmute toggle that's muted by default, since browsers block autoplay. **Don't ship the reel's track; it's copyrighted.** Leave a slot for `assets/music.mp3`. In the README, give me 3 search terms for a royalty-free track with a matching BPM and mood.

### Performance and quality
- Hold 60fps:
  - animate `transform`, `opacity` and shaders only
  - use `requestAnimationFrame` for pointer-driven motion
  - lower the pixel ratio and particle counts on mobile
- Respect `prefers-reduced-motion` by falling back to simple fades.
- Make it fully responsive (desktop and phone).
- **Test before saying it's done.** Use Playwright (install it with `npm i -D playwright && npx playwright install chromium` if needed):
  - load the page in normal mode and in `?ad=1`
  - check the console for errors
  - screenshot at 1440×900, 390×844 and 1080×1920 (ad mode)
  - record a short video of ad mode if possible
  - look at the results and fix anything that looks broken or underwhelming

## Deliverables
- `index.html` and `assets/`
- `reference/reel-analysis.md` and `reference/beats.json`
- `screenshots/` (and `screenshots/ad-mode.webm` if you recorded one)
- `README.md`: how to open the page, how to record the ad (open `?ad=1` in Chrome at 1080×1920, record with OBS, add music in CapCut or Premiere), and credits for any assets

## Step 4: Push to GitHub
When it all works and the screenshots look great:
- commit with clear messages
- push to the current branch with `git push -u origin <current-branch>`
- **don't open a pull request** unless I ask
- tell me which branch you pushed to, summarize what you built, and list anything you couldn't do
