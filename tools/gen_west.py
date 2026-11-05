# Monde « Far West » : saloon, cactus, mesas, train, cowboy, boule d'herbe.
# Usage : python3 tools/gen_west.py
import os, math, random, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

WW_PAL = {'T':'#7a4a22','t':'#4a2a12','S':'#f0b890','s':'#c88a60','K':'#14100c','R':'#c8283c','r':'#8a1a28','B':'#3c6ad0','b':'#2a4a98','P':'#4a5a7a','g':'#6c7488',
          'C':'#2f8a3c','c':'#58c060','M':'#ff6fa0','Y':'#f2c45a','y':'#a67c1c','O':'#e0733a','o':'#a8481f','E':'#c8581f','e':'#8a3a14','D':'#e8c890','d':'#c9a870',
          'W':'#fcfcfc','w':'#e8e0d0','H':'#8a5a2a','l':'#5a3a18','F':'#ffd23a','N':'#ff4d5a'}
WW_STARS = ['#fff4d8', '#fff4d8', '#f2c45a', '#ffb070', '#c8a4ff']
FONT = {'S': [".##", "#..", ".#.", "..#", "##."], 'A': [".#.", "#.#", "###", "#.#", "#.#"], 'L': ["#..", "#..", "#..", "#..", "###"],
        'O': ["###", "#.#", "#.#", "#.#", "###"], 'N': ["##.", "#.#", "#.#", "#.#", "#.#"]}
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
def make_saguaro(h, seed=1):
    rnd = random.Random(seed); W = 15; g = grid(W, h); cx = W // 2
    def col(x0, y0, y1, w=4):
        for y in range(y0, y1):
            for x in range(x0, x0 + w):
                g[y][x] = 'c' if x < x0 + w // 2 else 'C'
            if (y % 3) == 0: g[y][x0 + w // 2] = 'C'
        for x in range(x0 + 1, x0 + w - 1): g[y0][x] = 'c'
    col(cx - 2, 3, h)
    ay = int(h * 0.45); ay2 = int(h * 0.60)
    for x in range(cx - 6, cx - 1): g[ay + 2][x] = g[ay + 3][x] = 'c'
    col(cx - 6, ay - 4, ay + 4, 3)
    for x in range(cx + 2, cx + 7): g[ay2 + 2][x] = g[ay2 + 3][x] = 'C'
    col(cx + 5, ay2 - 6, ay2 + 4, 3)
    g[2][cx] = g[2][cx - 1] = 'M'; g[ay - 5][cx - 5] = 'M'; g[ay2 - 7][cx + 6] = 'M'
    return done(g)
def make_mesa(w, h, seed=1):
    rnd = random.Random(seed); g = grid(w, h); tiers = 4; th = h // tiers
    for t in range(tiers):
        inset = [5, 1, 3, 0][t] + rnd.randint(0, 1); top = t * th
        for y in range(top, h if t == tiers - 1 else top + th + 1):
            for x in range(inset + (tiers - 1 - t) * 0, w - inset):
                if y < h: g[y][x] = ['O', 'E', 'o', 'e'][(y // 2 + t) % 4] if x < w * 0.68 else ['o', 'e', 'e', 'e'][(y // 2 + t) % 4]
    for x in range(w): g[0][x] = '.' if g[0][x] == '.' else g[0][x]
    return done(g)
def make_saloon():
    W, H = 34, 27; g = grid(W, H)
    for y in range(0, 9):
        for x in range(4, 30): g[y][x] = 'l'
    for i, ch in enumerate('SALOON'):
        for y, row in enumerate(FONT[ch]):
            for x, c in enumerate(row):
                if c == '#': g[2 + y][6 + i * 4 + x] = 'Y'
    for y in range(9, H):
        for x in range(1, 33): g[y][x] = 'H' if (x % 4) else 'l'
    for x in range(0, W): g[9][x] = 'l'; g[10][x] = 'l'
    for wx in (4, 24):
        for y in range(13, 19):
            for x in range(wx, wx + 6): g[y][x] = 'Y' if (x + y) % 5 else 'F'
        for x in range(wx - 1, wx + 7): g[12][x] = 'l'; g[19][x] = 'l'
    for y in range(15, H):
        for x in range(14, 20): g[y][x] = 'K'
    for y in range(17, 24):
        for x in range(14, 17): g[y][x] = 'T'
        for x in range(17, 20): g[y][x] = 'T'
    for y in range(17, 24): g[y][16] = 'K'; g[y][17] = 'K'
    for x in range(0, W): g[21][x] = g[21][x] if 14 <= x < 20 else 'l'
    for yy in range(21, H): g[yy][1] = g[yy][W - 2] = 'l'
    for x in range(1, W - 1): g[22][x] = 'l' if g[22][x] != 'K' else 'K'
    return done(g)
def make_train():
    W, H = 70, 17; g = grid(W, H)
    def rect(x0, y0, x1, y1, ch):
        for y in range(y0, y1):
            for x in range(x0, x1): g[y][x] = ch
    rect(0, 6, 22, 13, 'K'); rect(2, 6, 22, 7, 'g'); rect(8, 3, 14, 6, 'K'); rect(9, 1, 13, 3, 'g')      # chaudière, cheminée
    rect(16, 3, 24, 13, 'R'); rect(17, 4, 23, 7, 'Y'); rect(16, 2, 25, 3, 'r')                          # cabine
    rect(0, 11, 4, 14, 'K'); g[12][0] = 'F'                                                              # chasse-pierres + phare
    rect(26, 5, 46, 13, 'E'); rect(26, 5, 46, 6, 'e'); rect(26, 12, 46, 13, 'e')
    for x in range(27, 46, 5): rect(x, 6, x + 1, 12, 'e')
    rect(48, 5, 68, 13, 'O'); rect(48, 5, 68, 6, 'o'); rect(48, 12, 68, 13, 'o')
    for x in range(49, 68, 5): rect(x, 6, x + 1, 12, 'o')
    rect(22, 11, 26, 12, 'g'); rect(46, 11, 48, 12, 'g')
    for wx in (3, 9, 17, 29, 40, 52, 63):
        for y in range(12, 16):
            for x in range(wx, wx + 4):
                if math.hypot(x - wx - 1.5, y - 13.5) <= 2.2: g[y][x] = 'g' if (x + y) % 3 else 'W'
    return done(g)
def make_tumble(seed):
    rnd = random.Random(seed); g = grid(9, 9)
    for _ in range(26):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(2.2, 4.4); x = int(round(4 + math.cos(a) * r)); y = int(round(4 + math.sin(a) * r))
        if 0 <= x < 9 and 0 <= y < 9: g[y][x] = 'T' if rnd.random() < 0.7 else 'H'
    return done(g)
def make_star():
    g = grid(11, 11); cx, cy = 5, 5.2; pts = []
    for k in range(10):
        r = 5.4 if k % 2 == 0 else 2.4; a = -math.pi / 2 + k * math.pi / 5; pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    fill(g, pts, 'Y'); g[5][5] = 'W'
    for k in range(0, 10, 2): g[int(round(cy + 5.6 * math.sin(-math.pi / 2 + k * math.pi / 5)))][int(round(cx + 5.6 * math.cos(-math.pi / 2 + k * math.pi / 5)))] = 'y'
    return done(g)
WW_SPR = {
 'saguaro_l': make_saguaro(40, 1), 'saguaro_m': make_saguaro(30, 2), 'saguaro_s': make_saguaro(20, 3), 'saguaro_xl': make_saguaro(48, 4),
 'mesa_l': make_mesa(40, 24, 1), 'mesa_m': make_mesa(30, 18, 2), 'mesa_xl': make_mesa(44, 28, 3), 'saloon': make_saloon(), 'train': make_train(),
 'tumble_a': make_tumble(1), 'tumble_b': make_tumble(2), 'sheriff': make_star(),
 'cowboy': ["...TTT...", "..TTTTT..", "TTTTTTTTT", "..SSSSS..", "..SKSKS..", "..StttS..", ".RRRRRRR.", ".BBBBBBB.", "SBBBBBBBg", ".BBBBBBB.", "..PPPPP..", "..PP.PP..", ".tt..tt.."],
 'skull': ["..wwwww..", ".wwwwwww.", "wwKwwwKww", ".wwwKwww.", "..wwwww..", "..w.w.w.."],
 'barrel': [".HHHHH.", "HHHHHHH", "ggggggg", "HlHHHlH", "HHHHHHH", "ggggggg", "HHHHHHH", ".HHHHH."],
 'horseshoe': ["g.....g", "gg...gg", "gW...Wg", "gg...gg", ".gg.gg.", "..ggg.."],
 'poster': ["dddddddd", "dDDDDDDd", "dDKKKKDd", "dDDDDDDd", "dDDKKDDd", "dDKKKKDd", "dDDKKDDd", "dDDDDDDd", "dDKKKKDd", "dddddddd"],
 'crow': ["..KK.", "KKKKK", ".KKK.", "..K.K"],
}
def west(P): return Svg('west', P, WW_PAL, WW_SPR, WW_STARS)
def dust(s, n, dur=(9, 20)):
    for _ in range(n):
        y = random.uniform(8, 96); d = random.uniform(*dur); b = -random.uniform(0, d); sz = random.choice((3, 4, 5))
        s.o.append(f'<rect x="-4%" y="{y:.1f}%" width="{sz}" height="{max(2, sz-2)}" fill="#e8c890" fill-opacity="0.45"><animate attributeName="x" values="-4%;104%" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></rect>')
def cross(s, y_pct, dur, begin, inner, lo=-12, hi=112, step=1.5, idle=30, bottom=False, bob=(0, -2, 0, 2)):
    vals = [lo + k * step for k in range(int((hi - lo) / step) + 1)]
    xs = ';'.join(f'{v:.1f}%' for v in vals) + ';' + ';'.join([f'{hi}%'] * idle)
    yattr = 'y="100%"' if bottom else f'y="{y_pct}%"'
    s.add(f'<svg {yattr} overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
          f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0,{v}" for v in bob)}" calcMode="discrete" dur="1.6s" repeatCount="indefinite"/>{inner}</g></svg>')

# ---------- PLEIN ÉCRAN : fil télégraphique et corbeaux, sable, train, boule d'herbe, poussière ----------
random.seed(81); s = west(3)
ys = [round(4 * ((i % 260) / 260) * (1 - (i % 260) / 260) * 9) for i in range(1500)]
wire, i = '', 0
while i < 1500:
    k = i
    while k < 1500 and ys[k] == ys[i]: k += 1
    wire += s.rect(i, ys[i], k - i, 1, '#4a2a12'); i = k
for px_ in range(130, 1500, 260): wire += s.rect(px_ - 1, 0, 2, 13, '#7a4a22') + s.rect(px_ - 5, 1, 10, 1, '#7a4a22') + s.rect(px_ - 4, 2, 8, 1, '#5a3a18')
for cx_ in (60, 150, 330, 460, 690, 880): u = (cx_ % 260) / 260; wire += s.sprite('crow', cx_, round(4 * u * (1 - u) * 9) - 3)
s.add('<svg x="0" y="0" overflow="visible">' + wire + '</svg>')
s.bank(1500, 4, 1, 82, '#e8c890'); s.bank(1500, 2, 1, 83, '#c9a870')
tr = s.sprite('train', 0, 0)
smoke = ''.join(f'<rect x="{(10 + k)*s.P}" y="0" width="{(3 + k % 2)*s.P}" height="{(3 + k % 2)*s.P}" fill="#e8e0d0" fill-opacity="0.8"><animate attributeName="y" values="0;{-30*s.P}" dur="3s" begin="-{k}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="3s" begin="-{k}s" repeatCount="indefinite"/></rect>' for k in range(3))
cross(s, 0, 80, 0, tr + smoke, step=1.1, bottom=True, bob=(0, -1, 0, -1))
tw = f'<g><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="0.5s" repeatCount="indefinite"/>{s.sprite("tumble_a", 0, 0)}</g><g><animate attributeName="opacity" values="0;1" calcMode="discrete" dur="0.5s" repeatCount="indefinite"/>{s.sprite("tumble_b", 0, 0)}</g>'
cross(s, 0, 40, -14, f'<g transform="translate(0,-34)">{tw}</g>', step=1.8, bottom=True, bob=(0, -9, 0, -3))
dust(s, 28); s.save('fullscreen')

# ---------- ÉDITEUR : étoiles, mesas et cactus en bas à droite ----------
random.seed(82); s = west(3)
s.stars(90, 4)
s.pin_sprites([('mesa_l', 0, 12, None, 1), ('mesa_m', 28, 18, None, 1), ('saguaro_l', 22, 0, None, 1), ('saguaro_s', 46, 20, None, 1), ('skull', 56, 30, None, 1)], 'br', 14, 22)
s.save('editor')

# ---------- TERMINAL : saloon, cowboy, barils, cactus, crâne de vache ----------
random.seed(83); s = west(4)
s.stars(18, 4, 2, 52); s.bank(1100, 3, 1, 84, '#e8c890'); s.bank(1100, 2, 1, 85, '#c9a870')
s.pin(s.sprite('saloon', 0, 0) + s.sprite('cowboy', 37, 14) + s.sprite('barrel', 46, 19) + s.sprite('barrel', 54, 19), 62 * s.P, 27 * s.P, 'bl', 90, 6)
s.pin(s.sprite('saguaro_m', 0, 0) + s.sprite('skull', 17, 21) + s.sprite('tumble_a', 12, 18), 27 * s.P, 30 * s.P, 'br', 60, 6)
dust(s, 8, dur=(8, 16)); s.save('panel')

# ---------- EXPLORATEUR : mesa, grand cactus, affiche « WANTED », cowboy ----------
random.seed(84); s = west(4)
s.stars(16, 4, 0, 92); dust(s, 10)
s.pin(s.sprite('mesa_xl', 0, 20) + s.sprite('saguaro_xl', 28, 0) + s.rect(20, 33, 1, 15, '#5a3a18') + s.sprite('poster', 17, 22) + s.sprite('cowboy', 4, 35), 44 * s.P, 48 * s.P, 'bl', 10, 4)
s.save('sidebar')

# ---------- BARRE DE DROITE : étoiles de shérif et fers à cheval qui se balancent ----------
random.seed(85); s = west(4)
for i, (xp, L, name) in enumerate([(18, 8, 'sheriff'), (50, 18, 'horseshoe'), (78, 12, 'sheriff')]):
    gg = s.rect(5, 0, 1, L, '#6c7488') + s.sprite(name, 0 if name == 'sheriff' else 2, L)
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{3 + i * 0.5:.1f}s" repeatCount="indefinite"/>{gg}</g></svg>')
s.save('aux')
print('Far West : décors générés')
