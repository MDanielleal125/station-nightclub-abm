import random
import numpy as np
from collections import defaultdict
from scipy.ndimage import convolve as ndconvolve

from config.constants import WALL, FIRE

def build_step_arrays(agentes: list, world):
    """
    Builds the two per-step precomputed arrays.  Call once per
    simulation step, before the agent loop.
    """
    # --- occupancy ---
    occupancy = np.zeros((world.height, world.width), dtype=np.int16)
    for a in agentes:
        if a.alive:
            occupancy[a.y][a.x] += 1

    # --- fire_score ---

    
    fire_grid = (world.grid == FIRE).astype(np.float32)
    kernel_5x5 = np.ones((5, 5), dtype=np.float32)
    fire_score = ndconvolve(fire_grid, kernel_5x5, mode='constant', cval=0)

    return occupancy, fire_score


# =========================================================
# DENSIDAD LOCAL
# =========================================================

def calcular_densidad_local(x: int, y: int, occupancy: np.ndarray, world) -> int:
    """Cuenta agentes vivos en radio Manhattan <= 1."""
    total = int(occupancy[y][x])
    if y > 0:
        total += int(occupancy[y - 1][x])
    if y < world.height - 1:
        total += int(occupancy[y + 1][x])
    if x > 0:
        total += int(occupancy[y][x - 1])
    if x < world.width - 1:
        total += int(occupancy[y][x + 1])
    return total


# =========================================================
# ELEGIR MEJOR SALIDA
# =========================================================

def elegir_mejor_salida(agente, world, fire_score: np.ndarray):
    """
    Evalúa cada salida conocida por el agente con un score
    que combina distancia, humo y fuego cercano.
    """
    mejor = None
    mejor_score = float("inf")

    for e in world.exits:
        ex, ey = e
        d = world.distance_maps[e][agente.y][agente.x]

        if np.isinf(d):
            continue

        score = d
        score += world.smoke[ey][ex] * 10

        score += fire_score[ey][ex] * 250

        if score < mejor_score:
            mejor_score = score
            mejor = e

    return mejor


# =========================================================
# COMPORTAMIENTO SOCIAL
# =========================================================

def actualizar_comportamiento_social(agente, agentes: list):
    """
    Si el agente sigue a su grupo, adopta la salida más
    popular entre sus vecinos del mismo grupo (radio 6).
    """
    if not agente.follow_group:
        return

    vecinos = [
        a for a in agentes
        if a != agente
        and a.alive
        and a.group_number == agente.group_number
        and abs(a.x - agente.x) + abs(a.y - agente.y) <= 6
    ]

    if not vecinos:
        return

    salida_popular = defaultdict(int)
    for v in vecinos:
        salida_popular[v.target_exit] += 1

    agente.target_exit = max(salida_popular, key=salida_popular.get)


# =========================================================
# MOVIMIENTO PRINCIPAL
# =========================================================

def mover(agente, agentes: list, world, t: int,
          occupancy: np.ndarray, fire_score: np.ndarray):
    """
    Executes one movement step for the agent.
    """
    if t < agente.reaction_time:
        return

    actualizar_comportamiento_social(agente, agentes)

    humo_actual = world.smoke[agente.y][agente.x]

    # --- Pánico ---
    agente.panic = 0
    if humo_actual > 20:
        agente.panic += 1
    if humo_actual > 50:
        agente.panic += 2

    agente.panic += int(fire_score[agente.y][agente.x] * 3)

    # --- Velocidad de movimiento ---
    move_prob = agente.base_speed

    if humo_actual > 20:
        move_prob *= 0.65
    if humo_actual > 40:
        move_prob *= 0.40
    if humo_actual > 70:
        move_prob *= 0.18
    if agente.injured:
        move_prob *= 0.55
    if agente.panic >= 5:
        move_prob *= 1.2

    move_prob = min(move_prob, 1.0)

    if random.random() > move_prob:
        return

    # --- Duda (hesitation) ---
    hesitation = 0.01 if agente.panic >= 4 else 0.05
    if random.random() < hesitation:
        return

    # --- Crowd crush ---
    densidad = calcular_densidad_local(agente.x, agente.y, occupancy, world)

    if densidad >= 7:
        agente.energy -= 0.5
        if random.random() < 0.80:
            return

    if densidad >= 9:
        agente.energy -= 1.5
        agente.injured = True
        if random.random() < 0.92:
            return

    # --- Actualizar salida objetivo ---
    nueva = elegir_mejor_salida(agente, world, fire_score)
    if nueva is not None:
        agente.target_exit = nueva

    # --- Evaluar celdas adyacentes ---
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(dirs)

    distmap = world.distance_maps[agente.target_exit]
    best_score = float("inf")
    best_pos = (agente.x, agente.y)
    best_dir = (0, 0)

    for dx, dy in dirs:
        nx, ny = agente.x + dx, agente.y + dy

        if not (0 <= nx < world.width and 0 <= ny < world.height):
            continue
        if world.grid[ny][nx] == WALL:
            continue
        if world.grid[ny][nx] == FIRE:
            continue
        if occupancy[ny][nx] > 0:
            continue

        score = distmap[ny][nx]
        score += world.smoke[ny][nx] * 8
        score += random.uniform(0, 4)

        if (dx, dy) == agente.last_direction:
            score -= 2
        score += fire_score[ny][nx] * 90

        score += calcular_densidad_local(nx, ny, occupancy, world) * 7

        if score < best_score:
            best_score = score
            best_pos = (nx, ny)
            best_dir = (dx, dy)

    agente.x, agente.y = best_pos
    agente.last_direction = best_dir