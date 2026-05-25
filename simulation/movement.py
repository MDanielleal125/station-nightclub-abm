import random
import numpy as np
from collections import defaultdict

from config.constants import WALL, FIRE


# =========================================================
# DENSIDAD LOCAL
# =========================================================

def calcular_densidad_local(x: int, y: int, agentes: list) -> int:
    """Cuenta agentes vivos en radio Manhattan ≤ 1."""
    return sum(
        1 for a in agentes
        if a.alive and abs(a.x - x) + abs(a.y - y) <= 1
    )


# =========================================================
# ELEGIR MEJOR SALIDA
# =========================================================

def elegir_mejor_salida(agente, world):
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

        # Penalizar si hay fuego cerca de la salida
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                fx, fy = ex + dx, ey + dy
                if 0 <= fx < world.width and 0 <= fy < world.height:
                    if world.grid[fy][fx] == FIRE:
                        score += 250

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

def mover(agente, agentes: list, world, t: int):
    """
    Ejecuta un paso de movimiento para el agente:
    1. Verifica tiempo de reacción
    2. Actualiza comportamiento social
    3. Calcula pánico
    4. Ajusta velocidad por humo / lesiones
    5. Evalúa crowd crush
    6. Elige la mejor celda adyacente hacia la salida
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

    for dx in range(-2, 3):
        for dy in range(-2, 3):
            nx, ny = agente.x + dx, agente.y + dy
            if 0 <= nx < world.width and 0 <= ny < world.height:
                if world.grid[ny][nx] == FIRE:
                    agente.panic += 3

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
    densidad = calcular_densidad_local(agente.x, agente.y, agentes)

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
    nueva = elegir_mejor_salida(agente, world)
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

        # Evitar colisiones
        if any(a.alive and a != agente and a.x == nx and a.y == ny for a in agentes):
            continue

        score = distmap[ny][nx]
        score += world.smoke[ny][nx] * 8
        score += random.uniform(0, 4)

        if (dx, dy) == agente.last_direction:
            score -= 2  # momentum: premiar continuar en misma dirección

        # Penalizar celdas cerca del fuego
        for dx2 in range(-2, 3):
            for dy2 in range(-2, 3):
                fx, fy = nx + dx2, ny + dy2
                if 0 <= fx < world.width and 0 <= fy < world.height:
                    if world.grid[fy][fx] == FIRE:
                        score += 90

        score += calcular_densidad_local(nx, ny, agentes) * 7

        if score < best_score:
            best_score = score
            best_pos = (nx, ny)
            best_dir = (dx, dy)

    agente.x, agente.y = best_pos
    agente.last_direction = best_dir
