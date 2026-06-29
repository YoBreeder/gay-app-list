"""Create GAL icon — same style as reference, 512x512 for Play Store"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = r'C:\Users\DH\gay-app-list\store_assets'
os.makedirs(OUT, exist_ok=True)

W, H = 512, 512
BG = (22, 20, 35)  # deep dark navy

# Rainbow gradient stops (red → orange → yellow → green → blue → violet)
RAINBOW = [
    (255, 0,   60),   # red-pink
    (255, 80,  0),    # orange
    (255, 220, 0),    # yellow
    (0,  200, 80),    # green
    (0,  120, 255),   # blue
    (160, 0,  255),   # violet
]

def lerp_color(colors, t):
    """Interpolate through a list of colors. t in [0,1]"""
    if t <= 0: return colors[0]
    if t >= 1: return colors[-1]
    n = len(colors) - 1
    i = int(t * n)
    i = min(i, n - 1)
    local_t = (t * n) - i
    c0, c1 = colors[i], colors[i+1]
    return tuple(int(c0[j] + (c1[j]-c0[j]) * local_t) for j in range(3))

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return None

def find_font(bold=False):
    candidates = [
        r'C:\Windows\Fonts\arialbd.ttf',
        r'C:\Windows\Fonts\Arial Bold.ttf',
        r'C:\Windows\Fonts\calibrib.ttf',
        r'C:\Windows\Fonts\segoeui.ttf',
        r'C:\Windows\Fonts\arial.ttf',
    ] if bold else [
        r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\segoeui.ttf',
        r'C:\Windows\Fonts\calibri.ttf',
    ]
    for c in candidates:
        f = get_font(c, 10)
        if f: return c
    return None

# ── Canvas ──────────────────────────────────────────────────
img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Rounded rect mask ────────────────────────────────────────
mask = Image.new('L', (W, H), 0)
mdraw = ImageDraw.Draw(mask)
mdraw.rounded_rectangle([0, 0, W-1, H-1], radius=90, fill=255)

# ── Rainbow arc (ring around right side) ────────────────────
arc_img = Image.new('RGBA', (W, H), (0,0,0,0))
arc_draw = ImageDraw.Draw(arc_img)
CX, CY = 270, 256
R_outer, R_inner = 230, 210
for angle_deg in range(-50, 230, 1):
    t = (angle_deg + 50) / 280.0
    col = lerp_color(RAINBOW, t)
    angle_rad = math.radians(angle_deg)
    x0 = CX + R_outer * math.cos(angle_rad)
    y0 = CY - R_outer * math.sin(angle_rad)
    x1 = CX + R_inner * math.cos(angle_rad)
    y1 = CY - R_inner * math.sin(angle_rad)
    arc_draw.line([(x0, y0), (x1, y1)], fill=col + (255,), width=3)

img.paste(arc_img.convert('RGB'), mask=arc_img.split()[3])

# ── Globe (simplified circle with gradient) ──────────────────
globe_img = Image.new('RGBA', (W, H), (0,0,0,0))
globe_draw = ImageDraw.Draw(globe_img)

# Globe base circle
gx, gy, gr = 310, 200, 130
for px in range(gx - gr, gx + gr + 1):
    for py in range(gy - gr, gy + gr + 1):
        dx, dy = px - gx, py - gy
        if dx*dx + dy*dy <= gr*gr:
            t = ((px - (gx-gr)) / (gr*2))
            tv = ((py - (gy-gr)) / (gr*2))
            col = lerp_color(RAINBOW, t * 0.7 + tv * 0.3)
            globe_draw.point([px, py], fill=col + (200,))

# Dark overlay on globe for depth
for px in range(gx - gr, gx + gr + 1):
    for py in range(gy - gr, gy + gr + 1):
        dx, dy = px - gx, py - gy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist <= gr:
            alpha = int(160 * (1 - dist/gr) * 0.5)
            globe_draw.point([px, py], fill=(0, 0, 0, alpha))

img.paste(globe_img.convert('RGB'), mask=globe_img.split()[3])

# ── "GAL" text with rainbow gradient ────────────────────────
bold_font_path = find_font(bold=True)
reg_font_path = find_font(bold=False)
print(f'Font: {bold_font_path}')

f_gal = ImageFont.truetype(bold_font_path, 260) if bold_font_path else ImageFont.load_default()
f_sub = ImageFont.truetype(reg_font_path, 34) if reg_font_path else ImageFont.load_default()

# Measure "GAL"
bbox = draw.textbbox((0, 0), 'GAL', font=f_gal)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
tx = (W - tw) // 2 - 10
ty = (H - th) // 2 - 30

# Render each letter in rainbow gradient
letters = 'GAL'
letter_colors = [
    lerp_color(RAINBOW, 0.0),   # G = red-pink
    lerp_color(RAINBOW, 0.45),  # A = green-blue
    lerp_color(RAINBOW, 0.85),  # L = violet
]

# Draw shadow first
draw.text((tx+4, ty+4), 'GAL', font=f_gal, fill=(0, 0, 0, 180))

# Draw each letter separately with its color
x_cursor = tx
for i, letter in enumerate(letters):
    col = letter_colors[i]
    draw.text((x_cursor, ty), letter, font=f_gal, fill=col)
    lbbox = draw.textbbox((0, 0), letter, font=f_gal)
    x_cursor += lbbox[2] - lbbox[0]

# ── Subtitle ─────────────────────────────────────────────────
sub = 'THE GAY APPS DIRECTORY'
sbbox = draw.textbbox((0, 0), sub, font=f_sub)
sw = sbbox[2] - sbbox[0]
draw.text(((W - sw)//2, 440), sub, font=f_sub, fill=(0, 220, 220))  # cyan

# ── Apply rounded rect mask ──────────────────────────────────
final = Image.new('RGB', (W, H), (0, 0, 0))
final.paste(img, mask=mask)

path = os.path.join(OUT, 'gal_icon_512.png')
final.save(path)
print(f'Saved: {path}')
