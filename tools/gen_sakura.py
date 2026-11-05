# Monde « Sakura » : pétales de cerisier, torii, pagode, mont Fuji, koinobori. Usage : python3 tools/gen_sakura.py
import os, math, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

SAK_PAL = {'p':'#ffb7d5','P':'#ff8fbf','d':'#d6578a','w':'#fff0f6','Y':'#f8b800','y':'#ac7c00','R':'#d82800','r':'#881400','K':'#1c1c1c','k':'#3a3a4a',
           'G':'#58b878','g':'#2f7a4c','l':'#9be8b0','T':'#7c3c00','t':'#503000','F':'#5b6fb5','f':'#3f4f8f','W':'#fcfcfc','z':'#98a0b0','Z':'#5c6478','Q':'#ffe08a','B':'#2c8c8c','b':'#1c5c5c','C':'#8fd0ff','S':'#e8e0f0'}
PETALS = ['#ffb7d5', '#ff8fbf', '#ffd6e8', '#fff0f6', '#ffb7d5']
SAK_STARS = ['#fff0f6', '#fff0f6', '#ffb7d5', '#f8b800']

def grid(w, h): return [['.'] * w for _ in range(h)]
def done(g): return [''.join(r) for r in g]
def make_fuji(w, h):
    g = grid(w, h); cx = (w - 1) / 2
    for y in range(h):
        half = 2 + (w / 2 - 2) * (y / (h - 1)) ** 0.85
        for x in range(w):
            if abs(x - cx) <= half:
                snow = h * 0.30 + 2.6 * math.sin(x * 0.9) + 1.8 * math.sin(x * 0.37 + 1) + abs(x - cx) * 0.18
                g[y][x] = 'W' if y < snow else ('f' if x > cx + half * 0.12 else 'F')
    return done(g)
def make_cherry(w, h, seed=5):
    rnd = random.Random(seed); g = grid(w, h); cx = w // 2; ch = int(h * 0.64)
    for y in range(int(ch * 0.55), h):                        # tronc
        wide = 3 if y < h - 5 else 5
        for x in range(cx - wide // 2, cx + wide // 2 + 1): g[y][x] = 't' if x > cx else 'T'
    for k in range(1, 9):                                     # branches
        for dx, base in ((-1, int(ch * 0.9)), (1, int(ch * 0.8))):
            yy, xx = base - k, cx + dx * k
            if 0 <= yy < h and 0 <= xx < w: g[yy][xx] = 'T'
    blobs = [(cx, ch * .45, w * .30), (cx - w * .22, ch * .6, w * .22), (cx + w * .23, ch * .58, w * .22), (cx - w * .1, ch * .25, w * .2),
             (cx + w * .12, ch * .22, w * .2), (cx - w * .36, ch * .82, w * .14), (cx + w * .37, ch * .8, w * .14)]
    for y in range(ch + 4):
        for x in range(w):
            if any(((x - bx) / br) ** 2 + ((y - by) / (br * .85)) ** 2 <= 1 for bx, by, br in blobs):
                lit = (cx - x) * 0.5 + (ch / 2 - y) * 0.5
                c = 'p' if lit > w * .12 else ('d' if lit < -w * .12 else 'P')
                if rnd.random() < .08: c = 'w'
                if rnd.random() < .025: continue
                g[y][x] = c
    return done(g)
def make_torii(w=24, h=20):
    g = grid(w, h)
    for x in range(w): g[0][x] = 'K'
    for x in range(1, w - 1): g[1][x] = 'R'
    for x in range(3, w - 3): g[5][x] = 'R'; g[6][x] = 'r'
    for y in range(2, h):
        for px_ in (4, 5, w - 6, w - 5): g[y][px_] = 'R'
    for y in range(h - 2, h):
        for px_ in (3, 4, 5, 6, w - 7, w - 6, w - 5, w - 4): g[y][px_] = 'K'
    return done(g)
def make_pagoda(tiers=4, tier_h=7):
    W = 8 + (tiers - 1) * 3 + 4; H = 6 + tiers * tier_h; g = grid(W, H); cx = W // 2
    for y in range(0, 6): g[y][cx] = 'Y'
    g[2][cx - 1] = g[2][cx + 1] = 'Y'
    for i in range(tiers):
        top = 6 + i * tier_h; wi = 8 + i * 3
        for x in range(cx - wi // 2 - 2, cx + wi // 2 + 3): g[top][x] = 'B'; g[top + 1][x] = 'b'
        g[top - 1][cx - wi // 2 - 2] = g[top - 1][cx + wi // 2 + 2] = 'B'   # bords relevés
        for y in range(top + 2, top + tier_h):
            for x in range(cx - wi // 2 + 1, cx + wi // 2):
                g[y][x] = 'W'
            g[y][cx - wi // 2 + 1] = g[y][cx + wi // 2 - 1] = 'R'
        for y in range(top + 3, top + tier_h - 1): g[y][cx] = 'K'
    return done(g)
def make_koi(w=22, h=9, body='R', dark='r'):
    g = grid(w, h); mid = h // 2
    for x in range(w):
        t = x / (w - 1); half = min(1 + round(3 * min(1, t * 1.5)), mid, h - 1 - mid)
        for y in range(mid - half, mid + half + 1):
            if x < 3 and abs(y - mid) < 1: continue                    # queue fourchue
            c = body if (x // 3) % 2 == 0 else dark
            if x >= w - 5: c = 'W'
            g[y][x] = c
    g[mid - 1][w - 4] = 'K'; g[mid][w - 1] = 'K'
    return done(g)
def make_bamboo(h, seed=1):
    """Une tige de bambou : segments séparés par des nœuds, avec quelques feuilles."""
    rnd = random.Random(seed); w = 9; g = grid(w, h)
    for y in range(h):
        for x in (3, 4): g[y][x] = 'G' if x == 3 else 'g'
        if y % 7 == 6:
            for x in (2, 3, 4, 5): g[y][x] = 'g'
            if y > 4 and rnd.random() < 0.8:
                d = rnd.choice((-1, 1))
                for k in range(1, 4):
                    xx = 4 + d * (k + 1); yy = y - k
                    if 0 <= xx < w and yy >= 0: g[yy][xx] = 'l' if k < 3 else 'G'
    return done(g)
SAK_SPR = {
 'fuji_l': make_fuji(60, 26), 'fuji_xl': make_fuji(64, 28), 'cherry_l': make_cherry(30, 34), 'bamboo_a': make_bamboo(36, 1), 'bamboo_b': make_bamboo(30, 2), 'bamboo_c': make_bamboo(33, 3), 'cherry_xl': make_cherry(46, 58),
 'torii': make_torii(), 'pagoda': make_pagoda(),
 'toro': ["...Z...", ".zzzzz.", "zzzzzzz", ".zQQQz.", ".zQQQz.", ".zzzzz.", "..zzz..", "...z...", "..zzz..", ".zzzzz."],
 'chochin': ["..YYYY..", ".RRRRRR.", "RRRRRRRR", "RRrRRrRR", "RRRRRRRR", "RRrRRrRR", "RRRRRRRR", ".RRRRRR.", "..YYYY..", "...YY..."],
 'flower': ["..P..", ".PPP.", "PPYPP", ".PPP.", "..P.."],
 'koi_r': make_koi(22, 9, 'R', 'r'), 'koi_b': make_koi(20, 8, 'C', 'F'),
}
def sak(P): return Svg('sakura', P, SAK_PAL, SAK_SPR, SAK_STARS)

# ---------- PLEIN ÉCRAN : branche en fleurs en haut à gauche, tapis de pétales, koinobori, pétales qui tombent ----------
random.seed(21); s = sak(3)
pts = [(0, 3), (10, 6), (22, 8), (34, 12), (46, 14), (58, 20), (70, 22), (82, 28)]
br = []
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    for k in range(x1 - x0):
        y = y0 + (y1 - y0) * k / max(1, x1 - x0); br.append(s.rect(x0 + k, round(y), 1, 2, 'T' if k % 3 else 't'))
for x, y in ((24, 8), (40, 13), (60, 21)):                     # petites brindilles
    for k in range(7): br.append(s.rect(x + k // 2, y + 1 + k, 1, 1, 'T'))
for _ in range(34):
    i = random.randrange(len(pts) - 1); x = pts[i][0] + random.uniform(-4, 14); y = pts[i][1] + random.uniform(-6, 12)
    br.append(s.sprite('flower', round(x), round(y)) if random.random() < 0.5 else s.rect(round(x), round(y), 2, 2, random.choice(['p', 'P', 'w']) and random.choice(PETALS)))
s.add('<svg x="0" y="0" overflow="visible">' + ''.join(br) + '</svg>')
s.bank(1500, 4, 1, 31, '#ffd6e8'); s.bank(1500, 2, 1, 32, '#ffb7d5')
koi = s.sprite('koi_r', 0, 0) + s.sprite('koi_b', 8, 12)
xs = ';'.join(f'{x:.1f}%' for x in [-8 + k * 1.2 for k in range(0, 100)]) + ';' + ';'.join(['112%'] * 60)
s.add(f'<svg y="16%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="48s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0;0,3" calcMode="discrete" dur="1.6s" repeatCount="indefinite"/>{koi}</g></svg>')
s.flakes(48, 3, dur=(13, 26), colors=PETALS, sway=11, wide=1); s.save('fullscreen')

# ---------- ÉDITEUR : étoiles, bambous, lanterne de pierre et cerisier en bas à droite ----------
random.seed(22); s = sak(3)
s.stars(110, 4)
s.pin_sprites([('bamboo_a', 0, 0, None, 1), ('bamboo_b', 7, 6, None, 1), ('bamboo_c', 14, 3, None, 1), ('toro', 26, 26, None, 1), ('cherry_l', 36, 2, None, 1)], 'br', 14, 22); s.save('editor')

# ---------- TERMINAL : tapis de pétales, torii, mont Fuji, pagode, lanternes ----------
random.seed(23); s = sak(4)
s.stars(26, 4, 2, 62); s.bank(1100, 3, 1, 33, '#ffd6e8'); s.bank(1100, 2, 1, 34, '#ffb7d5')
s.pin_sprites([('torii', 0, 0, None, 1), ('toro', 28, 10, None, 1)], 'bl', 90, 8)
s.pin_sprites([('fuji_xl', 0, 6, None, 1), ('pagoda', 40, 0, None, 1), ('toro', 70, 24, None, 1)], 'br', 30, 8)
s.flakes(20, 4, dur=(8, 16), colors=PETALS, sway=9, wide=1); s.save('panel')

# ---------- EXPLORATEUR : grand cerisier en fleurs, lanterne, pétales qui tombent ----------
random.seed(24); s = sak(4)
s.stars(12, 4, 0, 96); s.flakes(55, 3, dur=(10, 20), colors=PETALS, sway=10, wide=1)
s.pin_sprites([('cherry_xl', 0, 0, None, 1), ('toro', 48, 48, None, 1)], 'bl', 8, 24); s.save('sidebar')

# ---------- BARRE DE DROITE : lanternes chōchin et branches en fleurs qui se balancent ----------
random.seed(25); s = sak(4)
for i, (xp, L, kind) in enumerate([(18, 6, 'chochin'), (50, 16, 'branch'), (78, 9, 'chochin')]):
    if kind == 'chochin': gg = s.rect(3, 0, 1, L, '#7c7c7c') + s.sprite('chochin', 0, L)
    else:
        gg = s.rect(2, 0, 1, L + 12, '#7c3c00') + ''.join(s.sprite('flower', dx, L - 8 + dy) for dx, dy in ((-4, 0), (3, 4), (-5, 9), (4, 13), (-3, 18)))
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{2.8+i*0.5:.1f}s" repeatCount="indefinite"/>{gg}</g></svg>')
s.save('aux')
print('Sakura : décors générés')
