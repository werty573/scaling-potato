# Hurricane Survival: full execution prompt for Claude Code (Windows + UEFN + uefn-mcp-server)

## What you do by hand (Claude Code can't click inside UEFN)
1. Windows PC with **UEFN** installed and signed in, **Python 3.10+** (real python.exe, not the Microsoft Store alias),
   **Git**, and **Claude Code**.
2. In UEFN, create a new project from a **blank island** template, named `HurricaneSurvival`.
3. In that project: **Project > Project Settings**, search **Python**, tick **Python Editor Script Plugin**.
   (Also tick **UEFN MCP Toolsets (beta)** if you want Epic's official MCP as a second server.) Restart UEFN if asked.
4. In UEFN set **Load on Startup = Most Recent Project** (helps crash recovery).
5. Open a terminal in a work folder **outside** the UEFN project folder (e.g. `C:\dev`), run `claude`, and paste the
   prompt below.
6. When Claude Code asks you to click **Launch Session** / **Push Changes** in UEFN, do it — those buttons have no scripting API.

---

```
ROLE
You are my lead Fortnite (UEFN) developer. You will (A) install and connect the uefn-mcp-server, then (B) build a
complete, polished, publish-ready UEFN island called "HURRICANE SURVIVAL", working through the MCP tools and Verse.
I am on Windows. UEFN is open with my project "HurricaneSurvival". Work methodically, verify everything, and stop
at each CHECKPOINT to report and wait for my "go".

GLOBAL RULES
- Never send mouse/keyboard input; use only MCP tools, files and terminal commands.
- Experimental tools (execute_python, shutdown, delete_asset, asset_batch_rename, verse_push, uefn_launch_project,
  uefn_set_load_on_startup): ask me before EACH call and say exactly what it will do.
- Never delete or rename my assets without asking. Save the level (save_current_level) after every phase.
- Never put .py files inside the UEFN project folder (causes [ContainsPythonData] upload failures).
  Keep the MCP clone and any helper scripts in C:\dev\uefn-mcp-server.
- In execute_python never call tk.Tk(); use get_tk_root() + tk.Toplevel(root) if you ever need Tk.
- Listener calls time out after 30s but keep running in the editor: after a timeout, check editor state
  (get_level_info / get_all_actors / get_log) instead of re-running.
- Before using any Verse API you are not 100% sure of, check Epic's current Verse docs or the digest files in the
  project. Never invent API names. If a feature is impossible with current tools/APIs, say so and propose the
  simplest workaround (often: a step I do by hand, with exact click instructions).
- Keep a running log in C:\dev\hurricane-notes\BUILD_LOG.md: what you did, what's left, known issues.
- Commit Verse files to a git repo in the project's Verse folder after each phase (outside of Content .py rules).

=====================================================================
PART A — INSTALL & CONNECT uefn-mcp-server  (https://github.com/kirchuvakov/uefn-mcp-server)
=====================================================================
A1. Check prerequisites and report versions: `python --version` (must be 3.10+ and NOT the WindowsApps alias —
    if `where python` shows ...\WindowsApps\python.exe first, tell me how to disable the alias or use the full path
    to a real python.exe in every command/config below), `git --version`, `claude --version`.
A2. cd C:\dev ; git clone https://github.com/kirchuvakov/uefn-mcp-server
    Read its README fully and follow it if anything below differs (the README wins).
A3. Preview the setup script, show me the output, then ask before running it for real:
    powershell -NoProfile -ExecutionPolicy Bypass -File .\uefn-mcp-server\setup.ps1 -DryRun
A4. Set the env var (user scope):
    [Environment]::SetEnvironmentVariable('UEFN_MCP_PATH', (Resolve-Path .\uefn-mcp-server).Path, 'User')
A5. Install host deps (host Python, not UEFN's): pip install -r C:\dev\uefn-mcp-server\requirements.txt
    Optional: pip install mss  (for screenshot_desktop)
A6. Autostart listener hook (ask me first):
    $hook = Join-Path $env:UEFN_MCP_PATH 'ensure_mcp_hook.ps1'
    powershell -NoProfile -ExecutionPolicy Bypass -File $hook
    Explain that Fortnite updates remove this hook and offer to create the hourly schtasks re-run the README suggests.
    Fallback if autostart doesn't fire: I run Tools > Execute Python Script > uefn_listener.py in UEFN.
A7. Register with Claude Code (user scope):
    claude mcp add uefn -s user -- python "$env:UEFN_MCP_PATH\mcp_server.py"
    (use the full path to the real python.exe if needed). If I enabled Epic's official MCP too, also add:
    claude mcp add unreal-mcp -s user --transport http http://127.0.0.1:8000/mcp
    The listener uses 127.0.0.1:8765 by default (scans to 8770); set UEFN_MCP_PORT if needed.
A8. Tell me to close and reopen UEFN (so the hook runs) and restart Claude Code. Then verify:
    claude mcp list → "uefn ... Connected"; call ping, uefn_status, get_project_info, get_level_info.
A9. CHECKPOINT A: report versions, connection status, tools available, and anything that failed.

=====================================================================
PART B — BUILD "HURRICANE SURVIVAL"
=====================================================================
GAME PITCH
2–8 players on a small tropical island. Each round: 90s to gather materials and build/reinforce a shelter, then a
hurricane hits. Storms escalate Category 1 → 5 across rounds. Survive to earn Storm Points; spend them on
upgrades. Rare MEGA STORM rounds. Chaotic, funny, short rounds. Hook in the first 30s: siren + countdown + sky
turning dark.

TUNING TABLE (put ALL of these as constants at the top of one Verse file, game_config.verse)
- LobbySeconds 20, BuildSeconds 90, WarningSeconds 10, ResultsSeconds 10
- StormSeconds by category: C1 60, C2 75, C3 90, C4 105, C5 120
- Exposed damage/sec by category: C1 2, C2 4, C3 6, C4 9, C5 13
- Structure damage multiplier: C1 0.5, C2 0.8, C3 1.0, C4 1.4, C5 2.0
- Debris spawn interval (s): C1 4.0, C2 3.0, C3 2.0, C4 1.4, C5 0.9 ; debris damage 15
- Storm surge every 3rd round: water rises for the middle 40% of the storm
- MegaStormChance 0.05, never before round 3, rewards x2, debris x1.5
- Rewards: +10 per round survived, +5 per full minute alive in storm
- Category progression: round 1 = C1, +1 per round, cap C5; after C5 survived, loop at C5 with MEGA chance x2

ARCHITECTURE (Verse)
- game_config.verse — constants above.
- hurricane_game_manager.verse — creative_device; state machine LOBBY → BUILD → WARNING → STORM → RESULTS → LOBBY;
  @editable references to all devices it drives; ends round early if all players eliminated.
- storm_controller.verse — category logic, exposed-damage ticks, debris spawning loop, surge, MEGA STORM.
- shelter_detection.verse — decides if a player is "sheltered". Use the most reliable method available, in order of
  preference: (1) mutator/volume zones placed inside huts, caves and around the build area that mark players as
  sheltered; (2) an upward trace if the Verse API supports it. Document the choice.
- progression.verse — persistable per-player data (Storm Points, rounds survived, best category, owned upgrades);
  load on join, save on change.
- shop.verse — upgrades via buttons/item granters in the lobby; deducts points; HUD feedback.
- hud.verse — phase name, countdown, category, players alive, Storm Points; big center messages for
  "STORM WARNING!", "CATEGORY 4 INCOMING", "MEGA STORM!!", "YOU SURVIVED +X".
- Use the verse_* introspection tools to check @editables are all wired (verse_check_editable_coverage).

PHASE 1 — PROJECT SCAN & PLAN
- get_project_info, get_level_info, get_all_actors, list_assets. Summarize what exists.
- Write C:\dev\hurricane-notes\PLAN.md: map layout (with coordinates), full device list, Verse file list,
  and the order you'll build things. CHECKPOINT 1.

PHASE 2 — MAP BLOCKOUT (gameplay first, art later)
- Island ~150 m across, centred at origin: beach ring, grass interior, a central hill, 4–6 breakable wooden huts
  (village), 2 rock caves (natural shelters), a lighthouse landmark on the north point, a wooden dock.
- Ocean around the island (water device/volume available in UEFN).
- Player spawn pads: 8, spread around the beach, facing inland.
- Lobby platform 200 m off the east coast (or sky lobby): spawn pads, shop area, leaderboard, "Next Round" board.
- Use mesh_scatter for palm trees, bushes, rocks; spawn_actor for buildings/props; set_actor_transform to adjust.
- Keep prop counts sensible; report the memory/performance budget if available.
- screenshot_viewport from 4 angles + top-down; show me. CHECKPOINT 2.

PHASE 3 — DEVICES
- Place and configure (device_set_editables_bulk) everything the managers need, e.g.: timer devices, HUD message
  devices, team/class settings, item granters (materials, starter tools), mutator zones for shelter detection,
  damage volumes or player-damage approach for storm damage, VFX spawners / Niagara for rain, lightning, wind,
  audio players (siren, wind loop, thunder, win/lose stingers), sky/atmosphere control for darkening, water
  level control for surge, elimination manager, end-game device, scoreboard/leaderboard, buttons for shop.
- Island settings: max players 8, building allowed, harvesting on, respawn handled by manager, spectate on
  elimination, no fall damage in lobby.
- List every device with its key settings in BUILD_LOG.md. CHECKPOINT 3.

PHASE 4 — VERSE CORE LOOP
- Write game_config, hurricane_game_manager, hud. Compile with verse_compile; fix every error and warning.
- Ask me to Launch Session; then playtest_start; run a full round; read get_log; screenshot key moments.
- Fix and repeat until one full LOBBY → RESULTS cycle works with 1 player. CHECKPOINT 4.

PHASE 5 — THE STORM
- storm_controller + shelter_detection. Categories, exposed damage, debris (spawned physics/props moving across
  the island and damaging on hit), storm surge, MEGA STORM. Darken sky, rain, wind audio, lightning flashes,
  camera shake if available.
- Test each category quickly by temporarily forcing the category in game_config (then restore).
  CHECKPOINT 5 with clips/screenshots of C1, C3, C5 and a surge.

PHASE 6 — PROGRESSION, SHOP, LEADERBOARD
- progression (persistable), shop upgrades:
  Reinforced Walls (structures take 25% less storm damage) 150 pts; Extra Health (+25 max HP) 100 pts;
  Fast Builder (more starting materials) 75 pts; Storm Sense (warning 5s earlier) 120 pts;
  cosmetic Umbrella back bling-style item or trail 300 pts (only if achievable with allowed assets).
- Lobby leaderboard: best category survived, total rounds survived.
- Verify data persists across a session restart. CHECKPOINT 6.

PHASE 7 — POLISH & ONBOARDING
- First-join tutorial popup (≤3 lines, ≤15 s): "Build a shelter. Get inside when the siren sounds. Survive the storm."
- Juice: countdown beeps last 5 s, big screen text, survivor celebration, eliminated spectate camera.
- Art pass on the map: lighting, fog, foliage density, colour grading toward bright Fortnite style (sunny tropical
  in LOBBY/BUILD, dark green-purple storm during STORM).
- Balance pass: new player survives C1–C2 easily; C5 should be rare solo, doable in a good team shelter.
- validate_folder on the project content; fix issues. Performance check with playtests. CHECKPOINT 7.

PHASE 8 — PLAYTEST KIT & PUBLISH PREP
- Write C:\dev\hurricane-notes\PLAYTEST.md: 4-player test script, what to watch, a feedback form.
- Write README (how the manager works, where to tweak numbers, how to add a new storm type).
- Take clean gameplay screenshots for the island thumbnail (dramatic storm + shelter + players) using
  screenshot_viewport from good camera angles (set_viewport_camera); save to C:\dev\hurricane-notes\shots.
- Draft island listing: title "HURRICANE SURVIVAL", 3 description lines, tags, age-appropriate wording.
- Final checklist for me: Launch Session, private code test with friends, then submit for publishing in the
  Creator Portal. CHECKPOINT 8 (done).

CONTENT RULES
- No paid random items, no fake timers or pressure tactics, nothing against Epic's island rules/content guidelines.
- Only use assets allowed in UEFN; no other games' names, characters or music.
```

---

## Should you use "ultracode" on a Pro plan?
Ultracode runs many Claude agents in parallel, which uses your plan's usage very quickly. For this project it
also doesn't help much: everything happens in **one live UEFN editor**, so parallel agents would step on each other.

**Recommendation:** don't use ultracode. Run the prompt in a normal Claude Code session, one phase at a time, and
start a fresh session (or `/compact`) between phases, pointing it at `C:\dev\hurricane-notes\BUILD_LOG.md` so it
picks up where it left off. If you hit your usage limit mid-phase, wait for the reset and continue from the log.
