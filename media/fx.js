/* Pixel Worlds — animations de compilation 8 bits (injectées dans VS Code).
   L'extension fait apparaître un instant un élément « PXFX:<nom> » dans la barre d'état ; on le détecte ici. */
(function () {
  if (window.__pxwFx) return; window.__pxwFx = true;
  var P = 4, running = false; // taille d'un « pixel » de l'animation

  function stage(draw, total) {
    if (running) return; running = true;
    var cv = document.createElement('canvas');
    var w = Math.ceil(innerWidth / P), h = Math.ceil(innerHeight / P);
    cv.width = w; cv.height = h;
    cv.style.cssText = 'position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:2147483647;pointer-events:none;image-rendering:pixelated;';
    document.body.appendChild(cv);
    var g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
    var t0 = performance.now(), last = -1, step = 1000 / 24, st = {};
    function px(x, y, c, s) { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), s || 1, s || 1); }
    (function frame(now) {
      var t = now - t0, f = Math.floor(t / step);
      if (f !== last) { last = f; g.clearRect(0, 0, w, h); draw(g, px, w, h, t, f, st); } // 24 images par seconde : effet « jeu d'époque »
      if (t < total) requestAnimationFrame(frame); else { cv.remove(); running = false; }
    })(performance.now());
  }

  // ---------- Noël : étoile filante qui explose ----------
  var PAL = ['#fcfcfc', '#f8b800', '#f87800', '#f83800', '#3cbcfc', '#f878f8', '#58f898'];
  function star() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = 1, sy = h - 2, ex = w - 2, ey = 1, EXPL = 0.70, TRAVEL = 1500;
      S.trail = S.trail || []; S.parts = S.parts || []; S.rays = S.rays || [];
      var p = Math.min(t / TRAVEL, 1) * EXPL, x = sx + (ex - sx) * p, y = sy + (ey - sy) * p, i;
      if (!S.boom) {
        S.trail.push({ x: x, y: y, a: 1 });
        if (t >= TRAVEL) {
          S.boom = { x: x, y: y, t: t };
          for (i = 0; i < 130; i++) { var a = Math.random() * 6.283, sp = (0.4 + Math.random() * 1.8) * 1.5; S.parts.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp * 0.9, life: 1, c: PAL[(Math.random() * PAL.length) | 0], s: Math.random() < 0.25 ? 2 : 1 }); }
          for (i = 0; i < 8; i++) S.rays.push({ a: i * Math.PI / 4, r: 0 });
        }
      }
      for (i = S.trail.length - 1; i >= 0; i--) {
        var q = S.trail[i]; q.a -= 0.035; if (q.a <= 0) { S.trail.splice(i, 1); continue; }
        px(q.x, q.y, q.a > 0.7 ? '#fcfcfc' : q.a > 0.45 ? '#f8b800' : q.a > 0.2 ? '#f87800' : '#f83800', q.a > 0.6 ? 2 : 1);
      }
      if (!S.boom) { px(x - 1, y - 1, '#f8b800', 3); px(x, y, '#fcfcfc', 1); px(x - 2, y, '#fcfcfc'); px(x + 2, y, '#fcfcfc'); px(x, y - 2, '#fcfcfc'); px(x, y + 2, '#fcfcfc'); return; }
      var e = S.boom, age = t - e.t;
      if (age < 120) { var r = 8 + age / 8; for (var yy = -r; yy <= r; yy++) for (var xx = -r; xx <= r; xx++) if (xx * xx + yy * yy <= r * r) px(e.x + xx, e.y + yy, age < 60 ? '#fcfcfc' : '#f8b800'); }
      S.rays.forEach(function (r) { r.r += 2.4; if (age > 700) return; for (var k = 6; k < r.r; k += 2) px(e.x + Math.cos(r.a) * k, e.y + Math.sin(r.a) * k, k % 4 ? '#f8b800' : '#fcfcfc'); });
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy += 0.05; q.vx *= 0.985; q.life -= 0.018; if (q.life > 0 && (q.life > 0.3 || f % 2 === 0)) px(q.x, q.y, q.life > 0.6 ? q.c : '#f83800', q.s); });
    }, 3400);
  }

  // ---------- Pôle Nord : une boule de neige est lancée depuis le coin en bas à gauche et explose en neige ----------
  var SNOW = ['#fcfcfc', '#fcfcfc', '#d8ecff', '#a4e4fc', '#88b8f0'];
  function snowball() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = 2, sy = h - 3, ex = w - 2, ey = 2, EXPL = 0.70, TRAVEL = 1500, R = 4, i;
      S.trail = S.trail || []; S.parts = S.parts || []; S.flakes = S.flakes || [];
      var p = Math.min(t / TRAVEL, 1) * EXPL, u = p / EXPL;
      var x = sx + (ex - sx) * p, y = sy + (ey - sy) * p - 24 * Math.sin(Math.PI * u); // un lancer en arc
      if (!S.boom) {
        S.trail.push({ x: x + (Math.random() - 0.5) * 2, y: y + (Math.random() - 0.5) * 2, a: 1 });
        if (t >= TRAVEL) {
          S.boom = { x: x, y: y, t: t };
          for (i = 0; i < 150; i++) { var a = Math.random() * 6.283, sp = (0.5 + Math.random() * 1.9) * 1.5; S.parts.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp * 0.9 - 0.4, life: 1, c: SNOW[(Math.random() * SNOW.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
          for (i = 0; i < 20; i++) S.flakes.push({ x: x + (Math.random() - 0.5) * 8, y: y + (Math.random() - 0.5) * 8, vx: (Math.random() - 0.5) * 1.1, vy: -0.9 + Math.random() * 0.9, life: 1 });
        }
      }
      // traînée de petits flocons
      for (i = S.trail.length - 1; i >= 0; i--) {
        var q = S.trail[i]; q.a -= 0.05; if (q.a <= 0) { S.trail.splice(i, 1); continue; }
        px(q.x, q.y, q.a > 0.66 ? '#fcfcfc' : q.a > 0.33 ? '#a4e4fc' : '#88b8f0', q.a > 0.5 ? 2 : 1);
      }
      if (!S.boom) { // la boule : blanche, ombrée en bas à droite, avec quelques « grumeaux » qui tournent
        for (var dy = -R; dy <= R; dy++) for (var dx = -R; dx <= R; dx++) {
          var d = Math.sqrt(dx * dx + dy * dy); if (d > R + 0.3) continue;
          var sh = (dx * 0.6 + dy * 0.8) / R, c = d > R - 0.8 ? '#88b8f0' : sh > 0.5 ? '#a4e4fc' : sh > 0.15 ? '#d8ecff' : '#fcfcfc';
          px(x + dx, y + dy, c);
        }
        for (i = 0; i < 3; i++) { var ang = t * 0.012 + i * 2.1; px(x + Math.cos(ang) * R * 0.55, y + Math.sin(ang) * R * 0.55, '#88b8f0'); }
        return;
      }
      var e = S.boom, age = t - e.t, k;
      if (age < 160) { var r = 8 + age / 7; for (var yy = -r; yy <= r; yy++) for (var xx = -r; xx <= r; xx++) if (xx * xx + yy * yy <= r * r) px(e.x + xx, e.y + yy, age < 70 ? '#fcfcfc' : '#a4e4fc'); } // éclat blanc
      if (age < 700) { var rr = age / 18; for (k = 0; k < 44; k++) { var an = k / 44 * 6.283; px(e.x + Math.cos(an) * rr, e.y + Math.sin(an) * rr * 0.9, k % 2 ? '#fcfcfc' : '#88b8f0'); } } // onde de choc
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy += 0.05; q.vx *= 0.985; q.life -= 0.016; if (q.life > 0 && (q.life > 0.3 || f % 2 === 0)) px(q.x, q.y, q.life > 0.5 ? q.c : '#88b8f0', q.s); });
      S.flakes.forEach(function (q) { // grands flocons en croix qui retombent doucement
        q.x += q.vx; q.y += q.vy; q.vy += 0.012; q.vx *= 0.99; q.life -= 0.007;
        if (q.life > 0 && (q.life > 0.3 || f % 2 === 0)) { px(q.x, q.y, '#fcfcfc'); px(q.x - 1, q.y, '#d8ecff'); px(q.x + 1, q.y, '#d8ecff'); px(q.x, q.y - 1, '#d8ecff'); px(q.x, q.y + 1, '#d8ecff'); }
      });
    }, 3600);
  }

  // ---------- Sakura : feu d'artifice (hanabi) qui éclate en pétales ----------
  var HPAL = [['#ffb7d5', '#ff8fbf', '#fff0f6'], ['#f8b800', '#ffe08a', '#fcfcfc'], ['#c9b6ff', '#9be8d0', '#fff0f6']];
  function hanabi() {
    stage(function (g, px, w, h, t, f, S) {
      if (!S.rockets) {
        S.rockets = [{ x: 0.30, y: 0.30, l: 0, b: 900, p: 0, n: 100 }, { x: 0.70, y: 0.22, l: 450, b: 1350, p: 1, n: 100 }, { x: 0.50, y: 0.42, l: 1000, b: 1750, p: 2, n: 70 }];
        S.parts = []; S.trail = []; S.petals = [];
      }
      var i;
      S.rockets.forEach(function (r) {
        if (t < r.l) return;
        var ty = Math.round(h * r.y), sx0 = Math.round(w * r.x);
        if (t < r.b) {
          var u = (t - r.l) / (r.b - r.l), e = u * (2 - u), x = sx0 + Math.sin(u * 7) * 1.2, y = (h - 2) - ((h - 2) - ty) * e;
          S.trail.push({ x: x, y: y, a: 1 }); px(x, y, '#fff0f6', 2);
        } else if (!r.done) {
          r.done = true;
          for (i = 0; i < r.n; i++) { var a = Math.random() * 6.283, sp = (0.6 + Math.random() * 1.7) * 1.4, pal = HPAL[r.p];
            S.parts.push({ x: sx0, y: ty, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, c: pal[(Math.random() * pal.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
          for (i = 0; i < 10; i++) S.petals.push({ x: sx0 + (Math.random() - 0.5) * 14, y: ty + (Math.random() - 0.5) * 10, ph: Math.random() * 6, vy: 0.25 + Math.random() * 0.25, life: 1 });
        }
      });
      for (i = S.trail.length - 1; i >= 0; i--) { var q = S.trail[i]; q.a -= 0.07; if (q.a <= 0) { S.trail.splice(i, 1); continue; } px(q.x, q.y, q.a > 0.6 ? '#ffe08a' : q.a > 0.3 ? '#f8b800' : '#d6578a'); }
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.955; q.vy = q.vy * 0.955 + 0.035; q.life -= 0.014;
        if (q.life > 0 && (q.life > 0.35 || f % 2 === 0)) px(q.x, q.y, q.life > 0.55 ? q.c : '#d6578a', q.s); });
      if (t > 1100 && t < 3200 && f % 2 === 0) for (i = 0; i < 2; i++) S.petals.push({ x: Math.random() * w, y: -2, ph: Math.random() * 6, vy: 0.3 + Math.random() * 0.3, life: 1 });
      S.petals.forEach(function (q) { q.y += q.vy; q.ph += 0.12; q.x += Math.sin(q.ph) * 0.45; q.life -= 0.004;
        if (q.life > 0 && q.y < h) { px(q.x, q.y, '#ffb7d5', 2); px(q.x + 1, q.y + 1, '#fff0f6'); } });
    }, 3900);
  }

  // ---------- Néon City : une voiture volante traverse l'écran du coin bas gauche vers le coin haut droit, puis explose ----------
  var CAR = ['.......KKKKK........', '......KCCCCCK.......', '..KmmmmmmmmmmmmmmK..', '.KmmmMMMMMMMMmmmmmmA', '..KKKKKKKKKKKKKKKK..', '...cc........cc.....', '...CC........CC.....'];
  var CC = { K: '#0b0818', C: '#7ff3ff', m: '#ff2a9d', M: '#ff77c5', A: '#ffd66b', c: '#00e5ff' };
  var SPARK = ['#ff2a9d', '#00e5ff', '#ffb020', '#fcfcfc', '#ff77c5', '#7ff3ff'];
  function hovercar() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = -8, sy = h - 6, ex = w - 10, ey = 3, EXPL = 0.70, TRAVEL = 1500, i, r, c;
      S.trail = S.trail || []; S.parts = S.parts || []; S.chunks = S.chunks || [];
      var p = Math.min(t / TRAVEL, 1) * EXPL, x = sx + (ex - sx) * p, y = sy + (ey - sy) * p + Math.sin(t * 0.02) * 0.7;
      if (!S.boom) {
        S.trail.push({ x: x, y: y + 3, a: 1 });
        if (t >= TRAVEL) {
          S.boom = { x: x + 10, y: y + 3, t: t };
          for (i = 0; i < 170; i++) { var an = Math.random() * 6.283, sp = (0.5 + Math.random() * 2.1) * 1.5; S.parts.push({ x: x + 10, y: y + 3, vx: Math.cos(an) * sp, vy: Math.sin(an) * sp * 0.9 - 0.3, life: 1, c: SPARK[(Math.random() * SPARK.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
          for (i = 0; i < 9; i++) S.chunks.push({ x: x + 6 + Math.random() * 8, y: y + 2, vx: (Math.random() - 0.5) * 2.4, vy: -1.2 - Math.random() * 1.5, life: 1, c: i % 2 ? '#ff2a9d' : '#0b0818' });
        }
      }
      for (i = S.trail.length - 1; i >= 0; i--) { var q = S.trail[i]; q.a -= 0.04; if (q.a <= 0) { S.trail.splice(i, 1); continue; } px(q.x, q.y, q.a > 0.6 ? '#fcfcfc' : q.a > 0.35 ? '#00e5ff' : '#ff2a9d', 2); }
      if (!S.boom) { for (r = 0; r < CAR.length; r++) for (c = 0; c < CAR[r].length; c++) { var ch = CAR[r][c]; if (ch !== '.') px(x + c, y + r, CC[ch]); } return; }
      var e = S.boom, age = t - e.t;
      if (age < 170) { var rr = 8 + age / 6; for (var yy = -rr; yy <= rr; yy++) for (var xx = -rr; xx <= rr; xx++) if (xx * xx + yy * yy <= rr * rr) px(e.x + xx, e.y + yy, age < 70 ? '#fcfcfc' : age < 120 ? '#ffd66b' : '#ff2a9d'); }
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.975; q.vy += 0.05; q.life -= 0.015; if (q.life > 0 && (q.life > 0.35 || f % 2 === 0)) px(q.x, q.y, q.life > 0.5 ? q.c : '#6c2a8f', q.s); });
      S.chunks.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy += 0.09; q.life -= 0.012; if (q.life > 0 && q.y < h) px(q.x, q.y, q.c, 2); });
    }, 3600);
  }

  // ---------- Espace : une fusée décolle du bas de l'écran, monte au-delà du milieu, puis libère un feu d'artifice d'étoiles ----------
  var ROCKET = ['...R...', '..RRR..', '..WWW..', '.WWBWW.', '.WWWWW.', '.WWWWW.', '.WRRRW.', '.WWWWW.', '.WWWWW.', 'RWWWWWR', 'RR.W.RR', '..GGG..'];
  var RC = { R: '#ff5a3c', W: '#fcfcfc', B: '#4df0ff', G: '#6c7488' };
  var STARC = ['#fcfcfc', '#ffe066', '#4df0ff', '#a56bff', '#ff9a2e', '#ff77c5'];
  function rocket() {
    stage(function (g, px, w, h, t, f, S) {
      var x0 = Math.round(w * 0.58) - 3, i, r, c, ty = Math.round(h * 0.30), T1 = 1700;
      S.smoke = S.smoke || []; S.parts = S.parts || [];
      var u = Math.min(t / T1, 1), y = (h - 14) - ((h - 14) - ty) * (u * u);       // elle accélère
      if (t < T1) {
        for (i = 0; i < 2; i++) S.smoke.push({ x: x0 + 3 + (Math.random() - 0.5) * 3, y: y + 12, a: 1, s: 1 + Math.random() * 2 });
        for (r = 0; r < ROCKET.length; r++) for (c = 0; c < 7; c++) { var ch = ROCKET[r][c]; if (ch !== '.') px(x0 + c, y + r, RC[ch]); }
        var fl = 3 + ((f % 3) | 0) * 2; for (i = 0; i < fl; i++) { px(x0 + 2, y + 12 + i, i < 2 ? '#ffe066' : '#ff9a2e'); px(x0 + 3, y + 12 + i, i < 3 ? '#fcfcfc' : '#ff9a2e'); px(x0 + 4, y + 12 + i, i < 2 ? '#ffe066' : '#ff5a3c'); }
      } else if (!S.boom) {
        S.boom = { x: x0 + 3, y: y + 3, t: t };
        for (i = 0; i < 160; i++) { var a = Math.random() * 6.283, sp = (0.6 + Math.random() * 1.9) * 1.4; S.parts.push({ x: S.boom.x, y: S.boom.y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, c: STARC[(Math.random() * STARC.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
        S.cap = { x: x0, y: y };
      }
      for (i = S.smoke.length - 1; i >= 0; i--) { var q = S.smoke[i]; q.a -= 0.035; q.y += 0.6; if (q.a <= 0) { S.smoke.splice(i, 1); continue; } px(q.x, q.y, q.a > 0.6 ? '#fcfcfc' : q.a > 0.3 ? '#9aa3b8' : '#4a5068', q.s > 2 ? 2 : 1); }
      if (!S.boom) return;
      var e = S.boom, age = t - e.t;
      if (age < 160) { var rr = 7 + age / 7; for (var yy = -rr; yy <= rr; yy++) for (var xx = -rr; xx <= rr; xx++) if (xx * xx + yy * yy <= rr * rr) px(e.x + xx, e.y + yy, age < 70 ? '#fcfcfc' : '#ffe066'); }
      if (age < 800) { var ring = age / 14; for (var k = 0; k < 40; k++) { var an = k / 40 * 6.283; px(e.x + Math.cos(an) * ring, e.y + Math.sin(an) * ring, k % 2 ? '#4df0ff' : '#a56bff'); } }
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.96; q.vy = q.vy * 0.96 + 0.025; q.life -= 0.013;
        if (q.life > 0 && (q.life > 0.35 || f % 2 === 0)) { px(q.x, q.y, q.life > 0.5 ? q.c : '#6b3fd0', q.s); if (q.s === 2 && q.life > 0.6) { px(q.x - 1, q.y, q.c); px(q.x + 2, q.y, q.c); } } });
      if (S.cap && S.cap.y > -14) { S.cap.y -= 1.2 + age / 400; for (r = 0; r < 7; r++) for (c = 0; c < 7; c++) { var ch2 = ROCKET[r][c]; if (ch2 !== '.') px(S.cap.x + c, S.cap.y + r, RC[ch2]); } px(S.cap.x + 3, S.cap.y + 7, '#ffe066'); px(S.cap.x + 3, S.cap.y + 8, '#ff9a2e'); }  // la capsule continue vers le haut
    }, 3800);
  }

  // ---------- Fantasy : un dragon monte en diagonale, crache un jet de feu qui explose en boule de feu, puis s'envole ----------
  var DRAGON = [["....pPPPP.................", ".....pPPPPPPPP............", ".....ppPPPPPPP......YY....", "......pPPPPPPPP.....YGGGG.", "......ppPPPPPPP.....GGRGG.", ".......pYPYPYPY.Y..GGGGGGG", "........pGGGGGGG..GGGGGGGG", "......GGGGGGGGGGGGGGG.ggg.", ".....GGGGGGGGGGGGGGG......", "...ggggGGGGGGGGGGGGGG.....", ".ggggggGGGGGGGGGGGGG......", ".ggg.YYYYYYYYYYYYYY.......", ".gg..Y.Y.gGYGYgY.Y........", ".g.......gg...gg..........", "..gY......................", ".........................."], ["..........................", "..........................", "....................YY....", "....................YGGGG.", "....................GGRGG.", "........Y.Y.Y.Y.Y..GGGGGGG", ".........GGGGGGG..GGGGGGGG", "......GGGGGGGGGGGGGGG.ggg.", ".....GGGGGGGGGGGGGGG......", "...ggggGGGGGGGGGGGGGG.....", ".ggggggGGGGGGGGGGGGG......", ".ggg.YYYYYYYYYYYYYY.......", ".gg..YPYPgGYGYgY.Y........", ".g..pPPPPggPPPgg..........", "..gYpPPPPPPPPP............", ".........................."]];
  var DC = { G: '#3ecf6a', g: '#217a42', Y: '#f2c45a', P: '#9a5fe0', p: '#6b3fb0', R: '#ff4d5a' };
  var FIRE = ['#fcfcfc', '#ffd23a', '#ffd23a', '#ff8a1e', '#ff8a1e', '#ff4d5a'];
  function dragon() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = -26, sy = h - 18, ex = w - 30, ey = 2, TOTAL = 3900, i, r, c;
      S.flame = S.flame || []; S.embers = S.embers || [];
      var p = Math.min(t / 3300, 1), x = sx + (ex - sx) * p, y = sy + (ey - sy) * p + Math.sin(t * 0.012) * 1.2;
      var fr = DRAGON[Math.floor(t / 180) % 2];
      for (r = 0; r < fr.length; r++) for (c = 0; c < fr[r].length; c++) { var ch = fr[r][c]; if (ch !== '.' && DC[ch]) px(x + c, y + r, DC[ch]); }
      var mx = x + 25, my = y + 5, dxn = (ex - sx), dyn = (ey - sy), ln = Math.sqrt(dxn * dxn + dyn * dyn), ux = dxn / ln, uy = dyn / ln;
      if (t > 1500 && t < 2250) {                                   // le jet de feu
        for (i = 0; i < 9; i++) { var spd = 1.6 + Math.random() * 1.6, sp = (Math.random() - 0.5) * 0.5;
          S.flame.push({ x: mx, y: my, vx: (ux - uy * sp) * spd, vy: (uy + ux * sp) * spd - 0.05, life: 1, c: FIRE[(Math.random() * FIRE.length) | 0], s: Math.random() < 0.4 ? 2 : 1 }); }
      }
      if (t >= 2250 && !S.boom) {                                    // la boule de feu au bout du jet
        S.boom = { x: mx + ux * 22, y: my + uy * 22, t: t };
        for (i = 0; i < 120; i++) { var a = Math.random() * 6.283, sp2 = (0.5 + Math.random() * 2.0) * 1.4; S.embers.push({ x: S.boom.x, y: S.boom.y, vx: Math.cos(a) * sp2, vy: Math.sin(a) * sp2 - 0.5, life: 1, c: FIRE[(Math.random() * FIRE.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
      }
      S.flame.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy -= 0.01; q.life -= 0.045; if (q.life > 0) px(q.x, q.y, q.life > 0.65 ? q.c : q.life > 0.3 ? '#ff8a1e' : '#c8283c', q.s); });
      if (S.boom) {
        var e = S.boom, age = t - e.t;
        if (age < 200) { var rr = 6 + age / 9; for (var yy = -rr; yy <= rr; yy++) for (var xx = -rr; xx <= rr; xx++) if (xx * xx + yy * yy <= rr * rr) px(e.x + xx, e.y + yy, age < 70 ? '#fcfcfc' : age < 130 ? '#ffd23a' : '#ff8a1e'); }
        S.embers.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.975; q.vy += 0.045; q.life -= 0.013; if (q.life > 0 && (q.life > 0.35 || f % 2 === 0)) px(q.x, q.y, q.life > 0.55 ? q.c : '#7a1f2e', q.s); });
      }
    }, 3900);
  }

  // ---------- Océan : un sous-marin monte en diagonale, tire une torpille qui explose en bulles et fait fuir les poissons ----------
  var SUB = ["............SSS...........", "............S.............", ".........YYYSYy...........", ".........YYYYYy...........", ".......YYYYYYYyYYYY.......", "S...YYYYYYYYYYYYYYYYYY....", "S..YYYYYYYYYYYYYYYYYYYY...", "SSYYYYYYYYYYYYYYYYYYYYYY..", "SYYYYYWCYYYYWCYYYYWCYYYYFF", "SSyyyyCCyyyyCCyyyyCCyyyyF.", "S..yyyyyyyyyyyyyyyyyyyy...", "....yyyyyyyyyyyyyyyyyy....", "...ss..yyyyyyyyyyyy......."];
  var SC = { Y: '#ffd84d', y: '#c8a020', S: '#8a9bb0', s: '#5c6a80', C: '#4df0ff', W: '#fcfcfc', F: '#d8ff6b' };
  var FISHG = ['..XXX..', 'X.XXXX.', 'XXXXKXX', 'X.XXXX.', '..XXX..'];
  function torpedo() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = -28, sy = h - 18, ex = w - 34, ey = 6, i, r, c, dxn = ex - sx, dyn = ey - sy, ln = Math.sqrt(dxn * dxn + dyn * dyn), ux = dxn / ln, uy = dyn / ln;
      S.bub = S.bub || []; S.fish = S.fish || []; S.tr = S.tr || [];
      var p = Math.min(t / 3300, 1), x = sx + dxn * p, y = sy + dyn * p;
      for (r = 0; r < SUB.length; r++) for (c = 0; c < SUB[r].length; c++) { var ch = SUB[r][c]; if (ch !== '.' && SC[ch]) px(x + c, y + r, SC[ch]); }
      if (f % 3 === 0) S.bub.push({ x: x - 1, y: y + 7, vx: -0.3, vy: -0.25, life: 1, big: Math.random() < 0.4 });
      var T0 = 1100, T1 = 1900;
      if (t >= T0 && t < T1) {                                       // la torpille file devant le sous-marin
        var u = (t - T0) / (T1 - T0), p1 = Math.min((T0 / 3300), 1), bx = sx + dxn * p1 + 26, by = sy + dyn * p1 + 8;
        var tx = sx + dxn * 0.74, ty = sy + dyn * 0.74, tpx = bx + (tx - bx) * u, tpy = by + (ty - by) * u;
        S.tp = { x: tpx, y: tpy };
        S.tr.push({ x: tpx, y: tpy, a: 1 });
        px(tpx - 2, tpy, '#8a9bb0', 3); px(tpx - 2, tpy + 1, '#5c6a80', 3); px(tpx + 1, tpy, '#ff4d5a', 2); px(tpx + 1, tpy + 1, '#ff4d5a', 1);
      }
      for (i = S.tr.length - 1; i >= 0; i--) { var q = S.tr[i]; q.a -= 0.05; if (q.a <= 0) { S.tr.splice(i, 1); continue; } px(q.x - 3, q.y, q.a > 0.5 ? '#fcfcfc' : '#4df0ff'); }
      if (t >= T1 && !S.boom && S.tp) {
        S.boom = { x: S.tp.x, y: S.tp.y, t: t };
        for (i = 0; i < 120; i++) { var a = Math.random() * 6.283, sp = (0.4 + Math.random() * 1.8) * 1.3; S.bub.push({ x: S.boom.x, y: S.boom.y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 0.2, life: 1, big: Math.random() < 0.35, burst: true }); }
        for (i = 0; i < 8; i++) { var a2 = Math.random() * 6.283; S.fish.push({ x: S.boom.x, y: S.boom.y, vx: Math.cos(a2) * (1.4 + Math.random()), vy: Math.sin(a2) * (1.0 + Math.random()), life: 1, col: ['#ff8a1e', '#4df0ff', '#ff77c5'][i % 3] }); }
      }
      S.bub.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy -= 0.012; q.vx *= 0.97; if (q.burst) q.vy *= 0.97; q.life -= q.burst ? 0.012 : 0.02;
        if (q.life > 0) { var col = q.life > 0.5 ? '#fcfcfc' : '#4df0ff'; if (q.big) { px(q.x, q.y, col); px(q.x + 2, q.y, col); px(q.x, q.y + 2, col); px(q.x + 2, q.y + 2, col); px(q.x + 1, q.y + 1, '#1d7fa8'); } else px(q.x, q.y, col, 1); } });
      S.fish.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy -= 0.02; q.life -= 0.012; if (q.life > 0) for (var rr = 0; rr < 5; rr++) for (var cc = 0; cc < 7; cc++) { var k = FISHG[rr][cc]; if (k !== '.') px(q.x + (q.vx < 0 ? 6 - cc : cc), q.y + rr, k === 'K' ? '#031018' : q.col); } });
      if (S.boom) {
        var e = S.boom, age = t - e.t;
        if (age < 150) { var r2 = 5 + age / 16; for (var yy = -r2; yy <= r2; yy++) for (var xx = -r2; xx <= r2; xx++) if (xx * xx + yy * yy <= r2 * r2) px(e.x + xx, e.y + yy, age < 70 ? '#fcfcfc' : age < 130 ? '#d8f4ff' : '#4df0ff'); }
        if (age < 900) { var ring = age / 12; for (var k2 = 0; k2 < 48; k2++) { var an = k2 / 48 * 6.283; px(e.x + Math.cos(an) * ring, e.y + Math.sin(an) * ring, k2 % 2 ? '#fcfcfc' : '#4df0ff'); } }
      }
    }, 3900);
  }

  // ---------- Far West : un bâton de dynamite est lancé en arc depuis le coin bas gauche, la mèche crépite, puis tout explose ----------
  var DYN = [[0, -3, '#c8283c'], [0, -2, '#c8283c'], [0, -1, '#c8283c'], [0, 0, '#f2c45a'], [0, 1, '#c8283c'], [0, 2, '#c8283c'], [0, 3, '#c8283c'], [-1, -3, '#8a1a28'], [-1, 0, '#e8c890'], [-1, 3, '#8a1a28'], [1, -3, '#8a1a28'], [1, 0, '#e8c890'], [1, 3, '#8a1a28'], [0, -4, '#14100c'], [0, -5, '#14100c']];
  var BOOM = ['#fcfcfc', '#ffd23a', '#ff8a1e', '#c8581f', '#8a3a14'];
  var HAT = ['..TT..', '.TTTT.', 'TTTTTT', '.tttt.'];
  var HC = { T: '#7a4a22', t: '#4a2a12' };
  function dynamite() {
    stage(function (g, px, w, h, t, f, S) {
      var sx = 3, sy = h - 6, tx = sx + (w - 12 - sx) * 0.70, ty = sy + (4 - sy) * 0.70, TFLY = 1500, i;
      S.sp = S.sp || []; S.dust = S.dust || []; S.parts = S.parts || []; S.deb = S.deb || [];
      if (t < TFLY) {
        var u = t / TFLY, x = sx + (tx - sx) * u, y = sy + (ty - sy) * u - 34 * Math.sin(Math.PI * u), ang = t * 0.012, ca = Math.cos(ang), sa = Math.sin(ang);
        DYN.forEach(function (d) { px(x + d[0] * ca - d[1] * sa, y + d[0] * sa + d[1] * ca, d[2]); });
        var fx0 = x - 5 * sa * -1 + 0, fy0 = y - 5 * ca;                         // le bout de la mèche
        for (i = 0; i < 2; i++) S.sp.push({ x: x + 5 * sa, y: y - 5 * ca, vx: (Math.random() - 0.5) * 0.9, vy: -Math.random() * 0.8, a: 1 });
        px(x + 5 * sa, y - 5 * ca, f % 2 ? '#ffd23a' : '#fcfcfc', 2);
      } else if (!S.boom) {
        S.boom = { x: tx, y: ty, t: t };
        for (i = 0; i < 140; i++) { var a = Math.random() * 6.283, sp = (0.5 + Math.random() * 2.1) * 1.4; S.parts.push({ x: tx, y: ty, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 0.3, life: 1, c: BOOM[(Math.random() * BOOM.length) | 0], s: Math.random() < 0.3 ? 2 : 1 }); }
        for (i = 0; i < 46; i++) S.dust.push({ x: tx + (Math.random() - 0.5) * 10, y: ty + (Math.random() - 0.5) * 6, vx: (Math.random() - 0.5) * 1.6, vy: -0.4 - Math.random() * 0.9, life: 1, s: 2 + (Math.random() < 0.5 ? 1 : 0) });
        for (i = 0; i < 8; i++) S.deb.push({ x: tx, y: ty, vx: (Math.random() - 0.5) * 3, vy: -1.6 - Math.random() * 1.8, life: 1, kind: 'plank' });
        S.hat = { x: tx - 3, y: ty - 2, vx: 0.45, vy: -2.6, life: 1 };
      }
      S.sp.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy += 0.07; q.a -= 0.07; if (q.a > 0) px(q.x, q.y, q.a > 0.5 ? '#ffd23a' : '#ff8a1e'); });
      if (!S.boom) return;
      var e = S.boom, age = t - e.t;
      if (age < 170) { var rr = 6 + age / 10; for (var yy = -rr; yy <= rr; yy++) for (var xx = -rr; xx <= rr; xx++) if (xx * xx + yy * yy <= rr * rr) px(e.x + xx, e.y + yy, age < 60 ? '#fcfcfc' : age < 120 ? '#ffd23a' : '#ff8a1e'); }
      if (age < 700) { var ring = age / 10; for (var k = 0; k < 44; k++) { var an = k / 44 * 6.283; px(e.x + Math.cos(an) * ring, e.y + Math.sin(an) * ring * 0.45, k % 2 ? '#e8c890' : '#c9a870'); } }  // l'onde de poussière
      S.dust.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.985; q.life -= 0.012; if (q.life > 0) px(q.x, q.y, q.life > 0.5 ? '#c9a870' : '#8a6a52', q.s); });
      S.parts.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vx *= 0.975; q.vy += 0.05; q.life -= 0.014; if (q.life > 0 && (q.life > 0.35 || f % 2 === 0)) px(q.x, q.y, q.life > 0.5 ? q.c : '#4a2a12', q.s); });
      S.deb.forEach(function (q) { q.x += q.vx; q.y += q.vy; q.vy += 0.09; q.life -= 0.01; if (q.life > 0 && q.y < h) { px(q.x, q.y, '#8a5a2a', 3); px(q.x, q.y + 1, '#5a3a18', 3); } });
      if (S.hat && S.hat.y < h) {                                     // le chapeau de cowboy est projeté en l'air, puis retombe
        S.hat.x += S.hat.vx; S.hat.y += S.hat.vy; S.hat.vy += 0.1;
        for (var r = 0; r < 4; r++) for (var c = 0; c < 6; c++) { var ch = HAT[r][c]; if (ch !== '.') px(S.hat.x + c, S.hat.y + r, HC[ch]); }
      }
    }, 3900);
  }

  var FX = { star: star, snowball: snowball, hanabi: hanabi, hovercar: hovercar, rocket: rocket, dragon: dragon, torpedo: torpedo, dynamite: dynamite };
  window.__pxwBoom = function (name) { (FX[name] || star)(); };

  var on = false;
  function check() {
    var el = document.querySelector('[aria-label*="PXFX:"]');
    if (el) { if (!on) { on = true; var m = /PXFX:(\w+)/.exec(el.getAttribute('aria-label')); window.__pxwBoom(m && m[1]); } } else on = false;
  }
  new MutationObserver(check).observe(document.body || document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['aria-label'] });
})();
