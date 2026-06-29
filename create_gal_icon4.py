"""GAL icon v4 — just GAL text + subtitle, no arc, no globe"""
from PIL import Image, ImageDraw, ImageFont
import os

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

SCALE = 2
WS, HS = W*SCALE, H*SCALE

img = Image.new('RGB', (WS, HS), (18, 16, 30))
draw = ImageDraw.Draw(img)

# ── "GAL" letters ─────────────────────────────────────────────
f_gal = fnt(BOLD, 240*SCALE)
letters = ['G', 'A', 'L']
cols    = [lerp(RAINBOW, 0.02), lerp(RAINBOW, 0.48), lerp(RAINBOW, 0.82)]

GAP = 12 * SCALE
widths = [draw.textbbox((0,0), l, font=f_gal)[2] - draw.textbbox((0,0), l, font=f_gal)[0] for l in letters]
text_h = draw.textbbox((0,0), 'G', font=f_gal)[3] - draw.textbbox((0,0), 'G', font=f_gal)[1]

total_w = sum(widths) + GAP * (len(letters)-1)
tx = (WS - total_w) // 2
ty = (HS - text_h) // 2 - 40*SCALE

# Shadow
sx = tx
for l, w in zip(letters, widths):
    draw.text((sx+5*SCALE, ty+5*SCALE), l, font=f_gal, fill=(0,0,0))
    sx += w + GAP

# Colored letters
sx = tx
for l, c, w in zip(letters, cols, widths):
    draw.text((sx, ty), l, font=f_gal, fill=c)
    sx += w + GAP

# ── Subtitle ──────────────────────────────────────────────────
f_sub = fnt(REG, 32*SCALE)
sub = 'THE APP DIRECTORY'
sbb = draw.textbbox((0,0), sub, font=f_sub)
sw = sbb[2]-sbb[0]
draw.text(((WS-sw)//2, ty + text_h + 40*SCALE), sub, font=f_sub, fill=(0, 215, 225))

# ── Downscale + rounded mask ──────────────────────────────────
img = img.resize((W, H), Image.LANCZOS)
mask = Image.new('L', (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([0,0,W-1,H-1], radius=88, fill=255)
final = Image.new('RGB', (W, H), (0,0,0))
final.paste(img, mask=mask)

path = os.path.join(OUT, 'gal_icon_512.png')
final.save(path, quality=95)
print(f'Saved: {path}')
