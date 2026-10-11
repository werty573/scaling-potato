"""Hurricane Survival thumbnail: original stylized 3D scene (no Fortnite assets).
Run:  python3 thumbnail_scene.py <font.ttf> <out.png> [samples]
(needs the `bpy` module: pip install bpy)"""
import sys, math, random
import bpy
from mathutils import Vector

FONT, OUT = sys.argv[1], sys.argv[2]
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 64
random.seed(7)
R = math.radians

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------- helpers ----------
def mat(name, color, rough=0.5, emit=None, strength=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m

def put(obj, m=None, smooth=True):
    if m: obj.data.materials.append(m)
    if smooth and obj.type == "MESH":
        for p in obj.data.polygons: p.use_smooth = True
    return obj

def sphere(loc, scale, m, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.scale = scale; return put(o, m)

def cube(loc, scale, m, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale
    if bevel:
        md = o.modifiers.new("b", "BEVEL"); md.width = bevel; md.segments = 3
    return put(o, m, smooth=False)

def cyl(loc, r, d, m, rot=(0, 0, 0), r2=None, verts=24):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=d, location=loc, rotation=rot)
    return put(bpy.context.object, m)

def between(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    o = cyl((a + b) / 2, r, d.length, m)
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    return o

# ---------- materials ----------
M = {
    "sand": mat("sand", (0.95, 0.72, 0.38), 0.9),
    "grass": mat("grass", (0.18, 0.55, 0.12), 0.8),
    "wood": mat("wood", (0.55, 0.30, 0.12), 0.7),
    "wood_dark": mat("wood_dark", (0.30, 0.15, 0.06), 0.8),
    "trunk": mat("trunk", (0.40, 0.24, 0.10), 0.9),
    "leaf": mat("leaf", (0.10, 0.62, 0.15), 0.6),
    "sea": mat("sea", (0.03, 0.36, 0.44), 0.32),
    "cloud": mat("cloud", (0.42, 0.45, 0.58), 1.0),
    "cloud_dark": mat("cloud_dark", (0.16, 0.17, 0.26), 1.0),
    "funnel": mat("funnel", (0.55, 0.60, 0.68), 1.0),
    "bolt": mat("bolt", (1, 1, 1), 0.5, (0.75, 0.95, 1.0), 60),
    "eye_glow": mat("eye_glow", (0.4, 1, 0.9), 0.5, (0.5, 1.0, 0.85), 6),
    "skin": mat("skin", (1.0, 0.68, 0.50), 0.55),
    "hoodie": mat("hoodie", (1.0, 0.32, 0.06), 0.6),
    "white": mat("white", (1, 1, 1), 0.2),
    "black": mat("black", (0.01, 0.01, 0.02), 0.3),
    "hair": mat("hair", (0.12, 0.06, 0.03), 0.7),
    "mouth": mat("mouth", (0.25, 0.02, 0.04), 0.6),
    "tongue": mat("tongue", (0.9, 0.25, 0.3), 0.5),
    "title": mat("title", (1.0, 0.78, 0.05), 0.25, (1.0, 0.55, 0.0), 1.2),
    "title2": mat("title2", (0.75, 0.95, 1.0), 0.25, (0.6, 0.9, 1.0), 1.0),
    "title_side": mat("title_side", (0.05, 0.05, 0.25), 0.4),
}
# wood planks pattern
w = M["wood"].node_tree; wt = w.nodes.new("ShaderNodeTexWave"); wt.inputs["Scale"].default_value = 6
wt.wave_type = "BANDS"; wt.bands_direction = "Z"
ramp = w.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.42, 0.22, 0.08, 1); ramp.color_ramp.elements[1].color = (0.66, 0.38, 0.16, 1)
w.links.new(wt.outputs["Fac"], ramp.inputs["Fac"])
w.links.new(ramp.outputs["Color"], w.nodes["Principled BSDF"].inputs["Base Color"])

# ---------- world & lights ----------
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.16, 0.10, 0.42, 1); bg.inputs["Strength"].default_value = 1.6

bpy.ops.object.light_add(type="SUN", rotation=(R(55), 0, R(-35)))
bpy.context.object.data.energy = 3.0; bpy.context.object.data.color = (0.75, 0.82, 1.0)
bpy.ops.object.light_add(type="AREA", location=(9, -26, 6), rotation=(R(70), 0, R(40)))
L = bpy.context.object.data; L.energy = 1500; L.size = 6; L.color = (1.0, 0.65, 0.35)   # warm key on character
bpy.ops.object.light_add(type="AREA", location=(1, -15, 6), rotation=(R(-60), 0, R(-160)))
L = bpy.context.object.data; L.energy = 900; L.size = 4; L.color = (0.4, 0.9, 1.0)     # cyan rim from storm

# ---------- ocean ----------
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 150, 0))
sea = bpy.context.object
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=120); bpy.ops.object.mode_set(mode="OBJECT")
tex = bpy.data.textures.new("waves", "CLOUDS"); tex.noise_scale = 14
disp = sea.modifiers.new("d", "DISPLACE"); disp.texture = tex; disp.strength = 3.2
put(sea, M["sea"])

# ---------- island ----------
sphere((-11, 8, -1.2), (11, 7, 2.2), M["sand"])
sphere((-11, 9, 0.2), (7.5, 4.8, 1.2), M["grass"])

# fort (player-built style)
fx, fy, fz = -10, 8.5, 1.2
for dx, dy, sx, sy in [(0, -2, 2.2, 0.15), (0, 2, 2.2, 0.15), (-2.1, 0, 0.15, 2.0), (2.1, 0, 0.15, 2.0)]:
    cube((fx + dx, fy + dy, fz + 1.6), (sx, sy, 1.6), M["wood"], bevel=0.04)
for dx, dy, sx, sy in [(0, -2, 2.2, 0.15), (2.1, 0, 0.15, 2.0)]:
    cube((fx + dx, fy + dy, fz + 4.9), (sx, sy, 1.6), M["wood"], bevel=0.04)
cube((fx, fy - 2.2, fz + 1.2), (0.6, 0.05, 1.1), M["wood_dark"])            # door
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=3.6, radius2=0, depth=2.2,
                                location=(fx, fy, fz + 7.6), rotation=(0, 0, R(45)))
put(bpy.context.object, M["wood_dark"], smooth=False)
cube((fx + 4.2, fy - 0.5, fz + 1.4), (1.6, 1.6, 0.12), M["wood"], rot=(0, R(-40), 0), bevel=0.03)  # ramp
cube((fx + 3.6, fy - 3.4, fz + 7.5), (1.3, 0.12, 0.9), M["wood"], rot=(R(20), R(30), R(-35)), bevel=0.03)  # wall ripping off

# palm trees bending in wind (toward +x)
def palm(base, h, lean):
    pts = [Vector(base) + Vector((lean * (t / 6) ** 2, 0, h * t / 6)) for t in range(7)]
    for a, b in zip(pts, pts[1:]): between(a, b, 0.32, M["trunk"])
    top = pts[-1]
    for i in range(8):
        ang = R(-70 + i * 22)
        d = Vector((math.cos(ang), math.sin(ang) * 0.6, 0))
        o = sphere(top + d * 2.0 + Vector((0.8, 0, -0.4 - abs(i - 3.5) * 0.15)), (2.4, 0.45, 0.12), M["leaf"], 16)
        o.rotation_euler = (R(random.uniform(-15, 15)), R(25 + abs(i - 3.5) * 6), ang)
palm((-17, 7.5, 0.5), 8, 5); palm((-4, 10, 0.6), 7, 4.5); palm((-14, 11, 0.6), 6, 3.5)

# ---------- hurricane ----------
HX, HY = 20, 95
for i in range(70):
    z = i * 0.65
    rad = 2.0 + (z / 45) ** 1.8 * 16
    for j in range(5):
        a = i * 0.55 + j * 1.256
        sphere((HX + math.cos(a) * rad + math.sin(z * 0.12) * 3, HY + math.sin(a) * rad * 0.6, z),
               (rad * 0.55 + 1.2, rad * 0.4 + 1.0, 1.4), M["funnel"], 14)
for k in range(1400):
    t = random.random() * 9.5
    rad = 8 + t * 9 + random.uniform(-4, 4)
    a = t * 1.25 + random.uniform(-0.2, 0.2)
    p = (HX + math.cos(a) * rad * 1.4, HY + math.sin(a) * rad * 0.7, 46 + random.uniform(-4, 5) - rad * 0.05)
    s = random.uniform(3, 8)
    sphere(p, (s * 1.6, s, s * 0.6), M["cloud"] if random.random() < 0.7 else M["cloud_dark"], 12)
sphere((HX, HY, 47), (9, 6, 1.2), M["eye_glow"], 24)
# lightning bolts
def bolt(start, n, step):
    p = Vector(start)
    for _ in range(n):
        q = p + Vector((random.uniform(-2.5, 2.5), random.uniform(-1, 1), -step))
        between(p, q, 0.18, M["bolt"]); p = q
bolt((HX - 24, HY - 10, 44), 10, 4.5); bolt((HX + 30, HY + 5, 46), 9, 5); bolt((HX - 6, HY - 30, 40), 7, 4)

# flying debris between island and storm
for i in range(55):
    p = (random.uniform(-4, 30), random.uniform(5, 70), random.uniform(3, 30))
    if random.random() < 0.7:
        cube(p, (random.uniform(0.6, 1.4), 0.12, 0.05), M["wood"], rot=[R(random.uniform(0, 360)) for _ in range(3)])
    else:
        o = sphere(p, (1.2, 0.3, 0.08), M["leaf"], 10); o.rotation_euler = [R(random.uniform(0, 360)) for _ in range(3)]

# ---------- character (original cartoon, scared reaction) ----------
sphere((7.5, -22, -1.2), (7, 4.5, 2.6), M["sand"])                                # foreground dune
bpy.ops.object.empty_add(location=(0, 0, 0)); RIG = bpy.context.object
CX, CY, CZ = 0.0, 0.0, 0.0
_objs_before = set(bpy.data.objects)
sphere((CX, CY, CZ - 1.6), (1.55, 1.1, 1.9), M["hoodie"])                      # torso
sphere((CX, CY + 0.3, CZ + 0.55), (0.95, 0.9, 0.35), M["hoodie"])               # hood collar
head = sphere((CX, CY, CZ + 1.6), (1.15, 1.05, 1.2), M["skin"])
sphere((CX, CY + 0.15, CZ + 2.35), (1.2, 1.1, 0.75), M["hair"])                 # hair cap
for sx in (-1, 1):
    sphere((CX + sx * 0.42, CY - 0.92, CZ + 1.85), (0.34, 0.2, 0.42), M["white"])   # big eyes
    sphere((CX + sx * 0.40, CY - 1.10, CZ + 1.80), (0.13, 0.06, 0.16), M["black"])  # pupils
    cube((CX + sx * 0.45, CY - 1.0, CZ + 2.42), (0.3, 0.06, 0.07), M["hair"], rot=(0, R(sx * 22), 0))  # worried brows
    sphere((CX + sx * 1.15, CY - 0.1, CZ + 1.6), (0.18, 0.15, 0.3), M["skin"])      # ears
sphere((CX, CY - 0.93, CZ + 0.95), (0.32, 0.12, 0.38), M["mouth"])               # screaming mouth
sphere((CX, CY - 0.97, CZ + 0.78), (0.2, 0.08, 0.12), M["tongue"])
sphere((CX, CY - 1.1, CZ + 1.42), (0.14, 0.12, 0.12), M["skin"])                # nose
for sx in (-1, 1):                                                               # hands on head
    between((CX + sx * 1.4, CY, CZ - 0.6), (CX + sx * 1.9, CY - 0.3, CZ + 1.0), 0.32, M["hoodie"])
    between((CX + sx * 1.9, CY - 0.3, CZ + 1.0), (CX + sx * 1.25, CY - 0.4, CZ + 2.1), 0.28, M["hoodie"])
    sphere((CX + sx * 1.15, CY - 0.45, CZ + 2.2), (0.36, 0.3, 0.3), M["skin"])

for o in set(bpy.data.objects) - _objs_before:
    if o is not RIG: o.parent = RIG
RIG.location = (6.6, -23.0, 3.4); RIG.rotation_euler = (0, 0, R(-30)); RIG.scale = (1.05, 1.05, 1.05)

# ---------- 3D title ----------
def title(text, loc, size, m):
    curve = bpy.data.curves.new(text, "FONT"); curve.body = text
    curve.font = bpy.data.fonts.load(FONT); curve.size = size
    curve.extrude = 0.22; curve.bevel_depth = 0.06; curve.bevel_resolution = 3
    o = bpy.data.objects.new(text, curve); sc.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (R(90), R(-4), 0)
    o.data.materials.append(m); o.data.materials.append(M["title_side"])
    for sp in curve.splines: pass
    return o
# title is added in post (crisp 2D text with outline), see add_title.py

# ---------- camera & render ----------
bpy.ops.object.camera_add(location=(0, -34, 3.5), rotation=(R(90.5), 0, 0))
cam = bpy.context.object; cam.data.lens = 24; sc.camera = cam
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("rendered", OUT)
