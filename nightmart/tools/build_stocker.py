"""Procedurally builds "The Stocker" - the monster for Nightmart.

Outputs a low-poly OBJ + MTL (Y-up, 1 unit = 1 metre, ~2.9 m tall) and a
preview PNG. No Blender needed to generate; open the OBJ in Blender to
export FBX for UEFN (see nightmart/README.md).

    python3 nightmart/tools/build_stocker.py
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "models")

verts, faces = [], []  # faces: (material, [vertex indices])


# ---------------------------------------------------------------- math ----
def rot(v, rx=0.0, ry=0.0, rz=0.0):
    x, y, z = v
    if rx:
        c, s = math.cos(rx), math.sin(rx)
        y, z = y * c - z * s, y * s + z * c
    if ry:
        c, s = math.cos(ry), math.sin(ry)
        x, z = x * c + z * s, -x * s + z * c
    if rz:
        c, s = math.cos(rz), math.sin(rz)
        x, y = x * c - y * s, x * s + y * c
    return (x, y, z)


def add(mat, pts, quads, pos=(0, 0, 0), r=(0, 0, 0)):
    base = len(verts)
    for p in pts:
        p = rot(p, *r)
        verts.append((p[0] + pos[0], p[1] + pos[1], p[2] + pos[2]))
    for q in quads:
        faces.append((mat, [base + i for i in q]))


# ---------------------------------------------------------- primitives ----
def box(mat, size, pos, r=(0, 0, 0), taper=1.0):
    """Box; `taper` scales the top (+Y) face for organic shapes."""
    sx, sy, sz = (s / 2 for s in size)
    pts = []
    for y in (-sy, sy):
        t = taper if y > 0 else 1.0
        for x, z in ((-sx, -sz), (sx, -sz), (sx, sz), (-sx, sz)):
            pts.append((x * t, y, z * t))
    quads = [(0, 1, 2, 3)[::-1], (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    add(mat, pts, quads, pos, r)


def limb(mat, a, b, ra, rb, seg=7):
    """Tapered cylinder from point a (radius ra) to point b (radius rb)."""
    ax, ay, az = a
    d = (b[0] - ax, b[1] - ay, b[2] - az)
    L = math.sqrt(sum(c * c for c in d))
    # orientation: build cylinder along +Y then rotate onto d
    pitch = math.acos(max(-1, min(1, d[1] / L)))
    yaw = math.atan2(d[0], d[2])
    pts = []
    for y, rr in ((0, ra), (L, rb)):
        for i in range(seg):
            t = 2 * math.pi * i / seg
            pts.append((math.cos(t) * rr, y, math.sin(t) * rr))
    pts += [(0, 0, 0), (0, L, 0)]
    quads = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i)[::-1] for i in range(seg)]
    quads += [(2 * seg, (i + 1) % seg, i) for i in range(seg)]
    quads += [(2 * seg + 1, seg + i, seg + (i + 1) % seg) for i in range(seg)]
    base = len(verts)
    for p in pts:
        p = rot(p, rx=pitch)
        p = rot(p, ry=yaw)
        verts.append((p[0] + ax, p[1] + ay, p[2] + az))
    for q in quads:
        faces.append((mat, [base + i for i in q]))


def sphere(mat, radius, pos, scale=(1, 1, 1), seg=8, rings=6):
    pts = [(0, -radius, 0)]
    for j in range(1, rings):
        phi = math.pi * j / rings - math.pi / 2
        for i in range(seg):
            t = 2 * math.pi * i / seg
            pts.append((math.cos(phi) * math.cos(t) * radius,
                        math.sin(phi) * radius,
                        math.cos(phi) * math.sin(t) * radius))
    pts.append((0, radius, 0))
    pts = [(x * scale[0], y * scale[1], z * scale[2]) for x, y, z in pts]
    top = len(pts) - 1
    quads = [(0, i + 1, (i + 1) % seg + 1) for i in range(seg)]
    for j in range(rings - 2):
        o = 1 + j * seg
        for i in range(seg):
            n = (i + 1) % seg
            quads.append((o + i, o + seg + i, o + seg + n, o + n))
    o = 1 + (rings - 2) * seg
    quads += [(top, o + (i + 1) % seg, o + i) for i in range(seg)]
    add(mat, pts, quads, pos)


# --------------------------------------------------------- the Stocker ----
# Gaunt 2.9 m night-shift worker gone wrong: hunched spine, arms that drag
# past its knees, a torn apron, and a cracked barcode-scanner where a face
# should be. Faces +Z.
HIP_Y = 1.25
LEAN = 0.38  # forward hunch (radians)

for side in (-1, 1):
    hx = 0.17 * side
    knee = (0.22 * side, 0.68, 0.10)
    ankle = (0.20 * side, 0.08, -0.04)
    limb("skin", (hx, HIP_Y, 0), knee, 0.075, 0.05)
    limb("skin", knee, ankle, 0.05, 0.035)
    box("skin", (0.13, 0.06, 0.30), (ankle[0], 0.03, 0.05))  # long feet
    for t in (-0.045, 0.0, 0.045):  # toe claws
        limb("claw", (ankle[0] + t, 0.03, 0.19), (ankle[0] + t * 1.3, 0.0, 0.29), 0.018, 0.004, 4)

# pelvis + hunched torso (stack of tapering slabs bending forward)
box("cloth", (0.42, 0.18, 0.24), (0, HIP_Y, 0))
spine = []
y, z = HIP_Y + 0.08, 0.0
for i, (w, d) in enumerate(((0.36, 0.22), (0.40, 0.24), (0.50, 0.27), (0.56, 0.28), (0.50, 0.25))):
    a = LEAN * (i + 1) / 5
    y += 0.17 * math.cos(a)
    z += 0.17 * math.sin(a)
    spine.append((y, z, a))
    box("skin", (w, 0.19, d), (0, y, z), r=(a, 0, 0), taper=1.05)
    # protruding vertebrae on the back
    box("bone", (0.06, 0.06, 0.08), (0, y, z - d / 2 - 0.02), r=(a, 0, 0.785))

# apron: two flat panels over front of torso + hanging skirt
ay, az, aa = spine[2]
box("apron", (0.46, 0.55, 0.03), (0, ay - 0.05, az + 0.15), r=(aa, 0, 0))
box("apron", (0.50, 0.55, 0.03), (0, HIP_Y - 0.25, 0.15), r=(-0.08, 0, 0))
box("apron", (0.10, 0.10, 0.012), (0.10, ay + 0.08, az + 0.17), r=(aa, 0, 0))  # name badge
box("badge", (0.08, 0.04, 0.014), (0.10, ay + 0.09, az + 0.172), r=(aa, 0, 0))

# shoulders + very long arms
sy, sz, sa = spine[3]
for side in (-1, 1):
    sh = (0.32 * side, sy + 0.05, sz)
    elbow = (0.42 * side, sy - 0.55, sz + 0.25)
    wrist = (0.38 * side, sy - 1.25, sz + 0.38)
    sphere("skin", 0.09, sh)
    limb("skin", sh, elbow, 0.06, 0.042)
    limb("skin", elbow, wrist, 0.042, 0.03)
    box("skin", (0.10, 0.12, 0.05), (wrist[0], wrist[1] - 0.06, wrist[2]))
    for f in range(4):  # long finger-claws
        fx = wrist[0] + (f - 1.5) * 0.025
        mid = (fx, wrist[1] - 0.24, wrist[2] + 0.06)
        limb("skin", (fx, wrist[1] - 0.1, wrist[2]), mid, 0.012, 0.009, 4)
        limb("claw", mid, (fx, wrist[1] - 0.40, wrist[2] + 0.16), 0.009, 0.002, 4)

# neck + scanner head
ny, nz, na = spine[4]
head = (0, ny + 0.28, nz + 0.30)
limb("skin", (0, ny + 0.08, nz + 0.05), (head[0], head[1] - 0.08, head[2] - 0.06), 0.05, 0.04)
box("plastic", (0.30, 0.20, 0.26), head, r=(0.25, 0, 0), taper=0.85)       # scanner housing
box("plastic", (0.10, 0.22, 0.10), (0, head[1] - 0.17, head[2] - 0.05), r=(0.6, 0, 0))  # handle stub
box("eye", (0.24, 0.035, 0.02), (0, head[1] + 0.01, head[2] + 0.135), r=(0.25, 0, 0))  # red scan slit
box("eye", (0.035, 0.035, 0.02), (-0.08, head[1] + 0.06, head[2] + 0.125), r=(0.25, 0, 0))
# cracked jaw hanging open under the scanner, full of teeth
jaw_y, jaw_z = head[1] - 0.14, head[2] + 0.08
box("skin", (0.24, 0.05, 0.18), (0, jaw_y, jaw_z), r=(-0.35, 0, 0))
for i in range(7):
    tx = -0.09 + i * 0.03
    limb("bone", (tx, jaw_y + 0.02, jaw_z + 0.07), (tx, jaw_y + 0.08, jaw_z + 0.08), 0.012, 0.002, 4)
    limb("bone", (tx + 0.015, head[1] - 0.09, head[2] + 0.12), (tx + 0.015, head[1] - 0.14, head[2] + 0.13), 0.011, 0.002, 4)

MATERIALS = {
    "skin": (0.62, 0.64, 0.60),
    "bone": (0.86, 0.82, 0.70),
    "claw": (0.12, 0.10, 0.10),
    "cloth": (0.15, 0.15, 0.17),
    "apron": (0.55, 0.20, 0.10),
    "badge": (0.95, 0.95, 0.90),
    "plastic": (0.10, 0.10, 0.11),
    "eye": (1.00, 0.05, 0.05),
}


def write():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "the_stocker.mtl"), "w") as f:
        for name, (r, g, b) in MATERIALS.items():
            f.write(f"newmtl M_Stocker_{name}\nKd {r:.3f} {g:.3f} {b:.3f}\nKs 0.05 0.05 0.05\n")
            if name == "eye":
                f.write("Ke 4.0 0.2 0.2\n")
            f.write("\n")
    with open(os.path.join(OUT, "the_stocker.obj"), "w") as f:
        f.write("# The Stocker - Nightmart monster. Y-up, metres, faces +Z.\n")
        f.write("mtllib the_stocker.mtl\no TheStocker\n")
        for v in verts:
            f.write("v %.4f %.4f %.4f\n" % v)
        cur = None
        for mat, idx in sorted(faces, key=lambda fc: fc[0]):
            if mat != cur:
                f.write(f"usemtl M_Stocker_{mat}\n")
                cur = mat
            f.write("f " + " ".join(str(i + 1) for i in idx) + "\n")
    print(f"wrote {len(verts)} verts, {len(faces)} faces")


def preview():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(12, 9), facecolor="#07080a")
    for k, (azim, title) in enumerate(((55, "three-quarter"), (90, "front"), (0, "side"))):
        ax = fig.add_subplot(1, 3, k + 1, projection="3d", facecolor="#07080a")
        polys, cols = [], []
        light = (0.4, 0.8, 0.6)
        for mat, idx in faces:
            p = [(verts[i][0], verts[i][2], verts[i][1]) for i in idx]  # to Z-up
            u = [p[1][j] - p[0][j] for j in range(3)]
            w = [p[-1][j] - p[0][j] for j in range(3)]
            n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
            ln = math.sqrt(sum(c * c for c in n)) or 1
            shade = 0.35 + 0.65 * abs(sum(n[j] / ln * light[j] for j in range(3)))
            c = MATERIALS[mat]
            if mat == "eye":
                shade = 1.0
            polys.append(p)
            cols.append(tuple(min(1, ch * shade) for ch in c))
        ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=(0, 0, 0, 0.25), linewidths=0.2))
        ax.set_xlim(-0.6, 0.6); ax.set_ylim(-0.4, 0.8); ax.set_zlim(0, 2.9)
        ax.set_box_aspect((1.2, 1.2, 2.9), zoom=1.15)
        ax.view_init(elev=8, azim=azim)
        ax.set_axis_off()
        ax.set_title(title, color="#888")
    fig.suptitle("THE STOCKER  -  Nightmart", color="#e33", fontsize=18, family="monospace")
    fig.savefig(os.path.join(OUT, "the_stocker_preview.png"), dpi=110, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    write()
    preview()
