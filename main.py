import numpy as np
import matplotlib.pyplot as plt
import random
import csv

from collections import deque, defaultdict

# =========================================================
# CONFIG
# =========================================================

CELL_M = 0.5

FREE = 0
WALL = 1
EXIT = 2
FIRE = 3

WIDTH = 0
HEIGHT = 0

grid = None
inside_mask = None

smoke = None

exits = []

MIN_X = 0
MIN_Y = 0
SCALE = 1

fire_events = defaultdict(list)
smoke_events = defaultdict(list)

distance_maps = {}

MAX_FIRE_REPLAY_TIME = 0

# =========================================================
# MÉTRICAS TEMPORALES
# =========================================================

metric_time = []

metric_evacuated = []
metric_dead = []
metric_injured = []
metric_alive = []

metric_avg_smoke = []
metric_avg_density = []

# =========================================================
# AGENTE
# =========================================================

class Agente:

    def __init__(
        self,
        x,
        y,
        age,
        sex,
        prior_visit,
        behavior_type,
        group_number,
        group_leader,
        initial_energy
    ):

        self.x = x
        self.y = y

        self.age = age
        self.sex = sex

        self.prior_visit = prior_visit

        self.behavior_type = behavior_type

        self.group_number = group_number
        self.group_leader = group_leader

        self.energy = initial_energy

        self.smoke_inhaled = 0

        self.alive = True
        self.evacuated = False

        self.injured = False

        self.panic = 0

        # =================================================
        # COMPORTAMIENTO SOCIAL
        # =================================================

        self.follow_group = random.random() < 0.65

        self.social_delay = random.uniform(0, 12)

        # =================================================
        # VISIÓN
        # =================================================

        self.vision_radius = random.randint(4, 8)

        self.last_direction = (0, 0)

        # =================================================
        # VELOCIDAD HUMANA
        # =================================================

        if age > 60:

            self.base_speed = 0.65

        elif age < 16:

            self.base_speed = 0.85

        else:

            self.base_speed = random.uniform(0.9, 1.15)

        # =================================================
        # REACCIÓN HUMANA
        # =================================================

        r = random.random()

        if r < 0.15:

            self.reaction_time = random.uniform(8, 18)

        elif r < 0.75:

            self.reaction_time = random.uniform(22, 50)

        else:

            self.reaction_time = random.uniform(55, 95)

        self.reaction_time += self.social_delay

        # =================================================
        # CONOCIMIENTO SALIDAS
        # =================================================

        if self.prior_visit:

            self.knows_exits = exits.copy()

        else:

            self.knows_exits = [random.choice(exits)]

        # =================================================
        # SALIDA PREFERIDA
        # =================================================

        if random.random() < 0.72:

            self.target_exit = exits[0]

        else:

            self.target_exit = random.choice(self.knows_exits)

# =========================================================
# WORLD -> GRID
# =========================================================

def world_to_grid(x, y):

    gx = int((x - MIN_X) * SCALE)
    gy = int((y - MIN_Y) * SCALE)

    return gx, gy

# =========================================================
# CARGAR LAYOUT
# =========================================================

def cargar_layout(path):

    global grid
    global inside_mask
    global exits
    global WIDTH
    global HEIGHT
    global MIN_X
    global MIN_Y
    global SCALE
    global smoke

    elementos = []
    exits = []

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

                x1 = float(row[1].strip())
                y1 = float(row[2].strip())

                x2 = float(row[3].strip())
                y2 = float(row[4].strip())

                elementos.append((tipo, x1, y1, x2, y2))

                min_x = min(min_x, x1, x2)
                min_y = min(min_y, y1, y2)

                max_x = max(max_x, x1, x2)
                max_y = max(max_y, y1, y2)

            except:
                continue

    MIN_X = min_x
    MIN_Y = min_y

    world_w = max_x - min_x
    world_h = max_y - min_y

    WIDTH = int(world_w / CELL_M)
    HEIGHT = int(world_h / CELL_M)

    SCALE = WIDTH / world_w

    print("WIDTH:", WIDTH)
    print("HEIGHT:", HEIGHT)

    grid = np.zeros((HEIGHT, WIDTH), dtype=np.int8)

    inside_mask = np.zeros((HEIGHT, WIDTH), dtype=bool)

    smoke = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    # =====================================================
    # DIBUJAR
    # =====================================================

    for tipo, x1, y1, x2, y2 in elementos:

        gx1, gy1 = world_to_grid(x1, y1)
        gx2, gy2 = world_to_grid(x2, y2)

        steps = max(abs(gx2 - gx1), abs(gy2 - gy1)) + 1

        for i in range(steps):

            x = int(gx1 + (gx2 - gx1) * i / steps)
            y = int(gy1 + (gy2 - gy1) * i / steps)

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:

                if tipo == "wall":

                    grid[y][x] = WALL

                elif tipo == "exit":

                    grid[y][x] = EXIT

                    exits.append((x, y))

    print("EXITS:", len(exits))

# =========================================================
# CALCULAR INTERIOR
# =========================================================

def calcular_interior():

    global inside_mask

    seed = None

    for y in range(HEIGHT):

        for x in range(WIDTH):

            if grid[y][x] == FREE:

                seed = (x, y)
                break

        if seed:
            break

    q = deque([seed])

    inside_mask[seed[1]][seed[0]] = True

    while q:

        x, y = q.popleft()

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:

                if not inside_mask[ny][nx]:

                    if grid[ny][nx] != WALL:

                        inside_mask[ny][nx] = True

                        q.append((nx, ny))

# =========================================================
# CARGAR AGENTES
# =========================================================

def cargar_agentes(path):

    agentes = []

    with open(path, encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            wx = float(row["x"])
            wy = float(row["y"])

            gx, gy = world_to_grid(wx, wy)

            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:

                a = Agente(
                    gx,
                    gy,
                    int(row["age"]),
                    row["sex"],
                    row["prior_visit"] == "TRUE",
                    int(row[" behavior_type"]),
                    int(row[" group_number"]),
                    int(row[" group_leader"]),
                    float(row["initial_energy"])
                )

                agentes.append(a)

    print("Agentes:", len(agentes))

    return agentes

# =========================================================
# FIRE REPLAY
# =========================================================

def cargar_fire(path):

    global fire_events
    global MAX_FIRE_REPLAY_TIME

    with open(path, encoding="utf-8") as f:

        reader = csv.reader(f)

        next(reader)

        for row in reader:

            if len(row) < 3:
                continue

            x = int(float(row[0]))
            y = int(float(row[1]))

            t = int(float(row[2]))

            MAX_FIRE_REPLAY_TIME = max(
                MAX_FIRE_REPLAY_TIME,
                t
            )

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:

                fire_events[t].append((x, y))

    print("Fire events:", len(fire_events))
    print("Max fire replay time:", MAX_FIRE_REPLAY_TIME)

# =========================================================
# SMOKE REPLAY
# =========================================================

def cargar_smoke(path):

    global smoke_events

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

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:

                smoke_events[t].append((x, y, density))

    print("Smoke events:", len(smoke_events))

# =========================================================
# ACTUALIZAR FUEGO
# =========================================================

def actualizar_fuego(t):

    if t not in fire_events:
        return

    for x, y in fire_events[t]:

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:

            grid[y][x] = FIRE

# =========================================================
# EXPANSIÓN FUEGO SUAVE Y REALISTA
# =========================================================

def expandir_fuego(t):

    if t <= MAX_FIRE_REPLAY_TIME:

        factor = 0.10

    else:

        factor = 1.0

    nuevos = []

    extra_time = max(
        0,
        t - MAX_FIRE_REPLAY_TIME
    )

    if extra_time < 40:

        prob_base = 0.0008

    elif extra_time < 80:

        prob_base = 0.0012

    elif extra_time < 140:

        prob_base = 0.0018

    else:

        prob_base = 0.0025

    prob_base *= factor

    fire_cells = np.argwhere(grid == FIRE)

    for fy, fx in fire_cells:

        vecinos = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]

        if random.random() < 0.08:

            vecinos.extend([
                (-1,-1),
                (1,-1),
                (-1,1),
                (1,1)
            ])

        for dx, dy in vecinos:

            nx = fx + dx
            ny = fy + dy

            if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                continue

            if grid[ny][nx] != FREE:
                continue

            p = prob_base

            if nx > WIDTH * 0.58:

                p *= 1.8

            p += smoke[ny][nx] * 0.00001

            walls = 0

            for ddx, ddy in [
                (-1,0),
                (1,0),
                (0,-1),
                (0,1)
            ]:

                wx = nx + ddx
                wy = ny + ddy

                if 0 <= wx < WIDTH and 0 <= wy < HEIGHT:

                    if grid[wy][wx] == WALL:
                        walls += 1

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

        grid[ny][nx] = FIRE

# =========================================================
# ACTUALIZAR HUMO
# =========================================================

def actualizar_smoke(t):

    if t in smoke_events:

        for x, y, density in smoke_events[t]:

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:

                smoke[y][x] = max(
                    smoke[y][x],
                    density * 3.0
                )

    nuevo = smoke.copy()

    for y in range(HEIGHT):

        for x in range(WIDTH):

            if grid[y][x] == WALL:
                continue

            total = smoke[y][x]
            count = 1

            for dx, dy in [
                (-1,0),
                (1,0),
                (0,-1),
                (0,1)
            ]:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:

                    if grid[ny][nx] != WALL:

                        total += smoke[ny][nx]
                        count += 1

            nuevo[y][x] = max(
                nuevo[y][x],
                total / count * 0.992
            )

    smoke[:] = nuevo

    fire_cells = np.argwhere(grid == FIRE)

    for fy, fx in fire_cells:

        smoke[fy][fx] += 10

        for dx in range(-3,4):
            for dy in range(-3,4):

                nx = fx + dx
                ny = fy + dy

                if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                    continue

                if grid[ny][nx] == WALL:
                    continue

                dist = np.sqrt(dx*dx + dy*dy)

                if dist == 0:
                    continue

                humo_extra = max(
                    0,
                    4.0 - dist
                )

                smoke[ny][nx] += humo_extra

# =========================================================
# BFS POR SALIDA
# =========================================================

def calcular_distance_maps():

    global distance_maps

    for exit_pos in exits:

        ex, ey = exit_pos

        distmap = np.full((HEIGHT, WIDTH), np.inf)

        q = deque()

        distmap[ey][ex] = 0

        q.append((ex, ey))

        while q:

            x, y = q.popleft()

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:

                    if grid[ny][nx] != WALL:

                        nd = distmap[y][x] + 1

                        if nd < distmap[ny][nx]:

                            distmap[ny][nx] = nd

                            q.append((nx, ny))

        distance_maps[exit_pos] = distmap

    print("Distance maps calculados")

# =========================================================
# DENSIDAD LOCAL
# =========================================================

def calcular_densidad_local(x, y, agentes):

    densidad = 0

    for other in agentes:

        if other.alive:

            dist = abs(other.x - x) + abs(other.y - y)

            if dist <= 1:
                densidad += 1

    return densidad

# =========================================================
# ELEGIR MEJOR SALIDA
# =========================================================

def elegir_mejor_salida(a):

    mejor = None
    mejor_score = float("inf")

    for e in exits:

        ex, ey = e

        d = distance_maps[e][a.y][a.x]

        if np.isinf(d):
            continue

        score = d

        score += smoke[ey][ex] * 10

        for dx in range(-2,3):
            for dy in range(-2,3):

                fx = ex + dx
                fy = ey + dy

                if 0 <= fx < WIDTH and 0 <= fy < HEIGHT:

                    if grid[fy][fx] == FIRE:
                        score += 250

        if score < mejor_score:

            mejor_score = score
            mejor = e

    return mejor

# =========================================================
# COMPORTAMIENTO SOCIAL
# =========================================================

def actualizar_comportamiento_social(a, agentes):

    if not a.follow_group:
        return

    vecinos = []

    for other in agentes:

        if other == a:
            continue

        if not other.alive:
            continue

        if other.group_number != a.group_number:
            continue

        dist = abs(other.x - a.x) + abs(other.y - a.y)

        if dist <= 6:

            vecinos.append(other)

    if len(vecinos) == 0:
        return

    salida_popular = defaultdict(int)

    for v in vecinos:

        salida_popular[v.target_exit] += 1

    mejor = max(
        salida_popular,
        key=salida_popular.get
    )

    a.target_exit = mejor

# =========================================================
# MOVIMIENTO HUMANO
# =========================================================

def mover(a, agentes, t):

    if t < a.reaction_time:
        return

    actualizar_comportamiento_social(a, agentes)

    humo_actual = smoke[a.y][a.x]

    # =====================================================
    # PÁNICO
    # =====================================================

    a.panic = 0

    if humo_actual > 20:
        a.panic += 1

    if humo_actual > 50:
        a.panic += 2

    for dx in range(-2,3):
        for dy in range(-2,3):

            nx = a.x + dx
            ny = a.y + dy

            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:

                if grid[ny][nx] == FIRE:
                    a.panic += 3

    # =====================================================
    # VELOCIDAD HUMANA
    # =====================================================

    move_prob = a.base_speed

    if humo_actual > 20:
        move_prob *= 0.65

    if humo_actual > 40:
        move_prob *= 0.40

    if humo_actual > 70:
        move_prob *= 0.18

    if a.injured:
        move_prob *= 0.55

    if a.panic >= 5:
        move_prob *= 1.2

    move_prob = min(move_prob, 1.0)

    if random.random() > move_prob:
        return

    # =====================================================
    # DUDA HUMANA
    # =====================================================

    hesitation = 0.05

    if a.panic >= 4:
        hesitation = 0.01

    if random.random() < hesitation:
        return

    # =====================================================
    # CROWD CRUSH
    # =====================================================

    densidad = calcular_densidad_local(
        a.x,
        a.y,
        agentes
    )

    if densidad >= 7:

        a.energy -= 0.5

        if random.random() < 0.80:
            return

    if densidad >= 9:

        a.energy -= 1.5

        a.injured = True

        if random.random() < 0.92:
            return

    nueva = elegir_mejor_salida(a)

    if nueva is not None:
        a.target_exit = nueva

    dirs = [
        (1,0),
        (-1,0),
        (0,1),
        (0,-1)
    ]

    random.shuffle(dirs)

    distmap = distance_maps[a.target_exit]

    best_score = float("inf")

    best_pos = (a.x, a.y)

    best_dir = (0,0)

    for dx, dy in dirs:

        nx = a.x + dx
        ny = a.y + dy

        if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
            continue

        if grid[ny][nx] == WALL:
            continue

        if grid[ny][nx] == FIRE:
            continue

        # =================================================
        # COLISIONES
        # =================================================

        occupied = False

        for other in agentes:

            if other.alive and other != a:

                if other.x == nx and other.y == ny:

                    occupied = True
                    break

        if occupied:
            continue

        score = distmap[ny][nx]

        score += smoke[ny][nx] * 8

        score += random.uniform(0, 4)

        if (dx,dy) == a.last_direction:
            score -= 2

        for dx2 in range(-2,3):
            for dy2 in range(-2,3):

                fx = nx + dx2
                fy = ny + dy2

                if 0 <= fx < WIDTH and 0 <= fy < HEIGHT:

                    if grid[fy][fx] == FIRE:
                        score += 90

        local_density = calcular_densidad_local(
            nx,
            ny,
            agentes
        )

        score += local_density * 7

        if score < best_score:

            best_score = score

            best_pos = (nx, ny)

            best_dir = (dx, dy)

    a.x, a.y = best_pos

    a.last_direction = best_dir

# =========================================================
# MÉTRICAS
# =========================================================

def guardar_metricas(t, agentes):

    evacuados = sum(a.evacuated for a in agentes)

    muertos = sum(
        (not a.alive) and (not a.evacuated)
        for a in agentes
    )

    heridos = sum(a.injured for a in agentes)

    vivos = sum(
        a.alive
        for a in agentes
    )

    metric_time.append(t)

    metric_evacuated.append(evacuados)
    metric_dead.append(muertos)
    metric_injured.append(heridos)
    metric_alive.append(vivos)

    metric_avg_smoke.append(
        float(np.mean(smoke))
    )

    total_density = 0

    for a in agentes:

        if a.alive:

            total_density += calcular_densidad_local(
                a.x,
                a.y,
                agentes
            )

    if vivos > 0:

        metric_avg_density.append(
            total_density / vivos
        )

    else:

        metric_avg_density.append(0)

# =========================================================
# EXPORTAR MÉTRICAS CSV
# =========================================================

def exportar_metricas():

    with open(
        "metricas_simulacion.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "tiempo",
            "evacuados",
            "muertos",
            "heridos",
            "vivos",
            "humo_promedio",
            "densidad_promedio"
        ])

        for i in range(len(metric_time)):

            writer.writerow([
                metric_time[i],
                metric_evacuated[i],
                metric_dead[i],
                metric_injured[i],
                metric_alive[i],
                metric_avg_smoke[i],
                metric_avg_density[i]
            ])

    print("Métricas exportadas")

# =========================================================
# RENDER
# =========================================================

def render(agentes, t):

    img = np.ones((HEIGHT, WIDTH, 3), dtype=np.float32)

    img[:, :] = [0.95, 0.95, 0.95]

    wall_mask = (grid == WALL)
    img[wall_mask] = [0.10, 0.10, 0.10]

    exit_mask = (grid == EXIT)
    img[exit_mask] = [0.0, 0.8, 0.2]

    # =====================================================
    # HUMO
    # =====================================================

    for y in range(HEIGHT):
        for x in range(WIDTH):

            s = smoke[y][x]

            if s > 0:

                alpha = min(s / 180.0, 0.80)

                smoke_color = np.array([0.30, 0.30, 0.30])

                img[y][x] = (
                    img[y][x] * (1 - alpha)
                    + smoke_color * alpha
                )

    # =====================================================
    # FUEGO
    # =====================================================

    fire_mask = (grid == FIRE)
    img[fire_mask] = [1.0, 0.30, 0.0]

    # =====================================================
    # PERSONAS
    # =====================================================

    for a in agentes:

        if not a.alive:
            continue

        if a.injured:

            color = [0.0, 0.7, 1.0]

        elif a.panic >= 5:

            color = [1.0, 0.0, 1.0]

        else:

            color = [0.0, 0.0, 1.0]

        img[a.y][a.x] = color

    plt.clf()

    plt.title(
        f"Tiempo: {t}s",
        fontsize=16
    )

    plt.imshow(img)

    plt.xticks([])
    plt.yticks([])

    plt.pause(0.01)

# =========================================================
# SIMULACIÓN
# =========================================================

def simular():

    agentes = cargar_agentes("people.csv")

    plt.figure(figsize=(12,8))

    for t in range(300):

        actualizar_fuego(t)

        expandir_fuego(t)

        actualizar_smoke(t)

        for a in agentes:

            if not a.alive:
                continue

            mover(a, agentes, t)

            # =================================================
            # HUMO
            # =================================================

            densidad = smoke[a.y][a.x]

            a.smoke_inhaled += densidad * 0.22

            a.energy -= densidad * 0.05

            # =================================================
            # HERIDOS
            # =================================================

            if (
                a.smoke_inhaled > 120
                or a.energy < 45
            ):

                a.injured = True

            # =================================================
            # MUERTE FUEGO
            # =================================================

            if grid[a.y][a.x] == FIRE:

                a.alive = False

            # =================================================
            # EVACUACIÓN
            # =================================================

            elif grid[a.y][a.x] == EXIT:

                a.evacuated = True
                a.alive = False

            # =================================================
            # MUERTE HUMO
            # =================================================

            elif (
                a.energy <= 0
                or a.smoke_inhaled > 260
            ):

                a.alive = False

        guardar_metricas(t, agentes)

        render(agentes, t)

    exportar_metricas()

    evacuados = sum(a.evacuated for a in agentes)

    muertos = sum(
        (not a.alive) and (not a.evacuated)
        for a in agentes
    )

    atrapados = sum(
        a.alive and not a.evacuated
        for a in agentes
    )

    heridos = sum(
        a.injured
        for a in agentes
    )

    print("================================")
    print("RESULTADOS")
    print("================================")

    print("Evacuados:", evacuados)
    print("Muertos:", muertos)
    print("Heridos:", heridos)
    print("Atrapados:", atrapados)

# =========================================================
# MAIN
# =========================================================

cargar_layout("building_nightclub.csv")

calcular_interior()

cargar_fire("fire_nightclub_merged.csv")

cargar_smoke("smoke.csv")

calcular_distance_maps()

simular()