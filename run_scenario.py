"""
Punto de entrada para correr un escenario individual.

Uso:
    python run_scenario.py --scenario 1
    python run_scenario.py --scenario 3 --no-render
    python run_scenario.py --scenario 4 --steps 200
"""

import argparse
import os

from config.scenarios import get_scenario
from config.constants import EXIT, FIRE
from data_io.loaders import cargar_layout, cargar_agentes
from simulation.fire import FireSimulation
from simulation.smoke import SmokeSimulation
from simulation.movement import mover
from metrics.collector import MetricsCollector
from visualization.renderer import Renderer


def main():
    parser = argparse.ArgumentParser(description="Station Nightclub ABM")
    parser.add_argument(
        "--scenario", type=int, default=1,
        help="Número de escenario a correr (1-6)"
    )
    parser.add_argument(
        "--no-render", action="store_true",
        help="Desactivar visualización (más rápido)"
    )
    parser.add_argument(
        "--steps", type=int, default=None,
        help="Número de pasos de simulación (sobreescribe config)"
    )
    args = parser.parse_args()

    # ----------------------------------------------------------
    # Configuración
    # ----------------------------------------------------------
    cfg = get_scenario(args.scenario)
    if args.steps:
        cfg = {**cfg, "simulation_steps": args.steps}

    print(f"\n{'='*50}")
    print(f"  {cfg['name']}")
    print(f"{'='*50}\n")

    # ----------------------------------------------------------
    # Cargar mundo
    # ----------------------------------------------------------
    world = cargar_layout(os.path.join("data", "building_nightclub.csv"))
    world.calcular_interior()
    world.aplicar_blocked_exits(cfg["blocked_exits"])

    # ----------------------------------------------------------
    # Cargar fuego y humo
    # ----------------------------------------------------------
    fire_sim = FireSimulation()
    fire_sim.cargar_eventos(os.path.join("data", "fire_nightclub_merged.csv"), world)

    smoke_sim = SmokeSimulation()
    smoke_sim.cargar_eventos(os.path.join("data", "smoke.csv"), world)

    # ----------------------------------------------------------
    # Calcular mapas de distancia
    # ----------------------------------------------------------
    world.calcular_distance_maps()

    # ----------------------------------------------------------
    # Cargar agentes
    # ----------------------------------------------------------
    agentes = cargar_agentes(os.path.join("data", "people.csv"), world, cfg)

    # ----------------------------------------------------------
    # Inicializar métricas y renderer
    # ----------------------------------------------------------
    metrics = MetricsCollector()
    renderer = Renderer(world) if (cfg["render"] and not args.no_render) else None

    # ----------------------------------------------------------
    # Loop principal
    # ----------------------------------------------------------
    steps = cfg["simulation_steps"]

    for t in range(steps):

        # Fuego
        fire_sim.actualizar(world, t)
        fire_sim.expandir(world, t, cfg)

        # Humo
        smoke_sim.actualizar(world, t, cfg)

        # Agentes
        for a in agentes:
            if not a.alive:
                continue

            mover(a, agentes, world, t)

            # Efectos del humo en el agente
            densidad = world.smoke[a.y][a.x]
            a.smoke_inhaled += densidad * 0.22
            a.energy -= densidad * 0.05

            # Heridos por humo o energía baja
            if a.smoke_inhaled > 120 or a.energy < 45:
                a.injured = True

            # Muerte por fuego
            if world.grid[a.y][a.x] == FIRE:
                a.alive = False

            # Evacuación
            elif world.grid[a.y][a.x] == EXIT:
                a.evacuated = True
                a.alive = False

            # Muerte por humo extremo o energía agotada
            elif a.energy <= 0 or a.smoke_inhaled > 260:
                a.alive = False

        # Métricas y render
        metrics.record(t, agentes, world)

        if renderer:
            renderer.render(agentes, t)

    # ----------------------------------------------------------
    # Exportar resultados
    # ----------------------------------------------------------
    os.makedirs("results", exist_ok=True)
    metrics.export(f"results/scenario_{args.scenario}.csv")
    metrics.print_summary(cfg["name"])


if __name__ == "__main__":
    main()
