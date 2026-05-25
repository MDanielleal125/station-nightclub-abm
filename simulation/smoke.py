import numpy as np
from collections import defaultdict

from config.constants import WALL, FIRE


class SmokeSimulation:
    """
    Maneja el replay histórico del humo y su difusión
    física simplificada entre celdas.
    """

    def __init__(self):
        self.smoke_events: dict[int, list] = defaultdict(list)

    def cargar_eventos(self, path: str, world):
        """Lee el CSV de eventos de humo y los indexa por segundo."""
        import csv
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 4:
                    continue
                x = int(float(row[0]) / 10)
                y = int(float(row[1]) / 10)
                t = int(float(row[2]))
                density = float(row[3])
                if 0 <= x < world.width and 0 <= y < world.height:
                    self.smoke_events[t].append((x, y, density))

        print(f"Smoke events cargados: {len(self.smoke_events)} pasos")

    # ----------------------------------------------------------

    def actualizar(self, world, t: int, cfg: dict):
        """
        1. Aplica replay de humo del segundo t.
        2. Difunde el humo entre celdas vecinas.
        3. Genera humo adicional desde las celdas en llamas.
        """
        multiplier = cfg["smoke_density_multiplier"]
        decay = cfg["smoke_diffusion_decay"]

        # --- Replay ---
        if t in self.smoke_events:
            for x, y, density in self.smoke_events[t]:
                if 0 <= x < world.width and 0 <= y < world.height:
                    world.smoke[y][x] = max(
                        world.smoke[y][x],
                        density * multiplier
                    )

        # --- Difusión ---
        nuevo = world.smoke.copy()

        for y in range(world.height):
            for x in range(world.width):
                if world.grid[y][x] == WALL:
                    continue

                total = world.smoke[y][x]
                count = 1

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < world.width and 0 <= ny < world.height:
                        if world.grid[ny][nx] != WALL:
                            total += world.smoke[ny][nx]
                            count += 1

                nuevo[y][x] = max(
                    nuevo[y][x],
                    total / count * decay
                )

        world.smoke[:] = nuevo

        # --- Humo desde el fuego ---
        fire_cells = np.argwhere(world.grid == FIRE)

        for fy, fx in fire_cells:
            world.smoke[fy][fx] += 10

            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    nx, ny = fx + dx, fy + dy
                    if not (0 <= nx < world.width and 0 <= ny < world.height):
                        continue
                    if world.grid[ny][nx] == WALL:
                        continue
                    dist = np.sqrt(dx * dx + dy * dy)
                    if dist == 0:
                        continue
                    world.smoke[ny][nx] += max(0, 4.0 - dist)
