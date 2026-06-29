from PIL import Image, ImageDraw, ImageFont

SRC = r'C:\Users\DH\Downloads\WhatsApp Image 2026-06-28 at 12.31.51 PM.jpeg'
DST = r'C:\Users\DH\gay-app-list\store_assets\store_icon_512.png'

img = Image.open(SRC).convert('RGB')
W, H = img.size
print(f'Size: {W}x{H}')

# Scan a horizontal strip near the bottom to find the dark bg color
# The subtitle "THE GAY APPS DIRECTORY" appears around y=88-94% on the original image
# Let's scan the left edge at various y positions inside the icon
print('Scanning pixels:')
for y_frac in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.92, 0.94, 0.96]:
    y = int(H * y_frac)
    for x_frac in [0.15, 0.20, 0.25]:
        x = int(W * x_frac)
        print(f'  ({x_frac:.2f}, {y_frac:.2f}) = {img.getpixel((x,y))}')

# The dark background of the icon (very dark navy) — hardcode from visual inspection
# It's the darkest part around the rounded rect edges
bg = (20, 16, 28)  # very dark navy

draw = ImageDraw.Draw(img)

# The subtitle line is in the bottom ~8-10% of the image
y0 = int(H * 0.880)
y1 = int(H * 0.960)
x0 = int(W * 0.05)
x1 = int(W * 0.95)
draw.rectangle([x0, y0, x1, y1], fill=bg)

# Write new text
font_size = int(W * 0.053)
try:
    f = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', font_size)
except:
    f = ImageFont.load_default()

new_text = 'THE GAY APP DIRECTORY'
neon_blue = (0, 210, 255)

bb = draw.textbbox((0,0), new_text, font=f)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
tx = (W-tw)//2
ty = y0 + (y1-y0-th)//2

draw.text((tx, ty), new_text, font=f, fill=neon_blue)
img.save(DST, quality=95)
print(f'Saved: {DST}')
