import random, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
random.seed(7)
face = Image.open(os.path.join(ROOT, 'assets', 'faces', 'talita_7_super_32.png')).convert('RGBA')

def icon(size, face_frac, maskable):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    for y in range(size):                                   # night-sky gradient
        t = y / size
        d.line([(0, y), (size, y)], fill=(int(4 + 14 * t), int(3 + 10 * t), int(14 + 26 * t), 255))
    for _ in range(int(size * size / 900)):                 # pixel stars
        x, y, s = random.randrange(size), random.randrange(int(size * .75)), max(1, size // 256)
        c = random.choice([(255, 255, 255), (255, 233, 176), (190, 190, 255)])
        d.rectangle([x, y, x + s, y + s], fill=c + (255,))
    gy = int(size * .80)                                    # moon ground with the striped pad
    pts = [(0, gy)]
    for i in range(1, 17):
        pts.append((i * size / 16, gy + random.randint(-size // 40, size // 40)))
    pts += [(size, size), (0, size)]
    d.polygon(pts, fill=(80, 80, 88, 255))
    pw, px0 = size * .34, size * .33
    d.rectangle([px0, gy - size * .012, px0 + pw, gy + size * .018], fill=(255, 210, 60, 255))
    for i in range(8):
        x = px0 + i * pw / 8
        d.polygon([(x, gy + size * .018), (x + pw / 16, gy - size * .012), (x + pw / 8, gy - size * .012), (x + pw / 16, gy + size * .018)], fill=(27, 27, 27, 255))
    fs = int(size * face_frac) // 32 * 32                   # Talita, integer-scaled so pixels stay crisp
    f = face.resize((fs, fs), Image.NEAREST)
    im.alpha_composite(f, ((size - fs) // 2, int(size * (0.47 if maskable else 0.43)) - fs // 2))
    return im.convert('RGB') if maskable else im

import os
os.chdir(ROOT); os.makedirs('icons', exist_ok=True)
icon(512, .70, False).save('icons/icon-512.png')
icon(512, .70, False).resize((192, 192), Image.LANCZOS).save('icons/icon-192.png')
icon(512, .56, True).save('icons/icon-maskable-512.png')
icon(512, .70, False).convert('RGB').resize((180, 180), Image.LANCZOS).save('icons/apple-touch-icon.png')
print('icons ok')
