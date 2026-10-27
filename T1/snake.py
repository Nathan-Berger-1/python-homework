"""T1 – Snake procédural : le code de départ (étape 1).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lancez-le avec :  uv run snake.py
Testez-le avec :  uv run pytest
"""

import random

import pygame as pg

# Le plateau : X × Y cases de W × H pixels (étape 3).
X, Y = 30, 30
W, H = 20, 20


UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)


# --- logique du jeu : aucune fonction ici ne dessine -------------------------
# Ces fonctions sont vérifiées par les tests (tests/test_snake.py) :
# gardez leur nom et leurs paramètres.


def in_scope(tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    raise NotImplementedError("étape 5")


def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    raise NotImplementedError("étape 5")


def turn(direction, key):
    """La nouvelle direction après l'appui sur la touche `key` (ex. pg.K_UP)."""
    raise NotImplementedError("étape 6")


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    raise NotImplementedError("étapes 5, 7 et 8")


def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    raise NotImplementedError("étape 7")


# --- la boucle de jeu --------------------------------------------------------

def draw_tile(screen, tile, color):
    x, y = tile
    rect = pg.Rect(x * W, y * H, W, H)
    pg.draw.rect(screen, color, rect)


def main():
    pg.init()
    screen = pg.display.set_mode((X * W, Y * H))
    clock = pg.time.Clock()

    running = True

    while running:
        clock.tick(1)

        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_q
            ):
                running = False

        # Dessiner le damier
        screen.fill((255, 255, 255))

        for y in range(Y):
            for x in range(X):
                if (x + y) % 2 == 0:
                    draw_tile(screen, (x, y), (200, 200, 200))

        pg.display.update()

    pg.quit()

# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run snake.py),
# pas quand un autre fichier fait `import snake` (les tests, par ex.).
if __name__ == "__main__":
    main()
