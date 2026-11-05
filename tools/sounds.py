# Sons faits maison (synthétisés), donc libres de droits : « Ho ho ho » grave et cri de pingouin 8 bits.
import wave, struct, math, random, os
SR = 22050
def save(name, samples):
    peak = max(abs(x) for x in samples) or 1
    with wave.open(os.path.expanduser(f'~/pixel-worlds/sounds/{name}.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(x / peak * 0.8 * 32767)) for x in samples))

def ho(f0, dur):
    """Un « Hô » grave : harmoniques façonnées par deux formants de la voyelle « o », un peu de souffle au début."""
    n = int(SR * dur); out = []
    for i in range(n):
        t = i / SR; u = t / dur
        f = f0 * (1.0 - 0.12 * u) * (1 + 0.012 * math.sin(2 * math.pi * 5.5 * t))
        env = min(1, t / 0.03) * max(0, 1 - u) ** 0.6
        s = 0.0
        for k in range(1, 28):
            fk = f * k
            if fk > 3500: break
            a = math.exp(-((fk - 480) / 160) ** 2) + 0.6 * math.exp(-((fk - 850) / 220) ** 2) + 0.03
            s += a * math.sin(2 * math.pi * f * k * t + k)
        s *= env
        if t < 0.05: s += (random.random() * 2 - 1) * 0.5 * (1 - t / 0.05)  # le « h »
        out.append(s)
    return out
def gap(d): return [0.0] * int(SR * d)
noel = []
for f0, d in ((118, 0.30), (112, 0.30), (100, 0.42)):
    noel += ho(f0, d) + gap(0.09)
save('noel-fail', noel)

def squawk(dur, f_start, f_end, duty):
    n = int(SR * dur); out = []; ph = 0.0
    for i in range(n):
        t = i / SR; u = t / dur
        f = f_start + (f_end - f_start) * u + 55 * math.sin(2 * math.pi * 38 * t)   # vibrato rapide
        ph = (ph + f / SR) % 1.0
        sq = 1.0 if ph < duty else -1.0                                                 # onde carrée 8 bits
        env = min(1, t / 0.01) * (1 - u) ** 0.5
        out.append((sq * 0.7 + (random.random() * 2 - 1) * 0.25) * env)
    return out
peng = []
for a, b, d in ((880, 520, 0.16), (940, 480, 0.18), (780, 380, 0.26)):
    peng += squawk(d, a, b, random.choice([0.35, 0.5])) + gap(0.07)
save('../tools/polenord-fail-synth', peng)  # version de secours ; le vrai cri (extrait de gentoo-penguin.mp3) reste dans sounds/

def pluck(freq, dur, decay=0.996):
    """Corde pincée (algorithme de Karplus-Strong) : un son de koto."""
    n = int(SR * dur); N = max(2, int(SR / freq)); buf = [random.random() * 2 - 1 for _ in range(N)]; out = []
    for i in range(n):
        v = buf[i % N]; out.append(v)
        buf[i % N] = (v + buf[(i + 1) % N]) * 0.5 * decay
    return out
def gong(freq, dur):
    n = int(SR * dur)
    return [sum(a * math.sin(2 * math.pi * freq * m * i / SR) for m, a in ((1, 1), (2.01, 0.5), (2.76, 0.35), (4.1, 0.2))) * math.exp(-i / SR * 3.2) * min(1, i / (SR * 0.004)) for i in range(n)]
koto = []
for f in (659.3, 587.3, 493.9):          # trois notes qui descendent (gamme pentatonique)
    koto += [x * 0.9 for x in pluck(f, 0.34)] + gap(0.02)
koto += [x * 0.7 for x in gong(110, 0.9)]
save('sakura-fail', koto)

def square(freq, dur, duty=0.5, bits=5):
    n = int(SR * dur); out = []; ph = 0.0
    for i in range(n):
        ph = (ph + freq / SR) % 1.0
        v = 1.0 if ph < duty else -1.0
        env = min(1, i / (SR * 0.004)) * max(0, 1 - i / n) ** 0.4
        q = 2 ** bits; out.append(round(v * env * q) / q)             # on écrase la résolution : son 8 bits
    return out
def glitch(dur):
    n = int(SR * dur); out = []; hold = 0.0
    for i in range(n):
        if i % random.randint(20, 90) == 0: hold = random.random() * 2 - 1
        out.append(hold * (1 - i / n) * 0.8)
    return out
neon = square(640, 0.11, 0.5) + gap(0.03) + square(470, 0.11, 0.5) + gap(0.03) + square(300, 0.28, 0.25) + glitch(0.22)
save('neon-fail', neon)

alarm = []
for i in range(4):
    alarm += square(880 if i % 2 == 0 else 620, 0.11, 0.5, 6) + gap(0.02)
alarm += square(220, 0.35, 0.5, 4) + glitch(0.18)
save('space-fail', alarm)

def roar(dur=1.0):
    n = int(SR * dur); out = []; ph = 0.0
    for i in range(n):
        u = i / n; f = 120 - 70 * u + 12 * math.sin(2 * math.pi * 24 * i / SR)         # grave qui descend, avec un grondement
        ph = (ph + f / SR) % 1.0
        saw = 2 * ph - 1
        env = min(1, i / (SR * 0.03)) * (1 - u) ** 0.8
        out.append((saw * 0.75 + (random.random() * 2 - 1) * 0.45 * (1 - u)) * env * (0.6 + 0.4 * math.sin(2 * math.pi * 30 * i / SR)))
    return out
save('fantasy-fail', roar(1.05) + [x * 0.8 for x in glitch(0.12)])

def ping(freq, dur, amp=1.0):
    n = int(SR * dur)
    return [amp * math.sin(2 * math.pi * freq * i / SR) * math.exp(-i / SR * 7.5) * min(1, i / (SR * 0.004)) for i in range(n)]
def blop(f0, f1, dur):
    n = int(SR * dur); out = []; ph = 0.0
    for i in range(n):
        u = i / n; ph += 2 * math.pi * (f0 + (f1 - f0) * u) / SR
        out.append(math.sin(ph) * (1 - u) * 0.6)
    return out
sonar = ping(1180, 0.5) + [0.0] * int(SR * 0.04)
echo = [x * 0.45 for x in ping(1120, 0.5)]
mix = sonar + echo + [0.0] * int(SR * 0.02) + blop(300, 700, 0.08) + gap(0.03) + blop(260, 640, 0.08)
save('ocean-fail', mix)

def gunshot():
    n = int(SR * 0.9); out = [0.0] * n
    for i in range(n):
        t_ = i / SR
        noise = (random.random() * 2 - 1) * math.exp(-t_ * 22)                       # le « bang »
        thump = math.sin(2 * math.pi * 88 * t_) * math.exp(-t_ * 9) * 0.9              # le choc grave
        out[i] = noise * 0.9 + thump
    m = int(SR * 0.5); ph = 0.0
    for i in range(m):                                                                  # le ricochet : un sifflement qui descend
        u = i / m; ph += 2 * math.pi * (2600 - 1700 * u) / SR
        j = i + int(SR * 0.12)
        if j < n: out[j] += math.sin(ph) * (1 - u) ** 1.5 * 0.22
    for i in range(int(SR * 0.28), n):                                                  # l'écho dans le canyon
        out[i] += out[i - int(SR * 0.28)] * 0.28
    return out
save('west-fail', gunshot())
print('sons créés')
