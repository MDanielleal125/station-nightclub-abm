# Guía de ejecución del proyecto

Este documento explica cómo ejecutar el proyecto, los escenarios disponibles y cómo revisar los resultados generados.

---

## 1. Requisitos previos

1. Tener Python 3.11+ instalado.
2. Instalar las dependencias del proyecto desde `requirements.txt`.
3. Verificar que la carpeta del proyecto contiene los datos de entrada en `data/`.

Ejemplo:

```bash
pip install -r requirements.txt
```

---

## 2. Estructura básica de ejecución

### 2.1 Ejecutar un escenario individual

El punto de entrada principal para correr una simulación individual es `run_scenario.py`.

```bash
python run_scenario.py --scenario 1
```

Opciones útiles:

```bash
python run_scenario.py --scenario 3 --no-render
python run_scenario.py --scenario 4 --steps 200
```

- `--scenario`: número del escenario (1 a 6).
- `--no-render`: desactiva la visualización en tiempo real.
- `--steps`: número de pasos de simulación (sobreescribe la configuración por defecto).

### 2.2 Qué hace esta ejecución

Al correr `run_scenario.py` se realiza lo siguiente:

1. Carga la configuración del escenario desde `config/scenarios.py`.
2. Carga el layout del edificio desde `data/building_nightclub.csv`.
3. Carga los eventos de fuego y humo desde `data/fire_nightclub_merged.csv` y `data/smoke.csv`.
4. Carga los agentes desde `data/people.csv`.
5. Ejecuta la simulación paso a paso.
6. Exporta métricas a `results/scenario_<n>.csv`.

---

## 3. Escenarios disponibles

El proyecto define seis escenarios en `config/scenarios.py`.

| Escenario | Nombre | Modificación principal | Parámetros clave |
|---|---|---|---|
| 1 | Base | Configuración estándar | 465 agentes, humo base, reacción normal |
| 2 | Alta congestión | Más agentes | 700 agentes |
| 3 | Más humo | Mayor humo | `smoke_density_multiplier = 6.0`, `smoke_diffusion_decay = 0.998` |
| 4 | Salidas bloqueadas | Menos rutas de escape | `blocked_exits = [0, 1]` |
| 5 | Comportamiento grupal fuerte | Grupo más dominante | `follow_group_prob = 0.90` |
| 6 | Reacción tardía | Respuesta más lenta | `reaction_time_multiplier = 2.0` |

### Comandos sugeridos por escenario

#### Escenario 1 — Base
```bash
python run_scenario.py --scenario 1
```

#### Escenario 2 — Alta congestión
```bash
python run_scenario.py --scenario 2
```

#### Escenario 3 — Más humo
```bash
python run_scenario.py --scenario 3
```

#### Escenario 4 — Salidas bloqueadas
```bash
python run_scenario.py --scenario 4
```

#### Escenario 5 — Comportamiento grupal fuerte
```bash
python run_scenario.py --scenario 5
```

#### Escenario 6 — Reacción tardía
```bash
python run_scenario.py --scenario 6
```

---

## 4. Ejecución de análisis Monte Carlo

Para análisis estadístico y generación de reportes, se usa `montecarlo_analysis.py`.

```bash
python montecarlo_analysis.py --scenario 1 --simulations 50
```

Opciones recomendadas:

```bash
python montecarlo_analysis.py --scenario 2 --simulations 50
python montecarlo_analysis.py --scenario 6 --simulations 50
```

Este script genera:
- CSV de resultados por escenario.
- Gráficas de distribución y bootstrap.
- Reportes Markdown estadísticos.

---

## 5. Resultados generados

### 5.1 Resultados de escenarios individuales

Las simulaciones individuales exportan métricas en:

- `results/scenario_1.csv`
- `results/scenario_2.csv`
- etc.

### 5.2 Resultados de Monte Carlo

Se generan archivos como:

- `montecarlo_results_s1_n50.csv`
- `montecarlo_results_s2_n50.csv`
- `montecarlo_results_s3_n50.csv`
- etc.

También se generan reportes:

- `statistical_report_s1_n50.md`
- `statistical_report_s2_n50.md`
- `statistical_report_s3_n50.md`
- `statistical_report_s4_n50.md`
- `statistical_report_s5_n50.md`
- `statistical_report_s6_n50.md`

### 5.3 Gráficas y heatmaps

Las visualizaciones se guardan en carpetas como:

- `plots/`
- `heatmaps/`
- `scenario_1/plots/`
- `scenario_1/heatmaps/`

---

## 6. Ejecución rápida para presentar el proyecto

### 6.1 Mostrar el escenario base
```bash
python run_scenario.py --scenario 1
```

### 6.2 Mostrar un escenario con efecto ambiental fuerte
```bash
python run_scenario.py --scenario 3 --no-render
```

### 6.3 Mostrar un escenario con retraso en reacción
```bash
python run_scenario.py --scenario 6 --no-render
```

### 6.4 Ejecutar una comparación estadística
```bash
python montecarlo_analysis.py --scenario 1 --simulations 50
python montecarlo_analysis.py --scenario 2 --simulations 50
python montecarlo_analysis.py --scenario 3 --simulations 50
python montecarlo_analysis.py --scenario 4 --simulations 50
python montecarlo_analysis.py --scenario 5 --simulations 50
python montecarlo_analysis.py --scenario 6 --simulations 50
```

---

## 7. Consejos para la presentación

- Use `--scenario 1` para mostrar el caso base.
- Use `--scenario 3` para destacar el impacto del humo.
- Use `--scenario 4` para mostrar cómo afectan las salidas bloqueadas.
- Use `--scenario 6` para destacar la degradación por reacción tardía.
- Use `montecarlo_analysis.py` para mostrar resultados estadísticos, varianza y bootstrap.

---

## 8. Resumen

- `run_scenario.py` → ejecutar un escenario individual.
- `montecarlo_analysis.py` → análisis estadístico con múltiples réplicas.
- Los escenarios del proyecto van de 1 a 6 y están definidos en `config/scenarios.py`.
- Los resultados se guardan en `results/`, `plots/`, `heatmaps/` y en los reportes Markdown de estadísticas.
