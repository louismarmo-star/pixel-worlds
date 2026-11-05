# Génère le thème de couleurs « Pôle Nord » ; le thème « Noël » est repris tel quel.
import json, os, shutil
H = os.path.expanduser('~/pixel-worlds')
shutil.copy(os.path.expanduser('~/noel-pixel/themes/noel-pixel.json'), f'{H}/themes/noel.json')
t = json.load(open(f'{H}/themes/noel.json')); t['name'] = '🎄 Noël (Pixel Worlds)'
json.dump(t, open(f'{H}/themes/noel.json', 'w'), indent=1, ensure_ascii=False)

ED, ED2, SB, DARK, BAR = '#0e2b4a', '#0a2038', '#123a5c', '#081a2e', '#1a6fa8'
GREEN, VIOLET, CYAN, ICE, ORANGE = '#6cf0b0', '#c89cff', '#7fe0ff', '#eaf6ff', '#ffb86c'
c = {
 "editor.background": ED, "editor.foreground": ICE, "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#4f7fa8", "editorLineNumber.activeForeground": CYAN,
 "editor.lineHighlightBackground": "#14406a60", "editor.selectionBackground": "#3cbcfc55", "editor.selectionHighlightBackground": "#6cf0b030",
 "editorCursor.foreground": GREEN, "editorIndentGuide.background1": "#173f63", "editorIndentGuide.activeBackground1": "#3d7fb0", "editorWhitespace.foreground": "#173f63",
 "editorBracketHighlight.foreground1": CYAN, "editorBracketHighlight.foreground2": VIOLET, "editorBracketHighlight.foreground3": GREEN,
 "sideBar.background": SB, "sideBar.foreground": "#dff1ff", "sideBarTitle.foreground": CYAN, "sideBarSectionHeader.background": "#0e2f4f",
 "list.hoverBackground": "#1b5784", "list.activeSelectionBackground": "#1b78b0aa", "list.inactiveSelectionBackground": "#1b78b055", "list.highlightForeground": GREEN,
 "activityBar.background": DARK, "activityBar.foreground": CYAN, "activityBar.inactiveForeground": "#5f8fb8", "activityBar.activeBorder": GREEN, "activityBarBadge.background": VIOLET, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#ffffff", "titleBar.inactiveBackground": "#14537d",
 "statusBar.background": BAR, "statusBar.foreground": "#ffffff", "statusBar.noFolderBackground": "#14537d", "statusBar.debuggingBackground": "#7a4fc0", "statusBarItem.remoteBackground": "#14537d",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": GREEN, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#7fa8cc",
 "panel.background": ED2, "panel.border": "#3cbcfc44", "panelTitle.activeBorder": GREEN, "panelTitle.activeForeground": CYAN,
 "terminal.background": ED2, "terminal.foreground": ICE, "terminalCursor.foreground": GREEN,
 "terminal.ansiBlack": "#14406a", "terminal.ansiRed": "#ff7b8a", "terminal.ansiGreen": GREEN, "terminal.ansiYellow": "#ffd98a", "terminal.ansiBlue": "#7fd0ff", "terminal.ansiMagenta": VIOLET, "terminal.ansiCyan": "#8fe8ff", "terminal.ansiWhite": ICE,
 "terminal.ansiBrightBlack": "#5f9ac8", "terminal.ansiBrightRed": "#ff9aa6", "terminal.ansiBrightGreen": "#9bf7cc", "terminal.ansiBrightYellow": "#ffe8b0", "terminal.ansiBrightBlue": "#a8dcff", "terminal.ansiBrightMagenta": "#dcc0ff", "terminal.ansiBrightCyan": "#bff2ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": GREEN, "button.background": "#1b78b0", "button.hoverBackground": "#2a90cc", "badge.background": "#1b78b0",
 "input.background": ED2, "input.border": "#1f5a85", "dropdown.background": ED2, "editorWidget.background": "#0e2f4f", "quickInput.background": "#0e2f4f",
 "scrollbarSlider.background": "#7fe0ff30", "scrollbarSlider.hoverBackground": "#7fe0ff60",
 "gitDecoration.modifiedResourceForeground": "#ffd98a", "gitDecoration.untrackedResourceForeground": GREEN, "gitDecoration.deletedResourceForeground": "#ff7b8a",
 "editorError.foreground": "#ff7b8a", "editorWarning.foreground": "#ffd98a",
}
tok = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#6f9bc4", "italic"),
 ("Mots-clés — violet aurore", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], VIOLET, None),
 ("Fonctions — vert aurore", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], GREEN, None),
 ("Chaînes — cyan glacé", ["string", "string.quoted", "string.template"], "#9cf0ff", None),
 ("Nombres — orange bec de pingouin", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], ORANGE, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], "#7fd0ff", None),
 ("Variables", ["variable", "variable.other", "meta.definition.variable"], ICE, None),
 ("Paramètres", ["variable.parameter"], "#ffe0b0", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#a8d8ff", None),
 ("Balises", ["entity.name.tag"], "#ff9cc8", None),
 ("Attributs", ["entity.other.attribute-name"], "#ffd98a", None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#a8c8e8", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], VIOLET, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff9cc8", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], CYAN, "bold"),
]
theme = {"name": "🐧 Pôle Nord (Pixel Worlds)", "type": "dark", "colors": c, "semanticHighlighting": True,
         "tokenColors": [{"name": n, "scope": s, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, s, f, st in tok]}
json.dump(theme, open(f'{H}/themes/polenord.json', 'w'), indent=1, ensure_ascii=False)
print('thèmes créés')

# ---------- Sakura ----------
ED, ED2, SB, DARK, BAR = '#201a38', '#17122b', '#4a1f3d', '#241028', '#c2487a'
PINK, GOLD, MINT, LAV, PEACH, SKY = '#ff8fbf', '#ffd98a', '#9be8d0', '#c9b6ff', '#ff9d6c', '#9ec5ff'
c2 = {
 "editor.background": ED, "editor.foreground": "#fff0f6", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#6f5a9a", "editorLineNumber.activeForeground": PINK,
 "editor.lineHighlightBackground": "#3a2a6060", "editor.selectionBackground": "#ff8fbf44", "editor.selectionHighlightBackground": "#9be8d030",
 "editorCursor.foreground": PINK, "editorIndentGuide.background1": "#2e2552", "editorIndentGuide.activeBackground1": "#7a5fb0", "editorWhitespace.foreground": "#2e2552",
 "editorBracketHighlight.foreground1": PINK, "editorBracketHighlight.foreground2": GOLD, "editorBracketHighlight.foreground3": MINT,
 "sideBar.background": SB, "sideBar.foreground": "#ffe6f0", "sideBarTitle.foreground": PINK, "sideBarSectionHeader.background": "#3a1830",
 "list.hoverBackground": "#6b2d58", "list.activeSelectionBackground": "#c2487aaa", "list.inactiveSelectionBackground": "#c2487a55", "list.highlightForeground": GOLD,
 "activityBar.background": DARK, "activityBar.foreground": PINK, "activityBar.inactiveForeground": "#a47aa8", "activityBar.activeBorder": GOLD, "activityBarBadge.background": GOLD, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#ffffff", "titleBar.inactiveBackground": "#8f3560",
 "statusBar.background": BAR, "statusBar.foreground": "#ffffff", "statusBar.noFolderBackground": "#8f3560", "statusBar.debuggingBackground": "#7a4fc0", "statusBarItem.remoteBackground": "#8f3560",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": PINK, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#9c85c0",
 "panel.background": ED2, "panel.border": "#ff8fbf44", "panelTitle.activeBorder": PINK, "panelTitle.activeForeground": PINK,
 "terminal.background": ED2, "terminal.foreground": "#fff0f6", "terminalCursor.foreground": PINK,
 "terminal.ansiBlack": "#3a2a60", "terminal.ansiRed": "#ff6b8e", "terminal.ansiGreen": MINT, "terminal.ansiYellow": GOLD, "terminal.ansiBlue": SKY, "terminal.ansiMagenta": PINK, "terminal.ansiCyan": "#8fe8ff", "terminal.ansiWhite": "#fff0f6",
 "terminal.ansiBrightBlack": "#8a7aa8", "terminal.ansiBrightRed": "#ff93ab", "terminal.ansiBrightGreen": "#c0f5e6", "terminal.ansiBrightYellow": "#ffe8b0", "terminal.ansiBrightBlue": "#c4dcff", "terminal.ansiBrightMagenta": "#ffb7d5", "terminal.ansiBrightCyan": "#bff2ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": PINK, "button.background": "#c2487a", "button.hoverBackground": "#d65c90", "badge.background": "#c2487a",
 "input.background": ED2, "input.border": "#4a3a78", "dropdown.background": ED2, "editorWidget.background": "#2b2150", "quickInput.background": "#2b2150",
 "scrollbarSlider.background": "#ff8fbf30", "scrollbarSlider.hoverBackground": "#ff8fbf60",
 "gitDecoration.modifiedResourceForeground": GOLD, "gitDecoration.untrackedResourceForeground": MINT, "gitDecoration.deletedResourceForeground": "#ff6b8e",
 "editorError.foreground": "#ff6b8e", "editorWarning.foreground": GOLD,
}
tok2 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#8a7aa8", "italic"),
 ("Mots-clés — rose sakura", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], PINK, None),
 ("Fonctions — or", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], GOLD, None),
 ("Chaînes — matcha", ["string", "string.quoted", "string.template"], MINT, None),
 ("Nombres — pêche", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], PEACH, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], SKY, None),
 ("Variables", ["variable", "variable.other", "meta.definition.variable"], "#fff0f6", None),
 ("Paramètres", ["variable.parameter"], "#ffd9c4", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], LAV, None),
 ("Balises", ["entity.name.tag"], "#ff7aa8", None),
 ("Attributs", ["entity.other.attribute-name"], GOLD, None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#c8b4e0", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], PINK, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff7aa8", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], PINK, "bold"),
]
json.dump({"name": "🌸 Sakura (Pixel Worlds)", "type": "dark", "colors": c2, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok2]},
          open(f'{H}/themes/sakura.json', 'w'), indent=1, ensure_ascii=False)
print('thème Sakura créé')

# ---------- Néon City ----------
ED, ED2, SB, DARK, BAR = '#12102a', '#0c0a1e', '#1d1640', '#080614', '#a31d72'
MAG, CYA, LIM, AMB, VIO = '#ff5cb6', '#4df0ff', '#9dff6b', '#ffb020', '#b58cff'
c3 = {
 "editor.background": ED, "editor.foreground": "#eae6ff", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#4f4a86", "editorLineNumber.activeForeground": CYA,
 "editor.lineHighlightBackground": "#2a205060", "editor.selectionBackground": "#ff5cb644", "editor.selectionHighlightBackground": "#4df0ff30",
 "editorCursor.foreground": CYA, "editorIndentGuide.background1": "#221c48", "editorIndentGuide.activeBackground1": "#5b4fb0", "editorWhitespace.foreground": "#221c48",
 "editorBracketHighlight.foreground1": MAG, "editorBracketHighlight.foreground2": CYA, "editorBracketHighlight.foreground3": AMB,
 "sideBar.background": SB, "sideBar.foreground": "#dcd6ff", "sideBarTitle.foreground": CYA, "sideBarSectionHeader.background": "#150f33",
 "list.hoverBackground": "#2e2468", "list.activeSelectionBackground": "#a31d72aa", "list.inactiveSelectionBackground": "#a31d7255", "list.highlightForeground": CYA,
 "activityBar.background": DARK, "activityBar.foreground": CYA, "activityBar.inactiveForeground": "#5b52a0", "activityBar.activeBorder": MAG, "activityBarBadge.background": MAG, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#ffffff", "titleBar.inactiveBackground": "#701452",
 "statusBar.background": BAR, "statusBar.foreground": "#ffffff", "statusBar.noFolderBackground": "#701452", "statusBar.debuggingBackground": "#0e7a8c", "statusBarItem.remoteBackground": "#701452",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": CYA, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#7d74c0",
 "panel.background": ED2, "panel.border": "#4df0ff44", "panelTitle.activeBorder": MAG, "panelTitle.activeForeground": CYA,
 "terminal.background": ED2, "terminal.foreground": "#eae6ff", "terminalCursor.foreground": CYA,
 "terminal.ansiBlack": "#2a2050", "terminal.ansiRed": "#ff5a6e", "terminal.ansiGreen": LIM, "terminal.ansiYellow": AMB, "terminal.ansiBlue": "#7fa8ff", "terminal.ansiMagenta": MAG, "terminal.ansiCyan": CYA, "terminal.ansiWhite": "#eae6ff",
 "terminal.ansiBrightBlack": "#6b62a8", "terminal.ansiBrightRed": "#ff8a98", "terminal.ansiBrightGreen": "#c4ff9f", "terminal.ansiBrightYellow": "#ffd073", "terminal.ansiBrightBlue": "#a8c4ff", "terminal.ansiBrightMagenta": "#ff93d0", "terminal.ansiBrightCyan": "#a8f7ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": CYA, "button.background": "#a31d72", "button.hoverBackground": "#c42a8c", "badge.background": "#a31d72",
 "input.background": ED2, "input.border": "#3a3080", "dropdown.background": ED2, "editorWidget.background": "#1a1440", "quickInput.background": "#1a1440",
 "scrollbarSlider.background": "#4df0ff30", "scrollbarSlider.hoverBackground": "#4df0ff60",
 "gitDecoration.modifiedResourceForeground": AMB, "gitDecoration.untrackedResourceForeground": LIM, "gitDecoration.deletedResourceForeground": "#ff5a6e",
 "editorError.foreground": "#ff5a6e", "editorWarning.foreground": AMB,
}
tok3 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#6f6a9a", "italic"),
 ("Mots-clés — magenta néon", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], MAG, None),
 ("Fonctions — cyan néon", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], CYA, None),
 ("Chaînes — vert acide", ["string", "string.quoted", "string.template"], LIM, None),
 ("Nombres — ambre", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], AMB, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], VIO, None),
 ("Variables", ["variable", "variable.other", "meta.definition.variable"], "#eae6ff", None),
 ("Paramètres", ["variable.parameter"], "#ffd1a1", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#8fb8ff", None),
 ("Balises", ["entity.name.tag"], "#ff7a8a", None),
 ("Attributs", ["entity.other.attribute-name"], AMB, None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#a8a0e0", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], VIO, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff7a8a", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], CYA, "bold"),
]
json.dump({"name": "🌃 Néon City (Pixel Worlds)", "type": "dark", "colors": c3, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok3]},
          open(f'{H}/themes/neon.json', 'w'), indent=1, ensure_ascii=False)
print('thème Néon City créé')

# ---------- Espace ----------
ED, ED2, SB, DARK, BAR = '#0a0c26', '#06081c', '#12163f', '#04051a', '#4b2fb5'
CYA, VIO, ORA, GRN, PNK = '#4df0ff', '#b48cff', '#ff9a2e', '#7dffa0', '#ff77c5'
c4 = {
 "editor.background": ED, "editor.foreground": "#e6ebff", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#4a5090", "editorLineNumber.activeForeground": ORA,
 "editor.lineHighlightBackground": "#1a1f5260", "editor.selectionBackground": "#b48cff44", "editor.selectionHighlightBackground": "#4df0ff30",
 "editorCursor.foreground": ORA, "editorIndentGuide.background1": "#161a48", "editorIndentGuide.activeBackground1": "#4f5ab0", "editorWhitespace.foreground": "#161a48",
 "editorBracketHighlight.foreground1": ORA, "editorBracketHighlight.foreground2": CYA, "editorBracketHighlight.foreground3": PNK,
 "sideBar.background": SB, "sideBar.foreground": "#d6dcff", "sideBarTitle.foreground": ORA, "sideBarSectionHeader.background": "#0e1233",
 "list.hoverBackground": "#232a70", "list.activeSelectionBackground": "#4b2fb5aa", "list.inactiveSelectionBackground": "#4b2fb555", "list.highlightForeground": ORA,
 "activityBar.background": DARK, "activityBar.foreground": ORA, "activityBar.inactiveForeground": "#5560a8", "activityBar.activeBorder": CYA, "activityBarBadge.background": ORA, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#ffffff", "titleBar.inactiveBackground": "#35228a",
 "statusBar.background": BAR, "statusBar.foreground": "#ffffff", "statusBar.noFolderBackground": "#35228a", "statusBar.debuggingBackground": "#c25a10", "statusBarItem.remoteBackground": "#35228a",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": ORA, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#7580c8",
 "panel.background": ED2, "panel.border": "#b48cff44", "panelTitle.activeBorder": ORA, "panelTitle.activeForeground": ORA,
 "terminal.background": ED2, "terminal.foreground": "#e6ebff", "terminalCursor.foreground": ORA,
 "terminal.ansiBlack": "#232a70", "terminal.ansiRed": "#ff6b5a", "terminal.ansiGreen": GRN, "terminal.ansiYellow": "#ffe066", "terminal.ansiBlue": "#7fa8ff", "terminal.ansiMagenta": PNK, "terminal.ansiCyan": CYA, "terminal.ansiWhite": "#e6ebff",
 "terminal.ansiBrightBlack": "#6b74b8", "terminal.ansiBrightRed": "#ff9a8c", "terminal.ansiBrightGreen": "#b0ffc8", "terminal.ansiBrightYellow": "#fff0a0", "terminal.ansiBrightBlue": "#a8c4ff", "terminal.ansiBrightMagenta": "#ffa8d8", "terminal.ansiBrightCyan": "#a8f7ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": ORA, "button.background": "#4b2fb5", "button.hoverBackground": "#6040d0", "badge.background": "#4b2fb5",
 "input.background": ED2, "input.border": "#30388a", "dropdown.background": ED2, "editorWidget.background": "#0e1233", "quickInput.background": "#0e1233",
 "scrollbarSlider.background": "#b48cff30", "scrollbarSlider.hoverBackground": "#b48cff60",
 "gitDecoration.modifiedResourceForeground": "#ffe066", "gitDecoration.untrackedResourceForeground": GRN, "gitDecoration.deletedResourceForeground": "#ff6b5a",
 "editorError.foreground": "#ff6b5a", "editorWarning.foreground": "#ffe066",
}
tok4 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#6a72a8", "italic"),
 ("Mots-clés — violet nébuleuse", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], VIO, None),
 ("Fonctions — cyan", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], CYA, None),
 ("Chaînes — vert", ["string", "string.quoted", "string.template"], GRN, None),
 ("Nombres — orange fusée", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], ORA, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], "#8fb8ff", None),
 ("Variables", ["variable", "variable.other", "meta.definition.variable"], "#e6ebff", None),
 ("Paramètres", ["variable.parameter"], "#ffd9a8", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#9ad0ff", None),
 ("Balises", ["entity.name.tag"], PNK, None),
 ("Attributs", ["entity.other.attribute-name"], "#ffe066", None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#a8b0e8", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], VIO, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], PNK, None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], ORA, "bold"),
]
json.dump({"name": "🚀 Espace (Pixel Worlds)", "type": "dark", "colors": c4, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok4]},
          open(f'{H}/themes/space.json', 'w'), indent=1, ensure_ascii=False)
print('thème Espace créé')

# ---------- Fantasy ----------
ED, ED2, SB, DARK, BAR = '#14192b', '#0e1220', '#2a1e1a', '#0a0c16', '#7a1f2e'
GOLD, EMER, CORAL, MAG, ICE = '#f2c45a', '#6fe0a0', '#ff9f7a', '#d49bff', '#7fc4ff'
c5 = {
 "editor.background": ED, "editor.foreground": "#f1ead8", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#5a6488", "editorLineNumber.activeForeground": GOLD,
 "editor.lineHighlightBackground": "#262e4a60", "editor.selectionBackground": "#f2c45a40", "editor.selectionHighlightBackground": "#6fe0a030",
 "editorCursor.foreground": GOLD, "editorIndentGuide.background1": "#1f2640", "editorIndentGuide.activeBackground1": "#5a6488", "editorWhitespace.foreground": "#1f2640",
 "editorBracketHighlight.foreground1": GOLD, "editorBracketHighlight.foreground2": EMER, "editorBracketHighlight.foreground3": MAG,
 "sideBar.background": SB, "sideBar.foreground": "#f1e0c8", "sideBarTitle.foreground": GOLD, "sideBarSectionHeader.background": "#221814",
 "list.hoverBackground": "#44302a", "list.activeSelectionBackground": "#7a1f2eaa", "list.inactiveSelectionBackground": "#7a1f2e55", "list.highlightForeground": GOLD,
 "activityBar.background": DARK, "activityBar.foreground": GOLD, "activityBar.inactiveForeground": "#7a7088", "activityBar.activeBorder": GOLD, "activityBarBadge.background": "#c8283c", "activityBarBadge.foreground": "#ffffff",
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#fff4d8", "titleBar.inactiveBackground": "#561520",
 "statusBar.background": BAR, "statusBar.foreground": "#fff4d8", "statusBar.noFolderBackground": "#561520", "statusBar.debuggingBackground": "#217a42", "statusBarItem.remoteBackground": "#561520",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": GOLD, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#8088a8",
 "panel.background": ED2, "panel.border": "#f2c45a44", "panelTitle.activeBorder": GOLD, "panelTitle.activeForeground": GOLD,
 "terminal.background": ED2, "terminal.foreground": "#f1ead8", "terminalCursor.foreground": GOLD,
 "terminal.ansiBlack": "#262e4a", "terminal.ansiRed": "#ff7a7a", "terminal.ansiGreen": EMER, "terminal.ansiYellow": GOLD, "terminal.ansiBlue": ICE, "terminal.ansiMagenta": MAG, "terminal.ansiCyan": "#8fe8ff", "terminal.ansiWhite": "#f1ead8",
 "terminal.ansiBrightBlack": "#6a7498", "terminal.ansiBrightRed": "#ffa0a0", "terminal.ansiBrightGreen": "#a8f5c8", "terminal.ansiBrightYellow": "#ffe08a", "terminal.ansiBrightBlue": "#a8d8ff", "terminal.ansiBrightMagenta": "#e6c4ff", "terminal.ansiBrightCyan": "#bff2ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": GOLD, "button.background": "#7a1f2e", "button.hoverBackground": "#9a2a3e", "badge.background": "#7a1f2e",
 "input.background": ED2, "input.border": "#3a4470", "dropdown.background": ED2, "editorWidget.background": "#1a2038", "quickInput.background": "#1a2038",
 "scrollbarSlider.background": "#f2c45a30", "scrollbarSlider.hoverBackground": "#f2c45a60",
 "gitDecoration.modifiedResourceForeground": GOLD, "gitDecoration.untrackedResourceForeground": EMER, "gitDecoration.deletedResourceForeground": "#ff7a7a",
 "editorError.foreground": "#ff7a7a", "editorWarning.foreground": GOLD,
}
tok5 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#7d8aa8", "italic"),
 ("Mots-clés — or", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], GOLD, None),
 ("Fonctions — émeraude", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], EMER, None),
 ("Chaînes — corail", ["string", "string.quoted", "string.template"], CORAL, None),
 ("Nombres — magie violette", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], MAG, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], ICE, None),
 ("Variables — parchemin", ["variable", "variable.other", "meta.definition.variable"], "#f1ead8", None),
 ("Paramètres", ["variable.parameter"], "#ffd9b0", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#b0d8ff", None),
 ("Balises", ["entity.name.tag"], "#ff7a7a", None),
 ("Attributs", ["entity.other.attribute-name"], GOLD, None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#b8c0d8", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], GOLD, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff7a7a", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], GOLD, "bold"),
]
json.dump({"name": "🏰 Fantasy (Pixel Worlds)", "type": "dark", "colors": c5, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok5]},
          open(f'{H}/themes/fantasy.json', 'w'), indent=1, ensure_ascii=False)
print('thème Fantasy créé')

# ---------- Océan ----------
ED, ED2, SB, DARK, BAR = '#0a2a40', '#061c2c', '#0d3a52', '#041420', '#0f7a9a'
COR, AQU, SEA, SAND, ICE = '#ff8a7a', '#4df0ff', '#7dffc4', '#ffd870', '#9ab8ff'
c6 = {
 "editor.background": ED, "editor.foreground": "#e8faff", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#3f7a98", "editorLineNumber.activeForeground": AQU,
 "editor.lineHighlightBackground": "#12507060", "editor.selectionBackground": "#4df0ff40", "editor.selectionHighlightBackground": "#7dffc430",
 "editorCursor.foreground": AQU, "editorIndentGuide.background1": "#0f3d58", "editorIndentGuide.activeBackground1": "#2f7fa8", "editorWhitespace.foreground": "#0f3d58",
 "editorBracketHighlight.foreground1": COR, "editorBracketHighlight.foreground2": AQU, "editorBracketHighlight.foreground3": SAND,
 "sideBar.background": SB, "sideBar.foreground": "#d4f1ff", "sideBarTitle.foreground": AQU, "sideBarSectionHeader.background": "#093044",
 "list.hoverBackground": "#17608a", "list.activeSelectionBackground": "#0f7a9aaa", "list.inactiveSelectionBackground": "#0f7a9a55", "list.highlightForeground": SAND,
 "activityBar.background": DARK, "activityBar.foreground": AQU, "activityBar.inactiveForeground": "#3f7a98", "activityBar.activeBorder": SEA, "activityBarBadge.background": COR, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#ffffff", "titleBar.inactiveBackground": "#0a5670",
 "statusBar.background": BAR, "statusBar.foreground": "#ffffff", "statusBar.noFolderBackground": "#0a5670", "statusBar.debuggingBackground": "#c25a10", "statusBarItem.remoteBackground": "#0a5670",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": AQU, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#5f94b0",
 "panel.background": ED2, "panel.border": "#4df0ff44", "panelTitle.activeBorder": AQU, "panelTitle.activeForeground": AQU,
 "terminal.background": ED2, "terminal.foreground": "#e8faff", "terminalCursor.foreground": AQU,
 "terminal.ansiBlack": "#124e6e", "terminal.ansiRed": "#ff7a7a", "terminal.ansiGreen": SEA, "terminal.ansiYellow": SAND, "terminal.ansiBlue": ICE, "terminal.ansiMagenta": "#ff9bd8", "terminal.ansiCyan": AQU, "terminal.ansiWhite": "#e8faff",
 "terminal.ansiBrightBlack": "#4f8aa8", "terminal.ansiBrightRed": "#ffa0a0", "terminal.ansiBrightGreen": "#b0ffe0", "terminal.ansiBrightYellow": "#ffe8a0", "terminal.ansiBrightBlue": "#c0d0ff", "terminal.ansiBrightMagenta": "#ffc4e8", "terminal.ansiBrightCyan": "#a8f7ff", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": AQU, "button.background": "#0f7a9a", "button.hoverBackground": "#1d9abf", "badge.background": "#0f7a9a",
 "input.background": ED2, "input.border": "#1f5f80", "dropdown.background": ED2, "editorWidget.background": "#0a3248", "quickInput.background": "#0a3248",
 "scrollbarSlider.background": "#4df0ff30", "scrollbarSlider.hoverBackground": "#4df0ff60",
 "gitDecoration.modifiedResourceForeground": SAND, "gitDecoration.untrackedResourceForeground": SEA, "gitDecoration.deletedResourceForeground": "#ff7a7a",
 "editorError.foreground": "#ff7a7a", "editorWarning.foreground": SAND,
}
tok6 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#5f8fa8", "italic"),
 ("Mots-clés — corail", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], COR, None),
 ("Fonctions — aqua", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], AQU, None),
 ("Chaînes — écume", ["string", "string.quoted", "string.template"], SEA, None),
 ("Nombres — sable doré", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], SAND, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], ICE, None),
 ("Variables", ["variable", "variable.other", "meta.definition.variable"], "#e8faff", None),
 ("Paramètres", ["variable.parameter"], "#ffd9b8", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#8fd8ff", None),
 ("Balises", ["entity.name.tag"], "#ff8fb0", None),
 ("Attributs", ["entity.other.attribute-name"], SAND, None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#a8d4e8", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], COR, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff8fb0", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], AQU, "bold"),
]
json.dump({"name": "🌊 Océan (Pixel Worlds)", "type": "dark", "colors": c6, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok6]},
          open(f'{H}/themes/ocean.json', 'w'), indent=1, ensure_ascii=False)
print('thème Océan créé')

# ---------- Far West ----------
ED, ED2, SB, DARK, BAR = '#2b1d16', '#1d130e', '#4a2a18', '#140c08', '#b4541c'
ORA, GOLD, SAGE, SKY, LAV = '#ff7a4a', '#ffd166', '#9bd68a', '#6fd0e8', '#c8a0ff'
c7 = {
 "editor.background": ED, "editor.foreground": "#f3e3cf", "editorGutter.background": ED, "minimap.background": ED, "breadcrumb.background": ED,
 "editorLineNumber.foreground": "#7a5a44", "editorLineNumber.activeForeground": GOLD,
 "editor.lineHighlightBackground": "#44301f60", "editor.selectionBackground": "#ff7a4a44", "editor.selectionHighlightBackground": "#ffd16630",
 "editorCursor.foreground": GOLD, "editorIndentGuide.background1": "#3a2a1e", "editorIndentGuide.activeBackground1": "#8a6a4c", "editorWhitespace.foreground": "#3a2a1e",
 "editorBracketHighlight.foreground1": ORA, "editorBracketHighlight.foreground2": GOLD, "editorBracketHighlight.foreground3": SAGE,
 "sideBar.background": SB, "sideBar.foreground": "#f5dcc0", "sideBarTitle.foreground": GOLD, "sideBarSectionHeader.background": "#3a2012",
 "list.hoverBackground": "#6a4128", "list.activeSelectionBackground": "#b4541caa", "list.inactiveSelectionBackground": "#b4541c55", "list.highlightForeground": GOLD,
 "activityBar.background": DARK, "activityBar.foreground": GOLD, "activityBar.inactiveForeground": "#8a6a52", "activityBar.activeBorder": ORA, "activityBarBadge.background": ORA, "activityBarBadge.foreground": DARK,
 "titleBar.activeBackground": BAR, "titleBar.activeForeground": "#fff4e0", "titleBar.inactiveBackground": "#82400f",
 "statusBar.background": BAR, "statusBar.foreground": "#fff4e0", "statusBar.noFolderBackground": "#82400f", "statusBar.debuggingBackground": "#2f8a3c", "statusBarItem.remoteBackground": "#82400f",
 "editorGroupHeader.tabsBackground": ED2, "tab.inactiveBackground": ED2, "tab.activeBackground": ED, "tab.border": ED2, "tab.activeBorderTop": ORA, "tab.activeForeground": "#ffffff", "tab.inactiveForeground": "#a08468",
 "panel.background": ED2, "panel.border": "#ffd16644", "panelTitle.activeBorder": ORA, "panelTitle.activeForeground": GOLD,
 "terminal.background": ED2, "terminal.foreground": "#f3e3cf", "terminalCursor.foreground": GOLD,
 "terminal.ansiBlack": "#44301f", "terminal.ansiRed": "#ff6f6f", "terminal.ansiGreen": SAGE, "terminal.ansiYellow": GOLD, "terminal.ansiBlue": SKY, "terminal.ansiMagenta": "#e8a0d0", "terminal.ansiCyan": "#8fe0e8", "terminal.ansiWhite": "#f3e3cf",
 "terminal.ansiBrightBlack": "#8a6a52", "terminal.ansiBrightRed": "#ff9a9a", "terminal.ansiBrightGreen": "#bfe8b0", "terminal.ansiBrightYellow": "#ffe29a", "terminal.ansiBrightBlue": "#a0e0f2", "terminal.ansiBrightMagenta": "#f4c8e4", "terminal.ansiBrightCyan": "#bff2f4", "terminal.ansiBrightWhite": "#ffffff",
 "focusBorder": GOLD, "button.background": "#b4541c", "button.hoverBackground": "#d06a2c", "badge.background": "#b4541c",
 "input.background": ED2, "input.border": "#5a3a28", "dropdown.background": ED2, "editorWidget.background": "#33231a", "quickInput.background": "#33231a",
 "scrollbarSlider.background": "#ffd16630", "scrollbarSlider.hoverBackground": "#ffd16660",
 "gitDecoration.modifiedResourceForeground": GOLD, "gitDecoration.untrackedResourceForeground": SAGE, "gitDecoration.deletedResourceForeground": "#ff6f6f",
 "editorError.foreground": "#ff6f6f", "editorWarning.foreground": GOLD,
}
tok7 = [
 ("Commentaires", ["comment", "punctuation.definition.comment"], "#8a7360", "italic"),
 ("Mots-clés — orange coucher de soleil", ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression"], ORA, None),
 ("Fonctions — or", ["entity.name.function", "support.function", "meta.function-call entity.name.function"], GOLD, None),
 ("Chaînes — vert cactus", ["string", "string.quoted", "string.template"], SAGE, None),
 ("Nombres — ciel du désert", ["constant.numeric", "constant.language", "constant.character.escape", "constant.other"], SKY, None),
 ("Types", ["entity.name.type", "entity.name.class", "support.type", "support.class", "storage.type.primitive", "entity.other.inherited-class"], LAV, None),
 ("Variables — sable", ["variable", "variable.other", "meta.definition.variable"], "#f3e3cf", None),
 ("Paramètres", ["variable.parameter"], "#ffd9b0", None),
 ("Propriétés", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], "#e8c090", None),
 ("Balises", ["entity.name.tag"], "#ff6f6f", None),
 ("Attributs", ["entity.other.attribute-name"], GOLD, None),
 ("Opérateurs", ["keyword.operator", "punctuation"], "#c8b098", None),
 ("Imports", ["keyword.control.import", "keyword.control.from", "keyword.control.export"], ORA, "italic"),
 ("Préprocesseur C", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], "#ff6f6f", None),
 ("Titres Markdown", ["markup.heading", "entity.name.section"], GOLD, "bold"),
]
json.dump({"name": "🤠 Far West (Pixel Worlds)", "type": "dark", "colors": c7, "semanticHighlighting": True,
           "tokenColors": [{"name": n, "scope": sc, "settings": ({"foreground": f} | ({"fontStyle": st} if st else {}))} for n, sc, f, st in tok7]},
          open(f'{H}/themes/west.json', 'w'), indent=1, ensure_ascii=False)
print('thème Far West créé')
