"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math  # noqa: F401 (servira à l'étape 2)
import random  # noqa: F401 (servira à l'étape 4)
from pathlib import Path

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.ALMOND

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sky.png"  # le décor (étape 9)

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)

EVERYTHING = []

# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.


class Boid(arcade.Sprite):
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, others=None):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed=speed
        self.turning=0
        self.others = others if others is not None else []

    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        if self.neighbours(EVERYTHING):
            self.alpha = 127
        else:
            self.alpha = 255
        self.angle += self.turning * TURN_SPEED * delta_time
        self.angle += random.uniform(-NOISE,NOISE)
        rad = math.radians(self.angle)
        self.center_x += self.speed * delta_time * math.cos(rad)
        self.center_y += self.speed * delta_time * math.sin(rad)
        dx, dy = self.separation(EVERYTHING)
        self.center_x = (self.center_x + dx)%WIDTH
        self.center_y = (self.center_y + dy)%HEIGHT

    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        return [other for other in others if other is not self and math.dist(self.position, other.position) < radius]

    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        dx,dy=0,0
        for other in self.neighbours(others, radius):
            d = math.dist(self.position, other.position)
            delta = 0.5 * (1 - d / radius)
            dx += (self.center_x - other.center_x) * delta
            dy += (self.center_y - other.center_y) * delta
        return dx,dy

class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""

    def __init__(self, x, y):
        super().__init__(OBSTACLE, center_x=x, center_y=y)


def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    boids=[]
    for i in range (n) :
        x = random.uniform(0, 800)
        y = random.uniform(0, 800)
        angle = random.uniform(0, 360)
        boids.append(Boid(x, y, angle, others=others))
    return boids
        


def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    obstacles = []
    pas_x = WIDTH / n
    pas_y = HEIGHT / n
    for i in range(n):
        for j in range(n):
            x = (i + 0.5) * pas_x
            y = (j + 0.5) * pas_y
            obstacles.append(Obstacle(x, y))
    return obstacles


# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale

        # pour l'instant, un simple Sprite : une image posée en (100, 100),
        # comptés depuis le coin en bas à gauche
        #boid = arcade.Sprite(ARROW, center_x=100, center_y=100)
        # une SpriteList : une liste de sprites, qu'arcade dessine d'un coup
        
        global EVERYTHING
        EVERYTHING.clear()
        self.obstacles = arcade.SpriteList()
        self.obstacles.extend(obstacle_grid(GRID))
         
        self.boids = arcade.SpriteList()
        self.boids.extend(random_boids(N_BOIDS))

        EVERYTHING.extend(self.obstacles)
        EVERYTHING.extend(self.boids)



    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            for boid in self.boids:
                boid.turning = -1
        elif symbol == arcade.key.RIGHT:
            for boid in self.boids:
                boid.turning = 1
        elif symbol == arcade.key.Q:
            self.close()

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            for boid in self.boids:
                boid.turning = 0

    def on_update(self, delta_time):
        self.boids.update(delta_time)

    def on_draw(self):
        self.clear()
        self.obstacles.draw()
        self.boids.draw()


def main():
    MyWindow()
    arcade.run()

# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
