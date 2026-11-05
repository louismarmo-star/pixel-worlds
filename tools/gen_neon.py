# Monde « Néon City » : ville de néons sous la pluie, voitures volantes, enseignes qui grésillent.
# Usage : python3 tools/gen_neon.py
import os, math, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

NEON_PAL = {'K':'#0b0818','k':'#1a1430','j':'#2a2050','J':'#3a2f6a','m':'#ff2a9d','M':'#ff77c5','c':'#00e5ff','C':'#7ff3ff','a':'#ffb020','A':'#ffd66b',
            'v':'#a56bff','W':'#fcfcfc','g':'#6c7488','G':'#98a0b0','r':'#ff4d5a','w':'#fff7b0','n':'#39ff88','N':'#ff4d5a','q':'#150f30','Q':'#1f1844'}
NEON_STARS = ['#fcfcfc', '#fcfcfc', '#b58cff', '#4df0ff']
RAIN = ['#7ff3ff', '#a56bff', '#7ff3ff']

FONT = {'A': [".#.", "#.#", "###", "#.#", "#.#"], 'B': ["##.", "#.#", "##.", "#.#", "##."], 'C': [".##", "#..", "#..", "#..", ".##"],
        'D': ["##.", "#.#", "#.#", "#.#", "##."], 'E': ["###", "#..", "##.", "#..", "###"], 'H': ["#.#", "#.#", "###", "#.#", "#.#"],
        'K': ["#.#", "#.#", "##.", "#.#", "#.#"], 'O': ["###", "#.#", "#.#", "#.#", "###"], 'P': ["##.", "#.#", "##.", "#..", "#.."],
        'R': ["##.", "#.#", "##.", "#.#", "#.#"], 'T': ["###", ".#.", ".#.", ".#.", ".#."], 'Y': ["#.#", "#.#", ".#.", ".#.", ".#."],
        '2': ["##.", "..#", ".#.", "#..", "###"], '4': ["#.#", "#.#", "###", "..#", "..#"]}
def grid(w, h): return [['.'] * w for _ in range(h)]
def done(g): return [''.join(r) for r in g]
def make_sign(word, frame='m', ink='C'):
    w = 4 * len(word) + 2; g = grid(w, 9)
    for x in range(w): g[0][x] = frame; g[8][x] = frame
    for y in range(9): g[y][0] = frame; g[y][w - 1] = frame
    for i, ch in enumerate(word):
        for y, row in enumerate(FONT[ch]):
            for x, c in enumerate(row):
                if c == '#': g[2 + y][2 + i * 4 + x] = ink
    return done(g)
def make_building(w, h, seed, antenna=False, lit=0.42):
    rnd = random.Random(seed); extra = 9 if antenna else 0; g = grid(w, h + extra); cx = w // 2
    for y in range(extra, h + extra):
        for x in range(w): g[y][x] = 'k'
        g[y][0] = 'j'
    for x in range(w): g[extra][x] = 'J'
    for y in range(extra + 2, h + extra - 2, 3):
        for x in range(2, w - 2, 3):
            if rnd.random() < lit:
                c = rnd.choices(['w', 'a', 'c', 'm', 'L'], weights=[4, 3, 3, 1.5, 0.8])[0]
                g[y][x] = c
                if c != 'L': g[y][x + 1] = c; g[y + 1][x] = c; g[y + 1][x + 1] = c
    if antenna:
        for y in range(1, extra): g[y][cx] = 'g'
        g[0][cx] = 'N'
    return done(g)
def make_holo(d=13):
    g = grid(d, d); c = (d - 1) / 2
    for y in range(d):
        for x in range(d):
            r = math.hypot(x - c, y - c)
            if abs(r - c) < 0.6: g[y][x] = 'c'
            elif r < c and (abs(x - c) < 0.5 or abs(y - c) < 0.5): g[y][x] = 'C'
            elif r < c and abs(((x - c) / c) ** 2 + ((y - c) / (c * 0.45)) ** 2 - 1) < 0.22: g[y][x] = 'C'
    return done(g)
def make_ziggurat(tiers=5, tier_h=6, base=20):
    """Tour à étages en gradins : une bande de lumière cyan par étage, arêtes magenta."""
    W = base; H = tiers * tier_h + 5; g = grid(W, H); cx = W // 2; step = (base - 8) // (tiers - 1)
    for i in range(tiers):
        top = 5 + i * tier_h; wi = 8 + i * step
        for y in range(top, top + tier_h):
            for x in range(cx - wi // 2, cx + wi // 2 + (wi % 2)): g[y][x] = 'k'
        for x in range(cx - wi // 2, cx + wi // 2 + (wi % 2)): g[top][x] = 'm'; g[top + 2][x] = 'c' if x % 5 else 'k'
        for x in range(cx - wi // 2 + 1, cx + wi // 2 + (wi % 2) - 1, 2): g[top + 4][x] = 'w'
    for y in range(1, 5): g[y][cx] = 'g'
    g[0][cx] = 'N'
    return done(g)
def make_spire(h=48):
    """Aiguille avec une sphère et des anneaux lumineux."""
    w = 9; g = grid(w, h); cx = 4
    for y in range(1, h): g[y][cx] = 'g'
    for y in range(6, 13):
        for x in range(w):
            if math.hypot(x - cx, y - 9) <= 3.2: g[y][x] = 'v'
    g[8][cx - 1] = g[8][cx] = 'C'
    for yy in (22, 32):
        for x in range(1, 8): g[yy][x] = 'c'
        for x in range(2, 7): g[yy + 1][x] = 'k'
    for y in range(h - 9, h):
        half = min(4, 1 + (y - (h - 9)) // 2)
        for x in range(cx - half, cx + half + 1): g[y][x] = 'j' if x < cx else 'k'
    g[0][cx] = 'N'
    return done(g)
def make_dome(w=16, h=18):
    """Bâtiment à dôme : coupole bleutée, liseré magenta, fenêtres allumées."""
    g = grid(w, h); cx = (w - 1) / 2
    for y in range(8):
        half = round((w / 2) * math.sqrt(max(0, 1 - ((8 - y - 0.5) / 8) ** 2)))
        for x in range(w):
            if abs(x - cx) <= half - 0.5: g[y][x] = 'J' if x < cx else 'j'
    for x in range(w): g[8][x] = 'm'
    for y in range(9, h):
        for x in range(w): g[y][x] = 'k'
    for x in range(1, w - 1, 2): g[11][x] = 'w'; g[14][x + 1 if x + 1 < w else x] = 'c'
    return done(g)
def make_sil(w, h, seed):
    """Silhouette lointaine, sans fenêtres, avec un toit en créneaux."""
    rnd = random.Random(seed); g = grid(w, h)
    for x in range(w):
        top = rnd.choice((0, 0, 1, 2))
        for y in range(top, h): g[y][x] = 'q' if x % 4 else 'Q'
    return done(g)
NEON_SPR = {
 'hovercar': [".......KKKKK........", "......KCCCCCK.......", "..KmmmmmmmmmmmmmmK..", ".KmmmMMMMMMMMmmmmmmA", "..KKKKKKKKKKKKKKKK..", "...cc........cc.....", "...CC........CC....."],
 'robot': ["...N....", "..gggg..", ".gCccCg.", ".gggggg.", "..gggg..", ".gggggg.", "g.gmmg.g", ".gggggg.", "..g..g..", ".gg..gg."],
 'ramen': ["mmmmmmmmmmmmmmmmmm", "WmWmWmWmWmWmWmWmWm", "mWmWmWmWmWmWmWmWmW", ".K..............K.", ".K.aaaaaaaaaaaa.K.", ".K.aaaaaaaaaaaa.K.", ".K.aaAAaaaaAAaa.K.", ".KjjjjjjjjjjjjjjK.", ".KjjjjjjjjjjjjjjK.", ".K..gg..gg..gg..K.", ".K..gg..gg..gg..K."],
 'holo': make_holo(13),
 'sign_bar': make_sign('BAR', 'm', 'C'), 'sign_byte': make_sign('BYTE', 'c', 'M'), 'sign_hack': make_sign('HACK', 'v', 'C'), 'sign_24h': make_sign('24H', 'a', 'A'),
 'sign_data': make_sign('DATA', 'c', 'A'), 'sign_open': make_sign('CODE', 'm', 'A'),
 'bld_a': make_building(12, 26, 1, True), 'bld_b': make_building(10, 36, 2), 'bld_c': make_building(14, 44, 3, True), 'bld_d': make_building(11, 30, 4), 'bld_e': make_building(9, 22, 5),
 'tower': make_building(24, 70, 7, True, 0.5), 'zig': make_ziggurat(), 'spire': make_spire(), 'dome': make_dome(), 'sil_a': make_sil(9, 18, 1), 'sil_b': make_sil(11, 13, 2), 'sil_c': make_sil(8, 22, 3), 'bld_f': make_building(12, 40, 8), 'bld_g': make_building(10, 28, 9, True),
}
def neon(P): return Svg('neon', P, NEON_PAL, NEON_SPR, NEON_STARS)
def flicker(s, inner, lo=(0.25, 0.6), dur=(0.5, 1.6)): return s.twinkle(inner, lo=lo, dur=dur)
def rect_op(s, x, y, w, h, c, op):
    P = s.P; return f'<rect x="{x*P:g}" y="{y*P:g}" width="{w*P:g}" height="{h*P:g}" fill="{c}" fill-opacity="{op}"/>'
def rain(s, n, dur=(1.4, 2.6), length=8, drift=-24, width=2):
    for _ in range(n):
        x = random.uniform(0, 105); d = random.uniform(*dur); b = -random.uniform(0, d); col = random.choice(RAIN)
        s.o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0,0;{drift},0" dur="{d:.2f}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                   f'<rect x="{x:.1f}%" y="-6%" width="{width}" height="{length}" fill="{col}" fill-opacity="0.38"><animate attributeName="y" values="-6%;106%" dur="{d:.2f}s" begin="{b:.2f}s" repeatCount="indefinite"/></rect></g>')
def skyline(s, items, corner, mx, my):
    inner = ''; W = 0; H = 0
    for name, x, y in items:
        inner += s.sprite(name, x, y); w, h = s.size(name); W = max(W, x * s.P + w); H = max(H, y * s.P + h)
    s.pin(inner, W, H, corner, mx, my); return W, H

# ---------- PLEIN ÉCRAN : rail de néon en haut, enseignes, rue mouillée, voitures volantes, pluie ----------
random.seed(41); s = neon(3)
rail = []
cols = ['m', 'c', 'v']
for k in range(110):                                            # un segment de 14 pixels = un tube de néon
    col = NEON_PAL[cols[k % 3]]
    seg = rect_op(s, k * 14, 0, 14, 1, col, 0.95) + rect_op(s, k * 14, 1, 14, 1, col, 0.28)
    rail.append(flicker(s, seg, (0.2, 0.6), (0.6, 1.8)) if k % 11 == 4 else seg)
s.add('<svg x="0" y="0" overflow="visible">' + ''.join(rail) + '</svg>')
s.pin(flicker(s, s.sprite('sign_bar', 0, 0)), *s.size('sign_bar'), 'tr', 30, 8)
s.pin(flicker(s, s.sprite('sign_24h', 0, 0)), *s.size('sign_24h'), 'tr', 130, 8)
s.bank(1500, 3, 1, 42, '#1a1430')
refl = ''.join(flicker(s, rect_op(s, random.randint(0, 1400), -random.randint(0, 2), random.randint(6, 18), 1, random.choice([NEON_PAL['m'], NEON_PAL['c'], NEON_PAL['a']]), 0.55), (0.1, 0.5), (1, 3)) for _ in range(40))
s.add(f'<svg x="0" y="100%" overflow="visible">{refl}</svg>')
def car(s, y, dur, begin, lo=-14, hi=112, step=1.5, idle=30):
    xs = ';'.join(f'{lo + k*step:.1f}%' for k in range(int((hi - lo) / step) + 1)) + ';' + ';'.join([f'{hi}%'] * idle)
    trail = ''.join(rect_op(s, -3 - 5 * k, 3 + (k % 2), 5, 1, '#ff2a9d' if k % 2 else '#00e5ff', round(0.55 - 0.12 * k, 2)) for k in range(4))
    s.add(f'<svg y="{y}%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
          f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-2;0,0;0,2" calcMode="discrete" dur="0.9s" repeatCount="indefinite"/>{trail}{s.sprite("hovercar", 0, 0)}</g></svg>')
car(s, 13, 26, 0); car(s, 32, 38, -17)
rain(s, 34); s.save('fullscreen')

# ---------- ÉDITEUR : étoiles et skyline différente de celle du terminal (aiguille, gradins, dôme) ----------
random.seed(42); s = neon(3)
s.stars(70, 3)
skyline(s, [('sil_c', 6, 26), ('sil_a', 22, 30), ('sil_b', 44, 35), ('spire', 0, 0), ('dome', 9, 30), ('zig', 28, 14)], 'br', 14, 22)
s.save('editor')

# ---------- TERMINAL : rue mouillée, stand de nouilles, robot, enseignes ----------
random.seed(43); s = neon(4)
s.stars(18, 4, 2, 45); s.bank(1100, 3, 1, 44, '#1a1430'); s.bank(1100, 2, 1, 45, '#2a2050')
refl = ''.join(flicker(s, rect_op(s, random.randint(0, 1000), -random.randint(0, 2), random.randint(6, 16), 1, random.choice([NEON_PAL['m'], NEON_PAL['c'], NEON_PAL['a']]), 0.55), (0.1, 0.5), (1, 3)) for _ in range(30))
s.add(f'<svg x="0" y="100%" overflow="visible">{refl}</svg>')
inner = s.sprite('ramen', 0, 4) + flicker(s, s.sprite('sign_byte', 1, -6)) + s.sprite('robot', 22, 5)
s.pin(inner, 30 * s.P, 15 * s.P, 'bl', 90, 8)
W2, H2 = skyline(s, [('bld_g', 0, 12), ('bld_f', 12, 0), ('bld_e', 23, 18)], 'br', 30, 8)
s.pin(flicker(s, s.sprite('sign_hack', 0, 0)), *s.size('sign_hack'), 'br', 30 + 12 * s.P, 8 + 14 * s.P)
rain(s, 10); s.save('panel')

# ---------- EXPLORATEUR : grande tour, enseigne, hologramme, pluie ----------
random.seed(44); s = neon(4)
s.stars(10, 4, 0, 90)
s.pin(s.sprite('tower', 0, 0) + flicker(s, s.sprite('sign_data', 2, 30)) + flicker(s, s.sprite('holo', 27, 26), (0.3, 0.8), (0.9, 2.2)),
      40 * s.P, 79 * s.P, 'bl', 14, 0)
rain(s, 18); s.save('sidebar')

# ---------- BARRE DE DROITE : tubes de néon qui grésillent ----------
random.seed(45); s = neon(4)
for xp, L, col in ((20, 18, NEON_PAL['m']), (50, 28, NEON_PAL['v']), (80, 12, NEON_PAL['c'])):
    tube = rect_op(s, -1, 0, 3, L + 1, col, 0.25) + s.rect(0, 0, 1, L, col) + s.rect(0, 0, 1, L, '#fcfcfc', '') * 0
    s.add(f'<svg x="{xp}%" y="0" overflow="visible">' + flicker(s, tube, (0.15, 0.55), (0.5, 1.5)) + '</svg>')
s.add('<svg x="66%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;3,0;0,0;-3,0" calcMode="discrete" dur="3.2s" repeatCount="indefinite"/>'
      + s.rect(3, 0, 1, 14, '#6c7488') + flicker(s, s.sprite('sign_open', 0, 14)) + '</g></svg>')
s.save('aux')
print('Néon City : décors générés')
