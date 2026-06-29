from PIL import Image, ImageDraw, ImageFont

SRC = r'C:\Users\DH\Downloads\WhatsApp Image 2026-06-28 at 12.31.51 PM.jpeg'
DST = r'C:\Users\DH\gay-app-list\store_assets\store_icon_512.png'

img = Image.open(SRC).convert('RGB')
W, H = img.size

# Exact dark bg color from pixel scan
bg = (10, 7, 24)

draw = ImageDraw.Draw(img)

# Cover old subtitle — stays inside the rounded corners
y0 = int(H * 0.845)
y1 = int(H * 0.890)
x0 = int(W * 0.18)
x1 = int(W * 0.82)
draw.rectangle([x0, y0, x1, y1], fill=bg)

# Write new text
font_size = int(W * 0.048)
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
print(f'Done. Text at y={ty}, size {W}x{H}')
