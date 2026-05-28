import random
import numpy as np
from collections import defaultdict
from config.constants import FREE, FIRE, WALL
from scipy.ndimage import convolve


class FireSimulation:
    """
    Maneja el replay histórico del fuego y su expansión
    probabilística una vez terminado el replay.
    """

    def __init__(self):
        self.fire_events: dict[int, list] = defaultdict(list)
        self.max_replay_time: int = 0

        # Precomputed wall-neighbor count array, built once on first call to expandir().
        # Reused every step — the wall layout never changes.
        self._wall_neighbor_count = None

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

    def _build_wall_neighbor_count(self, world):

        wall_mask = (world.grid == WALL).astype(np.int8)
        kernel = np.array([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]], dtype=np.int8)
        # mode='constant', cval=0 → out-of-bounds cells don't count as walls
        self._wall_neighbor_count = convolve(
            wall_mask, kernel, mode='constant', cval=0
        ).astype(np.int8)

    # ----------------------------------------------------------

    def expandir(self, world, t: int, cfg: dict):
        """
        Expansión probabilística del fuego.
        Durante el replay usa factor bajo; después escala.
        """

        # --- Lazy-build the wall neighbor count cache ---
        if self._wall_neighbor_count is None:
            self._build_wall_neighbor_count(world)

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

        # --- Precompute probability grid ---

        # Start with prob_base broadcast across the whole grid
        p_grid = np.full((world.height, world.width), prob_base, dtype=np.float64)

        # Right-zone multiplier: nx > width * 0.58
        xs = np.arange(world.width)
        right_zone = (xs > world.width * 0.58).astype(np.float64)  # shape (W,)
        right_zone[right_zone == 1] = 1.8
        right_zone[right_zone == 0] = 1.0
        p_grid *= right_zone  # broadcasts (W,) across all H rows correctly


        # Smoke contribution: same formula, vectorized
        p_grid += world.smoke * 0.00001

        # Wall-neighbor multiplier (cached array)
        walls = self._wall_neighbor_count
        p_grid[walls >= 3] *= 0.12
        p_grid[(walls == 2)] *= 0.40

        if extra_time > 100:
            p_grid *= 1.2
        if extra_time > 180:
            p_grid *= 1.35

        # --- Fire expansion loop ---
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

                # O(1) lookup instead of recomputing from scratch
                p = p_grid[ny][nx]

                if random.random() < p:
                    nuevos.append((nx, ny))

        for nx, ny in nuevos:
            world.grid[ny][nx] = FIRE