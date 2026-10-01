import math, os, zipfile
from PIL import Image

W = H = 32
C = {
    'out': (42, 24, 16, 255), 'hd': (52, 32, 20, 255), 'hm': (96, 62, 36, 255), 'hl': (150, 104, 62, 255),
    'sk': (242, 198, 160, 255), 'ss': (214, 160, 124, 255), 'sl': (255, 222, 192, 255), 'ch': (236, 150, 140, 255),
    'cr': (230, 100, 100, 255), 'ey': (40, 24, 16, 255), 'wh': (255, 255, 255, 255), 'pu': (86, 50, 28, 255),
    'lp': (200, 100, 100, 255), 'md': (110, 30, 36, 255), 'tt': (255, 250, 240, 255), 'tg': (230, 110, 120, 255),
    'cl': (255, 95, 176, 255), 'cL': (255, 170, 215, 255), 'sh': (30, 36, 52, 255), 'so': (240, 160, 96, 255),
    'tr': (110, 190, 255, 255), 'st': (255, 220, 60, 255), 'sw': (255, 255, 200, 255), 'ba': (232, 196, 140, 255),
    'bd': (200, 160, 110, 255), 'fl': (250, 120, 110, 255),
}

def base():
    g = [[None] * W for _ in range(H)]
    cx = 15.5
    # hair mass (curly, bob length)
    for y in range(H):
        for x in range(W):
            a = math.atan2(y - 13, x - cx)
            r = ((x - cx) / 13.8) ** 2 + ((y - 13.2) / 12.6) ** 2
            if r <= 1 + 0.12 * math.sin(a * 11) and y <= 26:
                ox_ = 2 if (y // 3) % 2 else 0
                cx_, cy_ = (x + ox_) % 4, y % 3
                if (cx_, cy_) in ((0, 0), (1, 0), (0, 1)):
                    g[y][x] = 'hl'
                elif (cx_, cy_) in ((2, 2), (3, 1), (3, 2)):
                    g[y][x] = 'hd'
                else:
                    g[y][x] = 'hm'
    # shirt
    for y in range(27, 32):
        for x in range(W):
            if abs(x - cx) <= 9 + (y - 27) * 0.8:
                g[y][x] = 'sh'
    # neck
    for y in range(25, 29):
        for x in range(13, 19):
            g[y][x] = 'ss' if y == 25 else 'sk'
    for x in range(13, 19):
        g[28][x] = 'sk'
    g[29][14] = g[29][15] = g[29][16] = g[29][17] = 'sk'
    # shirt print hint
    for x in (10, 11, 12, 19, 20, 21):
        g[30][x] = 'so'
    g[31][11] = g[31][20] = 'so'
    # face
    for y in range(H):
        for x in range(W):
            if ((x - cx) / 7.6) ** 2 + ((y - 17.5) / 8.2) ** 2 <= 1:
                g[y][x] = 'sk'
    # face shading on right edge + chin
    for y in range(H):
        for x in range(W):
            if g[y][x] == 'sk' and y < 26:
                if ((x - cx - 1.2) / 7.6) ** 2 + ((y - 17.0) / 8.2) ** 2 > 1:
                    g[y][x] = 'ss'
    # bangs / fringe curls
    fringe = {9: 22, 10: 20, 11: 17, 12: 13}  # row: half-width covered
    for y, hw in fringe.items():
        for x in range(W):
            if abs(x - cx) <= 8 and g[y][x] in ('sk', 'ss'):
                edge = (x * 7) % 5
                if y <= 10 or edge in (0, 1, 3):
                    g[y][x] = 'hm' if (x + y) % 4 else 'hl'
    # side curls framing face
    for y in range(12, 24):
        for x in (8, 23):
            if g[y][x] in ('sk', 'ss'):
                g[y][x] = 'hm'
    # forehead highlight
    g[13][13] = g[13][14] = 'sl'
    # nose
    g[19][16] = 'ss'; g[20][15] = 'ss'; g[20][16] = 'ss'
    # cheeks
    for p in ((10, 20), (11, 20), (20, 20), (21, 20)):
        g[p[1]][p[0]] = 'ch'
    # pink hair clip (top right, like the photo)
    for (x, y, c) in ((21, 2, 'cl'), (22, 2, 'cl'), (20, 3, 'cl'), (21, 3, 'cL'), (22, 3, 'cl'), (23, 3, 'cl'), (21, 4, 'cl'), (22, 4, 'cl')):
        g[y][x] = c
    return g

def put(g, pts, c):
    for x, y in pts:
        g[y][x] = c

def eyes_open(g, pupil='pu', dy=0):
    for ox in (9, 19):
        put(g, [(ox, 16 + dy), (ox + 1, 16 + dy), (ox + 2, 16 + dy), (ox + 3, 16 + dy)], 'ey')
        put(g, [(ox, 17 + dy), (ox + 3, 17 + dy), (ox, 18 + dy), (ox + 3, 18 + dy)], 'wh')
        put(g, [(ox + 1, 17 + dy), (ox + 2, 17 + dy), (ox + 1, 18 + dy), (ox + 2, 18 + dy)], 'ey')
        put(g, [(ox + 1, 18 + dy)], pupil)
        put(g, [(ox + 1, 17 + dy)], 'wh')  # glint
    put(g, [(8, 15 + dy), (23, 15 + dy)], 'ey')  # lashes

def brows(g, left, right):
    put(g, left, 'hd'); put(g, right, 'hd')

def neutral(g):
    eyes_open(g)
    brows(g, [(10, 14), (11, 14), (12, 14)], [(19, 14), (20, 14), (21, 14)])
    put(g, [(13, 22), (18, 22)], 'lp'); put(g, [(14, 23), (15, 23), (16, 23), (17, 23)], 'lp')

def happy(g):
    brows(g, [(10, 13), (11, 13), (12, 13)], [(19, 13), (20, 13), (21, 13)])
    for ox in (10, 19):
        put(g, [(ox + 1, 16), (ox, 17), (ox + 2, 17)], 'ey')
    put(g, [(9, 16), (22, 16)], 'ey')
    put(g, [(x, 21) for x in range(12, 20)], 'md')
    put(g, [(12, 22), (19, 22)], 'md')
    put(g, [(x, 22) for x in range(13, 19)], 'tt')
    g[22][15] = 'md'  # little gap between front teeth
    put(g, [(13, 23), (18, 23)], 'md'); put(g, [(x, 23) for x in range(14, 18)], 'tg')
    put(g, [(x, 24) for x in range(14, 18)], 'md')
    put(g, [(10, 20), (11, 20), (20, 20), (21, 20), (10, 19), (21, 19)], 'ch')

def surprised(g):
    brows(g, [(10, 12), (11, 12), (12, 12)], [(19, 12), (20, 12), (21, 12)])
    for ox in (10, 19):
        put(g, [(ox, 15), (ox + 1, 15), (ox + 2, 15)], 'ey')
        put(g, [(ox, 16), (ox + 2, 16), (ox, 17), (ox + 1, 17), (ox + 2, 17)], 'wh')
        put(g, [(ox + 1, 16)], 'ey')
        put(g, [(ox, 18), (ox + 1, 18), (ox + 2, 18)], 'ss')
    put(g, [(9, 14), (22, 14)], 'ey')
    put(g, [(15, 21), (16, 21), (14, 22), (17, 22), (14, 23), (17, 23), (15, 24), (16, 24)], 'md')
    put(g, [(15, 22), (16, 22), (15, 23), (16, 23)], 'tg')

def angry(g):
    eyes_open(g)
    put(g, [(9, 16), (22, 16)], 'sk')
    brows(g, [(10, 14), (11, 14), (11, 15), (12, 15), (12, 16)], [(21, 14), (20, 14), (20, 15), (19, 15), (19, 16)])
    put(g, [(x, 21) for x in range(13, 19)], 'md'); put(g, [(x, 23) for x in range(13, 19)], 'md')
    put(g, [(13, 22), (18, 22)], 'md'); put(g, [(x, 22) for x in range(14, 18)], 'tt')
    put(g, [(16, 22)], 'ss')
    put(g, [(9, 20), (10, 20), (11, 20), (20, 20), (21, 20), (22, 20)], 'cr')

def hurt(g):
    brows(g, [(10, 13), (11, 14), (12, 14)], [(19, 14), (20, 14), (21, 13)])
    put(g, [(10, 17), (11, 16), (12, 17)], 'ey'); put(g, [(9, 16), (13, 16)], 'ey')  # squeezed left eye
    ox = 19
    put(g, [(ox, 16), (ox + 1, 16), (ox + 2, 16)], 'ey'); put(g, [(ox, 17), (ox + 2, 17)], 'wh')
    put(g, [(ox + 1, 17)], 'pu'); put(g, [(22, 15)], 'ey')
    put(g, [(13, 22), (14, 21), (15, 22), (16, 21), (17, 22), (18, 21)], 'md')  # wobbly "ouch"
    put(g, [(14, 22), (16, 22)], 'tg')
    # band-aid on cheek
    put(g, [(19, 19), (20, 19), (21, 19), (22, 19), (19, 20), (22, 20)], 'ba')
    put(g, [(20, 20), (21, 20)], 'bd')
    put(g, [(10, 20), (11, 20)], 'fl'); put(g, [(10, 21)], 'cr')

def sad(g):
    eyes_open(g, dy=0)
    brows(g, [(10, 14), (11, 14), (12, 13)], [(19, 13), (20, 14), (21, 14)])
    put(g, [(22, 18), (22, 19), (21, 20), (22, 20), (22, 21)], 'tr')
    put(g, [(10, 18)], 'tr')
    put(g, [(13, 23), (18, 23)], 'lp'); put(g, [(x, 22) for x in range(14, 18)], 'lp')

def super_star(g):
    brows(g, [(10, 13), (11, 13), (12, 13)], [(19, 13), (20, 13), (21, 13)])
    for ox in (10, 19):
        put(g, [(ox + 1, 15), (ox, 16), (ox + 2, 16), (ox, 18), (ox + 2, 18)], 'st')
        put(g, [(ox + 1, 16), (ox + 1, 17), (ox, 17), (ox + 2, 17)], 'sw')
        put(g, [(ox - 1, 17), (ox + 3, 17)], 'st')
    put(g, [(x, 21) for x in range(12, 20)], 'md'); put(g, [(12, 22), (19, 22)], 'md')
    put(g, [(x, 22) for x in range(13, 19)], 'tt'); g[22][15] = 'md'
    put(g, [(13, 23), (18, 23)], 'md'); put(g, [(x, 23) for x in range(14, 18)], 'tg')
    put(g, [(x, 24) for x in range(14, 18)], 'md')
    for sx, sy in ((4, 6), (27, 9), (6, 22), (26, 21)):
        put(g, [(sx, sy - 1), (sx - 1, sy), (sx + 1, sy), (sx, sy + 1)], 'st'); put(g, [(sx, sy)], 'sw')

def outline(g):
    o = [row[:] for row in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] is None:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and g[ny][nx] not in (None, 'st', 'sw'):
                        o[y][x] = 'out'; break
    return o

def render(g):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if g[y][x]:
                im.putpixel((x, y), C[g[y][x]])
    return im

FACES = [('1_neutral', neutral), ('2_happy', happy), ('3_surprised', surprised), ('4_angry', angry),
         ('5_hurt', hurt), ('6_sad', sad), ('7_super', super_star)]

# --- tiny 3x5 pixel font for labels ---
FONT = {
    '0': ['111', '101', '101', '101', '111'], '1': ['010', '110', '010', '010', '111'], '2': ['111', '001', '111', '100', '111'],
    '3': ['111', '001', '111', '001', '111'], '4': ['101', '101', '111', '001', '001'], '5': ['111', '100', '111', '001', '111'],
    '6': ['111', '100', '111', '101', '111'], '7': ['111', '001', '010', '010', '010'], '8': ['111', '101', '111', '101', '111'],
    '9': ['111', '101', '111', '001', '111'], '%': ['101', '001', '010', '100', '101'], 'A': ['010', '101', '111', '101', '101'],
    'E': ['111', '100', '110', '100', '111'], 'H': ['101', '101', '111', '101', '101'], 'L': ['100', '100', '100', '100', '111'],
    'T': ['111', '010', '010', '010', '010'], 'M': ['101', '111', '111', '101', '101'], 'O': ['111', '101', '101', '101', '111'],
    'R': ['110', '101', '110', '101', '101'], 'I': ['111', '010', '010', '010', '111'], 'S': ['111', '100', '111', '001', '111'],
    'N': ['101', '111', '111', '111', '101'], 'U': ['101', '101', '101', '101', '111'], 'P': ['111', '101', '111', '100', '100'],
    'Y': ['101', '101', '010', '010', '010'], 'D': ['110', '101', '101', '101', '110'], 'G': ['111', '100', '101', '101', '111'],
    'V': ['101', '101', '101', '101', '010'], 'F': ['111', '100', '110', '100', '100'], ' ': ['000'] * 5,
}

def text(im, s, x, y, col, scale=1):
    for ch in s:
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == '1':
                    for i in range(scale):
                        for j in range(scale):
                            im.putpixel((x + c * scale + i, y + r * scale + j), col)
        x += 4 * scale

os.makedirs('out', exist_ok=True)
imgs = []
for name, fn in FACES:
    g = base(); fn(g); g = outline(g)
    im = render(g); imgs.append((name, im))
    im.save(f'out/talita_{name}_32.png')
    im.resize((256, 256), Image.NEAREST).save(f'out/talita_{name}_256.png')

sheet = Image.new('RGBA', (32 * 7, 32), (0, 0, 0, 0))
for i, (_, im) in enumerate(imgs):
    sheet.paste(im, (i * 32, 0))
sheet.save('talita_faces_spritesheet_32.png')

# labeled preview sheet
SC = 6
labels = ['NEUTRAL', 'HAPPY', 'SURPRISED', 'ANGRY', 'HURT', 'SAD', 'SUPER']
prev = Image.new('RGBA', (7 * 32 * SC + 8 * 12, 32 * SC + 60), (24, 24, 30, 255))
for i, (_, im) in enumerate(imgs):
    x = 12 + i * (32 * SC + 12)
    tile = Image.new('RGBA', (32, 32), (70, 70, 78, 255)); tile.alpha_composite(im)
    prev.paste(tile.resize((32 * SC, 32 * SC), Image.NEAREST), (x, 12))
    lab = labels[i]; tw = len(lab) * 4 * 3
    text(prev, lab, x + (32 * SC - tw) // 2, 32 * SC + 26, (255, 200, 90, 255), 3)
prev.save('talita_faces_preview.png')

# Doom-style status bar mockup (original layout, native 160x32 -> scaled)
bar = Image.new('RGBA', (160, 32), (70, 70, 74, 255))
for y in range(32):
    for x in range(160):
        if (x * 7 + y * 13) % 11 == 0:
            bar.putpixel((x, y), (58, 58, 62, 255))
def panel(x0, x1):
    for x in range(x0, x1):
        bar.putpixel((x, 1), (110, 110, 116, 255)); bar.putpixel((x, 30), (36, 36, 40, 255))
    for y in range(1, 31):
        bar.putpixel((x0, y), (110, 110, 116, 255)); bar.putpixel((x1 - 1, y), (36, 36, 40, 255))
panel(0, 40); panel(40, 80); panel(80, 116); panel(116, 160)
red = (220, 40, 30, 255); gray = (200, 200, 200, 255)
text(bar, '42', 8, 7, red, 2); text(bar, 'AMMO', 12, 22, gray)
text(bar, '87%', 48, 7, red, 2); text(bar, 'HEALTH', 48, 22, gray)
fb = Image.new('RGBA', (34, 30), (40, 30, 34, 255)); fb.alpha_composite(imgs[0][1], (1, -1))
bar.paste(fb, (81, 1))
text(bar, '50%', 124, 7, red, 2); text(bar, 'ARMOR', 128, 22, gray)
bar.save('talita_statusbar_mockup_160.png')
bar.resize((160 * 5, 32 * 5), Image.NEAREST).save('talita_statusbar_mockup.png')

with zipfile.ZipFile('talita_face_sprites.zip', 'w') as z:
    for f in sorted(os.listdir('out')):
        z.write(f'out/{f}', f)
    z.write('talita_faces_spritesheet_32.png'); z.write('talita_statusbar_mockup_160.png')
print('ok')
