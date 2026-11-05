# Monde « Espace » : planète à anneaux, fusée sur son pas de tir, astronaute, satellite, étoiles filantes.
# Usage : python3 tools/gen_space.py
import os, math, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

SP_PAL = {'K':'#05061a','k':'#0e1033','W':'#fcfcfc','w':'#d8e4ff','g':'#9aa3b8','G':'#6c7488','Z':'#4a5068','R':'#ff5a3c','r':'#c23a22','O':'#ff9a2e','Y':'#ffe066',
          'B':'#3c7bff','b':'#1f4fb8','C':'#4df0ff','P':'#a56bff','p':'#6b3fd0','M':'#ff77c5','T':'#d9b38c','t':'#a9825a','S':'#e8c9a0','s':'#b8956a',
          'E':'#2e8bff','e':'#3ecf6a','N':'#ff4d5a','o':'#7a2a1a'}
SP_STARS = ['#fcfcfc', '#fcfcfc', '#ffe066', '#4df0ff', '#ff77c5']
def grid(w, h): return [['.'] * w for _ in range(h)]
def done(g): return [''.join(r) for r in g]
TONES = {'ring': ('S', 'T', 't'), 'mars': ('O', 'R', 'r'), 'ice': ('C', 'B', 'b'), 'moon': ('w', 'g', 'G'), 'earth': ('C', 'E', 'b')}
def make_planet(d, kind, ring=False, seed=1):
    rnd = random.Random(seed); lt, md, dk = TONES[kind]; W = d + (12 if ring else 0); g = grid(W, d); c = (d - 1) / 2; cx = (W - 1) / 2
    for y in range(d):
        for x in range(W):
            r = math.hypot(x - cx, y - c)
            if r <= d / 2:
                lit = ((x - cx) * 0.6 + (y - c) * 0.8) / (d / 2)
                ch = dk if lit > 0.55 else (md if lit > 0.05 else lt)
                if kind in ('ring', 'mars') and y % 4 == 1 and lit < 0.55: ch = md if ch == lt else ch    # bandes
                if kind == 'moon' and rnd.random() < 0.06: ch = dk
                if kind == 'earth' and rnd.random() < 0.18 and math.hypot(x - cx + 2, y - c + 1) < d * 0.3: ch = 'e'
                g[y][x] = ch
    if ring:
        a, b = W / 2 - 0.4, max(1.6, d * 0.2)
        for y in range(d):
            for x in range(W):
                dx, dy = x - cx, y - c; v = (dx / a) ** 2 + (dy / b) ** 2
                if abs(v - 1) < 0.28 and not (dy < 0 and math.hypot(dx, dy) <= d / 2): g[y][x] = 'S' if (x + y) % 5 else 's'
    return done(g)
def make_rocket(w=15, h=46):
    g = grid(w, h); cx = w // 2
    for y in range(12):
        half = round(cx * ((y + 1) / 12) ** 0.8)
        for x in range(cx - half, cx + half + 1): g[y][x] = 'R' if x <= cx else 'r'
    for y in range(12, h - 5):
        for x in range(cx - 4, cx + 5): g[y][x] = 'W' if x <= cx + 2 else 'w'
    for yy in range(18, 23):
        for x in range(w):
            if math.hypot(x - cx, yy - 20) <= 2.6: g[yy][x] = 'B'
            elif math.hypot(x - cx, yy - 20) <= 3.4: g[yy][x] = 'G'
    g[19][cx - 1] = 'C'
    for x in range(cx - 4, cx + 5): g[28][x] = 'R'; g[29][x] = 'r'
    for k in range(10):
        for x in (cx - 4 - k // 2 - 1, cx + 4 + k // 2 + 1):
            if 0 <= x < w: g[h - 14 + k][x] = 'R'
    for y in range(h - 5, h):
        for x in range(cx - 2, cx + 3): g[y][x] = 'G' if x <= cx else 'Z'
    return done(g)
def make_tower(w=9, h=54):
    g = grid(w, h)
    for y in range(h): g[y][0] = 'G'; g[y][w - 1] = 'G'
    for y in range(2, h - 2):
        if y % 6 == 0:
            for x in range(1, w - 1): g[y][x] = 'Z'
        else:
            k = (y % 6); g[y][min(w - 2, max(1, k))] = 'Z'
    for yy in (14, 32, 50):
        for x in range(w): g[yy][x] = 'g'
    g[0][w // 2] = 'N'
    return done(g)
SP_SPR = {
 'planet_ring': make_planet(21, 'ring', True, 1), 'planet_mars': make_planet(9, 'mars', False, 2), 'planet_ice': make_planet(7, 'ice', False, 3), 'planet_ring_s': make_planet(7, 'ring', True, 4),
 'moon': make_planet(9, 'moon', False, 5), 'moon_s': make_planet(7, 'moon', False, 6), 'earth': make_planet(13, 'earth', False, 7),
 'rocket': make_rocket(), 'tower': make_tower(),
 'asteroid_a': [".GG..", "GgGGG", "GGZGG", ".GGG."], 'asteroid_b': ["..GG.", ".GgGG", "GGGZG", ".ZGG."], 'asteroid_c': [".GG", "GZG", ".G."],
 'astronaut': ["..WWWWW..", ".WWWWWWW.", ".WBBBBBW.", ".WBCBBBW.", ".WWBBBWW.", "..WWWWW..", ".WWRWBWW.", "WWWWWWWWW", ".WWWWWWW.", "..WW.WW..", "..WW.WW..", ".GGG.GGG."],
 'rover': ["...BBBBBBBB.....", "...BCBCBCBC.....", "..gggggggggg....", ".gWWWWWWWWWWg...", ".gWWWWWWWWWWg..N", "..gggggggggg....", ".KKK..KKK..KKK..", ".KGK..KGK..KGK.."],
 'flag': ["GRRRR.", "GWWWW.", "GBBBB.", "G.....", "G.....", "G.....", "G.....", "G.....", "G....."],
 'satellite': ["BBBB..ggg..BBBB", "BCBC.gWWWg.BCBC", "BBBB..ggg..BBBB", "......gNg......"],
}
def space(P): return Svg('space', P, SP_PAL, SP_SPR, SP_STARS)
def streak(s, y0, x0, dur, begin, steps=18, dx=-3.2, dy=2.6):
    """Étoile filante : une tête blanche et une queue qui s'efface, qui descend en diagonale par petits sauts."""
    head = s.rect(0, 0, 2, 2, '#fcfcfc') + ''.join(s.rect(-k * 2.2, -k * 1.8, 2 - (k > 3), 2 - (k > 3), c) for k, c in ((1, '#ffe066'), (2, '#ffe066'), (3, '#ff9a2e'), (4, '#ff9a2e'), (5, '#c23a22'), (6, '#6b3fd0')))
    xs = ';'.join(f'{x0 + k*dx:.1f}%' for k in range(steps)) + ';' + ';'.join(['-30%'] * 26)
    ys = ';'.join(f'{y0 + k*dy:.1f}%' for k in range(steps)) + ';' + ';'.join(['-30%'] * 26)
    s.add(f'<svg overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
          f'<animate attributeName="y" values="{ys}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>{head}</svg>')

# ---------- PLEIN ÉCRAN : étoiles filantes, satellite qui traverse, sol lunaire ----------
random.seed(51); s = space(3)
s.stars(34, 4)
s.bank(1500, 3, 1, 52, '#9aa3b8'); s.bank(1500, 2, 1, 53, '#6c7488')
cr = ''.join(s.rect(random.randint(0, 1400), -random.randint(1, 2), random.randint(4, 8), 1, '#4a5068') for _ in range(40))
s.add(f'<svg x="0" y="100%" overflow="visible">{cr}</svg>')
xs = ';'.join(f'{x:.1f}%' for x in [-8 + k * 1.3 for k in range(0, 95)]) + ';' + ';'.join(['112%'] * 70)
s.add(f'<svg y="20%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="60s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0;0,3" calcMode="discrete" dur="2s" repeatCount="indefinite"/>{s.sprite("satellite", 0, 0)}</g></svg>')
streak(s, 4, 88, 22, 3); streak(s, 12, 62, 31, -9, dx=-2.6)
s.save('fullscreen')

# ---------- ÉDITEUR : étoiles, planète à anneaux, lune et astéroïdes en bas à droite ----------
random.seed(52); s = space(3)
s.stars(110, 4)
s.pin_sprites([('planet_ring', 0, 6, None, 1), ('moon', 40, 0, None, 1), ('asteroid_a', 36, 16, None, 1), ('asteroid_b', 48, 10, None, 1), ('asteroid_c', 29, 2, None, 1)], 'br', 16, 24)
s.save('editor')

# ---------- TERMINAL : surface lunaire, astronaute et drapeau, rover, Terre au loin ----------
random.seed(53); s = space(4)
s.stars(24, 4, 2, 60); s.bank(1100, 3, 1, 54, '#9aa3b8'); s.bank(1100, 2, 1, 55, '#6c7488')
cr = ''.join(s.rect(random.randint(0, 1000), -random.randint(1, 2), random.randint(4, 9), 1, '#4a5068') for _ in range(30))
s.add(f'<svg x="0" y="100%" overflow="visible">{cr}</svg>')
s.pin_sprites([('astronaut', 0, 0, None, 1), ('flag', 12, 3, None, 1)], 'bl', 140, 6)
s.pin_sprites([('rover', 0, 0, None, 1)], 'br', 60, 6)
s.pin_sprites([('earth', 0, 0, None, 1)], 'tr', 70, 14)
s.save('panel')

# ---------- EXPLORATEUR : grande fusée sur son pas de tir, tour de lancement, étoiles ----------
random.seed(54); s = space(4)
s.stars(28, 4, 0, 94)
inner = s.sprite('rocket', 0, 0) + s.sprite('tower', 19, -6) + ''.join(s.rect(15 + k, 15, 1, 1, '#6c7488') for k in range(4))
s.pin(inner + s.rect(-3, 46, 31, 2, '#4a5068') + s.rect(-1, 48, 27, 1, '#6c7488'), 28 * s.P, 54 * s.P, 'bl', 18, 4)
s.save('sidebar')

# ---------- BARRE DE DROITE : mini-planètes suspendues ----------
random.seed(55); s = space(4)
for i, (xp, L, name) in enumerate([(20, 8, 'planet_ring_s'), (52, 22, 'planet_mars'), (80, 12, 'moon_s')]):
    gg = s.rect(3, 0, 1, L, '#6c7488') + s.sprite(name, 0, L)
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{3 + i * 0.6:.1f}s" repeatCount="indefinite"/>{gg}</g></svg>')
s.save('aux')
print('Espace : décors générés')
