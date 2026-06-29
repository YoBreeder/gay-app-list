"""GAL icon v2 — cleaner, properly proportioned"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

OUT = r'C:\Users\DH\gay-app-list\store_assets'
W, H = 512, 512
BG = (18, 16, 30)

RAINBOW = [
    (255, 30,  80),
    (255, 140, 0),
    (255, 230, 0),
    (0,   200, 80),
    (0,   130, 255),
    (160, 0,   255),
]

def lerp(colors, t):
    t = max(0.0, min(1.0, t))
    n = len(colors) - 1
    i = min(int(t * n), n - 1)
    lt = t * n - i
    c0, c1 = colors[i], colors[i+1]
    return tuple(int(c0[j] + (c1[j]-c0[j])*lt) for j in range(3))

def font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

BOLD = r'C:\Windows\Fonts\arialbd.ttf'
REG  = r'C:\Windows\Fonts\arial.ttf'

# ── Base image ────────────────────────────────────────────────
img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# ── Smooth rainbow arc using PIL arc ─────────────────────────
# Draw arc as thick colored segments
arc_layer = Image.new('RGBA', (W, H), (0,0,0,0))
arc_d = ImageDraw.Draw(arc_layer)
CX, CY = W//2, H//2 - 10
R = 210
THICKNESS = 22
STEPS = 360
START_DEG = 135   # start at bottom-left
END_DEG   = 45    # end at bottom-right (going clockwise over the top)

for step in range(STEPS):
    t = step / STEPS
    # Go from 135° to 405° (=45°+360°) — top arc
    angle_deg = 135 + t * 270
    angle_rad = math.radians(angle_deg)
    col = lerp(RAINBOW, t) + (255,)
    for r in range(R - THICKNESS//2, R + THICKNESS//2):
        x = int(CX + r * math.cos(angle_rad))
        y = int(CY + r * math.sin(angle_rad))
        if 0 <= x < W and 0 <= y < H:
            arc_d.ellipse([x-1, y-1, x+1, y+1], fill=col)

# Smooth the arc
arc_layer = arc_layer.filter(ImageFilter.GaussianBlur(1))
img = Image.alpha_composite(img, arc_layer)

# ── Globe (soft gradient circle, right side) ──────────────────
globe_layer = Image.new('RGBA', (W, H), (0,0,0,0))
GX, GY, GR = 320, 185, 105
globe_data = globe_layer.load()
for py in range(max(0, GY-GR-2), min(H, GY+GR+2)):
    for px in range(max(0, GX-GR-2), min(W, GX+GR+2)):
        dx, dy = px - GX, py - GY
        dist = math.sqrt(dx*dx + dy*dy)
        if dist <= GR:
            # Gradient based on position
            t = (px - (GX-GR)) / (GR*2)
            tv = (py - (GY-GR)) / (GR*2)
            col = lerp(RAINBOW, t*0.65 + tv*0.35)
            # Fade near edge
            edge_fade = max(0, min(255, int(255 * (1 - (dist/GR)**2))))
            # Dark center dimming
            dark = int(120 * (1 - dist/GR))
            final_col = tuple(max(0, c - dark//3) for c in col)
            globe_data[px, py] = final_col + (edge_fade,)

img = Image.alpha_composite(img, globe_layer)

# ── "GAL" text ────────────────────────────────────────────────
draw = ImageDraw.Draw(img)
f_big = font(BOLD, 195)

letters = ['G', 'A', 'L']
colors  = [lerp(RAINBOW, 0.0), lerp(RAINBOW, 0.5), lerp(RAINBOW, 0.85)]

# Measure total width
widths = []
for l in letters:
    bb = draw.textbbox((0,0), l, font=f_big)
    widths.append(bb[2]-bb[0])
total_w = sum(widths) + 10 * (len(letters)-1)  # small spacing

# Vertically center — shift up a bit to leave room for subtitle
bb0 = draw.textbbox((0,0), 'GAL', font=f_big)
text_h = bb0[3] - bb0[1]
ty = (H - text_h) // 2 - 25
tx = (W - total_w) // 2

# Shadow
sx = tx
for l, w in zip(letters, widths):
    draw.text((sx+3, ty+3), l, font=f_big, fill=(0,0,0,160))
    sx += w + 10

# Colored letters
sx = tx
for l, col, w in zip(letters, colors, widths):
    draw.text((sx, ty), l, font=f_big, fill=col)
    sx += w + 10

# ── Subtitle ──────────────────────────────────────────────────
f_sub = font(REG, 28)
sub = 'THE GAY APPS DIRECTORY'
sbb = draw.textbbox((0,0), sub, font=f_sub)
sw = sbb[2]-sbb[0]
draw.text(((W-sw)//2, 455), sub, font=f_sub, fill=(0, 210, 220))

# ── Rounded rect mask ─────────────────────────────────────────
mask = Image.new('L', (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([0,0,W-1,H-1], radius=85, fill=255)

final = Image.new('RGB', (W, H), (0,0,0))
final.paste(img.convert('RGB'), mask=mask)

path = os.path.join(OUT, 'gal_icon_512.png')
final.save(path)
print(f'Saved: {path}')
