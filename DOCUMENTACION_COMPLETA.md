# Documentación Completa del Proyecto

**Fecha de creación:** 28 de mayo de 2026  
**Proyecto:** Station Nightclub ABM - Análisis Estadístico y Convergencia

---

## Índice

1. [Resumen del Proyecto Original](#resumen-del-proyecto-original)
2. [Extensión: Pipeline de Análisis Estadístico Monte Carlo](#extensión-pipeline-de-análisis-estadístico-monte-carlo)
3. [Extensión: Módulo de Convergencia de Simulación](#extensión-módulo-de-convergencia-de-simulación)
4. [Archivos Creados y Modificados](#archivos-creados-y-modificados)
5. [Guía de Uso](#guía-de-uso)
6. [Resultados Generados](#resultados-generados)

---

## Resumen del Proyecto Original

### ¿Qué es PRIORITEVAC?

**PRIORITEVAC** es un modelo basado en agentes (ABM - Agent-Based Model) desarrollado por Fridolf, Ronchi, Nilsson & Frantzich (2020) para examinar factores sociales en la evacuación de incendios de edificios. Se caracteriza por incorporar la dimensión social de lealtad grupal en la evacuación y respuestas al fuego y humo. El modelo está disponible en CoMSES Network.

### El Incidente: Station Nightclub Fire (2003)

El incendio de The Station Nightclub ocurrió el 20 de febrero de 2003 en West Warwick, Rhode Island. Una banda usó pirotecnia que encendió espuma de poliuretano en las paredes y techo del escenario. El NIST (National Institute of Standards and Technology) realizó una investigación técnica exhaustiva documentada en el reporte NCSTAR 2 Volume 1, que incluye datos detallados sobre:

- Layout del edificio
- Posiciones iniciales de las 465 personas
- Propagación del fuego en el tiempo
- Difusión del humo

### Tu Proyecto Actual

Es una implementación en Python de una simulación de evacuación basada en agentes, inspirada en PrioritEvac, usando como caso de estudio el incendio de Station Nightclub. No busca replicar completamente el modelo original, sino construir una versión simplificada, flexible y adaptable para estudiar comportamientos de evacuación bajo distintos escenarios.

### Características Principales

#### Modelo de Agente Humano
- 465 agentes con atributos realistas (edad, sexo, visitas previas, comportamiento grupal, energía inicial)
- Tiempos de reacción variables (15% rápido, 60% normal, 25% lento)
- Velocidad de movimiento según edad (mayores de 60: 65%, menores de 16: 85%)
- Conocimiento del lugar (visitantes previos conocen todas las salidas)
- Comportamiento social (65% siguen a su grupo)

#### Dinámica del Incendio
- Replay de fuego real (34 eventos hasta t=245s)
- Expansión probabilística del fuego después del replay
- Replay de humo real (62 eventos) con difusión
- Efectos del humo en movilidad y salud

#### Factores Implementados
- Pánico dinámico (aumenta con humo y fuego cercano)
- Crowd crush (aplastamiento por alta densidad)
- Lesiones por inhalación de humo
- Muerte por fuego directo o agotamiento de energía
- Congestión en salidas
- Selección dinámica de salidas usando mapas de distancia BFS

### Escenarios Experimentales

El proyecto permite ejecutar 6 escenarios comparativos:

1. **Escenario 1** - Evacuación base (465 agentes)
2. **Escenario 2** - Alta congestión (700 agentes)
3. **Escenario 3** - Mayor propagación de humo
4. **Escenario 4** - Salidas bloqueadas
5. **Escenario 5** - Comportamiento grupal fuerte (90% siguen grupo)
6. **Escenario 6** - Reacción tardía (tiempos ×2)

### Arquitectura del Código Original

```
run_scenario.py (punto de entrada)
├── config/
│   ├── constants.py
│   └── scenarios.py (configuración de 6 escenarios)
├── data/
│   ├── building_nightclub.csv (layout)
│   ├── people.csv (465 agentes)
│   ├── fire_nightclub_merged.csv (replay fuego)
│   └── smoke.csv (replay humo)
├── simulation/
│   ├── agent.py (clase Agente)
│   ├── world.py (entorno grid)
│   ├── fire.py (simulación fuego)
│   ├── smoke.py (simulación humo)
│   └── movement.py (navegación agentes)
├── data_io/ (carga de datos)
├── metrics/ (recolección métricas)
└── visualization/ (renderizado matplotlib)
```

---

## Extensión: Pipeline de Análisis Estadístico Monte Carlo

### Objetivo

Transformar la simulación de evacuación ABM en una plataforma analíticamente robusta con análisis estadístico completo tipo investigación académica.

### Implementación

#### Archivo Creado: `montecarlo_analysis.py` (33,499 bytes)

Script principal que implementa todo el pipeline de análisis estadístico.

#### Componentes Implementados

##### 1. MonteCarloRunner
Ejecuta múltiples simulaciones con diferentes semillas aleatorias.

**Características:**
- Ejecuta simulaciones independientes (default: 100)
- Cada simulación resetea completamente: grid, humo, fuego, agentes, métricas
- Usa semillas aleatorias diferentes para cada ejecución
- Almacena métricas globales de cada ejecución

**Métricas recolectadas:**
- `total_evacuated` - Personas evacuadas
- `total_dead` - Personas fallecidas
- `total_injured` - Personas heridas
- `total_trapped` - Personas atrapadas
- `average_escape_time` - Tiempo promedio de evacuación
- `max_density` - Densidad máxima
- `average_smoke` - Humo promedio
- `window_escape_count` - Escapes por ventana
- `total_simulation_time` - Tiempo total de simulación

##### 2. StatisticalAnalyzer
Módulo de análisis estadístico completo.

**Funciones implementadas:**

**Estadísticas de muestra:**
- Media muestral
- Varianza muestral
- Desviación estándar
- Mínimo y máximo
- Mediana
- Cuartiles (Q25, Q75)

**Intervalos de confianza:**
- Cálculo de IC al 95% usando fórmula:
  ```
  CI = mean ± 1.96 * (std / sqrt(n))
  ```
- Para: evacuated, dead, injured, trapped, average_escape_time

**Ajuste de distribuciones (MLE):**
- Ajuste de distribuciones usando Maximum Likelihood Estimation:
  - Normal
  - Lognormal
  - Weibull
- Cálculo de:
  - Log-likelihood
  - AIC (Akaike Information Criterion)
  - BIC (Bayesian Information Criterion)
- Determinación de mejor ajuste por AIC

**Bootstrapping:**
- 1000 remuestreos bootstrap
- Cálculo de intervalos de confianza bootstrap
- Distribución de medias bootstrap
- Para: evacuated, dead, trapped

##### 3. VisualizationGenerator
Generador automático de visualizaciones científicas.

**Gráficos generados:**
- `histogram_evacuated.png` - Histograma de evacuados
- `histogram_deaths.png` - Histograma de muertes
- `histogram_escape_times.png` - Histograma de tiempos de escape
- `boxplot_metrics.png` - Boxplot de métricas de evacuación
- `bootstrap_total_evacuated.png` - Distribución bootstrap (evacuados)
- `bootstrap_total_dead.png` - Distribución bootstrap (muertes)
- `bootstrap_total_trapped.png` - Distribución bootstrap (atrapados)
- `confidence_intervals.png` - Intervalos de confianza

##### 4. HeatmapAnalyzer
Análisis espacial de todas las simulaciones.

**Heatmaps generados:**
- `heatmap_congestion.png` - Mapa de calor de congestión (posiciones de agentes)
- `heatmap_death.png` - Mapa de calor de muertes (ubicaciones de fatalidades)
- `heatmap_smoke.png` - Mapa de calor de exposición al humo

**Exportaciones:**
- Visualizaciones PNG
- Matrices CSV crudas para análisis adicional

##### 5. ReportGenerator
Generador de reportes markdown profesionales.

**Secciones del reporte:**
1. Metodología Monte Carlo
2. Configuración de simulación
3. Estadísticas de muestra
4. Intervalos de confianza
5. Ajuste de distribuciones
6. Análisis bootstrap
7. Conclusiones

**Características:**
- Tablas formateadas en markdown
- Sin dependencia de tabulate
- Referencias a figuras generadas
- Interpretación de resultados

### Archivos de Salida del Pipeline Monte Carlo

**Archivos CSV:**
- `montecarlo_results.csv` - Resultados brutos de todas las simulaciones
- `sample_statistics.csv` - Estadísticas de muestra
- `confidence_intervals.csv` - Intervalos de confianza al 95%
- `distribution_fits.csv` - Resultados de ajuste de distribuciones (AIC, BIC, log-likelihood)
- `bootstrap_results.csv` - Resultados de análisis bootstrap

**Directorios:**
- `plots/` - 8 archivos PNG de visualizaciones
- `heatmaps/` - 3 archivos PNG + 3 matrices CSV

**Reporte:**
- `statistical_report.md` - Reporte completo en markdown

### Uso del Pipeline Monte Carlo

```bash
# Ejecutar con 100 simulaciones (default)
python montecarlo_analysis.py --scenario 1

# Ejecutar con número personalizado de simulaciones
python montecarlo_analysis.py --scenario 1 --simulations 50

# Ejecutar con número personalizado de muestras bootstrap
python montecarlo_analysis.py --scenario 1 --simulations 100 --bootstrap 2000
```

---

## Extensión: Módulo de Convergencia de Simulación

### Objetivo

Determinar el número estadísticamente requerido de simulaciones Monte Carlo basado en la precisión deseada. Esto transforma el proyecto de conteos arbitrarios a tamaños de muestra calculados estadísticamente, siguiendo estándares académicos.

### Implementación

#### Archivo Creado: `simulation_convergence.py`

Script que implementa análisis de convergencia estadística.

#### Metodología

**Fórmula de tamaño de muestra:**
```
n = (Z × σ / E)²
```

Donde:
- Z = 1.96 (z-score para nivel de confianza del 95%)
- σ = desviación estándar de simulaciones piloto
- E = error permitido (margen de error)

#### Componentes Implementados

##### 1. ConvergenceAnalyzer
Analizador de convergencia de simulaciones Monte Carlo.

**Fases del análisis:**

**Fase 1: Simulaciones Piloto**
- Ejecuta simulaciones piloto (default: 10)
- Calcula desviación estándar para:
  - Muertos
  - Evacuados
  - Atrapados

**Fase 2: Cálculo de Tamaño de Muestra**
- Calcula n requerido para cada métrica
- Usa el máximo de los requeridos
- Parámetros configurables:
  - `ALLOWED_ERROR_DEATHS = 5`
  - `ALLOWED_ERROR_EVACUATED = 5`
  - `ALLOWED_ERROR_TRAPPED = 5`

**Fase 3: Continuación Automática**
- Si `required_n > current_runs`, continúa ejecutando
- Detiene al alcanzar `ceil(required_n)`

**Seguimiento de estadísticas acumulativas:**
- Medias acumulativas
- Desviaciones estándar acumulativas
- Errores relativos

##### 2. Criterio de Parada Automática

Implementa criterio de parada basado en error relativo:

```
RelativeError = (CI half-width) / mean
```

**Condición de parada:**
- Detener cuando `RelativeError < 0.05` (5%)
- Para todas las métricas simultáneamente
- Muy usado en papers académicos

##### 3. ConvergenceVisualizer
Generador de gráficos de convergencia.

**Gráficos generados:**
- `convergence_evacuated.png` - Convergencia de media acumulativa (evacuados)
- `convergence_deaths.png` - Convergencia de media acumulativa (muertes)
- `convergence_trapped.png` - Convergencia de media acumulativa (atrapados)
- `convergence_relative_error.png` - Convergencia de error relativo
- `convergence_std.png` - Convergencia de desviación estándar

**Características de los gráficos:**
- Eje X: número de simulaciones
- Eje Y: media acumulativa
- Muestran estabilización estadística
- Indicador de desviación de últimos 10 puntos

##### 4. ConvergenceReportGenerator
Generador de sección de reporte de convergencia.

**Sección agregada al markdown:**
- Metodología de convergencia
- Simulaciones piloto
- Desviación estándar
- Cálculo de tamaño de muestra requerido
- Resultados de convergencia
- Justificación estadística
- Referencias a gráficos de convergencia

### Archivos de Salida del Módulo de Convergencia

**Archivos CSV:**
- `convergence_data.csv` - Datos completos de seguimiento de convergencia

**Directorios:**
- `plots/` - 5 archivos PNG de gráficos de convergencia

**Reporte:**
- Sección agregada a `statistical_report.md`

### Uso del Módulo de Convergencia

```bash
# Uso básico con parámetros default
python simulation_convergence.py --scenario 1

# Simulaciones piloto personalizadas
python simulation_convergence.py --scenario 1 --pilot 10

# Umbrales de error personalizados
python simulation_convergence.py --scenario 1 --error-deaths 3 --error-evacuated 5

# Desactivar criterio de parada automática
python simulation_convergence.py --scenario 1 --no-auto-stop
```

### Resultados de Prueba

**Prueba con 3 simulaciones piloto:**

```
Pilot Results:
  Evacuated: mean=186.00, std=1.00
  Deaths: mean=100.00, std=3.61
  Trapped: mean=179.00, std=4.00

Required Sample Sizes:
  For evacuated (E=5): 1
  For deaths (E=5): 2
  For trapped (E=5): 3
  Maximum required: 3

Final Relative Errors:
  Evacuated: 0.61%
  Deaths: 4.08%
  Trapped: 2.53%
```

---

## Archivos Creados y Modificados

### Archivos Nuevos Creados

1. **montecarlo_analysis.py** (33,499 bytes)
   - Pipeline completo de análisis estadístico Monte Carlo
   - 5 clases principales: MonteCarloRunner, StatisticalAnalyzer, VisualizationGenerator, HeatmapAnalyzer, ReportGenerator

2. **simulation_convergence.py** (aproximadamente 15,000 bytes)
   - Módulo de análisis de convergencia
   - 3 clases principales: ConvergenceAnalyzer, ConvergenceVisualizer, ConvergenceReportGenerator

### Archivos Modificados

1. **requirements.txt**
   - Original: `numpy`, `matplotlib`
   - Modificado: `numpy`, `matplotlib`, `pandas`, `scipy`

### Archivos de Salida Generados

**Del Pipeline Monte Carlo:**
- `montecarlo_results.csv`
- `sample_statistics.csv`
- `confidence_intervals.csv`
- `distribution_fits.csv`
- `bootstrap_results.csv`
- `statistical_report.md`
- `plots/` (8 archivos PNG)
- `heatmaps/` (6 archivos: 3 PNG + 3 CSV)

**Del Módulo de Convergencia:**
- `convergence_data.csv`
- `plots/` (5 archivos PNG adicionales)
- `statistical_report.md` (sección agregada)

---

## Guía de Uso

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Dependencias requeridas:
- numpy
- matplotlib
- pandas
- scipy

### Ejecutar Simulación Individual

```bash
# Escenario 1 (base)
python run_scenario.py --scenario 1

# Escenario 3 sin visualización
python run_scenario.py --scenario 3 --no-render

# Escenario 4 con 200 pasos
python run_scenario.py --scenario 4 --steps 200
```

### Ejecutar Análisis Monte Carlo

```bash
# Análisis completo con 100 simulaciones
python montecarlo_analysis.py --scenario 1

# Análisis con 50 simulaciones
python montecarlo_analysis.py --scenario 1 --simulations 50

# Análisis con 2000 muestras bootstrap
python montecarlo_analysis.py --scenario 1 --simulations 100 --bootstrap 2000
```

**Nomenclatura de Archivos Generados:**

Los archivos generados incluyen un sufijo que identifica el escenario, número de simulaciones y muestras de bootstrap:

- `_s{N}` - Número de escenario (siempre incluido)
- `_n{N}` - Número de simulaciones (si no es 100)
- `_bs{N}` - Muestras bootstrap (si no es 1000)

Ejemplos:
- `montecarlo_results_s1.csv` - Escenario 1, 100 simulaciones, 1000 bootstrap
- `montecarlo_results_s2_n50.csv` - Escenario 2, 50 simulaciones, 1000 bootstrap
- `montecarlo_results_s3_n100_bs2000.csv` - Escenario 3, 100 simulaciones, 2000 bootstrap

### Ejecutar Análisis de Convergencia

```bash
# Análisis de convergencia con parámetros default
python simulation_convergence.py --scenario 1

# Con 20 simulaciones piloto
python simulation_convergence.py --scenario 1 --pilot 20

# Con error permitido de 3 para muertes
python simulation_convergence.py --scenario 1 --error-deaths 3

# Sin criterio de parada automática
python simulation_convergence.py --scenario 1 --no-auto-stop
```

**Nomenclatura de Archivos de Convergencia:**

Los archivos de convergencia también incluyen sufijo de escenario:

- `_s{N}` - Número de escenario (siempre incluido)
- `_p{N}` - Simulaciones piloto (si no es 10)

Ejemplos:
- `convergence_data_s1.csv` - Escenario 1, 10 pilotos
- `convergence_data_s2_p20.csv` - Escenario 2, 20 pilotos

### Flujo de Trabajo Recomendado

1. **Primero:** Ejecutar análisis de convergencia para determinar n requerido
   ```bash
   python simulation_convergence.py --scenario 1
   ```

2. **Luego:** Ejecutar Monte Carlo con el n determinado
   ```bash
   python montecarlo_analysis.py --scenario 1 --simulations [n_determinado]
   ```

3. **Finalmente:** Revisar el reporte generado
   ```bash
   # Abrir statistical_report.md
   ```

---

## Resultados Generados

### Estructura de Directorios Final

```
station-nightclub-abm-implementar-escenarios/
│
├── run_scenario.py                 # Ejecución de escenarios individuales
├── montecarlo_analysis.py          # Pipeline Monte Carlo (NUEVO)
├── simulation_convergence.py       # Módulo de convergencia (NUEVO)
│
├── requirements.txt                # Dependencias (MODIFICADO)
│
├── config/
│   ├── constants.py
│   └── scenarios.py
│
├── data/
│   ├── building_nightclub.csv
│   ├── people.csv
│   ├── fire_nightclub_merged.csv
│   └── smoke.csv
│
├── simulation/
│   ├── agent.py
│   ├── world.py
│   ├── fire.py
│   ├── smoke.py
│   └── movement.py
│
├── data_io/
│   └── loaders.py
│
├── metrics/
│   └── collector.py
│
├── visualization/
│   └── renderer.py
│
├── plots/                          # Visualizaciones (GENERADO)
│   ├── histogram_evacuated.png
│   ├── histogram_deaths.png
│   ├── histogram_escape_times.png
│   ├── boxplot_metrics.png
│   ├── bootstrap_total_evacuated.png
│   ├── bootstrap_total_dead.png
│   ├── bootstrap_total_trapped.png
│   ├── confidence_intervals.png
│   ├── convergence_evacuated.png
│   ├── convergence_deaths.png
│   ├── convergence_trapped.png
│   ├── convergence_relative_error.png
│   └── convergence_std.png
│
├── heatmaps/                       # Heatmaps (GENERADO)
│   ├── heatmap_congestion.png
│   ├── heatmap_death.png
│   ├── heatmap_smoke.png
│   ├── congestion_matrix.csv
│   ├── death_matrix.csv
│   └── smoke_matrix.csv
│
├── montecarlo_results.csv          # Resultados Monte Carlo (GENERADO)
├── sample_statistics.csv           # Estadísticas de muestra (GENERADO)
├── confidence_intervals.csv        # Intervalos de confianza (GENERADO)
├── distribution_fits.csv           # Ajuste de distribuciones (GENERADO)
├── bootstrap_results.csv           # Resultados bootstrap (GENERADO)
├── convergence_data.csv            # Datos de convergencia (GENERADO)
│
└── statistical_report.md           # Reporte completo (GENERADO)
```

### Valor Académico

Las extensiones implementadas proporcionan:

1. **Justificación Estadística:**
   - El número de simulaciones no es arbitrario
   - Calculado estadísticamente basado en variabilidad
   - Reproducible y científicamente válido

2. **Evidencia de Convergencia:**
   - Gráficos de estabilización estadística
   - Errores relativos cuantificados
   - Criterios de parada automáticos

3. **Análisis Completo:**
   - Estadísticas descriptivas
   - Intervalos de confianza
   - Ajuste de distribuciones (MLE)
   - Bootstrapping robusto
   - Análisis espacial (heatmaps)

4. **Estándares de Publicación:**
   - Metodología reproducible
   - Visualizaciones científicas
   - Reporte profesional
   - Cumple con estándares académicos para ABM

---

## Conclusión

El proyecto ha sido transformado de una simulación ABM básica a una plataforma de análisis estadístico completo y científicamente válido. Las extensiones implementadas permiten:

- **Determinar estadísticamente** el número de simulaciones requerido
- **Analizar convergencia** y estabilidad de estimaciones
- **Realizar análisis estadístico completo** con métodos robustos
- **Generar visualizaciones profesionales** para publicación
- **Producir reportes académicos** con justificación estadística

Esto eleva el proyecto a estándares de investigación académica en modelado basado en agentes, proporcionando la rigurosidad estadística necesaria para publicación en revistas científicas.
