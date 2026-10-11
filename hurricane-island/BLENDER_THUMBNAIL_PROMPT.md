# Hurricane Survival thumbnail: Claude Code + Blender prompt (with a Fortnite character)

## Setup on your Windows PC (one time)

1. **Install Blender** (latest LTS) and **Claude Code**.
2. **Install FortnitePorting** (needs Fortnite installed on the PC) and its **Blender plugin**, so exports go
   straight into Blender. Check its current install guide.
3. **Connect Claude Code to Blender** with a Blender MCP add-on (for example the open-source "blender-mcp"):
   install the add-on in Blender, click **Connect** in its sidebar panel, and add the MCP server to Claude Code.
   Only install add-ons from sources you trust.
4. In FortnitePorting, **export the skin you want** (and optionally a pickaxe/glider/props) into the open
   Blender scene. Keep its materials and rig.
5. **Save the .blend file** as a backup before running the prompt.

> Note: exporting Fortnite assets is fan-content territory under Epic's rules. For an island thumbnail, use a
> character/look that players actually see in your island, and check Epic's current island thumbnail guidelines.

Then open Claude Code and paste everything in the box below.

---

```
You are connected to Blender through the Blender MCP. Build a Fortnite-style island thumbnail for my game
"HURRICANE SURVIVAL" (players build a shelter on a tropical island and survive a hurricane).
A Fortnite character I exported with FortnitePorting is already in the scene with its rig and materials.

FIRST
- List the scene: objects, the character armature/meshes, materials, current render engine. Don't delete or
  rename my imported character or its materials. Save a copy of the .blend before big changes.
- Take a viewport screenshot after each major step and check your own work. Tell me what you changed.

LOOK (match Fortnite's official key art / loading screens)
- Bright, saturated, stylized. Chunky shapes, clean silhouettes, soft cartoony PBR (not realistic, not flat).
- Strong rim light on the character, vivid sky gradient, glow and bloom, atmospheric depth/fog.
- Colour palette: stormy purple-blue sky with a cyan-green glow around the hurricane eye; warm orange-gold key
  light on the character; turquoise sea with white foam.

SCENE (16:9, 1920x1080 final)
1. Sky & storm: a huge swirling hurricane in the background (spiral cloud bands + twisting funnel touching the
   sea), volumetric clouds, 2–3 lightning bolts with emission, rain streaks. Make the storm read clearly at
   thumbnail size.
2. Island: small tropical island mid-ground on the left: sand, grass, palm trees bending hard in the wind,
   leaves and wooden planks flying through the air.
3. Fortnite-style build: a wooden player-built fort (wood wall panels, ramp, cone roof) on the island with one
   wall panel ripping off in the wind.
4. Sea: turquoise stylized water with waves, foam and spray near the island.
5. Character (foreground, right third, large — about 60% of frame height): pose the rig into a dramatic
   "oh no!" reaction — bracing against the wind, one arm up shielding face or hands on head, leaning back,
   cloth/hair blown in wind direction if possible. Face clearly visible, looking toward camera/storm.
   Use the existing rig; don't distort the mesh. If there are face shape keys/expressions, use a shocked one.
6. Camera: low hero angle on the character, slight wide lens (24–35mm), shallow depth of field so the
   background storm is a little soft but still readable. Leave the top-left ~40% of the frame clean for the title.

LIGHTING & RENDER
- Key: warm area light from front-right on the character. Rim: strong cyan light from behind (storm side).
  Fill: soft purple from the sky. Add a subtle god-ray / volumetric glow from the hurricane eye.
- Render with Cycles (or EEVEE if it looks closer to Fortnite key art — try both, show me), denoise on,
  AgX "Punchy" or similar contrast, add bloom/glare in the compositor, slight vignette.
- Render a quick low-res preview first, show me, then the final 1920x1080.

TEXT (compositor or a separate image step)
- Title top-left: "HURRICANE" (white→light cyan) and "SURVIVAL" (yellow→orange), heavy rounded Fortnite-like
  display font (e.g. Luckiest Guy or Burbank-style), thick dark navy outline, 3D extrude drop shadow, slight
  tilt. Tagline under it: "BUILD. HIDE. SURVIVE." Red rounded badge bottom-right: "CAT 5".
- Also export a version with NO text (for Epic's thumbnail upload if needed) and a 1:1 square crop.

DELIVER
- hurricane-thumb-final.png (with text), hurricane-thumb-clean.png (no text), hurricane-thumb-square.png,
  and the saved .blend. Then give me 2 alternative camera angles as quick previews so I can pick.
```

---

## Tips
- If the pose looks stiff, tell Claude Code: "Make the pose more exaggerated, like Fortnite emote key art."
- If it looks too realistic: "More stylized and saturated, softer shadows, bigger rim light."
- Real in-game screenshots from your UEFN island are still the safest choice for the uploaded thumbnail;
  use the render for ads, TikToks and the game's trailer.
