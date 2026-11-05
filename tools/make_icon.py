# Icône de l'extension : un globe pixel art dont chaque quartier est un monde. Usage : python3 tools/make_icon.py
import math, random, zlib, struct, os
N, S = 32, 4                                   # grille de 32 x 32, chaque case = 4 pixels → 128 x 128
rnd = random.Random(7)
def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def mix(c, t, k): return tuple(int(c[i] + (t[i] - c[i]) * k) for i in range(3))
BG = hexrgb('#0a0c26'); OUT = hexrgb('#05061a')
img = [[BG for _ in range(N)] for _ in range(N)]
for _ in range(26):                             # étoiles du fond
    x, y = rnd.randrange(N), rnd.randrange(N)
    img[y][x] = rnd.choice([hexrgb('#fff4d8'), hexrgb('#4df0ff'), hexrgb('#ffb7d5'), hexrgb('#f2c45a')])
cx = cy = (N - 1) / 2; R = 13.2
SECT = [  # (nom, angle début, angle fin, couleur de base, détails)
 ('pole',   -126, -54, '#d8ecff', ['#fcfcfc', '#88b8f0']),
 ('sakura', -54,  18,  '#ff9ec8', ['#fff0f6', '#d6578a']),
 ('desert', 18,   90,  '#e0733a', ['#f2c45a', '#8a3a14', '#2f8a3c']),
 ('ocean',  90,   162, '#1d7fa8', ['#4df0ff', '#124e6e']),
 ('neon',   162,  234, '#3a2f6a', ['#ff2a9d', '#00e5ff', '#ffb020']),
]
def sector(a):
    a = (a + 126) % 360 - 126
    for s in SECT:
        lo, hi = s[1], s[2]
        if lo <= a < hi or lo <= a + 360 < hi: return s
    return SECT[0]
for y in range(N):
    for x in range(N):
        dx, dy = x - cx, y - cy; r = math.hypot(dx, dy)
        if r > R + 1.0: continue
        if r > R: img[y][x] = OUT; continue
        a = math.degrees(math.atan2(dy, dx)); name, lo, hi, base, det = sector(a)
        c = hexrgb(base)
        h = rnd.random()
        if name == 'pole':
            if h < 0.22: c = hexrgb(det[1])
        elif name == 'sakura':
            c = hexrgb(det[0]) if h < 0.18 else (hexrgb(det[1]) if h < 0.30 else c)
        elif name == 'desert':
            if h < 0.07: c = hexrgb(det[0])
            elif h < 0.17: c = hexrgb(det[1])
        elif name == 'ocean':
            c = hexrgb(det[0]) if (x + y // 2) % 5 == 0 and h < 0.7 else (hexrgb(det[1]) if h < 0.18 else c)
        elif name == 'neon':
            c = hexrgb(det[int(h * 3) % 3]) if (x % 3 == 0 and y % 3 == 0) else c
        lit = (dx * 0.55 + dy * 0.8) / R           # lumière en haut à gauche
        if lit > 0.55: c = mix(c, OUT, 0.55 if lit > 0.8 else 0.32)
        elif lit < -0.55: c = mix(c, (255, 255, 255), 0.22)
        img[y][x] = c
for dy in (-1, 0, 1):                              # reflet
    for dx in (-1, 0):
        yy, xx = int(cy - 7 + dy), int(cx - 7 + dx)
        img[yy][xx] = mix(img[yy][xx], (255, 255, 255), 0.55)
raw = b''.join(b'\x00' + b''.join(bytes(img[y // S][x // S]) for x in range(N * S)) for y in range(N * S))
def ck(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + ck(b'IHDR', struct.pack('>IIBBBBB', N * S, N * S, 8, 2, 0, 0, 0)) + ck(b'IDAT', zlib.compress(raw, 9)) + ck(b'IEND', b'')
open(os.path.expanduser('~/pixel-worlds/images/icon.png'), 'wb').write(png)
print('icône créée', N * S, 'x', N * S)
