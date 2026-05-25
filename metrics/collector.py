import csv
import numpy as np

from simulation.movement import calcular_densidad_local


class MetricsCollector:
    """
    Recolecta métricas en cada paso de la simulación
    y las exporta a CSV al final.
    """

    def __init__(self):
        self.time = []
        self.evacuated = []
        self.dead = []
        self.injured = []
        self.alive = []
        self.avg_smoke = []
        self.avg_density = []

    # ----------------------------------------------------------

    def record(self, t: int, agentes: list, world):
        """Guarda una fila de métricas para el segundo t."""
        evacuados = sum(a.evacuated for a in agentes)
        muertos = sum((not a.alive) and (not a.evacuated) for a in agentes)
        heridos = sum(a.injured for a in agentes)
        vivos = sum(a.alive for a in agentes)

        self.time.append(t)
        self.evacuated.append(evacuados)
        self.dead.append(muertos)
        self.injured.append(heridos)
        self.alive.append(vivos)
        self.avg_smoke.append(float(np.mean(world.smoke)))

        if vivos > 0:
            total_density = sum(
                calcular_densidad_local(a.x, a.y, agentes)
                for a in agentes if a.alive
            )
            self.avg_density.append(total_density / vivos)
        else:
            self.avg_density.append(0)

    # ----------------------------------------------------------

    def export(self, path: str):
        """Escribe el CSV de métricas en la ruta indicada."""
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "tiempo", "evacuados", "muertos",
                "heridos", "vivos", "humo_promedio", "densidad_promedio"
            ])
            for i in range(len(self.time)):
                writer.writerow([
                    self.time[i],
                    self.evacuated[i],
                    self.dead[i],
                    self.injured[i],
                    self.alive[i],
                    self.avg_smoke[i],
                    self.avg_density[i],
                ])
        print(f"Métricas exportadas → {path}")

    # ----------------------------------------------------------

    def print_summary(self, scenario_name: str):
        """Imprime un resumen final de la simulación."""
        print("\n" + "=" * 40)
        print(f"RESULTADOS: {scenario_name}")
        print("=" * 40)
        print(f"Evacuados : {self.evacuated[-1]}")
        print(f"Muertos   : {self.dead[-1]}")
        print(f"Heridos   : {self.injured[-1]}")
        print(f"Atrapados : {self.alive[-1]}")
        print("=" * 40 + "\n")
