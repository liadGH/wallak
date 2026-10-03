"""Draws the Wallak home-screen icon and writes the PNG sizes iPhone and the web manifest need.

Run from the repo root:  python tools/make_icons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CORAL = (255, 107, 74)
CORAL_DEEP = (236, 78, 52)
SUN = (255, 194, 46)
WHITE = (255, 255, 255)
S = 1024  # master size; scaled down for each output

out = Path(__file__).resolve().parent.parent / "icons"
out.mkdir(exist_ok=True)

img = Image.new("RGB", (S, S), CORAL)
d = ImageDraw.Draw(img, "RGBA")

# soft diagonal shading: deeper coral toward the bottom-left
for y in range(S):
    t = y / S
    d.line([(0, y), (S, y)], fill=tuple(int(CORAL[i] + (CORAL_DEEP[i] - CORAL[i]) * t * 0.8) for i in range(3)))

# the same playful circles used on the app's main card
d.ellipse([560, -220, 1260, 480], fill=(255, 255, 255, 38))
d.ellipse([620, 700, 1000, 1080], fill=SUN + (150,))

# bold W
font = ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", 660)
text = "W"
box = d.textbbox((0, 0), text, font=font)
w, h = box[2] - box[0], box[3] - box[1]
x, y = (S - w) / 2 - box[0], (S - h) / 2 - box[1] - 20
d.text((x + 10, y + 16), text, font=font, fill=(150, 40, 20, 70))  # soft drop shadow
d.text((x, y), text, font=font, fill=WHITE)

# small star: the abs bonus mark
cx, cy, r1, r2 = 812, 890, 70, 30
import math
pts = []
for k in range(10):
    a = -math.pi / 2 + k * math.pi / 5
    r = r1 if k % 2 == 0 else r2
    pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
d.polygon(pts, fill=WHITE)

for size, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png"), (1024, "icon-1024.png")]:
    img.resize((size, size), Image.LANCZOS).save(out / name)

# maskable variant: artwork shrunk into the safe zone on a coral field
mask = Image.new("RGB", (S, S), CORAL)
inner = img.resize((int(S * 0.8), int(S * 0.8)), Image.LANCZOS)
mask.paste(inner, (int(S * 0.1), int(S * 0.1)))
mask.resize((512, 512), Image.LANCZOS).save(out / "icon-maskable-512.png")
print("icons written to", out)
