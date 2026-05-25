import random

from config.constants import EXIT


class Agente:
    """
    Representa a una persona dentro de la simulación.
    Sus atributos modelan velocidad, pánico, conocimiento
    de salidas y comportamiento social.
    """

    def __init__(
        self,
        x: int,
        y: int,
        age: int,
        sex: str,
        prior_visit: bool,
        behavior_type: int,
        group_number: int,
        group_leader: int,
        initial_energy: float,
        exits: list,
        cfg: dict,
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
        self.smoke_inhaled = 0.0

        self.alive = True
        self.evacuated = False
        self.injured = False
        self.panic = 0

        # --------------------------------------------------
        # Comportamiento social
        # --------------------------------------------------
        self.follow_group = random.random() < cfg["follow_group_prob"]
        self.social_delay = random.uniform(0, 12)

        # --------------------------------------------------
        # Visión
        # --------------------------------------------------
        self.vision_radius = random.randint(4, 8)
        self.last_direction = (0, 0)

        # --------------------------------------------------
        # Velocidad base según edad
        # --------------------------------------------------
        if age > 60:
            self.base_speed = 0.65
        elif age < 16:
            self.base_speed = 0.85
        else:
            self.base_speed = random.uniform(0.9, 1.15)

        # --------------------------------------------------
        # Tiempo de reacción (con multiplicador del escenario)
        # --------------------------------------------------
        mult = cfg["reaction_time_multiplier"]
        r = random.random()
        if r < 0.15:
            self.reaction_time = random.uniform(8, 18) * mult
        elif r < 0.75:
            self.reaction_time = random.uniform(22, 50) * mult
        else:
            self.reaction_time = random.uniform(55, 95) * mult

        self.reaction_time += self.social_delay

        # --------------------------------------------------
        # Conocimiento de salidas
        # --------------------------------------------------
        if self.prior_visit:
            self.knows_exits = exits.copy()
        else:
            self.knows_exits = [random.choice(exits)]

        # --------------------------------------------------
        # Salida preferida (72% sesgo hacia salida principal)
        # --------------------------------------------------
        if random.random() < 0.72:
            self.target_exit = exits[0]
        else:
            self.target_exit = random.choice(self.knows_exits)
