"""Add the 2D title, tagline, CAT 5 badge and rain on top of the Blender render.
Usage: python3 add_title.py <render.png> <font.ttf> <out.png>"""
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, font, out = sys.argv[1:4]
im = Image.open(src).convert("RGBA"); W, H = im.size
# rain
rain = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(rain); random.seed(3)
for _ in range(900):
    x, y = random.uniform(0, W), random.uniform(0, H)
    d.line([(x, y), (x - 22, y + 58)], fill=(225, 240, 255, random.randint(40, 90)), width=2)
im = Image.alpha_composite(im, rain.filter(ImageFilter.GaussianBlur(0.6)))

def big_text(img, text, xy, size, top, bottom, rot=-4):
    f = ImageFont.truetype(font, size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    x, y = xy
    for i in range(14, 0, -1):                                   # 3D extrude
        d.text((x + i * 1.2, y + i * 1.6), text, font=f, fill=(20, 14, 60, 255), stroke_width=14, stroke_fill=(20, 14, 60, 255))
    d.text((x, y), text, font=f, fill=(255, 255, 255, 255), stroke_width=14, stroke_fill=(12, 10, 40, 255))
    # vertical gradient fill on the face
    bbox = d.textbbox((x, y), text, font=f)
    grad = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    for yy in range(bbox[1], bbox[3] + 1):
        t = (yy - bbox[1]) / max(1, bbox[3] - bbox[1])
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3)) + (255,)
        gd.line([(bbox[0], yy), (bbox[2], yy)], fill=c)
    mask = Image.new("L", img.size, 0); ImageDraw.Draw(mask).text((x, y), text, font=f, fill=255)
    layer.paste(grad, (0, 0), mask)
    shadow = layer.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda a: int(a * 0.55))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 255)); sh.putalpha(shadow)
    layer = Image.alpha_composite(sh.transform(img.size, Image.AFFINE, (1, 0, -6, 0, 1, -14)), layer)
    return Image.alpha_composite(img, layer.rotate(rot, center=(x, y), resample=Image.BICUBIC))

im = big_text(im, "HURRICANE", (70, 40), 205, (255, 255, 255), (150, 225, 255))
im = big_text(im, "SURVIVAL", (95, 245), 185, (255, 236, 70), (255, 130, 20))
# tagline
d = ImageDraw.Draw(im); f = ImageFont.truetype(font, 62)
d.text((110, 470), "BUILD. HIDE. SURVIVE.", font=f, fill="white", stroke_width=9, stroke_fill=(12, 10, 40))
# CAT 5 badge
badge = Image.new("RGBA", (380, 170), (0, 0, 0, 0)); bd = ImageDraw.Draw(badge)
bd.rounded_rectangle([8, 8, 372, 162], 32, fill=(232, 30, 30), outline="white", width=10)
bf = ImageFont.truetype(font, 110); bd.text((190, 92), "CAT 5", font=bf, fill="white", anchor="mm", stroke_width=4, stroke_fill=(120, 0, 0))
badge = badge.rotate(8, expand=True, resample=Image.BICUBIC)
im.alpha_composite(badge, (W - badge.width - 40, H - badge.height - 30))
im.convert("RGB").save(out)
print("saved", out)
