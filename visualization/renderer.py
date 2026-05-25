import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from config.constants import WALL, EXIT, FIRE


def _elegir_backend():
    """
    Intenta backends interactivos en orden de preferencia.
    Si ninguno funciona, cae a Agg (sin ventana).
    """
    for backend in ["TkAgg", "Qt5Agg", "Qt6Agg", "wxAgg"]:
        try:
            matplotlib.use(backend)
            import matplotlib.pyplot as _plt
            _plt.figure()
            _plt.close()
            return backend
        except Exception:
            continue
    matplotlib.use("Agg")
    return "Agg"


class Renderer:
    """
    Visualización en tiempo real de la simulación usando Matplotlib.
    Si no hay display disponible (WSL, servidor), guarda frames en /tmp/abm_frames/.
    """

    def __init__(self, world, figsize=(12, 8)):
        self.world = world
        self.backend = _elegir_backend()
        self.headless = self.backend == "Agg"

        if self.headless:
            print("⚠  Sin display detectado — renderer en modo headless.")
            print("   Los frames se guardarán cada 10s en /tmp/abm_frames/")
            import os
            os.makedirs("/tmp/abm_frames", exist_ok=True)
        else:
            print(f"✓ Renderer usando backend: {self.backend}")

        self.fig = plt.figure(figsize=figsize)

    # ----------------------------------------------------------

    def _build_image(self, agentes: list) -> np.ndarray:
        """Construye el array RGB de la simulación."""
        world = self.world
        img = np.ones((world.height, world.width, 3), dtype=np.float32)
        img[:, :] = [0.95, 0.95, 0.95]

        # Paredes, salidas, fuego
        img[world.grid == WALL] = [0.10, 0.10, 0.10]
        img[world.grid == EXIT] = [0.0, 0.8, 0.2]

        # Humo
        smoke_color = np.array([0.30, 0.30, 0.30])
        for y in range(world.height):
            for x in range(world.width):
                s = world.smoke[y][x]
                if s > 0:
                    alpha = min(s / 180.0, 0.80)
                    img[y][x] = img[y][x] * (1 - alpha) + smoke_color * alpha

        img[world.grid == FIRE] = [1.0, 0.30, 0.0]

        # Personas
        for a in agentes:
            if not a.alive:
                continue
            if a.injured:
                color = [0.0, 0.7, 1.0]   # azul claro → herido
            elif a.panic >= 5:
                color = [1.0, 0.0, 1.0]   # magenta → pánico
            else:
                color = [0.0, 0.0, 1.0]   # azul → normal
            img[a.y][a.x] = color

        return img

    # ----------------------------------------------------------

    def render(self, agentes: list, t: int):
        img = self._build_image(agentes)

        plt.clf()
        plt.title(f"Tiempo: {t}s", fontsize=16)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])

        if self.headless:
            # Guardar frame cada 10 segundos para no llenar /tmp
            if t % 10 == 0:
                plt.savefig(
                    f"/tmp/abm_frames/frame_{t:04d}.png",
                    dpi=80,
                    bbox_inches="tight"
                )
        else:
            plt.pause(0.01)
