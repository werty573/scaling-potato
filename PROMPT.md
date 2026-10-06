# Claude Code prompt: mind-blowing animated website + Instagram ad

Copy everything inside the box below into Claude Code (local session).

```text
I want two things:
1. A WEBSITE with mind-blowing, award-level animation — the kind that wins Awwwards Site of the Day.
2. An INSTAGRAM REEL AD (9:16) that shows off that website. The ad must be modelled on this reference reel:
   https://www.instagram.com/reel/DdAgrCAO4km/

The reference reel is ONLY for the ad (its structure, pacing, transitions, text overlays, music timing). It is NOT the design reference for the website. The website's look and animation should simply be the best you can possibly make.

STEP 0: ASK ME FIRST
Before doing anything, ask me what the website is for: the brand or product name, what it does, the tagline, and any colours or style I want. Wait for my answer.

STEP 1: BUILD THE WEBSITE (go all out on the animation)
Build a single self-contained index.html in this project folder, plus an assets/ folder for local files.
- Plain HTML, CSS and JS, with no build step.
- Load libraries from CDNs only (cdnjs, jsDelivr or unpkg). Use whatever the effects need: GSAP (ScrollTrigger, SplitText, Flip, CustomEase), Three.js (WebGL shaders, particles, post-processing), Lenis (smooth scroll), <model-viewer> for 3D models.

The animation is the star. The bar is techniques like these:
- Cinematic intro: a preloader that turns into a hero reveal, with text revealed letter by letter or through masks/clip-paths.
- WebGL/3D centrepiece: a 3D object or shader scene that reacts to the cursor (tilts, follows the pointer, ripples, distorts), with particles and depth parallax.
- Physics-feeling interactivity: elements repelled by or attracted to the cursor, magnetic buttons, a custom cursor, inertia and spring easing.
- Scroll-driven storytelling: pinned sections, horizontal scroll, scrubbed timelines, zoom-through transitions, layered parallax.
- Choreographed transitions between sections or states: shader/liquid wipes, colour floods, morphs, implode/explode.
- Finishing polish: film grain, vignette, light sweeps, motion blur on fast moves, colour grading, smooth idle motion so it never looks static.
Every motion should feel intentional and premium: custom easing, nothing linear, nothing janky.

Quality:
- Hold 60fps: animate transform, opacity and shaders only; use requestAnimationFrame for pointer-driven motion; lower pixel ratio and particle counts on mobile.
- Respect prefers-reduced-motion with simple fades.
- Fully responsive (desktop and phone).
- Test with Playwright (install with npm i -D playwright && npx playwright install chromium if needed): check the console for errors, screenshot at 1440x900 and 390x844, look at the results and fix anything broken or underwhelming.

STEP 2: GET THE REFERENCE REEL (for the ad)
1. Check whether reference/reel.mp4 already exists in this project folder. If it does, use it.
2. Also check ~/Downloads for a recently downloaded reel video.
3. Otherwise try to download it:
   pip install yt-dlp && yt-dlp -o "reference/reel.%(ext)s" "https://www.instagram.com/reel/DdAgrCAO4km/"
4. If that fails for any reason, STOP and ask me to download it for you. Say exactly this:
   "I couldn't download the reel. Please download it (from the Instagram app or a reel downloader site) and save it in this project folder as reference/reel.mp4, or just tell me where you saved it. Then tell me to continue."
   Then wait. Don't guess what the reel looks like.

STEP 3: ANALYSE THE REEL
Write your findings to reference/reel-analysis.md.

Visuals: use ffmpeg (install it if missing) to extract one frame every 0.5s plus scene-change frames (-vf "select='gt(scene,0.3)',showinfo"). Look at every frame and document:
- shot-by-shot breakdown with timestamps and total length
- camera moves (zooms, pans, rotations, push-ins)
- transitions between shots and exactly how they work
- text overlays: wording style, font, size, position, how they animate in and out
- hook (first 1-3 seconds), how the product is revealed, and how it ends (CTA / end card)
- colour grade, effects, pacing and rhythm

Music: extract the audio (ffmpeg -i reference/reel.mp4 -vn reference/audio.wav) and analyse it with librosa (pip install librosa):
- BPM and beat timestamps
- onsets and strong hits/drops
- energy curve, genre and mood
- intro, build and drop timestamps
Save beats and hits to reference/beats.json.

Then show me a short shot list for MY ad that follows the reel's structure but uses my website, and wait for my OK.

STEP 4: MAKE THE AD
- Add an ad mode to the website: index.html?ad=1 renders a 1080x1920 (9:16) vertical version with no nav or scrolling, and auto-plays a scripted sequence that follows the approved shot list: the hook, the website's best animation moments, text overlays styled like the reel's, and an end card with the brand name and CTA. Every cut and hit lands on the timestamps in beats.json, and the total length matches the reel.
- Record it: use Playwright to record ad mode at 1080x1920, then use ffmpeg to export reference-free final videos to ad/:
  - ad/ad-silent.mp4 (H.264, 1080x1920, 30fps, Instagram-ready)
  - if assets/music.mp3 exists, also ad/ad-with-music.mp4 with the music mixed in and synced
- Do NOT use the reel's audio in the final ad; it's copyrighted. In the README, give me 3 search terms for royalty-free tracks with a matching BPM and mood, and tell me to drop one in as assets/music.mp3 and ask you to re-export.
- Watch your own export (pull frames from it) and fix anything that looks off before telling me it's done.

STEP 5: PUSH TO GITHUB
When everything works:
- add reference/reel.mp4 and reference/audio.wav to .gitignore so the copyrighted reel never gets pushed
- write a README.md: how to open the site, how to re-record the ad, and credits for any assets
- commit with clear messages
- push with git push -u origin <current-branch>. If this folder isn't a git repo or has no GitHub remote, ask me which repo to push to
- don't open a pull request unless I ask
- tell me where you pushed, summarise what you built, and list anything you couldn't do
```
