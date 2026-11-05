const vscode = require('vscode');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFile } = require('child_process');

// Chaque « monde » = des couleurs + 5 décors + une animation de compilation + un son d'erreur.
const WORLDS = {
  noel: { label: '🎄 Noël', detail: 'Sapins, neige, traîneau du Père Noël, étoile filante, « Ho ho ho »', theme: '🎄 Noël (Pixel Worlds)', fx: 'star', sound: 'noel-fail.wav' },
  west: { label: '🤠 Far West', detail: 'Saloon, cactus, mesas, train, cowboy, boule d\'herbe, dynamite qui explose, coup de feu', theme: '🤠 Far West (Pixel Worlds)', fx: 'dynamite', sound: 'west-fail.wav' },
  ocean: { label: '🌊 Océan', detail: 'Sous-marin, méduses lumineuses, poisson-lanterne, épave, bancs de poissons, torpille qui explose en bulles', theme: '🌊 Océan (Pixel Worlds)', fx: 'torpedo', sound: 'ocean-fail.wav' },
  fantasy: { label: '🏰 Fantasy', detail: 'Château, dragon qui survole, chevalier, forêt enchantée, coffre au trésor, dragon qui crache du feu', theme: '🏰 Fantasy (Pixel Worlds)', fx: 'dragon', sound: 'fantasy-fail.wav' },
  space: { label: '🚀 Espace', detail: 'Planète à anneaux, fusée sur son pas de tir, astronaute, satellite, étoiles filantes, lancement de fusée', theme: '🚀 Espace (Pixel Worlds)', fx: 'rocket', sound: 'space-fail.wav' },
  neon: { label: '🌃 Néon City', detail: 'Ville de néons sous la pluie, voitures volantes, enseignes qui grésillent, voiture volante qui explose', theme: '🌃 Néon City (Pixel Worlds)', fx: 'hovercar', sound: 'neon-fail.wav' },
  sakura: { label: '🌸 Sakura', detail: 'Pétales de cerisier, torii, pagode, mont Fuji, koinobori, feu d\'artifice hanabi, koto', theme: '🌸 Sakura (Pixel Worlds)', fx: 'hanabi', sound: 'sakura-fail.wav' },
  polenord: { label: '🐧 Pôle Nord', detail: 'Aurore boréale, igloo, ours polaire, pingouins qui glissent, boule de neige, cri de pingouin', theme: '🐧 Pôle Nord (Pixel Worlds)', fx: 'snowball', sound: 'polenord-fail.wav' },
};
const NONE = { label: '🚫 Aucun', detail: 'Retirer toutes les décorations (le thème de couleurs reste)' };

function svg(ctx, world, layer) {
  const data = fs.readFileSync(path.join(ctx.extensionPath, 'packs', world, layer + '.svg'));
  return 'data:image/svg+xml;base64,' + data.toString('base64');
}
const cfg = () => vscode.workspace.getConfiguration();
const G = vscode.ConfigurationTarget.Global;
const version = (ctx) => ctx.extension.packageJSON.version;

async function setDecor(ctx, id) {
  const c = cfg();
  await c.update('background.enabled', true, G);
  await c.update('background.fullscreen', { images: [svg(ctx, id, 'fullscreen')], opacity: 0.6, size: '100% 100%', position: 'center' }, G);
  await c.update('background.editor', { useFront: false, images: [svg(ctx, id, 'editor')],
    style: { 'background-position': '100% 100%', 'background-size': 'cover', 'background-repeat': 'no-repeat', opacity: 0.55 } }, G);
  await c.update('background.panel', { images: [svg(ctx, id, 'panel')], opacity: 0.5, size: 'cover', position: 'bottom' }, G);
  await c.update('background.sidebar', { images: [svg(ctx, id, 'sidebar')], opacity: 0.6, size: 'cover', position: 'bottom' }, G);
  await c.update('background.auxiliarybar', { images: [svg(ctx, id, 'aux')], opacity: 0.35, size: 'cover', position: 'top' }, G);
  await ctx.globalState.update('pixelWorlds.world', id);
  await ctx.globalState.update('pixelWorlds.version', version(ctx));
}

async function applyWorld(ctx, id) {
  await setDecor(ctx, id);
  await cfg().update('workbench.colorTheme', WORLDS[id].theme, G);
  await applyFx(ctx, false);
  try {
    await vscode.commands.executeCommand('extension.background.install'); // applique les images, puis recharge la fenêtre
  } catch (e) {
    vscode.window.showWarningMessage('Pixel Worlds : lance « Background: Enable and apply the background » puis redémarre VS Code.');
  }
}

async function removeDecor(ctx) {
  for (const k of ['fullscreen', 'editor', 'panel', 'sidebar', 'auxiliarybar']) await cfg().update('background.' + k, undefined, G);
  await ctx.globalState.update('pixelWorlds.world', undefined);
  await unpatchFx();
  try { await vscode.commands.executeCommand('extension.background.disable'); } catch (e) { /* rien */ }
}

async function choose(ctx) {
  const current = ctx.globalState.get('pixelWorlds.world');
  const items = Object.entries(WORLDS).map(([id, w]) => ({ label: w.label, description: id === current ? '✔ actuel' : '', detail: w.detail, id }));
  items.push({ label: NONE.label, detail: NONE.detail, id: null });
  const pick = await vscode.window.showQuickPick(items, { title: 'Pixel Worlds — choisis ton monde', placeHolder: 'Quel monde veux-tu ?', matchOnDetail: true });
  if (!pick) return;
  if (pick.id) await applyWorld(ctx, pick.id); else await removeDecor(ctx);
}

// ---------- Animation de compilation (injectée dans l'interface de VS Code) ----------
const FX_START = '<!-- pxw-fx-start -->';
const FX_END = '<!-- pxw-fx-end -->';
function workbenchHtml() {
  const base = path.join(vscode.env.appRoot, 'out', 'vs', 'code');
  for (const d of ['electron-browser', 'electron-sandbox']) {
    const f = path.join(base, d, 'workbench', 'workbench.html');
    if (fs.existsSync(f)) return f;
  }
  return path.join(base, 'electron-browser', 'workbench', 'workbench.html');
}
// On retire aussi les restes de l'ancienne extension « Noël Pixel » (noel-fx), pour éviter les doublons.
const stripFx = (html) => html.replace(/<!-- (pxw|noel)-fx-start -->[\s\S]*?<!-- (pxw|noel)-fx-end -->\n?/g, '');

// Écrit le fichier ; si le système refuse, on redemande avec les droits administrateur (Mac / Linux).
async function writeHtml(file, content) {
  try { fs.writeFileSync(file, content, 'utf8'); return; } catch (e) {
    if (!['EACCES', 'EPERM', 'EROFS'].includes(e.code)) throw e;
    const tmp = path.join(os.tmpdir(), 'pixel-worlds-workbench.html');
    fs.writeFileSync(tmp, content, 'utf8');
    await new Promise((resolve, reject) => {
      const done = (err) => (err ? reject(new Error(e.code + ' : ' + (err.message || err))) : resolve());
      if (process.platform === 'darwin') {
        const sh = `cp '${tmp}' '${file}'`.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
        execFile('osascript', ['-e', `do shell script "${sh}" with administrator privileges`], done);
      } else if (process.platform === 'linux') {
        execFile('pkexec', ['cp', tmp, file], done);
      } else {
        reject(new Error(e.code + ' : relance VS Code en administrateur'));
      }
    });
  }
}
async function patchFx(ctx) {
  try {
    const file = workbenchHtml();
    const script = fs.readFileSync(path.join(ctx.extensionPath, 'media', 'fx.js'), 'utf8');
    const html = fs.readFileSync(file, 'utf8');
    let out = stripFx(html);
    if (!/script-src\s+'unsafe-inline'/.test(out)) out = out.replace(/(script-src)(\s)/, "$1 'unsafe-inline'$2");
    const i = out.lastIndexOf('</html>');
    out = out.slice(0, i) + FX_START + '<script>' + script + '</script>' + FX_END + '\n' + out.slice(i);
    if (out === html) return { state: 'ok' };
    await writeHtml(file, out);
    return { state: 'patched' };
  } catch (e) { return { state: 'error', error: e.message || String(e) }; }
}
async function unpatchFx() {
  try {
    const file = workbenchHtml();
    const html = fs.readFileSync(file, 'utf8');
    const out = stripFx(html);
    if (out !== html) await writeHtml(file, out);
  } catch (e) { /* rien */ }
}
async function applyFx(ctx, announce) {
  const r = await patchFx(ctx);
  if (r.state === 'patched' && announce) vscode.window.showInformationMessage('🌠 Pixel Worlds : l\'animation de compilation est prête. Quitte complètement VS Code puis rouvre-le pour l\'activer.');
  else if (r.state === 'ok' && announce) vscode.window.showInformationMessage('🌠 Pixel Worlds : l\'animation est déjà en place. Si tu ne la vois pas, redémarre VS Code puis lance « Pixel Worlds: Voir l\'animation de compilation ».');
  else if (r.state === 'error') vscode.window.showWarningMessage('Pixel Worlds : impossible de préparer l\'animation de compilation (' + r.error + '). Les décorations ne sont pas touchées. Lance « Pixel Worlds: Réparer l\'animation de compilation » pour réessayer.');
  return r;
}

let lastFx = 0;
function triggerFx(ctx) {
  const id = ctx.globalState.get('pixelWorlds.world'); if (!id) return;
  const now = Date.now(); if (now - lastFx < 4500) return; lastFx = now;
  // L'interface détecte cet élément dans la barre d'état et lance l'animation du monde choisi.
  const item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 1000);
  item.text = '$(star-full)';
  item.accessibilityInformation = { label: 'PXFX:' + WORLDS[id].fx };
  item.show();
  setTimeout(() => item.dispose(), 1200);
}

// ---------- Son d'erreur (Mac, Windows, Linux) ----------
let lastSound = 0;
function playSound(file) {
  const q = (p) => "'" + p.replace(/'/g, "''") + "'";
  if (process.platform === 'darwin') execFile('afplay', [file], () => {});
  else if (process.platform === 'win32') execFile('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', `(New-Object Media.SoundPlayer ${q(file)}).PlaySync()`], { windowsHide: true }, () => {});
  else {
    const players = [['paplay', [file]], ['aplay', ['-q', file]], ['play', ['-q', file]], ['ffplay', ['-nodisp', '-autoexit', '-loglevel', 'quiet', file]], ['mpv', ['--no-video', '--really-quiet', file]]];
    const next = (i) => { if (i < players.length) execFile(players[i][0], players[i][1], (err) => { if (err && err.code === 'ENOENT') next(i + 1); }); };
    next(0);
  }
}
function errorSound(ctx, force) {
  const id = ctx.globalState.get('pixelWorlds.world'); if (!id) return;
  const now = Date.now(); if (!force && now - lastSound < 3000) return; lastSound = now;
  playSound(path.join(ctx.extensionPath, 'sounds', WORLDS[id].sound));
}

const COMPILE = /(^\s*|[;&|(]\s*|\b(sudo|time)\s+)(make|gcc|g\+\+|clang|clang\+\+|cc|c\+\+|cmake|ninja|tsc|javac|rustc|xcodebuild|mvn|gradle|cargo\s+build|go\s+build|swift\s+build|npm\s+run\s+(build|compile)|yarn\s+build|pnpm\s+build)(\s|$)/;

async function diagnostic(ctx) {
  const r = await patchFx(ctx);
  let present = false;
  try { present = fs.readFileSync(workbenchHtml(), 'utf8').includes('pxw-fx-start'); } catch (e) { /* rien */ }
  const shell = vscode.workspace.getConfiguration('terminal.integrated.shellIntegration').get('enabled', true);
  const bar = vscode.workspace.getConfiguration('workbench.statusBar').get('visible', true);
  const id = ctx.globalState.get('pixelWorlds.world');
  vscode.window.showInformationMessage([
    'Pixel Worlds — diagnostic',
    '• Monde choisi : ' + (id ? WORLDS[id].label : 'aucun'),
    '• Fichier VS Code modifié : ' + (present ? 'oui' : 'non') + (r.state === 'error' ? ' (erreur : ' + r.error + ')' : r.state === 'patched' ? ' (je viens de le faire : redémarre VS Code)' : ''),
    '• Barre d\'état visible : ' + (bar ? 'oui' : 'NON — l\'animation en a besoin'),
    '• Intégration du terminal : ' + (shell ? 'activée' : 'DÉSACTIVÉE — les compilations du terminal ne sont pas détectées'),
    '• Système : ' + process.platform + ' · VS Code ' + vscode.version,
  ].join('\n'), { modal: true });
}

async function activate(ctx) {
  ctx.subscriptions.push(
    vscode.commands.registerCommand('pixelWorlds.choose', () => choose(ctx)),
    vscode.commands.registerCommand('pixelWorlds.disable', () => removeDecor(ctx)),
    vscode.commands.registerCommand('pixelWorlds.testEffect', () => { lastFx = 0; triggerFx(ctx); }),
    vscode.commands.registerCommand('pixelWorlds.testSound', () => errorSound(ctx, true)),
    vscode.commands.registerCommand('pixelWorlds.repair', () => applyFx(ctx, true)),
    vscode.commands.registerCommand('pixelWorlds.diagnostic', () => diagnostic(ctx))
  );
  const on = (k) => vscode.workspace.getConfiguration('pixelWorlds').get(k, true);
  // Compilation réussie → animation
  ctx.subscriptions.push(vscode.tasks.onDidEndTaskProcess((e) => {
    const t = e.execution.task;
    const isBuild = (t.group && t.group.id === 'build') || COMPILE.test(String(t.name) + ' ' + ((t.execution && t.execution.commandLine) || ''));
    if (e.exitCode === 0 && isBuild && on('compileEffect')) triggerFx(ctx);
  }));
  // Commande du terminal : compilation réussie → animation ; échec → son
  if (vscode.window.onDidEndTerminalShellExecution) {
    ctx.subscriptions.push(vscode.window.onDidEndTerminalShellExecution((e) => {
      const cmd = (e.execution && e.execution.commandLine && e.execution.commandLine.value) || '';
      if (e.exitCode === 0 && COMPILE.test(cmd) && on('compileEffect')) { triggerFx(ctx); return; }
      if (e.exitCode === undefined || e.exitCode === 0 || e.exitCode === 130) return; // 130 = Ctrl+C
      if (on('errorSound')) errorSound(ctx, false);
    }));
  }
  // L'ancienne extension « Noël Pixel » ferait doublon
  if (vscode.extensions.getExtension('lmia34.noel-pixel-mac')) {
    vscode.window.showWarningMessage('Pixel Worlds : l\'extension « Noël Pixel 8-bit » est aussi installée et ferait doublon (neige, sons, animations en double). Désinstalle-la : Pixel Worlds contient déjà le monde Noël.');
  }
  const world = ctx.globalState.get('pixelWorlds.world');
  if (world && WORLDS[world]) {
    // Après une mise à jour de l'extension : les nouvelles images remplacent les anciennes puis Background les réapplique
    if (ctx.globalState.get('pixelWorlds.version') !== version(ctx)) {
      await setDecor(ctx, world); await applyFx(ctx, false);
      try { await vscode.commands.executeCommand('extension.background.install'); } catch (e) { /* rien */ }
      return;
    }
    // Après une mise à jour de VS Code, l'injection disparaît : on la remet toute seule
    const r = await patchFx(ctx);
    if (r.state === 'patched') vscode.window.showInformationMessage('🌠 Pixel Worlds : redémarre VS Code (quitte-le complètement puis rouvre-le) pour réactiver l\'animation de compilation.');
    else if (r.state === 'error') vscode.window.showWarningMessage('Pixel Worlds : impossible de préparer l\'animation de compilation (' + r.error + '). Lance « Pixel Worlds: Diagnostic ».');
    return;
  }
  // Première installation : on propose les mondes
  if (!ctx.globalState.get('pixelWorlds.asked')) {
    await ctx.globalState.update('pixelWorlds.asked', true);
    choose(ctx);
  }
}
function deactivate() {}
module.exports = { activate, deactivate };
