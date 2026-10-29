"""T1 – Snake procédural : corrigé commenté (étapes 0 à 8).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lance-le :   uv run snake.py
Teste-le :   uv run pytest

Lis-le de haut en bas, l'énoncé à côté. Trois parties, dans cet ordre :

1. LOGIQUE : serpent, fruit, règles. En cases (x, y), ne dessine jamais.
   C'est ce que testent les tests ;
2. AFFICHAGE : cases → pixels, et dessin ;
3. BOUCLE DE JEU, dans `main()` : enchaîne les deux à chaque image.

Retiens cette séparation : c'est elle qui rend `move` testable sans fenêtre.
On la pousse plus loin en séance 3.
"""

from random import randint

import pygame as pg

# --- constantes ----------------------------------------------------------------
# Chaque taille est écrite UNE fois, ici, en MAJUSCULES (convention : constante).
# Ailleurs : X, Y, W, H, jamais 30, 29 ou 600. Un plateau 40 × 40 = une ligne
# à changer. Les nombres en dur sont LE bug n° 1 de ce TP (randint(0, 19)…).

# Le plateau : X × Y cases de W × H pixels.
X, Y = 30, 30
W, H = 20, 20

# Couleurs (rouge, vert, bleu), de 0 à 255.
LIGHT = (240, 240, 240)
DARK = (215, 215, 215)
SNAKE_COLOR = (128, 128, 0)
FRUIT_COLOR = (192, 16, 16)

# Direction = vecteur (dx, dy), en cases.
# ⚠️ L'axe y pointe vers le BAS : (0, 0) = coin haut gauche. Monter = y - 1.
UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)

# Étape 6 : touche → direction. Remplace une cascade de `if`.
KEYS = {pg.K_UP: UP, pg.K_DOWN: DOWN, pg.K_LEFT: LEFT, pg.K_RIGHT: RIGHT}

# Images (= pas du serpent) par seconde.
FPS = 6


# --- 1. logique : aucune fonction ici ne dessine -------------------------------
# Serpent = liste de cases, queue au DÉBUT, tête à la FIN :
#     snake = [(10, 15), (11, 15), (12, 15)]
#              queue                tête = snake[-1]
# Fruit = une case (x, y), pas un rectangle de pixels.


def in_scope(tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    x, y = tile  # déballage : plus lisible que tile[0], tile[1]
    # Cases valides : 0 à X - 1, d'où `< X`.
    # Une comparaison vaut déjà True/False : pas de `if ...: return True`.
    return 0 <= x < X and 0 <= y < Y


def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    # Ne MODIFIE PAS `snake` : calcule et renvoie. Fonction "pure" → facile à
    # tester (réponse à la question de l'étape 5).
    x, y = snake[-1]
    dx, dy = direction
    return (x + dx, y + dy)


def turn(direction, key):
    """La nouvelle direction après l'appui sur `key` ; pas de demi-tour."""
    # `get(clé, défaut)` : touche non flèche → direction inchangée, sans `if`.
    new = KEYS.get(key, direction)
    # Opposées = somme nulle : RIGHT + LEFT = (0, 0) → demi-tour, ignoré.
    # Une seule ligne pour les quatre cas.
    if (new[0] + direction[0], new[1] + direction[1]) == (0, 0):
        return direction
    return new


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    # MODIFIE la liste (`append`, `pop`) : `main` voit le changement sans
    # qu'on renvoie le serpent. On renvoie juste CE QUI S'EST PASSÉ ; `main`
    # décide de la suite (nouveau fruit, fin de partie).

    # D'abord calculer, sans rien toucher...
    head = next_head(snake, direction)

    # ... puis vérifier. Ajouter la tête avant = case fantôme si mort → score +1.
    if not in_scope(head):
        return "out-of-board"
    # Inclut la queue (snake[0]). Elle part pendant ce pas, donc
    # `head in snake[1:]` se défend aussi. Ici : la règle la plus simple.
    if head in snake:
        return "self-bite"

    # Coup valide : la tête avance (`append` = à la fin).
    snake.append(head)

    # Étape 7 : fruit mangé → on garde la queue, le serpent grandit.
    if head == fruit:
        return "ate"

    # Sinon la queue avance : on retire le PREMIER élément.
    # ⚠️ `pop()` sans argument retire le DERNIER = la tête ajoutée : serpent
    # immobile, et aucune erreur !
    # ⚠️ `append`/`pop` modifient sur place : jamais `snake = snake.append(head)`
    # (→ None).
    snake.pop(0)
    return "moved"


def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    # `randint(a, b)` inclut les DEUX bornes (≠ `range`) : 0 à X - 1.
    # On retire tant que la case est prise. OK ici : le serpent occupe peu du
    # plateau. (Plateau plein → boucle infinie ; un vrai jeu déclare la
    # victoire avant.)
    while True:
        tile = (randint(0, X - 1), randint(0, Y - 1))
        if tile not in snake:
            return tile  # sort de la fonction, donc de la boucle


# --- 2. affichage --------------------------------------------------------------
# Seule partie en pixels. Case (x, y) → rectangle au pixel (x * W, y * H).


def draw_tile(screen, tile, color):
    """Colorie la case `tile` = (x, y) : le seul endroit qui convertit en pixels."""
    # Une fonction pour damier, serpent et fruit : formule écrite une fois,
    # juste partout ou fausse partout (et ça se voit tout de suite).
    x, y = tile
    pg.draw.rect(screen, color, pg.Rect(x * W, y * H, W, H))


def draw(screen, snake, fruit):
    """Dessine toute l'image, en mémoire : damier, puis serpent, puis fruit."""
    # On redessine TOUT à chaque image : pas besoin d'effacer la queue à la
    # main, l'image d'avant est recouverte.
    screen.fill(LIGHT)
    # Damier : cases où x + y est impair en foncé. (x + y) % 2 vaut 0 ou 1,
    # et 0 est "faux" en Python.
    for x in range(X):
        for y in range(Y):
            if (x + y) % 2:
                draw_tile(screen, (x, y), DARK)
    # L'ordre compte : le dernier dessiné passe dessus.
    for tile in snake:
        draw_tile(screen, tile, SNAKE_COLOR)
    draw_tile(screen, fruit, FRUIT_COLOR)


# --- 3. boucle de jeu ----------------------------------------------------------


def main():
    """Lance une partie ; renvoie le score (la longueur du serpent)."""
    pg.init()
    screen = pg.display.set_mode((X * W, Y * H))  # taille déduite des constantes
    clock = pg.time.Clock()

    # L'état vit DANS `main`, pas au niveau du module : pas de globale, chaque
    # partie repart de zéro.
    snake = [(10, 15), (11, 15), (12, 15)]
    direction = RIGHT
    fruit = (10, 10)  # loin du serpent ; `random_fruit(snake)` marche aussi
    status = "quit"  # ce qui s'est passé au dernier tour
    pg.display.set_caption(f"Score : {len(snake)}")

    running = True
    while running:
        # Attend ce qu'il faut pour ne pas dépasser FPS images/s. Sans lui, le
        # serpent traverse l'écran en un éclair.
        clock.tick(FPS)

        # 1. événements depuis l'image précédente. À lire à chaque tour, sinon
        # la fenêtre "ne répond plus".
        for event in pg.event.get():
            if event.type == pg.QUIT:  # la croix
                running = False
            elif event.type == pg.KEYDOWN:  # une touche
                if event.key == pg.K_q:
                    running = False
                else:
                    direction = turn(direction, event.key)
        if not running:  # on quitte : pas de pas en plus
            break

        # 2. état : un pas, puis on réagit.
        status = move(snake, direction, fruit)
        if status == "ate":
            fruit = random_fruit(snake)
            pg.display.set_caption(f"Score : {len(snake)}")  # le score ne change qu'ici
        elif status in ("self-bite", "out-of-board"):
            break

        # 3. affichage : image en mémoire (rapide)...
        draw(screen, snake, fruit)
        # ... envoyée à l'écran une fois par tour (lent).
        pg.display.update()

    # Hors de la boucle, mais DANS `main` (indentation !).
    # Oublier `pg.quit()` = fenêtre fantôme possible, sous Windows surtout.
    pg.quit()
    print(f"Fin de partie ({status}), score : {len(snake)}")
    return len(snake)


# Ne tourne que si on lance ce fichier, pas sur `import snake` (les tests).
# Sans ce bloc, importer lancerait le jeu : le test de l'étape 0 le vérifie.
if __name__ == "__main__":
    main()


# --- pour aller plus loin : le demi-tour "impossible" ---------------------------
# Vers la droite, tape très vite ↑ puis ← entre deux images. Les deux touches
# arrivent dans le MÊME tour : `turn` accepte ↑ (→ UP), puis ← (pas un
# demi-tour par rapport à UP !). Au pas suivant, la tête recule dans le corps.
# Fix : comparer chaque touche à la direction du DERNIER PAS :
#
#     last = direction
#     for event in pg.event.get():
#         ...
#         new = turn(last, event.key)
#         if new != last:
#             direction = new
#
# Autre option : une seule touche prise en compte par image.
