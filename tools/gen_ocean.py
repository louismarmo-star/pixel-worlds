# Monde « Océan » : sous-marin, méduses lumineuses, poisson-lanterne, épave, algues.
# Usage : python3 tools/gen_ocean.py
import os, math, random, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

OC_PAL = {'K':'#031018','k':'#06202e','d':'#0a3a52','b':'#124e6e','B':'#1d7fa8','C':'#4df0ff','c':'#1fb5c8','W':'#fcfcfc','w':'#d8f4ff',
          'Y':'#ffd84d','y':'#c8a020','O':'#ff8a1e','o':'#c25a10','P':'#ff77c5','p':'#c8409a','V':'#a56bff','v':'#6b3fd0','G':'#3ecf9a','g':'#1f8a68',
          'S':'#8a9bb0','s':'#5c6a80','T':'#8a5a2a','t':'#5a3a18','R':'#ff4d5a','F':'#d8ff6b','Z':'#2a4560','e':'#e8c9a0','M':'#ff9a6a','m':'#c25a40'}
OC_STARS = ['#d8f4ff', '#d8f4ff', '#4df0ff', '#7dffc4']
def grid(w, h): return [['.'] * w for _ in range(h)]
def done(g): return [''.join(r) for r in g]
def inpoly(x, y, pts):
    ins = False; j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]; xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi: ins = not ins
        j = i
    return ins
def fill(g, pts, ch):
    for y in range(len(g)):
        for x in range(len(g[0])):
            if inpoly(x + 0.5, y + 0.5, pts): g[y][x] = ch
def line(g, x0, y0, x1, y1, ch, th=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n; y = y0 + (y1 - y0) * k / n
        for dy in range(th):
            for dx in range(th):
                xx, yy = int(x) + dx, int(y) + dy
                if 0 <= yy < len(g) and 0 <= xx < len(g[0]): g[yy][xx] = ch
def make_sub():
    W, H = 26, 13; g = grid(W, H)
    for y in range(H):
        for x in range(W):
            if ((x - 12.5) / 11.5) ** 2 + ((y - 8) / 4.6) ** 2 <= 1: g[y][x] = 'Y' if y < 9 else 'y'
    for y in range(2, 5):
        for x in range(9, 15): g[y][x] = 'Y' if x < 14 else 'y'
    for y in range(0, 3): g[y][12] = 'S'
    g[0][13] = g[0][14] = 'S'
    for px_ in (6, 12, 18):
        g[8][px_] = g[8][px_ + 1] = g[9][px_] = g[9][px_ + 1] = 'C'; g[8][px_] = 'W'
    for y in range(5, 11): g[y][0] = 'S'
    g[7][1] = g[9][1] = 'S'; g[12][3] = g[12][4] = 's'
    g[8][24] = g[8][25] = 'F'; g[9][24] = 'F'
    return done(g)
def make_angler():
    W, H = 18, 13; g = grid(W, H)
    for y in range(H):
        for x in range(W):
            if ((x - 8) / 6.8) ** 2 + ((y - 8) / 4.3) ** 2 <= 1: g[y][x] = 'd' if y < 8 else 'b'
    fill(g, [(0, 4), (4, 8), (0, 13)], 'b')                                                     # queue
    for k in range(5): g[4 - k // 2][9 + k] = 'k'                                                # canne
    g[0][13] = g[0][14] = g[1][13] = g[1][14] = 'F'
    for x in range(11, 16): g[9][x] = 'K'; g[10][x] = 'K'
    for x in range(11, 16, 2): g[9][x] = 'W'; g[10][x + 1 if x + 1 < 16 else x] = 'W'
    g[6][11] = g[6][12] = g[7][11] = g[7][12] = 'Y'; g[7][12] = 'K'
    return done(g)
def make_jelly(a, b):
    W, H = 9, 15; g = grid(W, H)
    for y in range(5):
        half = round(4.5 * math.sqrt(max(0, 1 - ((4 - y) / 5) ** 2)))
        for x in range(W):
            if abs(x - 4) <= half: g[y][x] = a if x < 5 else b
    g[1][2] = g[1][3] = 'w'
    for x in range(W): g[5][x] = b if x % 2 == 0 else a
    for tx in (1, 3, 5, 7):
        for y in range(6, 14): g[y][tx + (1 if (y // 2 + tx) % 2 else 0) % 2 if tx + (1 if (y // 2 + tx) % 2 else 0) < W else tx] = b
    return done(g)
def make_kelp(h, frame):
    g = grid(7, h)
    for y in range(h):
        x = 3 + round(math.sin(y * 0.45 + frame * math.pi) * 1.6)
        g[y][x] = 'G'; g[y][x + 1 if x + 1 < 7 else x] = 'g'
        if y % 6 == 3:
            for k in (1, 2):
                xx = x + (k if (y // 6) % 2 else -k)
                if 0 <= xx < 7: g[y - k][xx] = 'G'
    return done(g)
def make_coral(h, seed, a='M', b='m'):
    rnd = random.Random(seed); W = h; g = grid(W, h)
    def branch(x, y, dx, dy, n, th):
        for _ in range(n):
            x += dx + rnd.uniform(-0.4, 0.4); y += dy
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < W and 0 <= yi < h:
                g[yi][xi] = a
                if th and xi + 1 < W: g[yi][xi + 1] = b
            if rnd.random() < 0.18 and n > 3: branch(x, y, dx + rnd.choice((-0.7, 0.7)), dy, n // 2, 0)
    for k in range(3): branch(W // 2 + (k - 1) * 2, h - 1, (k - 1) * 0.35, -1, h - 2, 1)
    for y in range(h):
        for x in range(W):
            if g[y][x] == a and (y < 2 or g[y - 1][x] == '.') and rnd.random() < 0.5: g[y][x] = 'W'
    return done(g)
def make_wreck():
    W, H = 34, 22; g = grid(W, H)
    fill(g, [(1, 8), (32, 7), (28, 19), (5, 20)], 'T')
    fill(g, [(32, 7), (33.5, 2.5), (30, 7)], 'T')
    for y in (11, 14, 17):
        for x in range(W):
            if g[y][x] == 'T': g[y][x] = 't'
    line(g, 14, 8, 11, 0, 'T', 1); line(g, 9, 3, 15, 2, 't', 1)
    fill(g, [(11, 3), (5, 5), (10, 8)], 'w')
    for (x, y) in ((8, 6), (9, 5)): g[y][x] = '.'
    for px_ in (10, 17, 24): g[13][px_] = g[13][px_ + 1] = g[14][px_] = g[14][px_ + 1] = 'C'
    fill(g, [(21, 15), (26, 14), (25, 19), (20, 19)], 'K')
    return done(g)
FISH = ["..XXX..", "X.XXXX.", "XXXXKXX", "X.XXXX.", "..XXX.."]
OC_SPR = {
 'sub': make_sub(), 'angler': make_angler(), 'jelly_p': make_jelly('P', 'p'), 'jelly_v': make_jelly('V', 'v'), 'jelly_c': make_jelly('C', 'c'),
 'kelp_a': make_kelp(34, 0), 'kelp_b': make_kelp(34, 1), 'kelp_s_a': make_kelp(22, 0), 'kelp_s_b': make_kelp(22, 1),
 'coral_a': make_coral(14, 1), 'coral_b': make_coral(11, 2, 'O', 'o'), 'coral_c': make_coral(12, 3, 'V', 'v'), 'wreck': make_wreck(),
 'fish': FISH,
 'crab': ["R.......R.", "RR.RRRR.RR", ".RRRRRRRR.", "..RKRRKR..", "..RRRRRR..", ".R.R..R.R."],
 'starfish': ["..M..", "MMMMM", ".MMM.", ".M.M.", "M...M"],
}
def oc(P): return Svg('ocean', P, OC_PAL, OC_SPR, OC_STARS)
def both(s, a, b, x, y, dur=1.6):
    """Deux images qui alternent (algues qui ondulent)."""
    return (f'<g><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>{s.sprite(a, x, y)}</g>'
            f'<g><animate attributeName="opacity" values="0;1" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>{s.sprite(b, x, y)}</g>')
def bubbles(s, n, dur=(7, 15), px=(3, 5)):
    for _ in range(n):
        x = random.uniform(0, 100); d = random.uniform(*dur); b = -random.uniform(0, d); amp = random.uniform(2, 8) * s.P; ph = random.uniform(0, 6.28); sz = random.choice(range(px[0], px[1] + 1))
        vals = ';'.join(f'{amp*math.sin(ph + k*0.9):.1f},0' for k in range(14))
        s.o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                   f'<rect x="{x:.1f}%" y="104%" width="{sz}" height="{sz}" fill="none" stroke="#d8f4ff" stroke-opacity="0.75" stroke-width="1"><animate attributeName="y" values="104%;-4%" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></rect></g>')
def bob(s, inner, xp, yp, amp=6, dur=5.0):
    return (f'<svg x="{xp}%" y="{yp}%" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;0,{-amp};0,0;0,{amp};0,0" dur="{dur}s" repeatCount="indefinite"/>{inner}</g></svg>')
def glow(s, inner, lo=(0.55, 0.85), dur=(1.6, 3.2)): return s.twinkle(inner, lo=lo, dur=dur)
def cross(s, name, y_pct, dur, begin, flip=False, lo=-12, hi=112, step=1.5, idle=30, extra=''):
    seq = list(range(int((hi - lo) / step) + 1))
    vals = [lo + k * step for k in seq]
    if flip: vals = vals[::-1]
    xs = ';'.join(f'{v:.1f}%' for v in vals) + ';' + ';'.join([f'{vals[-1]}%'] * idle)
    body = extra
    s.add(f'<svg y="{y_pct}%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
          f'<g{" transform=\'scale(-1,1)\'" if flip else ""}><animateTransform attributeName="transform" additive="sum" type="translate" values="0,0;0,-2;0,0;0,2" calcMode="discrete" dur="1.8s" repeatCount="indefinite"/>{body}</g></svg>')
FC = [('#ff8a1e', '#c25a10'), ('#4df0ff', '#1fb5c8'), ('#ff77c5', '#c8409a')]
def school(s, n, seed, col):
    r = random.Random(seed); out = ''
    for _ in range(n): out += s.sprite('fish', r.randint(0, 22), r.randint(0, 9), col)
    return out

# ---------- PLEIN ÉCRAN : surface, rayons de lumière, fond sableux, sous-marin, bancs de poissons, bulles ----------
random.seed(71); s = oc(3)
ys = [round(math.sin(i * 0.16) * 1.3) for i in range(1500)]
sf, i = '', 0
while i < 1500:                                                  # on regroupe les colonnes de même hauteur en un seul rectangle
    k = i
    while k < 1500 and ys[k] == ys[i]: k += 1
    sf += s.rect(i, ys[i], k - i, 1, '#d8f4ff') + f'<rect x="{i*s.P}" y="{(ys[i]+1)*s.P}" width="{(k-i)*s.P}" height="{s.P}" fill="#4df0ff" fill-opacity="0.55"/>'
    i = k
s.add('<svg x="0" y="0" overflow="visible">' + sf + '</svg>')
for k, x0 in enumerate((300, 900, 1500, 2200)):
    s.add(f'<svg overflow="visible"><polygon points="{x0},0 {x0+70},0 {x0+330},1500 {x0+230},1500" fill="#d8f4ff" fill-opacity="0.05"><animate attributeName="fill-opacity" values="0.02;0.08;0.02" dur="{7+k*1.3:.1f}s" repeatCount="indefinite"/></polygon></svg>')
s.bank(1500, 4, 1, 72, '#d8c090'); s.bank(1500, 2, 1, 73, '#b89c68')
rk = ''.join(s.rect(random.randint(0, 1400), -random.randint(2, 5), random.randint(6, 12), random.randint(2, 4), '#2a4560') for _ in range(14))
s.add(f'<svg x="0" y="100%" overflow="visible">{rk}</svg>')
cross(s, 'sub', 26, 58, 0, extra=s.sprite('sub', 0, 0))
cross(s, 'school', 56, 34, -8, flip=True, step=1.8, extra=school(s, 7, 1, FC[0]))
cross(s, 'school', 74, 46, -26, flip=False, step=1.6, extra=school(s, 6, 2, FC[1]))
bubbles(s, 34); s.save('fullscreen')

# ---------- ÉDITEUR : plancton, épave, algues, corail et poisson-lanterne en bas à droite ----------
random.seed(72); s = oc(3)
s.stars(90, 4)
inner = s.sprite('wreck', 0, 4) + both(s, 'kelp_a', 'kelp_b', 36, 4) + both(s, 'kelp_s_a', 'kelp_s_b', 42, 16) + s.sprite('coral_a', 48, 24) + s.sprite('coral_b', 26, 27) \
        + glow(s, s.sprite('angler', 40, 0), (0.7, 1), (1.4, 2.6))
s.pin(inner, 62 * s.P, 38 * s.P, 'br', 14, 22); s.save('editor')

# ---------- TERMINAL : fond marin, algues, corail, crabe, étoile de mer, méduses, petits poissons ----------
random.seed(73); s = oc(4)
s.stars(20, 4, 2, 55); s.bank(1100, 3, 1, 74, '#d8c090'); s.bank(1100, 2, 1, 75, '#b89c68')
s.pin(both(s, 'kelp_a', 'kelp_b', 0, 0) + s.sprite('coral_c', 8, 21) + s.sprite('crab', 22, 29) + s.sprite('starfish', 36, 30), 42 * s.P, 35 * s.P, 'bl', 90, 6)
s.pin(both(s, 'kelp_s_a', 'kelp_s_b', 0, 7) + s.sprite('coral_a', 8, 15), 22 * s.P, 29 * s.P, 'br', 50, 6)
s.add(bob(s, glow(s, s.sprite('jelly_p', 0, 0)), 35, 12, 6, 5)); s.add(bob(s, glow(s, s.sprite('jelly_c', 0, 0)), 72, 22, 5, 6.5))
cross(s, 'school', 78, 30, -6, step=1.6, extra=school(s, 5, 3, FC[2]))
bubbles(s, 12, dur=(6, 11), px=(3, 4)); s.save('panel')

# ---------- EXPLORATEUR : gros sous-marin, méduses, forêt d'algues ----------
random.seed(74); s = oc(4)
s.stars(18, 4, 0, 92); bubbles(s, 22, dur=(9, 18))
for xp, yp, nm in ((20, 18, 'jelly_p'), (62, 36, 'jelly_v'), (36, 54, 'jelly_c')): s.add(bob(s, glow(s, s.sprite(nm, 0, 0)), xp, yp, 7, 5 + xp / 40))
s.pin(both(s, 'kelp_a', 'kelp_b', 0, 0) + both(s, 'kelp_s_a', 'kelp_s_b', 8, 12) + s.sprite('sub', 15, 22, None, 2) + both(s, 'kelp_a', 'kelp_b', 70, 0) + s.sprite('coral_c', 62, 24) + s.sprite('coral_a', 48, 34), 80 * s.P, 48 * s.P, 'bl', 6, 4)
s.save('sidebar')

# ---------- BARRE DE DROITE : leurres lumineux des abysses qui se balancent ----------
random.seed(75); s = oc(4)
for i, (xp, L, c1, c2) in enumerate([(16, 12, '#d8ff6b', '#7dffc4'), (46, 24, '#ff77c5', '#a56bff'), (76, 8, '#4df0ff', '#1fb5c8')]):
    orb = f'<rect x="{-2*s.P}" y="{(L-2)*s.P}" width="{5*s.P}" height="{5*s.P}" fill="{c1}" fill-opacity="0.22"/>' + s.rect(-1, L - 1, 3, 3, c2) + s.rect(0, L, 1, 1, '#fcfcfc')
    stalk = s.rect(0, 0, 1, L - 1, '#2a4560')
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{3.2 + i*0.5:.1f}s" repeatCount="indefinite"/>{stalk}{glow(s, orb, (0.35, 0.8), (1.2, 2.4))}</g></svg>')
s.save('aux')
json.dump(OC_SPR['sub'], open(os.path.expanduser('~/pixel-worlds/tools/sub_frame.json'), 'w'))
print('Océan : décors générés')
