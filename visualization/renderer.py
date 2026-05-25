import numpy as np
import matplotlib.pyplot as plt

from config.constants import WALL, EXIT, FIRE


class Renderer:
    """
    Visualización en tiempo real de la simulación
    usando Matplotlib.
    """

    def __init__(self, world, figsize=(12, 8)):
        self.world = world
        plt.figure(figsize=figsize)

    # ----------------------------------------------------------

    def render(self, agentes: list, t: int):
        world = self.world
        img = np.ones((world.height, world.width, 3), dtype=np.float32)

        # Fondo gris claro
        img[:, :] = [0.95, 0.95, 0.95]

        # Paredes
        img[world.grid == WALL] = [0.10, 0.10, 0.10]

        # Salidas
        img[world.grid == EXIT] = [0.0, 0.8, 0.2]

        # Humo (capa semitransparente)
        smoke_color = np.array([0.30, 0.30, 0.30])
        for y in range(world.height):
            for x in range(world.width):
                s = world.smoke[y][x]
                if s > 0:
                    alpha = min(s / 180.0, 0.80)
                    img[y][x] = img[y][x] * (1 - alpha) + smoke_color * alpha

        # Fuego
        img[world.grid == FIRE] = [1.0, 0.30, 0.0]

        # Personas
        for a in agentes:
            if not a.alive:
                continue
            if a.injured:
                color = [0.0, 0.7, 1.0]    # azul claro → herido
            elif a.panic >= 5:
                color = [1.0, 0.0, 1.0]    # magenta → pánico
            else:
                color = [0.0, 0.0, 1.0]    # azul → normal
            img[a.y][a.x] = color

        plt.clf()
        plt.title(f"Tiempo: {t}s", fontsize=16)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.pause(0.01)
