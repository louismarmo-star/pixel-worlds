# Monde « Fantasy » : château, dragon, chevalier, forêt enchantée, trésor.
# Usage : python3 tools/gen_fantasy.py
import os, math, random, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')).read()
exec(src[:src.index('# =====================================  PÔLE NORD')])   # réutilise la classe Svg

FA_PAL = {'S':'#8c8fa6','s':'#5c6078','a':'#a7abc4','R':'#c8283c','r':'#7a1f2e','Y':'#f2c45a','y':'#a67c1c','V':'#7a3fd0','v':'#4a2590',
          'G':'#3ecf6a','g':'#217a42','e':'#2e8b57','E':'#4fd08a','l':'#8cffb8','T':'#7c4a22','t':'#4a2a12','W':'#fcfcfc','w':'#e8e0d0','K':'#14141e',
          'B':'#3c7bff','b':'#1f4fb8','P':'#9a5fe0','p':'#6b3fb0','O':'#ff8a1e','F':'#ffd23a','M':'#ff6fa0','N':'#ff4d5a','C':'#7fe0ff'}
FA_STARS = ['#fff4d8', '#fff4d8', '#f2c45a', '#8cffb8', '#c8a4ff']
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
def make_dragon(frame):
    W, H = 26, 16; g = grid(W, H)
    wing = [(9, 7), (4, 0), (14, 1), (16, 7)] if frame == 0 else [(9, 9), (3, 15), (13, 15.5), (16, 10)]
    fill(g, wing, 'P'); line(g, 9, 7.5 if frame == 0 else 9.5, 4.5 if frame == 0 else 4, 0.5 if frame == 0 else 14, 'p')
    for y in range(H):                                          # corps
        for x in range(W):
            if ((x - 12) / 8.2) ** 2 + ((y - 9) / 3.4) ** 2 <= 1: g[y][x] = 'G'
    for x in range(5, 19): g[11][x] = 'Y'; g[12][x] = 'Y' if x % 2 else g[12][x]                           # ventre
    line(g, 17, 8, 20.5, 5, 'G', 2)                                                                          # cou
    for y in range(3, 7):
        for x in range(20, 25): g[y][x] = 'G'
    g[5][25] = g[6][24] = g[6][25] = 'G'; g[7][22] = g[7][23] = g[7][24] = 'g'; g[4][22] = 'R'; g[2][20] = g[3][20] = 'Y'; g[2][21] = 'Y'
    line(g, 5, 9, 1, 11, 'g', 2); line(g, 1, 11, 2, 14, 'g', 1); g[14][3] = 'Y'                              # queue
    for lx in (9, 14): g[12][lx] = g[13][lx] = g[13][lx + 1] = 'g'                                           # pattes
    for x in range(8, 18, 2): g[5][x] = 'Y'                                                                  # dos
    return done(g)
def make_castle(w, h, seed=3):
    rnd = random.Random(seed); g = grid(w, h); tw = max(7, int(w * 0.22)); keep_h = int(h * 0.50)
    parts = [(2, tw, int(h * 0.70)), (w - tw - 2, tw, int(h * 0.82)), (tw, w - 2 * tw, keep_h)]
    for x0, ww, hh in parts:
        for y in range(h - hh, h):
            for x in range(x0, x0 + ww):
                if x < w: g[y][x] = 's' if ((y - h) % 3 == 0 or (x + (y // 3) * 2) % 6 == 0) else 'S'
        for x in range(x0, x0 + ww, 2):
            if h - hh - 1 >= 0 and x < w: g[h - hh - 1][x] = 'S'
    for x0, ww, hh in parts[:2]:                               # toits coniques
        top = h - hh - 1; rh = int(ww * 1.3); cx = x0 + ww // 2
        for k in range(rh):
            half = int((ww / 2 + 1) * (k + 1) / rh)
            for x in range(cx - half, cx + half + 1):
                yy = top - rh + k + 1
                if 0 <= yy < h and 0 <= x < w: g[yy][x] = 'V' if x <= cx else 'v'
        for k in range(4):
            if top - rh - k >= 0: g[top - rh - k][cx] = 't'
        if top - rh - 3 >= 0: g[top - rh - 3][cx + 1] = g[top - rh - 3][cx + 2] = 'R'; g[top - rh - 2][cx + 1] = 'R'
    for x0, ww, hh in parts:                                    # meurtrières
        for y in range(h - hh + 4, h - 8, 6):
            for x in range(x0 + 2, x0 + ww - 2, 4):
                lit = rnd.random() < 0.55; g[y][x] = g[y + 1][x] = 'F' if lit else 'K'
    gx = w // 2 - 3
    for y in range(h - 8, h):
        for x in range(gx, gx + 6):
            g[y][x] = 'K'
    for x in range(gx - 1, gx + 7): g[h - 9][x] = 't'
    for y in range(h - 8, h): g[y][gx + 2] = g[y][gx + 3] = 'T'
    return done(g)
def make_magic_tree(w, h, seed=4):
    rnd = random.Random(seed); g = grid(w, h); cx = w // 2; ch = int(h * 0.62)
    for y in range(int(ch * 0.55), h):
        off = int(round(math.sin(y * 0.35) * 1.2)); wide = 3 if y < h - 4 else 5
        for x in range(cx + off - wide // 2, cx + off + wide // 2 + 1):
            if 0 <= x < w: g[y][x] = 't' if x > cx + off else 'T'
    blobs = [(cx, ch * .42, w * .36), (cx - w * .26, ch * .62, w * .26), (cx + w * .27, ch * .60, w * .26), (cx, ch * .18, w * .24)]
    for y in range(ch + 4):
        for x in range(w):
            if any(((x - bx) / br) ** 2 + ((y - by) / (br * .82)) ** 2 <= 1 for bx, by, br in blobs):
                lit = (cx - x) * 0.5 + (ch / 2 - y) * 0.5
                c = 'E' if lit > w * .1 else ('e' if lit > -w * .1 else 'g')
                r = rnd.random()
                if r < 0.06: c = 'l'
                elif r < 0.10: c = 'L'
                g[y][x] = c
    return done(g)
def make_banner(h=16):
    g = grid(7, h)
    for x in range(7): g[0][x] = 'Y'
    for y in range(1, h - 3):
        for x in range(7): g[y][x] = 'R'
    for k, y in enumerate(range(h - 3, h)):
        for x in range(k, 7 - k): g[y][x] = 'R'
    for (x, y) in ((3, 3), (2, 4), (3, 4), (4, 4), (3, 5), (3, 6), (3, 7)): g[y][x] = 'Y'
    return done(g)
FA_SPR = {
 'dragon_up': make_dragon(0), 'dragon_down': make_dragon(1),
 'castle_l': make_castle(40, 36), 'castle_xl': make_castle(46, 56, 5),
 'tree_a': make_magic_tree(22, 30, 4), 'tree_b': make_magic_tree(17, 24, 6),
 'knight': ["...RRR...", "..SSSSS..", "..SKKKS..", "..SSSSS..", ".BBsSSsW.", ".BYBSSsW.", ".BBBSSsW.", "..sSSSs..", "..SS.SS..", "..SS.SS..", ".ssS.Sss."],
 'torch': [".F.", "FOF", ".O.", ".T.", ".T.", ".T."],
 'mush': ["..RRR..", ".RWRRWR", "RRRRRRR", "..www..", "..www.."],
 'chest': ["..Y.YY.Y..", ".YYYYYYYY.", "TTTTTTTTTT", "TyTTTTTTyT", "TTTTYYTTTT", "TTTTYKTTTT", "tttttttttt"],
 'banner': make_banner(), 'lantern': ["..y..", ".YYY.", "YFFFY", "YFFFY", ".YYY.", "..y.."],
}
def fan(P): return Svg('fantasy', P, FA_PAL, FA_SPR, FA_STARS)
def fireflies(s, n, dur=(9, 18)):
    for _ in range(n):
        x = random.uniform(0, 100); d = random.uniform(*dur); b = -random.uniform(0, d); amp = random.uniform(4, 14) * s.P; ph = random.uniform(0, 6.28)
        vals = ';'.join(f'{amp*math.sin(ph + k*0.8):.1f},0' for k in range(14))
        s.o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                   f'<rect x="{x:.1f}%" y="104%" width="{s.P}" height="{s.P}" fill="#d8ff6b"><animate attributeName="y" values="104%;-4%" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0.1;1;0.2;1;0.1" dur="{random.uniform(1.5, 3.5):.1f}s" repeatCount="indefinite"/></rect></g>')
def flames(s, inner): return s.twinkle(inner, lo=(0.45, 0.8), dur=(0.35, 0.9))

# ---------- PLEIN ÉCRAN : fanions en haut, herbe, dragon qui survole, lucioles ----------
random.seed(61); s = fan(3)
rope = []; cols = ['R', 'Y', 'B', 'G']
for i in range(0, 1500, 2):
    u = (i % 120) / 120; y = round(4 * u * (1 - u) * 7); rope.append(s.rect(i, y, 2, 1, '#7c4a22'))
    if (i // 2) % 4 == 2: rope.append(s.rect(i, y + 1, 3, 1, FA_PAL[cols[(i // 8) % 4]]) + s.rect(i, y + 2, 3, 1, FA_PAL[cols[(i // 8) % 4]]) + s.rect(i + 1, y + 3, 1, 1, FA_PAL[cols[(i // 8) % 4]]))
s.add('<svg x="0" y="0" overflow="visible">' + ''.join(rope) + '</svg>')
s.bank(1500, 4, 1, 62, '#3a8f52'); s.bank(1500, 2, 1, 63, '#2a6b3e')
fl = ''.join(s.rect(random.randint(0, 1400), -random.randint(1, 4), 1, 1, random.choice(['#f2c45a', '#ff6fa0', '#fcfcfc', '#c8a4ff'])) for _ in range(40))
s.add(f'<svg x="0" y="100%" overflow="visible">{fl}</svg>')
xs = ';'.join(f'{x:.1f}%' for x in [-8 + k * 1.2 for k in range(0, 100)]) + ';' + ';'.join(['112%'] * 80)
fa = f'<g><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="0.8s" repeatCount="indefinite"/>{s.sprite("dragon_up", 0, 0)}</g><g><animate attributeName="opacity" values="0;1" calcMode="discrete" dur="0.8s" repeatCount="indefinite"/>{s.sprite("dragon_down", 0, 0)}</g>'
s.add(f'<svg y="15%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="70s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0;0,3" calcMode="discrete" dur="3.2s" repeatCount="indefinite"/>{fa}</g></svg>')
fireflies(s, 36); s.save('fullscreen')

# ---------- ÉDITEUR : étoiles, château lointain, arbres enchantés, chevalier ----------
random.seed(62); s = fan(3)
s.stars(100, 4)
s.pin_sprites([('tree_b', 0, 10, None, 1), ('castle_l', 14, 0, None, 1), ('tree_a', 56, 6, None, 1), ('knight', 40, 25, None, 1)], 'br', 14, 22); s.save('editor')

# ---------- TERMINAL : herbe, chevalier, champignons magiques, coffre au trésor ----------
random.seed(63); s = fan(4)
s.stars(20, 4, 2, 55); s.bank(1100, 3, 1, 64, '#3a8f52'); s.bank(1100, 2, 1, 65, '#2a6b3e')
fl = ''.join(s.rect(random.randint(0, 1000), -random.randint(1, 3), 1, 1, random.choice(['#f2c45a', '#ff6fa0', '#fcfcfc', '#c8a4ff'])) for _ in range(30))
s.add(f'<svg x="0" y="100%" overflow="visible">{fl}</svg>')
inner = s.sprite('knight', 0, 4) + flames(s, s.sprite('torch', 11, 5)) + s.twinkle(s.sprite('mush', 17, 10), lo=(0.6, 0.9), dur=(1.5, 3))
s.pin(inner, 24 * s.P, 15 * s.P, 'bl', 120, 6)
s.pin(s.sprite('chest', 0, 3) + s.twinkle(s.rect(2, 0, 1, 1, '#fcfcfc') + s.rect(7, 1, 1, 1, '#fcfcfc'), lo=(0.1, 0.5), dur=(0.8, 1.8)), 10 * s.P, 10 * s.P, 'br', 70, 6)
fireflies(s, 10, dur=(6, 12)); s.save('panel')

# ---------- EXPLORATEUR : grand château, torches, lucioles ----------
random.seed(64); s = fan(4)
s.stars(16, 4, 0, 92); fireflies(s, 26, dur=(10, 20))
s.pin(s.sprite('castle_xl', 0, 0) + flames(s, s.sprite('torch', 17, 49)) + flames(s, s.sprite('torch', 26, 49)), 46 * s.P, 56 * s.P, 'bl', 4, 0); s.save('sidebar')

# ---------- BARRE DE DROITE : bannières et lanterne qui se balancent ----------
random.seed(65); s = fan(4)
for i, (xp, L, name) in enumerate([(16, 0, 'banner'), (46, 10, 'lantern'), (76, 4, 'banner')]):
    gg = (s.rect(3, 0, 1, L, '#7c4a22') if L else '') + s.sprite(name, 0, L)
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{3 + i * 0.5:.1f}s" repeatCount="indefinite"/>{gg}</g></svg>')
s.save('aux')
json.dump({'up': FA_SPR['dragon_up'], 'down': FA_SPR['dragon_down']}, open(os.path.expanduser('~/pixel-worlds/tools/dragon_frames.json'), 'w'))
print('Fantasy : décors générés')
