"""Edit the store icon: replace 'THE GAY APPS DIRECTORY' with 'THE GAY APP DIRECTORY'"""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = r'C:\Users\DH\Downloads\WhatsApp Image 2026-06-28 at 12.31.51 PM.jpeg'
DST = r'C:\Users\DH\gay-app-list\store_assets\store_icon_512.png'

img = Image.open(SRC).convert('RGB')
W, H = img.size
print(f'Image size: {W}x{H}')

draw = ImageDraw.Draw(img)

# Paint over the existing bottom text with the background color (~dark navy)
# The text sits near the bottom ~88-94% down the image
text_y_start = int(H * 0.865)
text_y_end   = int(H * 0.935)
text_x_start = int(W * 0.05)
text_x_end   = int(W * 0.95)

# Sample background color from that area (should be dark navy)
bg_color = (22, 18, 35)
draw.rectangle([text_x_start, text_y_start, text_x_end, text_y_end], fill=bg_color)

# Now write the new text in blue neon (cyan-blue)
BOLD = r'C:\Windows\Fonts\arialbd.ttf'
REG  = r'C:\Windows\Fonts\arial.ttf'

# Scale font size to image dimensions
font_size = int(W * 0.048)
try:
    f = ImageFont.truetype(BOLD, font_size)
except:
    f = ImageFont.load_default()

new_text = 'THE GAY APP DIRECTORY'
neon_blue = (0, 210, 255)  # bright cyan-blue neon

bb = draw.textbbox((0,0), new_text, font=f)
tw = bb[2] - bb[0]
th = bb[3] - bb[1]

tx = (W - tw) // 2
ty = text_y_start + (text_y_end - text_y_start - th) // 2

draw.text((tx, ty), new_text, font=f, fill=neon_blue)

img.save(DST, quality=95)
print(f'Saved: {DST}')
