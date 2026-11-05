# Génère les décors pixel art des deux mondes (Noël et Pôle Nord), collés aux bords de la fenêtre.
# Usage : python3 tools/gen.py        (la taille d'un « pixel » se règle avec la variable P de chaque calque)
import random, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import noel_sprites as N
ROOT = os.path.expanduser('~/pixel-worlds/packs')

POLE_PAL = {'W':'#fcfcfc','I':'#d8ecff','i':'#88b8f0','J':'#4878c8','s':'#a4e4fc','Q':'#242c48','K':'#1c1c1c','o':'#f87800','z':'#98a0b0','Z':'#5c6478'}
POLE_SPR = {
 'penguin': ["...QQQ...","..QQQQQ..","..QWQWQ..","..QQoQQ..",".QQWWWQQ.","QQQWWWQQQ","QQQWWWQQQ",".QQWWWQQ.","..QWWWQ..","..QQQQQ..","..oo.oo..",".ooo.ooo."],
 'slider': [".........QQQ..","..QQQQQQQQQWQo",".QQQQQQQQQQQQ.","..WWWWWWWWWW..","..ooo.....ooo."],
 'bear': ["..............WW....","....WWWWWWWWWWWWWW..","..WWWWWWWWWWWWWWKWW.",".WWWWWWWWWWWWWWWWWWK",".WWWWWWWWWWWWWWWWWW.",".WWWWWWWWWWWWWWWWW..","..WWWWWWWWWWWWWWW...","...IIIIIIIIIIIII....","...WW.WW.....WW.WW..","...WW.WW.....WW.WW..","...ii.ii.....ii.ii.."],
 'seal': ["..........zzz...","...zzzzzzzzKzz..",".zzzzzzzzzzzzzzK",".zzZzzZzzzzzzzz.","..zzzzzzzzzzzz..","zzz..zzzzzzzz..."],
 'iciS': ["iIi","iIi",".I.",".i."], 'iciM': ["iIi","iIi","iIi",".I.",".I.",".i."], 'iciL': ["iIi","iIi","iIi","iIi",".I.",".I.",".I.",".i.",".i."],
}
def make_igloo(w, h):
    rows = []; cx = (w - 1) / 2
    for y in range(h):
        half = max(1, round((w / 2) * math.sqrt(max(0, 1 - ((h - y - 0.5) / h) ** 2))))
        row = ['.'] * w
        for x in range(w):
            dx = x - cx
            if abs(dx) <= half - 0.5:
                edge = abs(dx) > half - 1.5; seam = (y % 3 == 2) or ((x + (y // 3) * 3) % 7 == 0)
                row[x] = 'i' if edge else ('I' if seam else 'W')
        rows.append(row)
    dh = max(6, h // 3); dw = max(7, w // 4)
    for k in range(dh):
        y = h - dh + k; cur = min(dw, 3 + 2 * k)
        for x in range(w):
            if abs(x - cx) <= cur / 2 and rows[y][x] != '.': rows[y][x] = 'K' if abs(x - cx) < cur / 2 - 0.4 else 'J'
    return [''.join(r) for r in rows]
def make_tree(w, h, seed=3):
    """Grand sapin dessiné par code : étoile, 4 étages, guirlandes lumineuses, tronc."""
    rnd = random.Random(seed); g = [['.'] * w for _ in range(h)]; cx = w // 2
    star, trunk, tiers = 5, 4, 4; body = h - star - trunk; th = body // tiers
    for k in range(tiers):
        top = star + k * th - (k * 2 if k else 0); bottom = min(star + (k + 1) * th + 3, h - trunk)
        maxw = (w * (0.42 + 0.58 * (k + 1) / tiers)) / 2
        for y in range(top, bottom):
            half = max(1, round(maxw * (y - top + 1) / (bottom - top)))
            for x in range(max(0, cx - half), min(w, cx + half + 1)):
                g[y][x] = 'G' if x <= cx + half * 0.3 else 'g'
        for x in range(max(0, cx - round(maxw)), min(w, cx + round(maxw) + 1)): g[bottom - 1][x] = 'g'
    for y in range(h):
        for x in range(w):
            if g[y][x] == 'G' and rnd.random() < 0.055: g[y][x] = 'L'
    for y in range(h - trunk, h):
        for x in range(cx - 2, cx + 3): g[y][x] = 'T'
    for (dy, half) in ((0, 0), (1, 1), (2, 2), (3, 1), (4, 0)):
        for x in range(cx - half, cx + half + 1): g[dy][x] = 'Y'
    return [''.join(r) for r in g]

class Svg:
    """Calque sans taille propre : il s'étire à la fenêtre, chaque élément s'accroche à un bord."""
    def __init__(s, pack, P, pal, spr, stars=None):
        s.pack, s.P, s.pal, s.spr = pack, P, pal, spr; s.stars_c = stars or ['#fcfcfc']; s.defs = ''; s.o = []
    def blink(s, d=None):
        d = d or random.uniform(0.6, 1.6)
        return f'<animate attributeName="opacity" values="1;0.15" calcMode="discrete" dur="{d:.1f}s" begin="-{random.uniform(0,2):.1f}s" repeatCount="indefinite"/>'
    def rect(s, x, y, w, h, c, anim=''):
        P = s.P; r = f'<rect x="{x*P:g}" y="{y*P:g}" width="{w*P:g}" height="{h*P:g}" fill="{c}"'
        return r + (f'>{anim}</rect>' if anim else '/>')
    def twinkle(s, inner, lo=(0.05, 0.2), dur=(1.6, 3.6)):
        d = random.uniform(*dur)
        return f'<g>{inner}<animate attributeName="opacity" values="1;{random.uniform(*lo):.2f};1" dur="{d:.1f}s" begin="-{random.uniform(0, d):.1f}s" repeatCount="indefinite"/></g>'
    def sprite(s, name, x, y, col=None, scale=1):
        out = []
        for j, row in enumerate(s.spr[name]):
            i = 0
            while i < len(row):
                ch = row[i]
                if ch == '.': i += 1; continue
                if ch in 'LN':
                    c = random.choice(N.LIGHTS) if ch == 'L' else s.pal['N']
                    out.append(s.rect(x+i*scale, y+j*scale, scale, scale, c, s.blink(None if ch == 'L' else 0.8))); i += 1; continue
                k = i
                while k < len(row) and row[k] == ch: k += 1
                c = col[0] if ch == 'X' else col[1] if ch == 'x' else s.pal[ch]
                out.append(s.rect(x+i*scale, y+j*scale, (k-i)*scale, scale, c)); i = k
        return ''.join(out)
    def size(s, name, scale=1):
        rows = s.spr[name]; return len(rows[0]) * scale * s.P, len(rows) * scale * s.P
    def add(s, xml): s.o.append(xml)
    def pin(s, inner, w, h, corner, mx=0, my=0):
        ax = '0' if corner[1] == 'l' else '100%'; ay = '0' if corner[0] == 't' else '100%'
        tx = mx if corner[1] == 'l' else -(w + mx); ty = my if corner[0] == 't' else -(h + my)
        s.o.append(f'<svg x="{ax}" y="{ay}" overflow="visible"><g transform="translate({tx:g},{ty:g})">{inner}</g></svg>')
    def pin_sprites(s, items, corner, mx, my):
        """items = [(nom, x, y, couleurs, échelle)] en unités."""
        inner = ''.join(s.sprite(n, x, y, c, sc) for n, x, y, c, sc in items)
        w = max(x * s.P + s.size(n, sc)[0] for n, x, y, c, sc in items); h = max(y * s.P + s.size(n, sc)[1] for n, x, y, c, sc in items)
        s.pin(inner, w, h, corner, mx, my)
    def bank(s, cols, base, amp, seed, c='#fcfcfc'):
        random.seed(seed); a, b, ph = random.uniform(.05, .12), random.uniform(.02, .05), random.uniform(0, 6)
        hs = [max(1, round(base + amp * (math.sin(i*a+ph) + math.sin(i*b)) / 2)) for i in range(cols)]
        out, i = [], 0
        while i < cols:
            k = i
            while k < cols and hs[k] == hs[i]: k += 1
            out.append(s.rect(i, -hs[i], k-i, hs[i], c)); i = k
        s.o.append(f'<svg x="0" y="100%" overflow="visible">{"".join(out)}</svg>')
    def stars(s, n, px, y0=0, y1=100):
        for _ in range(n):
            x, y = random.uniform(0.5, 99), random.uniform(y0, y1)
            s.o.append(s.twinkle(f'<rect x="{x:.1f}%" y="{y:.1f}%" width="{px}" height="{px}" fill="{random.choice(s.stars_c)}"/>'))
    def flakes(s, n, px, dur=(16, 30), colors=None, sway=7, wide=0):
        K = 14; colors = colors or ['#fcfcfc']
        for _ in range(n):
            x = random.uniform(0, 100); d = random.uniform(*dur); b = -random.uniform(0, d)
            amp = random.uniform(2, sway) * s.P; ph = random.uniform(0, 6.28); sw = random.uniform(0.5, 1.1)
            vals = ';'.join(f'{amp*math.sin(ph + k*sw):.1f},0' for k in range(K + 1))
            col = random.choice(colors)
            s.o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                       f'<rect x="{x:.1f}%" y="-5%" width="{px + wide}" height="{px}" fill="{col}"><animate attributeName="y" values="-5%;105%" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></rect></g>')
    def slider(s, name, bottom_px, dur, begin, lo=-8, hi=110, step=1.6, idle=40):
        xs = ';'.join(f'{lo + k*step:.1f}%' for k in range(int((hi - lo) / step) + 1)) + ';' + ';'.join([f'{hi}%'] * idle)
        w, h = s.size(name)
        s.add(f'<svg y="100%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
              f'<g transform="translate(0,{-(h + bottom_px):g})">{s.sprite(name, 0, 0)}</g></svg>')
    def save(s, name):
        d = f'{ROOT}/{s.pack}'; os.makedirs(d, exist_ok=True)
        open(f'{d}/{name}.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">' + (f'<defs>{s.defs}</defs>' if s.defs else '') + ''.join(s.o) + '</svg>')

def aurora(s, width_px=4400, col=8, top_h=(110, 280)):
    s.defs += ''.join(f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="0.95"/><stop offset="0.55" stop-color="{c}" stop-opacity="0.35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>'
                      for i, c in (('ag', '#58f898'), ('ac', '#3cbcfc'), ('av', '#c878f8')))
    out = []
    for i in range(width_px // col):
        h = (top_h[0] + top_h[1]) / 2 + (top_h[1] - top_h[0]) / 2 * (0.6 * math.sin(i * 0.12) + 0.4 * math.sin(i * 0.04 + 2))
        h = round(h / col) * col
        gid = ('ag', 'ac', 'av')[int((math.sin(i * 0.03) + 1) * 1.49)]
        d = 7 + 2 * math.sin(i * 0.3); ph = (i * 0.08) % d
        out.append(f'<rect x="{i*col}" y="0" width="{col}" height="{h}" fill="url(#{gid})" opacity="0.1"><animate attributeName="opacity" values="0.08;0.55;0.08" dur="{d:.1f}s" begin="-{ph:.2f}s" repeatCount="indefinite"/></rect>')
    s.o.append('<svg x="0" y="0" overflow="visible">' + ''.join(out) + '</svg>')

GIFTC = [('#d82800','#881400'), ('#00a800','#005800'), ('#3cbcfc','#0058f8'), ('#f878f8','#a800a8'), ('#f8b800','#ac7c00')]

# =====================================  PÔLE NORD  =====================================
SP = dict(POLE_SPR); SP['igloo'] = make_igloo(28, 14); SP['igloo_l'] = make_igloo(36, 18); SP['igloo_xl'] = make_igloo(42, 21)
STARS = ['#fcfcfc', '#fcfcfc', '#a4e4fc', '#58f898']
def pole(P): return Svg('polenord', P, POLE_PAL, SP, STARS)

random.seed(11); s = pole(3)                                  # plein écran
aurora(s); s.bank(1500, 4, 1, 21, '#eaf6ff'); s.bank(1500, 2, 1, 22, '#fcfcfc')
s.slider('slider', 3, 38, 0, step=1.4); s.flakes(45, 3, dur=(14, 28)); s.save('fullscreen')

random.seed(12); s = pole(3)                                  # éditeur
s.stars(110, 4)
s.pin_sprites([('bear', 0, 7, None, 1), ('igloo_l', 22, 0, None, 1), ('penguin', 62, 6, None, 1)], 'br', 18, 24); s.save('editor')

random.seed(13); s = pole(4)                                  # terminal
s.stars(26, 4, 2, 62); s.bank(1100, 3, 1, 23, '#eaf6ff'); s.bank(1100, 2, 1, 24, '#fcfcfc')
s.slider('slider', 3, 30, 0, step=1.5); s.slider('slider', 3, 30, -17, step=1.5)
s.pin_sprites([('seal', 0, 0, None, 1)], 'br', 36, 10); s.flakes(20, 4, dur=(8, 16)); s.save('panel')

random.seed(14); s = pole(4)                                  # explorateur
s.stars(14, 4, 0, 96); s.flakes(55, 3, dur=(10, 20))
s.pin_sprites([('igloo_xl', 0, 2, None, 1), ('penguin', 44, 4, None, 1), ('penguin', 54, 6, None, 1)], 'bl', 12, 26); s.save('sidebar')

random.seed(15); s = pole(4)                                  # barre de droite
for xp, n in [(8, 'iciM'), (19, 'iciS'), (31, 'iciL'), (43, 'iciS'), (55, 'iciM'), (66, 'iciL'), (78, 'iciS'), (90, 'iciM')]:
    s.add(f'<svg x="{xp}%" y="0" overflow="visible">' + s.twinkle(s.sprite(n, 0, 0), lo=(0.4, 0.7), dur=(2.5, 5)) + '</svg>')
s.save('aux')

# =====================================  NOËL  =====================================
NS = dict(N.SPR); NS['tree_xl'] = make_tree(41, 60)
NSTARS = ['#fcfcfc', '#fcfcfc', '#f8b800', '#f8b800']
def noel(P): return Svg('noel', P, N.PAL, NS, NSTARS)

random.seed(1); s = noel(3)                                   # plein écran
g = []
for i in range(1500):
    u = (i % 100) / 100; y = round(4*u*(1-u)*6); g.append(s.rect(i, y, 1, 1, '#00a800'))
    if i % 25 == 12: g.append(s.rect(i, y+1, 2, 2, random.choice(N.LIGHTS), s.blink(random.uniform(1.2, 2.2))))
s.add('<svg x="0" y="0" overflow="visible">' + ''.join(g) + '</svg>')
s.bank(1500, 3, 1, 3)
santa = s.sprite('sleigh', 0, 0) + s.rect(16, 6, 3, 1, '#f8b800') + s.sprite('reindeer', 19, 2)
xs = ';'.join(f'{x:.1f}%' for x in [-6 + k * 1.2 for k in range(0, 100)]) + ';' + ';'.join(['110%'] * 60)
s.add(f'<svg y="14%" overflow="visible"><animate attributeName="x" values="{xs}" calcMode="discrete" dur="45s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-3" calcMode="discrete" dur="1.2s" repeatCount="indefinite"/>{santa}</g></svg>')
s.flakes(45, 3, dur=(14, 28)); s.save('fullscreen')

random.seed(2); s = noel(3)                                   # éditeur
s.stars(110, 4)
s.pin_sprites([('tree', 0, 0, None, 1), ('tree', 12, 3, None, 1), ('tree', 24, 1, None, 1)], 'br', 16, 22); s.save('editor')

random.seed(3); s = noel(4)                                   # terminal
s.stars(26, 4, 2, 62); s.bank(1100, 3, 1, 9)
s.pin_sprites([('snowman', 0, 0, None, 1)], 'bl', 140, 8)
s.pin_sprites([('tree', 0, 0, None, 1), ('tree', 10, 2, None, 1), ('gift', 22, 7, GIFTC[0], 1), ('gift', 31, 8, GIFTC[1], 1)], 'br', 24, 8)
s.flakes(20, 4, dur=(8, 16)); s.save('panel')

random.seed(4); s = noel(4)                                   # explorateur : grand sapin + pile de petits cadeaux
s.stars(14, 4, 0, 96); s.flakes(55, 3, dur=(10, 20))
tree = s.sprite('tree_xl', 0, 0)                              # 164 x 240 px
P0 = s.P; s.P = 3
rows = [(16, [0, 9, 18, 27]), (8, [4, 13, 22]), (0, [9, 18])]
gifts = ''.join(s.sprite('gift', x, y, GIFTC[(i + j) % 5]) for j, (y, xs_) in enumerate(rows) for i, x in enumerate(xs_))
s.P = P0
s.pin(tree + f'<g transform="translate(30,168)">{gifts}</g>', 164, 240, 'bl', 24, 24); s.save('sidebar')

random.seed(5); s = noel(4)                                   # barre de droite : boules
for i, (xp, L) in enumerate([(22, 12), (52, 27), (80, 8)]):
    gg = s.rect(2, 0, 1, L, '#7c7c7c') + s.sprite('bauble', 0, L, GIFTC[i])
    s.add(f'<svg x="{xp}%" y="0" overflow="visible"><g><animateTransform attributeName="transform" type="translate" values="0,0;4,0;0,0;-4,0" calcMode="discrete" dur="{2.5+i*0.4:.1f}s" repeatCount="indefinite"/>{gg}</g></svg>')
s.save('aux')
print('décors générés (Noël + Pôle Nord)')
