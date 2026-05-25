import random
import numpy as np
from collections import defaultdict

from config.constants import FREE, FIRE


class FireSimulation:
    """
    Maneja el replay histórico del fuego y su expansión
    probabilística una vez terminado el replay.
    """

    def __init__(self):
        self.fire_events: dict[int, list] = defaultdict(list)
        self.max_replay_time: int = 0

    def cargar_eventos(self, path: str, world):
        """Lee el CSV de eventos de fuego y los indexa por segundo."""
        import csv
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 3:
                    continue
                x = int(float(row[0]))
                y = int(float(row[1]))
                t = int(float(row[2]))
                self.max_replay_time = max(self.max_replay_time, t)
                if 0 <= x < world.width and 0 <= y < world.height:
                    self.fire_events[t].append((x, y))

        print(f"Fire events cargados: {len(self.fire_events)} pasos")
        print(f"Max replay time: {self.max_replay_time}s")

    # ----------------------------------------------------------

    def actualizar(self, world, t: int):
        """Aplica los eventos de fuego del segundo t al grid."""
        if t not in self.fire_events:
            return
        for x, y in self.fire_events[t]:
            if 0 <= x < world.width and 0 <= y < world.height:
                world.grid[y][x] = FIRE

    # ----------------------------------------------------------

    def expandir(self, world, t: int, cfg: dict):
        """
        Expansión probabilística del fuego.
        Durante el replay usa factor bajo; después escala.
        """
        factor = cfg["fire_expansion_factor"]

        if t <= self.max_replay_time:
            factor *= 0.10

        extra_time = max(0, t - self.max_replay_time)

        if extra_time < 40:
            prob_base = 0.0008
        elif extra_time < 80:
            prob_base = 0.0012
        elif extra_time < 140:
            prob_base = 0.0018
        else:
            prob_base = 0.0025

        prob_base *= factor

        nuevos = []
        fire_cells = np.argwhere(world.grid == FIRE)

        for fy, fx in fire_cells:
            vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            if random.random() < 0.08:
                vecinos.extend([(-1, -1), (1, -1), (-1, 1), (1, 1)])

            for dx, dy in vecinos:
                nx, ny = fx + dx, fy + dy

                if not (0 <= nx < world.width and 0 <= ny < world.height):
                    continue
                if world.grid[ny][nx] != FREE:
                    continue

                p = prob_base

                # Zona derecha del edificio: mayor riesgo
                if nx > world.width * 0.58:
                    p *= 1.8

                p += world.smoke[ny][nx] * 0.00001

                # Paredes alrededor frenan la expansión
                walls = sum(
                    1
                    for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= nx + ddx < world.width
                    and 0 <= ny + ddy < world.height
                    and world.grid[ny + ddy][nx + ddx] == 1
                )

                if walls >= 3:
                    p *= 0.12
                elif walls == 2:
                    p *= 0.40

                if extra_time > 100:
                    p *= 1.2
                if extra_time > 180:
                    p *= 1.35

                if random.random() < p:
                    nuevos.append((nx, ny))

        for nx, ny in nuevos:
            world.grid[ny][nx] = FIRE
