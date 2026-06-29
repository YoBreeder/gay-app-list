"""Create Play Store graphics for Gay App List"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r'C:\Users\DH\gay-app-list\store_assets'
os.makedirs(OUT, exist_ok=True)

# Color palette - rainbow pride flag colors
PRIDE_COLORS = ['#E40303','#FF8C00','#FFED00','#008026','#004DFF','#750787']
BG = '#1a1a2e'     # deep navy
PINK = '#FF69B4'   # hot pink
WHITE = '#FFFFFF'

def make_gradient_bg(img, colors, vertical=True):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    n = len(colors)
    for i, color in enumerate(colors):
        r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
        if vertical:
            y0 = int(i * h / n)
            y1 = int((i+1) * h / n)
            draw.rectangle([0, y0, w, y1], fill=(r,g,b))
        else:
            x0 = int(i * w / n)
            x1 = int((i+1) * w / n)
            draw.rectangle([x0, 0, x1, h], fill=(r,g,b))


def get_font(size, bold=False):
    """Try system fonts, fall back to default"""
    font_names = ['arialbd.ttf','arial.ttf','segoeui.ttf','calibri.ttf'] if bold else ['arial.ttf','segoeui.ttf','calibri.ttf']
    for name in font_names:
        for path in [r'C:\Windows\Fonts', r'/usr/share/fonts/truetype']:
            try:
                return ImageFont.truetype(os.path.join(path, name), size)
            except:
                pass
    return ImageFont.load_default()


# ─── App Icon 512x512 ───────────────────────────────────────
icon = Image.new('RGB', (512, 512), BG)
make_gradient_bg(icon, PRIDE_COLORS, vertical=True)

# Dark overlay
overlay = Image.new('RGBA', (512, 512), (26, 26, 46, 180))
icon = icon.convert('RGBA')
icon = Image.alpha_composite(icon, overlay)

draw = ImageDraw.Draw(icon)

# Circle background
draw.ellipse([56, 56, 456, 456], fill=(26, 26, 46, 220))

# "GL" letters
f_big = get_font(200, bold=True)
f_small = get_font(52)

# Draw the rainbow flag stripes at the bottom of circle
for i, c in enumerate(PRIDE_COLORS):
    r,g,b = int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
    y = 320 + i * 32
    draw.rectangle([80, y, 432, y+30], fill=(r,g,b,200))

# Clip to circle using mask
mask = Image.new('L', (512, 512), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse([56, 56, 456, 456], fill=255)
icon.putalpha(mask)

# Paste onto white bg for PNG
final_icon = Image.new('RGB', (512, 512), BG)
final_icon.paste(icon, mask=icon.split()[3])

draw2 = ImageDraw.Draw(final_icon)

# Text: "GAY" and "APP LIST"
f1 = get_font(110, bold=True)
f2 = get_font(70, bold=True)

# GAY - white text
bbox = draw2.textbbox((0,0), 'GAY', font=f1)
tw = bbox[2]-bbox[0]
draw2.text(((512-tw)//2, 120), 'GAY', font=f1, fill=WHITE)

# APP LIST
bbox2 = draw2.textbbox((0,0), 'APP LIST', font=f2)
tw2 = bbox2[2]-bbox2[0]
draw2.text(((512-tw2)//2, 250), 'APP LIST', font=f2, fill=PINK)

# Rainbow dots row
for i, c in enumerate(PRIDE_COLORS):
    x = 100 + i * 55
    draw2.ellipse([x, 370, x+35, 405], fill=c)

icon_path = os.path.join(OUT, 'icon_512.png')
final_icon.save(icon_path)
print(f'Saved icon: {icon_path}')


# ─── Feature Graphic 1024x500 ───────────────────────────────
feat = Image.new('RGB', (1024, 500), BG)
make_gradient_bg(feat, PRIDE_COLORS, vertical=False)

# Dark overlay
ov2 = Image.new('RGBA', (1024, 500), (26, 26, 46, 200))
feat = feat.convert('RGBA')
feat = Image.alpha_composite(feat, ov2)
feat = feat.convert('RGB')

draw3 = ImageDraw.Draw(feat)

f_title = get_font(100, bold=True)
f_sub = get_font(44)
f_small2 = get_font(30)

# Title
bbox = draw3.textbbox((0,0), 'GAY APP LIST', font=f_title)
tw = bbox[2]-bbox[0]
draw3.text(((1024-tw)//2, 80), 'GAY APP LIST', font=f_title, fill=WHITE)

# Subtitle
sub = 'The Ultimate LGBTQ+ App Directory'
bbox2 = draw3.textbbox((0,0), sub, font=f_sub)
tw2 = bbox2[2]-bbox2[0]
draw3.text(((1024-tw2)//2, 210), sub, font=f_sub, fill=PINK)

# Stats
stat = '70+ Apps  |  7 Regions  |  Free Forever'
bbox3 = draw3.textbbox((0,0), stat, font=f_small2)
tw3 = bbox3[2]-bbox3[0]
draw3.text(((1024-tw3)//2, 300), stat, font=f_small2, fill='#CCCCCC')

# Rainbow stripes at bottom
for i, c in enumerate(PRIDE_COLORS):
    x = i * (1024//6)
    draw3.rectangle([x, 440, x + 1024//6, 500], fill=c)

feat_path = os.path.join(OUT, 'feature_1024x500.png')
feat.save(feat_path)
print(f'Saved feature graphic: {feat_path}')


# ─── Phone Screenshots (1080x1920 - 9:16 portrait) ──────────
def make_screenshot(title, subtitle, items, filename, bg_col=BG):
    sc = Image.new('RGB', (1080, 1920), bg_col)
    # Header gradient
    header = Image.new('RGB', (1080, 300))
    make_gradient_bg(header, PRIDE_COLORS, vertical=False)
    sc.paste(header, (0, 0))

    # Dark overlay on header
    hov = Image.new('RGBA', (1080, 300), (0,0,0,120))
    sc_rgba = sc.convert('RGBA')
    sc_rgba.paste(hov, (0,0), hov)
    sc = sc_rgba.convert('RGB')

    draw4 = ImageDraw.Draw(sc)

    # App name in header
    f_h = get_font(80, bold=True)
    bbox = draw4.textbbox((0,0), 'GAY APP LIST', font=f_h)
    tw = bbox[2]-bbox[0]
    draw4.text(((1080-tw)//2, 90), 'GAY APP LIST', font=f_h, fill=WHITE)

    # Title
    f_t = get_font(58, bold=True)
    bbox = draw4.textbbox((0,0), title, font=f_t)
    tw = bbox[2]-bbox[0]
    draw4.text(((1080-tw)//2, 340), title, font=f_t, fill=PINK)

    # Subtitle
    f_sub2 = get_font(36)
    bbox = draw4.textbbox((0,0), subtitle, font=f_sub2)
    tw = bbox[2]-bbox[0]
    draw4.text(((1080-tw)//2, 430), subtitle, font=f_sub2, fill='#AAAAAA')

    # List items
    f_item = get_font(42)
    y = 530
    for item in items:
        # App row background
        draw4.rounded_rectangle([60, y, 1020, y+90], radius=15, fill=(40, 40, 70))
        # Colored dot
        color = PRIDE_COLORS[items.index(item) % len(PRIDE_COLORS)]
        draw4.ellipse([90, y+25, 130, y+65], fill=color)
        # Text
        draw4.text((155, y+20), item, font=f_item, fill=WHITE)
        y += 110

    # Bottom tagline
    f_tag = get_font(34)
    tag = 'Discover the LGBTQ+ world'
    bbox = draw4.textbbox((0,0), tag, font=f_tag)
    tw = bbox[2]-bbox[0]
    draw4.text(((1080-tw)//2, 1820), tag, font=f_tag, fill='#888888')

    path = os.path.join(OUT, filename)
    sc.save(path)
    print(f'Saved screenshot: {path}')

make_screenshot(
    'Global Apps',
    'Apps used worldwide',
    ['Grindr', 'Scruff', 'HER', 'Hornet', 'Taimi', 'Feeld', 'Lex', 'GROWLr', 'Recon', 'SURGE'],
    'screenshot_1_global.png'
)

make_screenshot(
    'Regional Apps',
    'Apps from around the world',
    ['Blued (Asia)', 'Jack\'d (US)', 'PlanetRomeo (EU)', 'Wapa (Latam)', 'GayLatino', 'Gaysir (EU)', 'Wapo (ES)', 'Scruff (US)', 'Bender', 'PinkApp'],
    'screenshot_2_regional.png'
)

make_screenshot(
    '70+ LGBTQ+ Apps',
    '7 regions, all identities',
    ['Gay Men', 'Queer Women', 'Trans People', 'Bears & Fetish', 'Bi & Queer', 'Pan & Non-binary', 'LGBTQ+ Social', 'Dating & Hookups', 'Community', 'Allies Welcome'],
    'screenshot_3_categories.png'
)

print('\nAll assets created!')
