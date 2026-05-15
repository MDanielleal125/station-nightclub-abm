
# Simulación Basada en Agentes de Evacuación en Incendios  
## Caso de estudio: The Station Nightclub Fire (2003)

# Descripción general del proyecto

Este proyecto busca desarrollar una simulación de evacuación humana basada en agentes (Agent-Based Modeling, ABM) implementada en Python, inspirada en el modelo presentado en el trabajo:

*Fridolf, K., Ronchi, E., Nilsson, D., & Frantzich, H. (2020). PrioritEvac: An Agent-Based Model (ABM) for Examining Social Factors of Building Fire Evacuation.*

La propuesta no pretende replicar completamente el modelo original, sino construir una versión simplificada, flexible y adaptable que permita estudiar comportamientos de evacuación humana bajo distintos escenarios y configuraciones de incendio.

El proyecto toma como caso de referencia el incendio de **The Station Nightclub Fire (2003)** debido a la gran cantidad de información técnica y documentación disponible en las investigaciones oficiales del NIST (National Institute of Standards and Technology).

---

# Objetivo del proyecto

El objetivo principal es analizar cómo distintos factores sociales, físicos y ambientales afectan el comportamiento colectivo durante una evacuación de emergencia en incendios estructurales.

La simulación busca representar dinámicas humanas como:

- Reacción ante emergencias
- Congestión en salidas
- Influencia del humo
- Propagación del fuego
- Comportamiento grupal
- Pánico
- Lesiones y mortalidad

mediante un modelo basado en agentes capaz de generar distintos escenarios experimentales.

---

# Enfoque del proyecto

La simulación implementa un modelo basado en agentes donde cada individuo actúa de forma autónoma según atributos y condiciones propias del entorno.

Cada agente posee características como:

- Edad
- Energía
- Tiempo de reacción
- Velocidad de movimiento
- Nivel de pánico
- Conocimiento de salidas
- Comportamiento grupal

El entorno incorpora elementos dinámicos como:

- Propagación probabilística del fuego
- Difusión y acumulación de humo
- Obstáculos estructurales
- Congestión de personas
- Bloqueo de rutas
- Salidas de evacuación

El objetivo no es producir predicciones exactas del incendio real, sino construir una plataforma experimental que permita estudiar dinámicas emergentes de evacuación humana.

---

# Objetivos del estudio de simulación

## Objetivo General

Desarrollar una simulación de evacuación humana basada en agentes (ABM) implementada en Python, inspirada en el modelo PrioritEvac y utilizando como caso de referencia el incendio de The Station Nightclub (2003), con el fin de analizar el comportamiento colectivo durante una evacuación bajo condiciones de incendio y estudiar cómo distintos factores sociales y ambientales afectan las dinámicas de supervivencia, congestión y evacuación.

---

## Objetivos Específicos

### 1. Simular dinámicas de evacuación humana mediante agentes autónomos

Implementar un modelo basado en agentes donde cada individuo posea atributos y comportamientos propios, incluyendo:

- Tiempo de reacción
- Velocidad de movimiento
- Nivel de energía
- Estado físico
- Nivel de pánico
- Conocimiento de salidas
- Comportamiento grupal básico

permitiendo representar decisiones individuales durante una evacuación de emergencia.

---

### 2. Modelar la propagación del fuego y la difusión del humo

Incorporar un sistema dinámico de propagación probabilística del fuego y difusión de humo sobre un entorno discretizado tipo grid, de forma que ambos fenómenos afecten directamente:

- La movilidad de los agentes
- La visibilidad
- La acumulación de daño
- La mortalidad
- Los patrones de evacuación

durante el desarrollo de la simulación.

---

### 3. Cuantificar resultados de evacuación

Medir las principales cantidades de interés al final de cada réplica de simulación (T_MAX = 300 s), incluyendo:

- Número de agentes evacuados
- Número de heridos
- Número de fallecidos
- Personas atrapadas
- Tiempo promedio de evacuación
- Densidad promedio de ocupación

en función de variables como el tiempo de reacción individual, el nivel de exposición al humo y la energía residual de cada agente.

---

### 4. Analizar el efecto de factores sociales y ambientales

Evaluar cómo distintos factores modifican el comportamiento colectivo y los resultados de evacuación, especialmente:

- Congestión en salidas
- Comportamiento grupal
- Niveles de humo
- Velocidad de propagación del fuego
- Bloqueos parciales de rutas
- Variaciones en tiempos de reacción

mediante la comparación de múltiples escenarios experimentales.

---

### 5. Identificar patrones de congestión y bloqueo

Detectar zonas del entorno donde se concentran agentes bloqueados o con movilidad limitada durante la evacuación, utilizando el análisis espacial del grid y los mapas de distancia BFS como indicadores de:

- Cuellos de botella
- Puntos de congestión emergente
- Acumulación de crowd crush
- Ineficiencias en rutas de evacuación

---

### 6. Comparar cualitativamente los resultados con datos históricos

Contrastar cualitativamente los resultados agregados de la simulación con los datos históricos documentados en el informe NIST NCSTAR 2 sobre el incendio de The Station Nightclub, particularmente en relación con:

- Número aproximado de fallecidos
- Número aproximado de heridos
- Comportamiento de evacuación observado
- Uso de salidas
- Evolución temporal de la emergencia

con el propósito de evaluar la razonabilidad y coherencia general del modelo propuesto.

---

# Alcance actual del proyecto

Actualmente el proyecto implementa parcialmente varios de los factores estudiados en PrioritEvac y en investigaciones de evacuación humana.

Entre los elementos ya implementados se encuentran:

- Simulación espacial basada en grids
- Propagación probabilística del fuego
- Difusión y acumulación de humo
- Agentes con atributos individuales
- Tiempos de reacción variables
- Reducción de movilidad por humo
- Lesiones por inhalación y crowd crush
- Comportamiento social básico
- Selección dinámica de salidas
- Métricas de evacuación
- Renderizado visual en tiempo real

Sin embargo, el proyecto continúa en desarrollo y muchos aspectos siguen siendo experimentales o simplificados.

---

# Objetivo experimental

Uno de los principales objetivos del proyecto es generar y comparar distintos escenarios de evacuación para estudiar cómo determinadas variables afectan la supervivencia y el comportamiento colectivo.

La intención es construir una plataforma flexible que permita modificar parámetros y evaluar diferencias en:

- Tiempo total de evacuación
- Número de sobrevivientes
- Número de personas heridas
- Personas atrapadas
- Congestión en salidas
- Impacto del humo
- Influencia del comportamiento grupal
- Efectos de la propagación del fuego
- Uso de distintas salidas
- Variaciones en tiempos de reacción

---

# Escenarios propuestos

El proyecto está diseñado para permitir pruebas bajo distintas condiciones experimentales.

## Escenario 1 — Evacuación base

Simulación estándar utilizando parámetros normales de reacción y propagación.

---

## Escenario 2 — Alta congestión

Mayor número de personas dentro del edificio para estudiar crowd crush y bloqueos.

---

## Escenario 3 — Mayor propagación de humo

Incrementar velocidad o densidad de humo para analizar pérdida de movilidad y mortalidad.

---

## Escenario 4 — Salidas bloqueadas

Cerrar parcialmente algunas salidas para observar redistribución de personas.

---

## Escenario 5 — Comportamiento grupal fuerte

Incrementar tendencia de los agentes a seguir grupos sociales.

---

## Escenario 6 — Reacción tardía

Aumentar tiempos de reacción para analizar impacto en la evacuación.

---

# Cambios respecto al Avance 2

Durante el desarrollo del proyecto, los objetivos definidos inicialmente fueron refinados y ampliados para adaptar el modelo a un enfoque más experimental y flexible.

## Principales modificaciones realizadas

### Cambio de enfoque

Inicialmente el proyecto se centraba principalmente en estimar cantidades finales y compararlas con los datos históricos del incendio.

Actualmente el enfoque se amplió hacia la construcción de una plataforma experimental capaz de analizar múltiples escenarios de evacuación y estudiar el impacto de distintos factores sociales y ambientales.

---

### Incorporación de escenarios comparativos

Se añadió explícitamente el análisis comparativo entre distintos escenarios de simulación, incluyendo:

- Alta congestión
- Mayor propagación de humo
- Salidas bloqueadas
- Reacciones tardías
- Comportamiento grupal intensificado

---

### Mayor énfasis en factores sociales

El modelo actual incorpora con mayor importancia aspectos inspirados en PrioritEvac como:

- Influencia grupal
- Seguimiento social
- Comportamiento colectivo
- Pánico
- Crowd crush

---

### Expansión de métricas

Además de evacuados, heridos y fallecidos, ahora también se consideran:

- Personas atrapadas
- Densidad promedio
- Congestión espacial
- Impacto temporal del humo
- Variaciones en patrones de evacuación

---

### Ajuste del alcance

Se redefinió explícitamente que el proyecto no busca replicar completamente el modelo PrioritEvac ni realizar predicciones exactas del incendio real, sino desarrollar una aproximación simplificada y académica implementada en Python.

---

# Propósito académico

El propósito principal del proyecto es académico y experimental.

No busca reemplazar herramientas profesionales de ingeniería de evacuación, sino explorar cómo modelos simplificados basados en agentes pueden representar dinámicas humanas complejas durante emergencias.

El sistema pretende servir como plataforma de análisis y experimentación para estudiar comportamientos emergentes en evacuaciones bajo incendio.

---

# Tecnologías utilizadas

- Python 3
- NumPy
- Matplotlib
- CSV
- Simulación basada en grids
- Agent-Based Modeling (ABM)

---
El sistema utiliza datos reales de:
- **Layout del edificio** (paredes, salidas)
- **Posiciones iniciales de personas** (465 agentes)
- **Propagación de fuego** (replay de datos reales)
- **Propagación de humo** (replay de datos reales)

## Características Principales

### Modelo de Agente Humano

Cada agente posee atributos realistas del archivo `People.csv`:
- **Posición inicial**: Coordenadas (x, y) en metros
- **Edad**: Afecta velocidad de movimiento
- **Sexo**: Información demográfica
- **Visitas previas**: Determina conocimiento del lugar
- **Tipo de comportamiento**: Patrón de reacción
- **Número de grupo**: Para comportamiento social
- **Líder de grupo**: Influencia en reacción del grupo
- **Energía inicial**: Resistencia al humo

### Comportamiento Humano Implementado

#### 1. **Velocidad de Movimiento**
- **Mayores de 60 años**: 65% de velocidad base
- **Menores de 16 años**: 85% de velocidad base
- **Adultos (16-60)**: 90-115% de velocidad base (aleatorio)
- **Lesionados**: 55% de velocidad base
- **Pánico alto (≥5)**: 120% de velocidad base

#### 2. **Tiempo de Reacción**
Distribución realista basada en estudios de comportamiento humano:
- **15% rápido**: 8-18 segundos
- **60% normal**: 22-50 segundos
- **25% lento**: 55-95 segundos
- **Retraso social**: 0-12 segundos adicionales
- **Líderes de grupo**: Reaccionan 30% más rápido

#### 3. **Conocimiento del Lugar**
- **Visitantes previos**: Conocen todas las salidas
- **Nuevos visitantes**: Conocen solo 1 salida aleatoria
- **Sesgo de entrada principal**: 72% prefieren la primera salida

#### 4. **Comportamiento Social**
- **Seguimiento de grupo**: 65% siguen a su grupo
- **Influencia de vecinos**: Cambian a la salida más popular del grupo cercano (radio 6 celdas)

#### 5. **Pánico**
El pánico se calcula dinámicamente:
- **Humo >20**: +1 punto de pánico
- **Humo >50**: +2 puntos de pánico
- **Fuego cercano (2 celdas)**: +3 puntos de pánico por celda

#### 6. **Efectos del Humo**
- **Reducción de velocidad**:
  - Humo >20: 65% de velocidad
  - Humo >40: 40% de velocidad
  - Humo >70: 18% de velocidad
- **Duda humana**: 5% probabilidad de no moverse (1% si pánico ≥4)
- **Acumulación de humo inhalado**: 0.22 por unidad de densidad
- **Reducción de energía**: 0.05 por unidad de densidad

#### 7. **Crowd Crush (Aplastamiento)**
- **Densidad ≥7**: Pierde 0.5 energía, 80% probabilidad de bloqueo
- **Densidad ≥9**: Pierde 1.5 energía, se lesiona, 92% probabilidad de bloqueo

#### 8. **Sistema de Salud**
- **Lesiones**: humo_inhaled >120 o energy <45
- **Muerte por fuego**: Contacto directo con celda de fuego
- **Muerte por humo**: energy ≤0 o humo_inhaled >260
- **Evacuación**: Llegar a una salida

### Dinámica del Incendio

#### 1. **Replay de Fuego**
- Utiliza datos reales de `fire_nightclub_merged.csv`
- 34 eventos de fuego hasta t=245 segundos
- Coordenadas exactas del fuego en el tiempo

#### 2. **Expansión de Fuego**
Después del replay, el fuego se expande con probabilidad progresiva:
- **Factor durante replay**: 0.10 (expansión mínima)
- **Factor después de replay**: 1.0 (expansión completa)
- **Probabilidades base**:
  - 0-40s extra: 0.0008
  - 40-80s extra: 0.0012
  - 80-140s extra: 0.0018
  - 140s+ extra: 0.0025
- **Modificadores**:
  - Zona derecha (>58% WIDTH): ×1.8
  - Humo presente: +0.00001 por unidad
  - Cercano a 3+ paredes: ×0.12
  - Cercano a 2 paredes: ×0.40
  - Tiempo >100s: ×1.2
  - Tiempo >180s: ×1.35
- **Propagación**: 4 direcciones cardinales + 8% diagonales

#### 3. **Dinámica de Humo**
- **Replay**: Datos de `smoke.csv` (62 eventos)
- **Factor de replay**: ×3.0
- **Difusión**: Promedio con vecinos ×0.992
- **Generación por fuego**: +10 en celda de fuego
- **Radiación de humo**: Hasta 3 celdas del fuego (4.0 - distancia)

### Navegación y Toma de Decisiones

#### 1. **Mapas de Distancia (BFS)**
- Calculados al inicio para todas las salidas
- BFS desde cada salida hacia el interior
- Distancia Manhattan (4 direcciones)

#### 2. **Elección de Salida**
Cada agente evalúa cada salida con un score:
- **Distancia**: Distancia BFS a la salida
- **Humo en salida**: +10 por unidad de humo
- **Fuego cercano a salida**: +250 si fuego en radio 2 celdas
- **Elige la salida con menor score**

#### 3. **Movimiento**
- **4 direcciones**: Norte, Sur, Este, Oeste
- **Score de cada celda**:
  - Distancia a salida objetivo
  - Humo en celda: +8 por unidad
  - Ruido aleatorio: 0-4
  - Continuidad de dirección: -2 si misma dirección
  - Fuego cercano: +90 si fuego en radio 2
  - Densidad local: +7 por persona cercana
- **Colisiones**: No puede moverse a celda ocupada
- **Solo se mueve dentro del interior** (inside_mask)

### Sistema de Métricas

Se registran métricas cada timestep (300 segundos):
- **tiempo**: Segundo actual
- **evacuados**: Personas que salieron por salidas
- **muertos**: Personas fallecidas (no evacuadas)
- **heridos**: Personas con lesiones
- **vivos**: Personas aún vivas
- **humo_promedio**: Densidad promedio de humo en el grid
- **densidad_promedio**: Densidad promedio de personas alrededor de vivos

Exportadas a `metricas_simulacion.csv`

### Visualización

Renderizado en tiempo real con matplotlib:
- **Fondo**: Blanco claro (0.95, 0.95, 0.95)
- **Paredes**: Gris oscuro (0.10, 0.10, 0.10)
- **Salidas**: Verde (0.0, 0.8, 0.2)
- **Fuego**: Naranja (1.0, 0.3, 0.0)
- **Humo**: Gris con transparencia (0.30, 0.30, 0.30, alpha hasta 0.80)
- **Personas sanas**: Azul (0.0, 0.0, 1.0)
- **Personas lesionadas**: Cyan claro (0.0, 0.7, 1.0)
- **Personas en pánico**: Magenta (1.0, 0.0, 1.0)

## Archivos Requeridos

### Datos de Entrada
1. **building_nightclub.csv**: Layout del edificio
   - Formato: Type, x1, y1, x2, y2
   - Tipos: wall, exit
   - Coordenadas en metros

2. **People.csv**: Datos de los 465 agentes
   - Columnas: x, y, age, sex, prior_visit, behavior_type, group_number, group_leader, initial_energy
   - Coordenadas en metros

3. **fire_nightclub_merged.csv**: Replay de fuego
   - Formato: x, y, t
   - Coordenadas en grid, tiempo en segundos

4. **smoke.csv**: Replay de humo
   - Formato: x, y, t, density
   - Coordenadas escaladas /10, tiempo en segundos

### Archivos Generados
1. **metricas_simulacion.csv**: Métricas temporales de la simulación

## Instalación y Dependencias

### Requisitos
- Python 3.7+
- pip

### Dependencias
```bash
pip install numpy matplotlib
```

## Cómo Ejecutar

```bash
python main.py
```

### Salida Esperada en Consola
```
WIDTH: 65
HEIGHT: 41
EXITS: 14
Fire events: 34
Max fire replay time: 245
Smoke events: 62
Distance maps calculados
Agentes: 465
Métricas exportadas
================================
RESULTADOS
================================
Evacuados: [número]
Muertos: [número]
Heridos: [número]
Atrapados: [número]
```

### Visualización
Se abrirá una ventana de matplotlib mostrando la simulación en tiempo real con actualizaciones cada 0.01 segundos.

## Configuración del Grid

### Escala
- **CELL_M = 0.5**: Cada celda representa 0.5 metros
- **Grid dinámico**: Calculado según dimensiones del layout
- **Ejemplo**: 65×41 celdas = 32.5m × 20.5m

### Tipos de Celdas
- **FREE = 0**: Espacio libre
- **WALL = 1**: Pared
- **EXIT = 2**: Salida
- **FIRE = 3**: Fuego

## Arquitectura del Código

### Estructura Principal
```
main.py (1294 líneas)
├── Configuración global
├── Clase Agente
├── Funciones de carga de datos
│   ├── cargar_layout()
│   ├── calcular_interior()
│   ├── cargar_agentes()
│   ├── cargar_fire()
│   └── cargar_smoke()
├── Funciones de simulación
│   ├── actualizar_fuego()
│   ├── expandir_fuego()
│   ├── actualizar_smoke()
│   └── mover()
├── Funciones de navegación
│   ├── calcular_distance_maps()
│   ├── elegir_mejor_salida()
│   └── calcular_densidad_local()
├── Funciones de comportamiento
│   └── actualizar_comportamiento_social()
├── Funciones de métricas
│   ├── guardar_metricas()
│   └── exportar_metricas()
├── Visualización
│   └── render()
└── Loop principal
    └── simular()
```

### Flujo de Ejecución
1. Cargar layout del edificio
2. Calcular interior del edificio (BFS)
3. Cargar eventos de fuego
4. Cargar eventos de humo
5. Calcular mapas de distancia a salidas (BFS)
6. Cargar agentes desde People.csv
7. Loop de simulación (300 timesteps):
   - Actualizar fuego (replay)
   - Expandir fuego (probabilístico)
   - Actualizar humo (replay + difusión)
   - Mover cada agente
   - Verificar muertes/evacuaciones
   - Guardar métricas
   - Renderizar
8. Exportar métricas a CSV
9. Imprimir resultados finales

## Resultados de Simulación

### Resultados Típicos
Basado en ejecuciones recientes:
- **Evacuados**: ~200-340 personas
- **Muertos**: ~50-100 personas
- **Heridos**: ~15-120 personas
- **Atrapados**: ~70-160 personas

### Factores que Afectan Resultados
- Distribución inicial de personas
- Tiempo de reacción individual
- Conocimiento del lugar
- Comportamiento de grupo
- Densidad de multitud
- Velocidad de propagación del fuego
- Intensidad del humo

## Parámetros Ajustables

### En el Código
- **CELL_M**: Escala de celda (línea 12)
- **Tiempos de simulación**: range(300) en simular() (línea 1184)
- **Umbrales de pánico**: líneas 827-842
- **Factores de velocidad**: líneas 850-863
- **Probabilidades de crowd crush**: líneas 892-906
- **Umbrales de salud**: líneas 1213-1244

## Limitaciones y Consideraciones

### Simplificaciones
- Movimiento en grid discreto (no continuo)
- 4 direcciones de movimiento (no diagonales principales)
- Una persona por celda
- Sin física de fluidos para humo (difusión simple)
- Sin modelo de temperatura
- Sin interacción con bomberos o personal de emergencia

### Suposiciones
- Las personas conocen el layout si visitaron previamente
- El comportamiento de grupo es simplificado
- No hay comunicación verbal explícita
- No hay obstáculos móviles
- Las salidas siempre están accesibles

## Futuras Mejoras Posibles

1. **Modelo de humo más avanzado**: CFD (Computational Fluid Dynamics)
2. **Movimiento continuo**: En lugar de grid discreto
3. **Comunicación entre agentes**: Información compartida
4. **Personal de emergencia**: Bomberos, guías
5. **Múltiples escenarios**: Diferentes layouts, condiciones
6. **Validación con datos reales**: Comparación con incidentes históricos
7. **Optimización de rendimiento**: Para simulaciones más grandes
8. **Interfaz gráfica**: Para ajustar parámetros en tiempo real

## Referencias

El modelo se basa en investigaciones de:

## Modelo social ABM

Fridolf, K., Ronchi, E., Nilsson, D., & Frantzich, H. (2020).  
*PrioritEvac: An Agent-Based Model (ABM) for Examining Social Factors of Building Fire Evacuation.*  
CoMSES Network.

https://www.comses.net/codebases/5f78b0ef-60b6-4049-9157-a2e82e7cc286/

---

## Caso de estudio del incendio

National Institute of Standards and Technology (NIST). (2008).  
*Report of the Technical Investigation of The Station Nightclub Fire.*  
NIST NCSTAR 2, Volume 1.

https://www.nist.gov/publications/report-technical-investigation-station-nightclub-fire-nist-ncstar-2-volume-1

## Licencia

Proyecto académico para investigación en simulación de evacuación.

## Contacto

Para preguntas o sugerencias, contactar al desarrollador.
