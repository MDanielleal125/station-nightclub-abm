import numpy as np
from collections import deque

from config.constants import FREE, WALL, EXIT, FIRE


class World:
    """
    Contiene el estado del entorno:
    grid, humo, salidas, máscara interior y mapas de distancia.
    """

    def __init__(self):
        self.grid = None
        self.smoke = None
        self.inside_mask = None
        self.exits = []

        self.width = 0
        self.height = 0

        self.min_x = 0.0
        self.min_y = 0.0
        self.scale = 1.0

        self.distance_maps = {}

    # ----------------------------------------------------------
    # Conversión coordenadas mundo → celda grid
    # ----------------------------------------------------------

    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        gx = int((x - self.min_x) * self.scale)
        gy = int((y - self.min_y) * self.scale)
        return gx, gy

    # ----------------------------------------------------------
    # Calcular interior con BFS desde la primera celda FREE
    # ----------------------------------------------------------

    def calcular_interior(self):
        seed = None

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == FREE:
                    seed = (x, y)
                    break
            if seed:
                break

        if seed is None:
            raise RuntimeError("No se encontró ninguna celda FREE en el grid.")

        q = deque([seed])
        self.inside_mask[seed[1]][seed[0]] = True

        while q:
            x, y = q.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.inside_mask[ny][nx] and self.grid[ny][nx] != WALL:
                        self.inside_mask[ny][nx] = True
                        q.append((nx, ny))

    # ----------------------------------------------------------
    # BFS desde cada salida → mapa de distancias
    # ----------------------------------------------------------

    def calcular_distance_maps(self):
        for exit_pos in self.exits:
            ex, ey = exit_pos
            distmap = np.full((self.height, self.width), np.inf)
            distmap[ey][ex] = 0

            q = deque([(ex, ey)])

            while q:
                x, y = q.popleft()
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.grid[ny][nx] != WALL:
                            nd = distmap[y][x] + 1
                            if nd < distmap[ny][nx]:
                                distmap[ny][nx] = nd
                                q.append((nx, ny))

            self.distance_maps[exit_pos] = distmap

        print(f"Distance maps calculados para {len(self.exits)} salidas.")

    # ----------------------------------------------------------
    # Aplicar salidas bloqueadas (de la config del escenario)
    # ----------------------------------------------------------

    def aplicar_blocked_exits(self, blocked_indices: list[int]):
        """Reemplaza salidas bloqueadas por WALL en el grid."""
        for idx in blocked_indices:
            if idx < len(self.exits):
                ex, ey = self.exits[idx]
                self.grid[ey][ex] = WALL
        # Reconstruir lista de salidas activas
        self.exits = [
            e for i, e in enumerate(self.exits)
            if i not in blocked_indices
        ]
        if blocked_indices:
            print(f"Salidas bloqueadas: índices {blocked_indices}. Activas: {len(self.exits)}")
