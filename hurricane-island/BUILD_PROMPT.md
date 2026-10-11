# Hurricane Survival: build prompt for Claude Code + UEFN MCP

## Before you start (checklist)

1. Windows PC with **UEFN 42.00 or newer** installed and signed in.
2. New UEFN project (start from a blank island template).
3. **Project Settings:** turn on **Python Editor Script Plugin** and **UEFN MCP Toolsets (beta)**. Restart UEFN if asked.
4. Install **Claude Code** on the same PC and connect it to the UEFN MCP server
   (check Epic's "UEFN MCP" docs for the exact address and port).
5. **Back up the project** (copy the project folder) before the first run.

Then open Claude Code in your project folder and paste everything in the box below.

---

```
You are building a Fortnite island in UEFN called "HURRICANE SURVIVAL" using the UEFN MCP tools and Verse.
Work in small steps. After each phase: build Verse, start a play session through the MCP, check for errors,
fix them, and give me a short summary of what changed and what I should test. Ask me before deleting anything.

FIRST
- List the MCP toolsets available to you and tell me which ones you'll use (actors/devices, Verse files,
  Scene Graph, play session). If something below isn't possible with the current tools, tell me and suggest
  the simplest workaround (e.g. a step I do by hand).
- Read Epic's current Verse and UEFN MCP documentation for any API you're unsure about. Don't guess API names.

GAME CONCEPT
2–8 players spawn on a small tropical island. Each round: gather materials and build/reinforce a shelter,
then survive a hurricane. Each round the storm gets stronger (Category 1 → 5). Survive to earn Storm Points,
spend them on upgrades between rounds. Rare "MEGA STORM" rounds (about 5% chance) for big rewards.
Short rounds, chaotic and funny with friends. Hook in the first 30 seconds: storm siren + countdown.

PHASE 1 — MAP (blockout first, pretty later)
- Small island (~150m across): beach ring, palm trees, a central hill, a small village of 4–6 breakable huts,
  rocks and caves that act as natural shelters, a lighthouse as a landmark.
- Ocean all around. Player spawn pads spread around the beach.
- Lobby area off to the side with a "Next Round" countdown and the upgrade shop.
- Keep total prop count modest for performance.

PHASE 2 — ROUND LOOP (Verse game manager)
- States: LOBBY (20s) → BUILD PHASE (90s) → STORM WARNING (10s, siren + big HUD text) → STORM (60–120s,
  scales with category) → RESULTS (10s) → back to LOBBY.
- HUD: current phase, countdown timer, storm category, players alive.
- Building and harvesting enabled in BUILD PHASE; harvesting disabled during STORM.
- Eliminated players spectate until the round ends; everyone respawns next round.
- Round ends early if everyone is eliminated.

PHASE 3 — THE STORM
- Storm strength by category (1–5): wind damage per second to players who are exposed (not under a roof/
  inside a shelter or cave), how often debris spawns, and how much damage structures take.
- "Exposed" check: simplest reliable method available (e.g. shelter volumes/mutator zones placed in huts,
  caves and around player-built structures, or a raycast upward if supported). Pick the most reliable option.
- Debris: during the storm, spawn flying props (planks, barrels, branches) that move across the island and
  damage players they hit. More debris at higher categories.
- Visuals/audio: darken sky/fog, rain, wind sound, lightning flashes, camera shake if available.
- Every 3rd round: the storm surge raises the water level for part of the storm (low areas become dangerous).
- MEGA STORM (5% chance, never before round 3): announce it, double rewards, extra debris.

PHASE 4 — PROGRESSION (persistent)
- Storm Points: +10 per round survived, +5 per minute alive in the storm, x2 in MEGA STORM.
- Save per player with Verse persistence: total Storm Points, best category survived, rounds survived,
  owned upgrades.
- Shop in the lobby (item granters / buttons): Stronger Walls (structures take less storm damage),
  Extra Health, Faster Building, Starter Materials, cosmetic umbrella / trail. Prices 50–500 points.
- Leaderboard in the lobby: best category survived and total rounds survived.

PHASE 5 — POLISH
- 15-second first-time tutorial popup (3 lines max): "Build a shelter. Get inside when the siren goes off.
  Survive the storm."
- Sound cues: siren, wind loop, thunder, round win/lose stingers.
- Balance pass: a new player should survive Category 1–2 easily; Category 5 should be rare to survive alone.
- Performance check: run a play session, report any warnings, reduce props/effects if needed.

PHASE 6 — HAND-OFF
- Write a short README in the project: how the game manager works, where to tweak numbers
  (round times, damage, debris rates, prices), and how to add a new storm type.
- Give me a test checklist for a 4-player private playtest.

RULES
- Keep all tunable numbers (times, damage, rewards, prices) in one place at the top of the Verse code.
- No paid random items, no fake timers, nothing that breaks Epic's island rules or content guidelines.
- Use only Epic/Fortnite assets that are allowed in UEFN. Don't use other games' names or characters.
```

---

## After the first build

- Playtest with 2–4 friends. Note what's boring, confusing or too hard.
- Paste your notes into Claude Code: "Players said X. Fix it." Repeat.
- Take real gameplay screenshots for the thumbnail (see `hurricane-survival-thumbnail.png` for the layout idea).
- Submit to Epic for review, then launch with daily TikTok/Shorts clips of the funniest storm moments.
