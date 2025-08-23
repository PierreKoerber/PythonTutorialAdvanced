
import sys, time

W, H = 70, 25  # largeur, hauteur (en caractères)

# --- Buffer écran: matrice de H lignes x W colonnes ---
screen = [[' ']*W for _ in range(H)]

def clear_buffer(fill=' '):
    for y in range(H):
        for x in range(W):
            screen[y][x] = fill

def put_char(x, y, ch):
    if 0 <= x < W and 0 <= y < H:
        screen[y][x] = ch

def put_text(x, y, text):
    for i, ch in enumerate(text):
        put_char(x+i, y, ch)

def draw_box(x, y, w, h, ch='#'):
    for i in range(w):
        put_char(x+i, y, ch)
        put_char(x+i, y+h-1, ch)
    for j in range(h):
        put_char(x, y+j, ch)
        put_char(x+w-1, y+j, ch)

def render():
    # \x1b[?25l = cacher curseur ; \x1b[H = curseur en haut/gauche
    sys.stdout.write("\x1b[?25l\x1b[H")
    for row in screen:
        sys.stdout.write(''.join(row) + '\n')
    sys.stdout.flush()

def teardown():
    # ré‑afficher le curseur
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()

# --- Démo: un sprite qui rebondit dans un cadre ---
try:
    sys.stdout.write("\x1b[2J\x1b[H")  # nettoyage initial (CLS)
    x, y, dx, dy = 2, 2, 1, 1
    while True:
        clear_buffer(' ')
        draw_box(0, 0, W, H, ch='*')
        put_text(2, 0, "  MATRICE TEXTE  ")
        put_char(x, y, '@')

        render()
        time.sleep(0.03)

        # rebond
        x += dx; y += dy
        if x <= 1 or x >= W-2: dx *= -1
        if y <= 1 or y >= H-2: dy *= -1
except KeyboardInterrupt:
    pass
finally:
    teardown()


