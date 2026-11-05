# Génère toutes les décos de Noël en pixel art 8 bits dans ~/noel-vscode/*.svg
import random, math, os
D = os.path.expanduser('~/noel-vscode')
LIGHTS = ['#f83800', '#f8b800', '#3cbcfc', '#f878f8', '#58f898']
PAL = {'G':'#00a800','g':'#005800','Y':'#f8b800','y':'#ac7c00','R':'#d82800','r':'#881400','W':'#fcfcfc',
       's':'#a4e4fc','T':'#7c3c00','K':'#1c1c1c','O':'#ac7c00','S':'#fcbcb0','B':'#c84c0c','D':'#503000',
       'C':'#7c7c7c','A':'#c88c3c','b':'#a0522d','N':'#f83800','E':'#3cbcfc','P':'#f878f8','o':'#f87800'}

SPR = {
 'tree': ["....Y....","...YYY...","....G....","...GGg...","..GLGgg..","...GGg...","..GGGLg..",".GLGGGgg.","..GGGGg..",".GGGLGgg.","GGGGGGLgg",".LGGGGGg.","GGGGLGGgg","....T....","....T...."],
 'bigtree': [".......Y.......","......YYY......",".......Y.......",".......G.......","......GGg......",".....GLGgg.....","......GGg......",".....GGGLg.....","....GLGGGgg....",".....GGGGg.....","....GGLGGgg....","...GGGGGGLgg...","....LGGGGgg....","...GGGGLGGgg...","..GLGGGGGGgLg..","...GGGLGGGgg...","..GGGGGGGLGgg..",".GGLGGGGGGGggg.","..GGGGGLGGGgg..",".GGGGGGGGGLGgg.","GLGGGLGGGGGgggg",".......T.......",".......T......."],
 'gift': ["..Y..Y..","...YY...","XXXYXXXx","XXXYXXXx","YYYYYYYY","XXXYXXXx","XXXYXXXx","XXXYXXXx"],
 'snowman': ["...KKK...","...KKK...","..KRRRK..","...WWW...","..WKWKs..","..WWoos..","...WWs...","..RRRRR..","..WWWWRs.","TWWWKWWsT",".TWWWWWs.T","..WWKWWs..","WWWWWWWss","WWWWKWWss",".WWWWWss."],
 'cane': [".RW.","R..W","W..R","...W","...R","...W","...R","...W","...R"],
 'house': [".....WWWW...C..","...WWWWWWWW.C..","..RRRRRRRRRRR..",".RRRRRRRRRRRRR.","RRRRRRRRRRRRRRR",".BBBBBBBBBBBBB.",".BLLBBBBBBBLLB.",".BLLBBBDBBBLLB.",".BBBBBBDBBBBBB.",".BBBBBBDBBBBBB."],
 'star': ["..Y..",".YYY.","YYYYY",".YYY.",".Y.Y."],
 'moon': ["..YYYY..",".YYYYyY.","YYyYYYYY","YYYYYYYY","YYYYYyYY","YYyYYYYY",".YYYYYY.","..YYYY.."],
 'reindeer': ["........A.A.",".........AA.","........bbbN","........bKb.",".......b....",".bbbbbbb....","bbbbbbbb....",".b..b.b.....",".b..b.b....."],
 'sleigh': [".......RR.......","......RRRW......","......SSS.......",".....WWWW.......","..OO.RRRRR......",".OOOORRRRR....RR",".OOOORRRRR.....R",".RRRRRRRRRRRRRR.","..RRRRRRRRRRRR..","...RRRRRRRRRR...","Y..Y......Y..Y..",".YYYYYYYYYYYYYYY"],
 'bauble': ["..Y..",".XXX.","XWXXX","XXXXX","XXXXX",".XXX."],
 'wreath': ["...GGG...","..GLGGG..",".GG...LG.","GL.....GG","GG.....LG","GG.....GG",".LG...GG.","..GGRGG..","...RRR..."],
}

