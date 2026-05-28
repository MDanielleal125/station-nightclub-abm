import numpy as np
from collections import defaultdict
from scipy.ndimage import convolve
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

        wall_mask = (world.grid == WALL)

        # Walls contribute 0 to both sum and count
        smoke_no_wall = np.where(wall_mask, 0.0, world.smoke)
        passable      = (~wall_mask).astype(np.float64)

        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.float64)

        smoke_sum = convolve(smoke_no_wall, kernel, mode='constant', cval=0.0)
        count_sum = convolve(passable,      kernel, mode='constant', cval=0.0)
        count_sum = np.maximum(count_sum, 1.0)  # avoid div/0 on isolated cells

        averaged = smoke_sum / count_sum * decay

        world.smoke = np.where(wall_mask, world.smoke, np.maximum(world.smoke, averaged))

        # --- Humo desde el fuego ---

        fire_cells = np.argwhere(world.grid == FIRE)

        if len(fire_cells) > 0:
            # Vectorized self-increment for all fire cells at once
            world.smoke[fire_cells[:, 0], fire_cells[:, 1]] += 10

            # Precompute the 7×7 contribution kernel once (matches original formula)
            r = 3
            size = 2 * r + 1  # 7
            ys, xs = np.ogrid[-r:r+1, -r:r+1]
            dist_kernel = np.sqrt(xs**2 + ys**2)
            contrib_kernel = np.maximum(0.0, 4.0 - dist_kernel)
            contrib_kernel[r, r] = 0.0  # original skips dist==0

            for fy, fx in fire_cells:
                # Compute the valid slice bounds (handles edges of the grid)
                y0 = max(0, fy - r);  y1 = min(world.height, fy + r + 1)
                x0 = max(0, fx - r);  x1 = min(world.width,  fx + r + 1)

                # Corresponding slice of the kernel
                ky0 = y0 - (fy - r);  ky1 = ky0 + (y1 - y0)
                kx0 = x0 - (fx - r);  kx1 = kx0 + (x1 - x0)

                kernel_slice = contrib_kernel[ky0:ky1, kx0:kx1]

                # Apply only to non-wall cells (original: `if world.grid[ny][nx] == WALL: continue`)
                non_wall = (world.grid[y0:y1, x0:x1] != WALL)
                world.smoke[y0:y1, x0:x1] += kernel_slice * non_wall