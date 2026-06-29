"""GAL icon v3 — clean PIL arc, proper composition"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

OUT = r'C:\Users\DH\gay-app-list\store_assets'
W, H = 512, 512

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

BOLD = r'C:\Windows\Fonts\arialbd.ttf'
REG  = r'C:\Windows\Fonts\arial.ttf'

def fnt(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# Work at 2x for anti-aliasing, then downscale
SCALE = 2
WS, HS = W*SCALE, H*SCALE

img = Image.new('RGB', (WS, HS), (18, 16, 30))
draw = ImageDraw.Draw(img)

# ── Rainbow arc: draw many thin arcs in different colors ──────
# Arc goes from about 200° to 340° (right side, bottom-right to top-right)
# Play Console icon: arc on the right, starting from bottom-left going over top to bottom-right
CX, CY = WS//2 + 30, HS//2
R = 195 * SCALE
THICK = 18 * SCALE

# Draw rainbow arc in 60 segments
N_SEGS = 120
for i in range(N_SEGS):
    t0 = i / N_SEGS
    t1 = (i + 1) / N_SEGS
    col = lerp(RAINBOW, t0)
    # Arc from ~135° to 405° (full top arc, left-bottom to right-bottom over top)
    a0 = 135 + t0 * 270
    a1 = 135 + t1 * 270
    for r in range(R - THICK//2, R + THICK//2 + 1, 2):
        bbox = [CX-r, CY-r, CX+r, CY+r]
        draw.arc(bbox, start=a0, end=a1, fill=col, width=4*SCALE)

# ── Globe: clean gradient circle upper-right ──────────────────
GX, GY = int(0.62*WS), int(0.36*HS)
GR = int(0.195*WS)

globe = Image.new('RGBA', (WS, HS), (0,0,0,0))
gdata = globe.load()
for py in range(GY-GR, GY+GR+1):
    for px in range(GX-GR, GX+GR+1):
        dx, dy = px-GX, py-GY
        d2 = dx*dx + dy*dy
        if d2 <= GR*GR:
            dist = math.sqrt(d2)
            t = (px-(GX-GR))/(GR*2)
            tv = (py-(GY-GR))/(GR*2)
            col = lerp(RAINBOW, t*0.6 + tv*0.4)
            # Edge fade
            fade = max(0, min(255, int(220*(1-(dist/GR)**1.5))))
            # Dark inner shadow for depth
            dark_factor = max(0, 1 - dist/GR * 0.6)
            col = tuple(max(0, int(c * (0.5 + 0.5*dark_factor))) for c in col)
            if 0<=px<WS and 0<=py<HS:
                gdata[px,py] = col + (fade,)

img_rgba = img.convert('RGBA')
img_rgba = Image.alpha_composite(img_rgba, globe)
img = img_rgba.convert('RGB')
draw = ImageDraw.Draw(img)

# ── "GAL" — each letter a different rainbow color ─────────────
f_gal = fnt(BOLD, 190*SCALE)
letters = ['G', 'A', 'L']
cols    = [lerp(RAINBOW, 0.02), lerp(RAINBOW, 0.48), lerp(RAINBOW, 0.82)]

# Measure
dummy = ImageDraw.Draw(img)
widths = [dummy.textbbox((0,0), l, font=f_gal)[2] - dummy.textbbox((0,0), l, font=f_gal)[0] for l in letters]
bb0 = dummy.textbbox((0,0), 'G', font=f_gal)
text_h = bb0[3] - bb0[1]

GAP = 8 * SCALE
total_w = sum(widths) + GAP * (len(letters)-1)
tx = (WS - total_w)//2 - 15*SCALE
ty = (HS - text_h)//2 - 10*SCALE

# Shadow
sx = tx
for l, w in zip(letters, widths):
    draw.text((sx+4*SCALE, ty+4*SCALE), l, font=f_gal, fill=(0,0,0))
    sx += w + GAP

# Letters
sx = tx
for l, c, w in zip(letters, cols, widths):
    draw.text((sx, ty), l, font=f_gal, fill=c)
    sx += w + GAP

# ── Subtitle ──────────────────────────────────────────────────
f_sub = fnt(REG, 28*SCALE)
sub = 'THE GAY APPS DIRECTORY'
sbb = draw.textbbox((0,0), sub, font=f_sub)
sw = sbb[2]-sbb[0]
draw.text(((WS-sw)//2, HS - 70*SCALE), sub, font=f_sub, fill=(0, 215, 225))

# ── Downscale to 512x512 (anti-alias) ────────────────────────
img = img.resize((W, H), Image.LANCZOS)

# ── Rounded rect mask ─────────────────────────────────────────
mask = Image.new('L', (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([0,0,W-1,H-1], radius=88, fill=255)
final = Image.new('RGB', (W, H), (0,0,0))
final.paste(img, mask=mask)

path = os.path.join(OUT, 'gal_icon_512.png')
final.save(path, quality=95)
print(f'Saved: {path}')
