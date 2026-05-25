import csv
import random
import numpy as np

from config.constants import CELL_M, FREE, WALL, EXIT
from simulation.world import World
from simulation.agent import Agente


# =========================================================
# CARGAR LAYOUT
# =========================================================

def cargar_layout(path: str) -> World:
    """
    Lee el CSV del edificio y construye el World:
    grid de celdas, lista de salidas, dimensiones.
    """
    world = World()
    elementos = []

    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                if len(row) < 5:
                    continue
                tipo = row[0].strip().lower()
                x1, y1 = float(row[1]), float(row[2])
                x2, y2 = float(row[3]), float(row[4])
                elementos.append((tipo, x1, y1, x2, y2))
                min_x = min(min_x, x1, x2)
                min_y = min(min_y, y1, y2)
                max_x = max(max_x, x1, x2)
                max_y = max(max_y, y1, y2)
            except Exception:
                continue

    world.min_x = min_x
    world.min_y = min_y

    world_w = max_x - min_x
    world_h = max_y - min_y

    world.width = int(world_w / CELL_M)
    world.height = int(world_h / CELL_M)
    world.scale = world.width / world_w

    print(f"Grid: {world.width}×{world.height} celdas")

    world.grid = np.zeros((world.height, world.width), dtype=np.int8)
    world.inside_mask = np.zeros((world.height, world.width), dtype=bool)
    world.smoke = np.zeros((world.height, world.width), dtype=np.float32)

    # Dibujar paredes y salidas
    for tipo, x1, y1, x2, y2 in elementos:
        gx1, gy1 = world.world_to_grid(x1, y1)
        gx2, gy2 = world.world_to_grid(x2, y2)
        steps = max(abs(gx2 - gx1), abs(gy2 - gy1)) + 1

        for i in range(steps):
            x = int(gx1 + (gx2 - gx1) * i / steps)
            y = int(gy1 + (gy2 - gy1) * i / steps)

            if 0 <= x < world.width and 0 <= y < world.height:
                if tipo == "wall":
                    world.grid[y][x] = WALL
                elif tipo == "exit":
                    world.grid[y][x] = EXIT
                    world.exits.append((x, y))

    print(f"Salidas encontradas: {len(world.exits)}")
    return world


# =========================================================
# CARGAR AGENTES
# =========================================================

def cargar_agentes(path: str, world: World, cfg: dict) -> list:
    """
    Lee el CSV de personas y crea objetos Agente.
    Aplica los parámetros del escenario (follow_group_prob,
    reaction_time_multiplier).
    """
    agentes = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            wx = float(row["x"])
            wy = float(row["y"])
            gx, gy = world.world_to_grid(wx, wy)

            if 0 <= gx < world.width and 0 <= gy < world.height:
                a = Agente(
                    x=gx,
                    y=gy,
                    age=int(row["age"]),
                    sex=row["sex"],
                    prior_visit=row["prior_visit"] == "TRUE",
                    behavior_type=int(row[" behavior_type"]),
                    group_number=int(row[" group_number"]),
                    group_leader=int(row[" group_leader"]),
                    initial_energy=float(row["initial_energy"]),
                    exits=world.exits,
                    cfg=cfg,
                )
                agentes.append(a)

    # Escenario 2: alta congestión → duplicar agentes si hace falta
    n_target = cfg["n_agents"]
    while len(agentes) < n_target and len(agentes) > 0:
        base = random.choice(agentes)
        clon = Agente(
            x=base.x + random.randint(-2, 2),
            y=base.y + random.randint(-2, 2),
            age=base.age,
            sex=base.sex,
            prior_visit=base.prior_visit,
            behavior_type=base.behavior_type,
            group_number=base.group_number,
            group_leader=base.group_leader,
            initial_energy=base.energy,
            exits=world.exits,
            cfg=cfg,
        )
        # Asegurar que el clon esté dentro del grid
        clon.x = max(0, min(world.width - 1, clon.x))
        clon.y = max(0, min(world.height - 1, clon.y))
        agentes.append(clon)

    print(f"Agentes cargados: {len(agentes)} (objetivo: {n_target})")
    return agentes
