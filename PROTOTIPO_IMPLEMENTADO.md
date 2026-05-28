# Prototipo Implementado - Modelo de Simulación de Evacuación

## Descripción General

Este prototipo implementa un **Modelo Basado en Agentes (ABM)** para simular la evacuación del incendio de The Station Nightclub (2003). El modelo simula el comportamiento de agentes individuales en un espacio 2D, considerando factores como fuego, humo, congestión, comportamiento grupal y tiempos de reacción.

## Arquitectura del Sistema

### Componentes Principales

```
station-nightclub-abm/
├── config/
│   └── scenarios.py          # Definición de 6 escenarios de simulación
├── world/
│   ├── world.py              # Clase World: maneja el grid y estado global
│   ├── agent.py              # Clase Agent: comportamiento individual
│   ├── fire.py               # Clase Fire: propagación del fuego
│   └── smoke.py              # Clase Smoke: dispersión del humo
├── run_scenario.py           # Ejecución individual de escenarios
├── montecarlo_analysis.py    # Análisis Monte Carlo estadístico
├── simulation_convergence.py # Análisis de convergencia
└── run_all_scenarios.py      # Ejecución automática de todos los escenarios
```

## Flujo de Ejecución

### 1. Inicialización del Mundo

```python
# Código fuente: world/world.py
class World:
    def __init__(self, width, height, cfg):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.agents = []
        self.fire = Fire(cfg)
        self.smoke = Smoke(cfg)
        self.exits = self._load_exits()
        self.distance_maps = self._calculate_distance_maps()
```

**Funcionalidad:**
- Crea grid 2D de celdas (65×41 para el escenario real)
- Inicializa agentes con posiciones aleatorias
- Calcula mapas de distancia hacia cada salida
- Carga eventos de fuego y humo históricos

### 2. Comportamiento del Agente

```python
# Código fuente: world/agent.py
class Agent:
    def __init__(self, id, position, cfg):
        self.id = id
        self.position = position
        self.alive = True
        self.escaped = False
        self.trapped = False
        self.injured = False
        self.reaction_time = cfg['reaction_time'] * random.random()
        self.group_id = random.randint(0, 5) if random.random() < cfg['follow_group_prob'] else None
        self.escape_time = 0
    
    def decide_move(self, world):
        if not self._should_move():
            return None
        
        if self.group_id is not None:
            return self._follow_group(world)
        else:
            return self._move_to_exit(world)
```

**Lógica de decisión:**
1. **Verificar estado:** Si está muerto, atrapado o escapado → no moverse
2. **Tiempo de reacción:** Esperar hasta que `current_time >= reaction_time`
3. **Comportamiento grupal:** Si tiene grupo, seguir al líder
4. **Movimiento hacia salida:** Usar mapa de distancia para encontrar camino más corto
5. **Evitar obstáculos:** No moverse a celdas ocupadas o con fuego

### 3. Propagación del Fuego

```python
# Código fuente: world/fire.py
class Fire:
    def __init__(self, cfg):
        self.fire_events = self._load_fire_events()
        self.current_fire_cells = set()
    
    def update(self, timestep):
        if timestep in self.fire_events:
            new_cells = self.fire_events[timestep]
            self.current_fire_cells.update(new_cells)
            return new_cells
        return set()
```

**Mecanismo:**
- Carga eventos históricos del incendio real (34 pasos)
- En cada timestep, activa celdas según datos históricos
- Agentes en celdas con fuego mueren inmediatamente

### 4. Dispersión del Humo

```python
# Código fuente: world/smoke.py
class Smoke:
    def __init__(self, cfg):
        self.smoke_events = self._load_smoke_events()
        self.smoke_grid = np.zeros((height, width))
    
    def update(self, timestep):
        if timestep in self.smoke_events:
            smoke_data = self.smoke_events[timestep]
            self.smoke_grid = smoke_data
        return self.smoke_grid
```

**Mecanismo:**
- Carga eventos de humo históricos (62 pasos)
- El humo reduce visibilidad y aumenta probabilidad de lesiones
- Agentes en áreas con humo acumulan exposición

### 5. Bucle Principal de Simulación

```python
# Código fuente: run_scenario.py
def run_simulation(cfg, seed):
    random.seed(seed)
    np.random.seed(seed)
    
    world = World(cfg['world_width'], cfg['world_height'], cfg)
    
    for timestep in range(cfg['simulation_steps']):
        # Actualizar fuego
        fire_cells = world.fire.update(timestep)
        
        # Actualizar humo
        smoke_grid = world.smoke.update(timestep)
        
        # Mover agentes
        for agent in world.agents:
            if agent.alive and not agent.escaped:
                move = agent.decide_move(world)
                if move:
                    agent.position = move
                    agent.escape_time = timestep
        
        # Verificar colisiones con fuego
        for agent in world.agents:
            if agent.position in fire_cells:
                agent.alive = False
        
        # Verificar escapes
        for agent in world.agents:
            if agent.position in world.exits:
                agent.escaped = True
    
    return collect_statistics(world)
```

## Análisis Estadístico

### Monte Carlo Analysis

```python
# Código fuente: montecarlo_analysis.py
class MonteCarloRunner:
    def __init__(self, scenario_num, num_simulations=100, bootstrap_samples=1000):
        self.scenario_num = scenario_num
        self.num_simulations = num_simulations
        self.bootstrap_samples = bootstrap_samples
        self.cfg = get_scenario(scenario_num)
        self.results = []
    
    def run_all_simulations(self):
        for i in range(self.num_simulations):
            seed = i + 1
            result = run_simulation(self.cfg, seed)
            self.results.append(result)
        
        return self.results
```

**Métricas recolectadas:**
- `total_evacuated`: Número de agentes que escaparon
- `total_dead`: Número de agentes muertos
- `total_injured`: Número de agentes lesionados
- `total_trapped`: Número de agentes atrapados
- `average_escape_time`: Tiempo promedio de escape
- `max_density`: Densidad máxima alcanzada
- `average_smoke`: Exposición promedio al humo

**Análisis estadístico:**
1. **Estadísticas descriptivas:** media, varianza, desviación estándar, cuartiles
2. **Intervalos de confianza:** 95% CI usando distribución normal
3. **Bootstrap:** Remuestreo para estimar estabilidad de estimadores
4. **Ajuste de distribuciones:** MLE para Normal, Log-Normal, Weibull
5. **Visualizaciones:** Histogramas, boxplots, heatmaps

### Análisis de Convergencia

```python
# Código fuente: simulation_convergence.py
class ConvergenceAnalyzer:
    def __init__(self, scenario_num, pilot_simulations=10):
        self.scenario_num = scenario_num
        self.pilot_simulations = pilot_simulations
        self.cumulative_means = {'evacuated': [], 'deaths': [], 'trapped': []}
        self.cumulative_stds = {'evacuated': [], 'deaths': [], 'trapped': []}
        self.relative_errors = {'evacuated': [], 'deaths': [], 'trapped': []}
    
    def run_convergence_analysis(self):
        # Fase 1: Simulaciones piloto
        for i in range(self.pilot_simulations):
            result = run_simulation(self.cfg, i+1)
            self._update_cumulative_stats(result)
        
        # Calcular tamaño de muestra requerido
        required_n = self._calculate_required_sample_size()
        
        # Fase 2: Continuar hasta convergencia
        while not self._has_converged():
            result = run_simulation(self.cfg, len(self.results)+1)
            self._update_cumulative_stats(result)
        
        return self.results
```

**Criterio de convergencia:**
- Fórmula: `n = (Z × σ / E)²`
- Z = 1.96 (95% confianza)
- σ = desviación estándar de pilotos
- E = error permitido (default 5)
- Auto-stop cuando error relativo < 5%

## Escenarios de Simulación

### Definición de Escenarios

```python
# Código fuente: config/scenarios.py
SCENARIOS = {
    1: {
        'name': 'Escenario 1 — Base',
        'num_agents': 465,
        'smoke_density': 1.0,
        'blocked_exits': 0,
        'follow_group_prob': 0.65,
        'reaction_time_multiplier': 1.0,
        'simulation_steps': 300
    },
    2: {
        'name': 'Escenario 2 — Alta congestión',
        'num_agents': 700,
        'smoke_density': 1.0,
        'blocked_exits': 0,
        'follow_group_prob': 0.65,
        'reaction_time_multiplier': 1.0,
        'simulation_steps': 300
    },
    # ... escenarios 3-6
}
```

### Descripción de Escenarios

| Escenario | Nombre | Agentes | Humo | Salidas Bloqueadas | Grupo | Reacción |
|----------|--------|---------|-------|-------------------|-------|----------|
| 1 | Base | 465 | 1.0x | 0 | 0.65 | 1.0x |
| 2 | Alta Congestión | 700 | 1.0x | 0 | 0.65 | 1.0x |
| 3 | Más Humo | 465 | 1.5x | 0 | 0.65 | 1.0x |
| 4 | Salidas Bloqueadas | 465 | 1.0x | 4 | 0.65 | 1.0x |
| 5 | Grupo Fuerte | 465 | 1.0x | 0 | 0.90 | 1.0x |
| 6 | Reacción Tardía | 465 | 1.0x | 0 | 0.65 | 2.0x |

## Generación de Reportes

### Reportes Markdown

```python
# Código fuente: montecarlo_analysis.py
class ReportGenerator:
    def __init__(self, output_file="statistical_report.md", suffix=""):
        self.output_file = output_file
        self.suffix = suffix
        self.sections = []
    
    def add_section(self, title, content):
        self.sections.append((title, content))
    
    def add_table(self, df, caption):
        self.sections.append((caption, df.to_markdown()))
    
    def generate_report(self):
        with open(self.output_file, 'w') as f:
            for title, content in self.sections:
                f.write(f"## {title}\n\n")
                f.write(f"{content}\n\n")
```

**Contenido del reporte:**
1. Metodología Monte Carlo
2. Configuración de simulación
3. Estadísticas descriptivas (tabla)
4. Intervalos de confianza (tabla)
5. Ajuste de distribuciones (tabla)
6. Resultados de bootstrap (tabla)
7. Conclusiones

### Visualizaciones

```python
# Código fuente: montecarlo_analysis.py
class VisualizationGenerator:
    def plot_histogram(self, data, title, xlabel, filename):
        plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
        plt.xlabel(xlabel)
        plt.ylabel('Frequency')
        plt.title(title)
        plt.savefig(filename, dpi=300)
    
    def plot_boxplot(self, data_dict, title, filename):
        plt.boxplot(data_dict.values(), labels=data_dict.keys())
        plt.title(title)
        plt.savefig(filename, dpi=300)
    
    def plot_heatmap(self, heatmap, title, filename):
        plt.imshow(heatmap, cmap='YlOrRd')
        plt.colorbar(label='Occupancy')
        plt.title(title)
        plt.savefig(filename, dpi=300)
```

**Gráficos generados:**
- Histogramas de métricas principales
- Boxplots comparativos
- Distribuciones bootstrap
- Intervalos de confianza
- Heatmaps de congestión
- Heatmaps de muertes
- Heatmaps de exposición al humo

## Ejecución Automática

### Script run_all_scenarios.py

```python
# Código fuente: run_all_scenarios.py
def run_all_scenarios():
    scenarios_to_run = args.scenarios or range(1, 7)
    
    for scenario_num in scenarios_to_run:
        # Crear directorio para escenario
        scenario_dir = f"scenario_{scenario_num}"
        os.makedirs(scenario_dir, exist_ok=True)
        
        # Cambiar al directorio del escenario
        os.chdir(scenario_dir)
        
        # Ejecutar análisis de convergencia
        if args.run_convergence:
            cmd = f"python ../simulation_convergence.py --scenario {scenario_num}"
            subprocess.run(cmd, shell=True)
        
        # Ejecutar Monte Carlo
        if args.run_montecarlo:
            cmd = f"python ../montecarlo_analysis.py --scenario {scenario_num} --simulations {args.simulations} --bootstrap {args.bootstrap}"
            subprocess.run(cmd, shell=True)
        
        # Volver al directorio raíz
        os.chdir("..")
    
    # Generar reporte resumen
    generate_summary_report()
```

## Dependencias

```
# requirements.txt
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0
matplotlib>=3.4.0
```

## Referencias de Código Fuente

### Archivos Principales

1. **world/world.py** - Clase World: manejo del grid y estado global
2. **world/agent.py** - Clase Agent: comportamiento individual de agentes
3. **world/fire.py** - Clase Fire: propagación del fuego
4. **world/smoke.py** - Clase Smoke: dispersión del humo
5. **config/scenarios.py** - Definición de escenarios de simulación
6. **run_scenario.py** - Ejecución individual de escenarios
7. **montecarlo_analysis.py** - Análisis Monte Carlo estadístico
8. **simulation_convergence.py** - Análisis de convergencia
9. **run_all_scenarios.py** - Ejecución automática de todos los escenarios

### Módulos de Análisis

10. **montecarlo_analysis.py::MonteCarloRunner** - Ejecuta simulaciones Monte Carlo
11. **montecarlo_analysis.py::VisualizationGenerator** - Genera gráficos
12. **montecarlo_analysis.py::HeatmapAnalyzer** - Genera heatmaps
13. **montecarlo_analysis.py::ReportGenerator** - Genera reportes markdown
14. **simulation_convergence.py::ConvergenceAnalyzer** - Analiza convergencia
15. **simulation_convergence.py::ConvergenceVisualizer** - Visualiza convergencia

## Características Técnicas

### Lenguaje y Framework
- **Lenguaje:** Python 3.8+
- **Paradigma:** Programación orientada a objetos
- **Librerías científicas:** NumPy, Pandas, SciPy
- **Visualización:** Matplotlib

### Optimizaciones
- Mapas de distancia precalculados para cada salida
- Grid 2D para búsqueda eficiente de vecinos
- Generación de números aleatorios con seeds reproducibles
- Procesamiento vectorizado con NumPy

### Validación
- Comparación con datos históricos del incendio real
- Análisis de convergencia para determinar tamaño de muestra
- Bootstrap para validar estabilidad de estimadores
- Intervalos de confianza al 95% para todas las métricas

## Limitaciones y Suposiciones

1. **Espacio 2D simplificado:** No modela altura del club
2. **Agentes homogéneos:** No considera diferencias individuales (edad, género)
3. **Comportamiento determinista:** Reglas fijas, no aprendizaje
4. **Datos históricos limitados:** Fuego y humo basados en reconstrucción
5. **Sin física de fluidos:** Humo no simula dinámica real de gases
6. **Sin pánico explícito:** Pánico modelado indirectamente por comportamiento grupal

## Extensiones Posibles

1. **Modelo 3D:** Incluir altura y escaleras
2. **Agentes heterogéneos:** Diferentes capacidades físicas
3. **Redes sociales:** Estructura de grupos más compleja
4. **Dinámica de fluidos:** Simulación CFD para humo
5. **Aprendizaje:** Agentes que adaptan comportamiento
6. **Interfaz gráfica:** Visualización interactiva en tiempo real

## Conclusión

Este prototipo implementa un modelo ABM completo para simular la evacuación del incendio de The Station Nightclub. El sistema incluye:

- **Simulación física:** Fuego, humo, congestión
- **Comportamiento humano:** Reacción, grupos, toma de decisiones
- **Análisis estadístico:** Monte Carlo, convergencia, bootstrap
- **Visualización:** Gráficos, heatmaps, reportes
- **Automatización:** Ejecución de múltiples escenarios

El código fuente está organizado modularmente, facilitando extensiones y modificaciones. El sistema ha sido validado con datos históricos y produce resultados estadísticamente robustos.
