# Cada escenario hereda los parámetros base y sobreescribe solo los valores que cambia.

BASE = {
    "name": "Escenario 1 — Base",
    # Agentes
    "n_agents": 465,
    "follow_group_prob": 0.65,
    "reaction_time_multiplier": 1.0,
    # Humo
    "smoke_density_multiplier": 3.0,
    "smoke_diffusion_decay": 0.992,
    # Fuego
    "fire_expansion_factor": 1.0,
    # Salidas bloqueadas (índices de la lista exits[])
    "blocked_exits": [],
    # Visualización
    "render": True,
    "simulation_steps": 300,
}

SCENARIOS = {
    1: BASE,

    2: {
        **BASE,
        "name": "Escenario 2 — Alta congestión",
        "n_agents": 700,
    },

    3: {
        **BASE,
        "name": "Escenario 3 — Más humo",
        "smoke_density_multiplier": 6.0,
        "smoke_diffusion_decay": 0.998,
    },

    4: {
        **BASE,
        "name": "Escenario 4 — Salidas bloqueadas",
        "blocked_exits": [0, 1],   # bloquea las dos primeras salidas
    },

    5: {
        **BASE,
        "name": "Escenario 5 — Comportamiento grupal fuerte",
        "follow_group_prob": 0.90,
    },

    6: {
        **BASE,
        "name": "Escenario 6 — Reacción tardía",
        "reaction_time_multiplier": 2.0,
    },
}


def get_scenario(n: int) -> dict:
    """Retorna la configuración del escenario n (1-6)."""
    if n not in SCENARIOS:
        raise ValueError(f"Escenario {n} no existe. Opciones: {list(SCENARIOS.keys())}")
    return SCENARIOS[n]
