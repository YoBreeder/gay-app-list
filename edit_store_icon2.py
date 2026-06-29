from PIL import Image, ImageDraw, ImageFont

SRC = r'C:\Users\DH\Downloads\WhatsApp Image 2026-06-28 at 12.31.51 PM.jpeg'
DST = r'C:\Users\DH\gay-app-list\store_assets\store_icon_512.png'

img = Image.open(SRC).convert('RGB')
W, H = img.size

# Sample the actual background color just above the text area
sample_y = int(H * 0.855)
sample_x = int(W * 0.5)
bg_color = img.getpixel((sample_x, sample_y))
print(f'Sampled bg color: {bg_color}')

# Also sample a few more points and average
samples = []
for sx in [int(W*0.1), int(W*0.2), int(W*0.5), int(W*0.8), int(W*0.9)]:
    for sy in [int(H*0.855), int(H*0.86)]:
        samples.append(img.getpixel((sx, sy)))

avg = tuple(int(sum(s[i] for s in samples)/len(samples)) for i in range(3))
print(f'Average bg color: {avg}')

draw = ImageDraw.Draw(img)

# Cover old text — use a slightly larger area to be safe
y0 = int(H * 0.855)
y1 = int(H * 0.960)
x0 = int(W * 0.02)
x1 = int(W * 0.98)

# Paint with averaged color
draw.rectangle([x0, y0, x1, y1], fill=avg)

# Write new text
font_size = int(W * 0.052)
try:
    f = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', font_size)
except:
    f = ImageFont.load_default()

new_text = 'THE GAY APP DIRECTORY'
neon_blue = (0, 215, 255)

bb = draw.textbbox((0,0), new_text, font=f)
tw = bb[2]-bb[0]
th = bb[3]-bb[1]
tx = (W-tw)//2
ty = y0 + (y1 - y0 - th)//2

draw.text((tx, ty), new_text, font=f, fill=neon_blue)

img.save(DST, quality=95)
print(f'Saved: {DST}')
