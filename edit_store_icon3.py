from PIL import Image, ImageDraw, ImageFont

SRC = r'C:\Users\DH\Downloads\WhatsApp Image 2026-06-28 at 12.31.51 PM.jpeg'
DST = r'C:\Users\DH\gay-app-list\store_assets\store_icon_512.png'

img = Image.open(SRC).convert('RGB')
W, H = img.size

# Sample from the dark area between the arc bottom and the subtitle — left side, clear of any element
# Try a few spots and pick darkest
test_points = [
    (int(W*0.08), int(H*0.80)),
    (int(W*0.08), int(H*0.82)),
    (int(W*0.10), int(H*0.84)),
    (int(W*0.12), int(H*0.86)),
]
for pt in test_points:
    print(f'  pixel at {pt}: {img.getpixel(pt)}')

# Use the darkest sample
samples = [img.getpixel(pt) for pt in test_points]
bg = min(samples, key=lambda c: c[0]+c[1]+c[2])
print(f'Using bg: {bg}')

draw = ImageDraw.Draw(img)

# Cover old text
y0 = int(H * 0.862)
y1 = int(H * 0.955)
x0 = int(W * 0.03)
x1 = int(W * 0.97)
draw.rectangle([x0, y0, x1, y1], fill=bg)

# New text
font_size = int(W * 0.052)
try:
    f = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', font_size)
except:
    f = ImageFont.load_default()

new_text = 'THE GAY APP DIRECTORY'
neon_blue = (0, 215, 255)

bb = draw.textbbox((0,0), new_text, font=f)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
tx = (W-tw)//2
ty = y0 + (y1-y0-th)//2

draw.text((tx, ty), new_text, font=f, fill=neon_blue)
img.save(DST, quality=95)
print(f'Saved: {DST}')
