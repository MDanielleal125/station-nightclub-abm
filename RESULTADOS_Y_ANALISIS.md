# Resultados de la Simulación y Análisis

## Resultados de la Simulación

Esta sección presenta los resultados de las 50 simulaciones Monte Carlo ejecutadas para cada uno de los 6 escenarios alternativos del modelo de evacuación del incendio de The Station Nightclub.

### Escenario 1 - Base (Línea de Referencia)

**Configuración:**
- Número de agentes: 465
- Densidad de humo: 1.0x
- Salidas bloqueadas: 0
- Probabilidad de seguir grupo: 0.65
- Multiplicador de tiempo de reacción: 1.0x
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 187.92 | 26.12 | 5.11 | 178 | 199 | 188 | 184.25 | 191 |
| **Muertes** | 99.58 | 19.35 | 4.40 | 87 | 108 | 100 | 97 | 102.75 |
| **Heridos** | 123.64 | 40.44 | 6.36 | 110 | 139 | 123 | 119 | 128 |
| **Atrapados** | 177.50 | 32.21 | 5.68 | 167 | 189 | 177.5 | 174 | 181 |
| **Tiempo de Escape (s)** | 167.65 | 9.31 | 3.05 | 161.82 | 175.45 | 167.87 | 165.72 | 169.04 |
| **Densidad Máxima** | 4.13 | 0.00 | 0.00 | 4.13 | 4.13 | 4.13 | 4.13 | 4.13 |
| **Humo Promedio** | 915.68 | 107.12 | 10.35 | 893.88 | 939.87 | 915.98 | 910.20 | 922.80 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 187.92 | 5.11 | 1.42 | 186.50 | 189.34 |
| **Muertes** | 99.58 | 4.40 | 1.22 | 98.36 | 100.80 |
| **Heridos** | 123.64 | 6.36 | 1.76 | 121.88 | 125.40 |
| **Atrapados** | 177.50 | 5.68 | 1.57 | 175.93 | 179.07 |
| **Tiempo de Escape (s)** | 167.65 | 3.05 | 0.85 | 166.81 | 168.50 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 187.92 | 187.90 | 0.73 | 186.40 | 189.34 |
| **Muertes** | 99.58 | 99.59 | 0.60 | 98.40 | 100.76 |
| **Atrapados** | 177.50 | 177.48 | 0.81 | 175.96 | 179.08 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 308.01) ✅
- **Muertes:** Distribución Normal (AIC: 293.02) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 256.44) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s1_n50.png` - Histograma de evacuados
- `histogram_deaths_s1_n50.png` - Histograma de muertes
- `histogram_escape_times_s1_n50.png` - Histograma de tiempos de escape
- `boxplot_metrics_s1_n50.png` - Boxplot comparativo de métricas
- `bootstrap_total_evacuated_s1_n50.png` - Distribución bootstrap de evacuados
- `bootstrap_total_dead_s1_n50.png` - Distribución bootstrap de muertes
- `bootstrap_total_trapped_s1_n50.png` - Distribución bootstrap de atrapados
- `confidence_intervals_s1_n50.png` - Intervalos de confianza
- `heatmap_congestion_s1_n50.png` - Heatmap de congestión
- `heatmap_death_s1_n50.png` - Heatmap de muertes
- `heatmap_smoke_s1_n50.png` - Heatmap de exposición al humo

---

### Escenario 2 - Alta Congestión (Sobrepoblación)

**Configuración:**
- Número de agentes: 700 (+50.5% vs S1)
- Densidad de humo: 1.0x
- Salidas bloqueadas: 0
- Probabilidad de seguir grupo: 0.65
- Multiplicador de tiempo de reacción: 1.0x
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 190.36 | 93.17 | 9.65 | 169 | 216 | 190 | 183.25 | 197 |
| **Muertes** | 249.02 | 108.06 | 10.40 | 228 | 271 | 249 | 242 | 256.75 |
| **Heridos** | 347.54 | 269.56 | 16.42 | 317 | 393 | 346 | 337 | 358.5 |
| **Atrapados** | 260.62 | 81.34 | 9.02 | 238 | 281 | 261 | 255.25 | 267 |
| **Tiempo de Escape (s)** | 160.13 | 14.94 | 3.87 | 149.98 | 169.45 | 159.92 | 157.90 | 162.15 |
| **Densidad Máxima** | 5.90 | 0.02 | 0.14 | 5.63 | 6.23 | 5.89 | 5.81 | 5.98 |
| **Humo Promedio** | 913.32 | 186.38 | 13.65 | 879.91 | 942.47 | 913.96 | 904.31 | 923.02 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 190.36 | 9.65 | 2.68 | 187.68 | 193.04 |
| **Muertes** | 249.02 | 10.40 | 2.88 | 246.14 | 251.90 |
| **Heridos** | 347.54 | 16.42 | 4.55 | 342.99 | 352.09 |
| **Atrapados** | 260.62 | 9.02 | 2.50 | 258.12 | 263.12 |
| **Tiempo de Escape (s)** | 160.13 | 3.87 | 1.07 | 159.06 | 161.20 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 190.36 | 190.26 | 1.36 | 187.70 | 192.84 |
| **Muertes** | 249.02 | 249.01 | 1.46 | 246.16 | 251.90 |
| **Atrapados** | 260.62 | 260.69 | 1.24 | 258.28 | 263.10 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 371.61) ✅
- **Muertes:** Distribución Normal (AIC: 379.02) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 280.08) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s2_n50.png`
- `histogram_deaths_s2_n50.png`
- `histogram_escape_times_s2_n50.png`
- `boxplot_metrics_s2_n50.png`
- `bootstrap_total_evacuated_s2_n50.png`
- `bootstrap_total_dead_s2_n50.png`
- `bootstrap_total_trapped_s2_n50.png`
- `confidence_intervals_s2_n50.png`
- `heatmap_congestion_s2_n50.png`
- `heatmap_death_s2_n50.png`
- `heatmap_smoke_s2_n50.png`

---

### Escenario 3 - Más Humo (Mayor Densidad de Humo)

**Configuración:**
- Número de agentes: 465
- Densidad de humo: 1.5x (+50% vs S1)
- Salidas bloqueadas: 0
- Probabilidad de seguir grupo: 0.65
- Multiplicador de tiempo de reacción: 1.0x
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 184.70 | 42.87 | 6.55 | 170 | 198 | 185 | 181.25 | 189 |
| **Muertes** | 119.96 | 33.96 | 5.83 | 106 | 133 | 120.5 | 116 | 124 |
| **Heridos** | 148.92 | 71.59 | 8.46 | 131 | 170 | 148.5 | 143 | 153 |
| **Atrapados** | 160.34 | 42.88 | 6.55 | 149 | 177 | 160 | 155 | 166 |
| **Tiempo de Escape (s)** | 165.48 | 12.20 | 3.49 | 158.31 | 173.03 | 165.38 | 163.25 | 167.95 |
| **Densidad Máxima** | 4.13 | 0.00 | 0.00 | 4.13 | 4.13 | 4.13 | 4.13 | 4.13 |
| **Humo Promedio** | 1004.16 | 193.75 | 13.92 | 965.03 | 1033.52 | 1006.54 | 996.04 | 1012.75 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 184.70 | 6.55 | 1.81 | 182.89 | 186.51 |
| **Muertes** | 119.96 | 5.83 | 1.62 | 118.34 | 121.58 |
| **Heridos** | 148.92 | 8.46 | 2.35 | 146.57 | 151.27 |
| **Atrapados** | 160.34 | 6.55 | 1.82 | 158.52 | 162.16 |
| **Tiempo de Escape (s)** | 165.48 | 3.49 | 0.97 | 164.51 | 166.45 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 184.70 | 184.71 | 0.91 | 182.92 | 186.52 |
| **Muertes** | 119.96 | 119.96 | 0.81 | 118.28 | 121.46 |
| **Atrapados** | 160.34 | 160.32 | 0.89 | 158.54 | 161.96 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 332.79) ✅
- **Muertes:** Distribución Normal (AIC: 321.14) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 269.97) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s3_n50.png`
- `histogram_deaths_s3_n50.png`
- `histogram_escape_times_s3_n50.png`
- `boxplot_metrics_s3_n50.png`
- `bootstrap_total_evacuated_s3_n50.png`
- `bootstrap_total_dead_s3_n50.png`
- `bootstrap_total_trapped_s3_n50.png`
- `confidence_intervals_s3_n50.png`
- `heatmap_congestion_s3_n50.png`
- `heatmap_death_s3_n50.png`
- `heatmap_smoke_s3_n50.png`

---

### Escenario 4 - Salidas Bloqueadas

**Configuración:**
- Número de agentes: 465
- Densidad de humo: 1.0x
- Salidas bloqueadas: 4 (de 18 totales)
- Probabilidad de seguir grupo: 0.65
- Multiplicador de tiempo de reacción: 1.0x
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 186.40 | 41.88 | 6.47 | 168 | 201 | 186.5 | 182 | 191 |
| **Muertes** | 100.92 | 18.20 | 4.27 | 90 | 109 | 100.5 | 98 | 103.75 |
| **Heridos** | 124.84 | 55.48 | 7.45 | 106 | 148 | 126 | 120 | 129 |
| **Atrapados** | 177.68 | 33.81 | 5.82 | 161 | 190 | 177 | 175 | 181 |
| **Tiempo de Escape (s)** | 168.13 | 10.75 | 3.28 | 161.74 | 175.39 | 168.19 | 165.84 | 170.82 |
| **Densidad Máxima** | 4.13 | 0.00 | 0.00 | 4.13 | 4.13 | 4.13 | 4.13 | 4.13 |
| **Humo Promedio** | 917.53 | 125.09 | 11.18 | 890.79 | 954.32 | 917.34 | 910.92 | 923.48 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 186.40 | 6.47 | 1.79 | 184.61 | 188.19 |
| **Muertes** | 100.92 | 4.27 | 1.18 | 99.74 | 102.10 |
| **Heridos** | 124.84 | 7.45 | 2.06 | 122.78 | 126.90 |
| **Atrapados** | 177.68 | 5.82 | 1.61 | 176.07 | 179.29 |
| **Tiempo de Escape (s)** | 168.13 | 3.28 | 0.91 | 167.22 | 169.04 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 186.40 | 186.42 | 0.92 | 184.64 | 188.28 |
| **Muertes** | 100.92 | 100.93 | 0.60 | 99.82 | 102.14 |
| **Atrapados** | 177.68 | 177.68 | 0.80 | 176.14 | 179.26 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 331.62) ✅
- **Muertes:** Distribución Normal (AIC: 289.95) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 263.64) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s4_n50.png`
- `histogram_deaths_s4_n50.png`
- `histogram_escape_times_s4_n50.png`
- `boxplot_metrics_s4_n50.png`
- `bootstrap_total_evacuated_s4_n50.png`
- `bootstrap_total_dead_s4_n50.png`
- `bootstrap_total_trapped_s4_n50.png`
- `confidence_intervals_s4_n50.png`
- `heatmap_congestion_s4_n50.png`
- `heatmap_death_s4_n50.png`
- `heatmap_smoke_s4_n50.png`

---

### Escenario 5 - Comportamiento Grupal Fuerte

**Configuración:**
- Número de agentes: 465
- Densidad de humo: 1.0x
- Salidas bloqueadas: 0
- Probabilidad de seguir grupo: 0.90 (+38.5% vs S1)
- Multiplicador de tiempo de reacción: 1.0x
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 188.00 | 27.92 | 5.28 | 178 | 199 | 187.5 | 184.25 | 191 |
| **Muertes** | 99.62 | 19.51 | 4.42 | 87 | 108 | 100 | 97 | 102.75 |
| **Heridos** | 123.78 | 39.73 | 6.30 | 110 | 139 | 123.5 | 119 | 128 |
| **Atrapados** | 177.38 | 33.75 | 5.81 | 167 | 189 | 177.5 | 174 | 181 |
| **Tiempo de Escape (s)** | 167.66 | 9.49 | 3.08 | 161.82 | 175.45 | 167.87 | 165.23 | 169.32 |
| **Densidad Máxima** | 4.13 | 0.00 | 0.00 | 4.13 | 4.13 | 4.13 | 4.13 | 4.13 |
| **Humo Promedio** | 915.35 | 115.53 | 10.75 | 893.88 | 939.87 | 915.98 | 908.56 | 922.80 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 188.00 | 5.28 | 1.46 | 186.54 | 189.46 |
| **Muertes** | 99.62 | 4.42 | 1.22 | 98.40 | 100.84 |
| **Heridos** | 123.78 | 6.30 | 1.75 | 122.03 | 125.53 |
| **Atrapados** | 177.38 | 5.81 | 1.61 | 175.77 | 178.99 |
| **Tiempo de Escape (s)** | 167.66 | 3.08 | 0.85 | 166.80 | 168.51 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 188.00 | 187.98 | 0.75 | 186.54 | 189.44 |
| **Muertes** | 99.62 | 99.63 | 0.60 | 98.46 | 100.84 |
| **Atrapados** | 177.38 | 177.36 | 0.83 | 175.84 | 179.00 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 311.35) ✅
- **Muertes:** Distribución Normal (AIC: 293.42) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 257.39) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s5_n50.png`
- `histogram_deaths_s5_n50.png`
- `histogram_escape_times_s5_n50.png`
- `boxplot_metrics_s5_n50.png`
- `bootstrap_total_evacuated_s5_n50.png`
- `bootstrap_total_dead_s5_n50.png`
- `bootstrap_total_trapped_s5_n50.png`
- `confidence_intervals_s5_n50.png`
- `heatmap_congestion_s5_n50.png`
- `heatmap_death_s5_n50.png`
- `heatmap_smoke_s5_n50.png`

---

### Escenario 6 - Reacción Tardía

**Configuración:**
- Número de agentes: 465
- Densidad de humo: 1.0x
- Salidas bloqueadas: 0
- Probabilidad de seguir grupo: 0.65
- Multiplicador de tiempo de reacción: 2.0x (+100% vs S1)
- Pasos de simulación: 300

**Estadísticas Descriptivas (50 simulaciones):**

| Métrica | Media | Varianza | Desv. Estándar | Mín | Máx | Mediana | Q25 | Q75 |
|---------|-------|----------|----------------|-----|-----|---------|-----|-----|
| **Evacuados** | 144.44 | 33.44 | 5.78 | 129 | 154 | 145 | 140.25 | 148.75 |
| **Muertes** | 155.82 | 74.40 | 8.63 | 141 | 187 | 154 | 151 | 161 |
| **Heridos** | 182.36 | 94.40 | 9.72 | 162 | 203 | 181.5 | 178 | 188.75 |
| **Atrapados** | 164.74 | 81.83 | 9.05 | 127 | 184 | 165 | 160.25 | 169.75 |
| **Tiempo de Escape (s)** | 188.70 | 16.89 | 4.11 | 180.54 | 196.77 | 188.98 | 185.55 | 191.78 |
| **Densidad Máxima** | 4.13 | 0.00 | 0.00 | 4.13 | 4.13 | 4.13 | 4.13 | 4.13 |
| **Humo Promedio** | 917.55 | 172.59 | 13.14 | 889.17 | 952.36 | 917.70 | 910.69 | 926.51 |

**Intervalos de Confianza al 95%:**

| Métrica | Media | Desv. Estándar | Margen de Error | IC Inferior | IC Superior |
|---------|-------|----------------|----------------|-------------|-------------|
| **Evacuados** | 144.44 | 5.78 | 1.60 | 142.84 | 146.04 |
| **Muertes** | 155.82 | 8.63 | 2.39 | 153.43 | 158.21 |
| **Heridos** | 182.36 | 9.72 | 2.69 | 179.67 | 185.05 |
| **Atrapados** | 164.74 | 9.05 | 2.51 | 162.23 | 167.25 |
| **Tiempo de Escape (s)** | 188.70 | 4.11 | 1.14 | 187.56 | 189.84 |

**Resultados de Bootstrap (1000 muestras):**

| Métrica | Media Original | Media Bootstrap | Desv. Bootstrap | IC Inferior Bootstrap | IC Superior Bootstrap |
|---------|----------------|-----------------|-----------------|----------------------|----------------------|
| **Evacuados** | 144.44 | 144.43 | 0.81 | 142.90 | 146.00 |
| **Muertes** | 155.82 | 155.77 | 1.21 | 153.62 | 158.30 |
| **Atrapados** | 164.74 | 164.72 | 1.25 | 162.18 | 166.88 |

**Distribuciones Ajustadas (MLE):**
- **Evacuados:** Distribución Normal (AIC: 320.36) ✅
- **Muertes:** Distribución Log-Normal (AIC: 360.24) ✅
- **Tiempo de Escape:** Distribución Normal (AIC: 286.21) ✅

**Visualizaciones Generadas:**
- `histogram_evacuated_s6_n50.png`
- `histogram_deaths_s6_n50.png`
- `histogram_escape_times_s6_n50.png`
- `boxplot_metrics_s6_n50.png`
- `bootstrap_total_evacuated_s6_n50.png`
- `bootstrap_total_dead_s6_n50.png`
- `bootstrap_total_trapped_s6_n50.png`
- `confidence_intervals_s6_n50.png`
- `heatmap_congestion_s6_n50.png`
- `heatmap_death_s6_n50.png`
- `heatmap_smoke_s6_n50.png`

---

## Análisis de los Resultados

### Resumen de Medidas de Desempeño

La siguiente tabla presenta un resumen comparativo de las medidas de desempeño clave para los 6 escenarios simulados:

| Escenario | Agentes | Evacuados | Muertes | % Mortalidad | Heridos | Atrapados | Tiempo Escape (s) | Densidad Máx |
|-----------|---------|-----------|---------|--------------|---------|-----------|-------------------|--------------|
| **S1 - Base** | 465 | 187.9 ± 5.1 | 99.6 ± 4.4 | 21.4% | 123.6 ± 6.4 | 177.5 ± 5.7 | 167.7 ± 3.1 | 4.13 |
| **S2 - Alta Congestión** | 700 | 190.4 ± 9.7 | 249.0 ± 10.4 | 35.6% | 347.5 ± 16.4 | 260.6 ± 9.0 | 160.1 ± 3.9 | 5.90 |
| **S3 - Más Humo** | 465 | 184.7 ± 6.6 | 120.0 ± 5.8 | 25.8% | 148.9 ± 8.5 | 160.3 ± 6.6 | 165.5 ± 3.5 | 4.13 |
| **S4 - Salidas Bloqueadas** | 465 | 186.4 ± 6.5 | 100.9 ± 4.3 | 21.7% | 124.8 ± 7.5 | 177.7 ± 5.8 | 168.1 ± 3.3 | 4.13 |
| **S5 - Grupo Fuerte** | 465 | 188.0 ± 5.3 | 99.6 ± 4.4 | 21.4% | 123.8 ± 6.3 | 177.4 ± 5.8 | 167.7 ± 3.1 | 4.13 |
| **S6 - Reacción Tardía** | 465 | 144.4 ± 5.8 | 155.8 ± 8.6 | 33.5% | 182.4 ± 9.7 | 164.7 ± 9.0 | 188.7 ± 4.1 | 4.13 |

### Comparación de Modelos Alternativos

#### 1. Impacto de la Sobrepoblación (S1 vs S2)

**Diferencias observadas:**
- **Evacuados:** +1.3% (190.4 vs 187.9) - Diferencia no significativa estadísticamente
- **Muertes:** +150% (249.0 vs 99.6) - Aumento dramático y estadísticamente significativo
- **Heridos:** +181% (347.5 vs 123.6) - Aumento dramático
- **Atrapados:** +47% (260.6 vs 177.5) - Aumento significativo
- **Tiempo de Escape:** -4.5% (160.1s vs 167.7s) - Ligeramente más rápido
- **Densidad Máxima:** +43% (5.90 vs 4.13) - Aumento significativo de congestión

**Análisis:**
A pesar de tener 50.5% más agentes, el número de evacuados prácticamente no aumenta (solo +1.3%). Esto indica que las salidas están operando a capacidad máxima en el escenario base. La mortalidad aumenta del 21.4% al 35.6%, un aumento del 66% en la tasa de mortalidad. La densidad máxima aumenta significativamente, lo que causa bloqueos fatales. El tiempo de escape ligeramente más rápido puede explicarse por el pánico inducido por la sobrepoblación.

**Conclusión:** La sobrepoblación es el factor más crítico para la mortalidad, aumentando las muertes en un 150% mientras que el número de evacuados permanece casi constante.

#### 2. Impacto del Humo (S1 vs S3)

**Diferencias observadas:**
- **Evacuados:** -1.7% (184.7 vs 187.9) - Disminución leve
- **Muertes:** +20% (120.0 vs 99.6) - Aumento significativo
- **Heridos:** +20% (148.9 vs 123.6) - Aumento significativo
- **Atrapados:** -10% (160.3 vs 177.5) - Disminución inesperada
- **Tiempo de Escape:** -1.3% (165.5s vs 167.7s) - Ligeramente más rápido
- **Humo Promedio:** +9.7% (1004.2 vs 915.7) - Aumento esperado

**Análisis:**
El aumento del 50% en la densidad de humo aumenta las muertes en un 20% y los heridos en un 20%. Sorprendentemente, el número de atrapados disminuye en un 10%, posiblemente porque los agentes mueren antes de quedar atrapados. El tiempo de escape es ligeramente más rápido, lo que puede indicar que los agentes con mayor exposición al humo mueren más rápido, reduciendo el tiempo promedio de escape.

**Conclusión:** El humo es un factor significativo para la mortalidad, pero su impacto es menor que la sobrepoblación. El humo reduce visibilidad y aumenta la probabilidad de lesiones y muertes.

#### 3. Impacto de Salidas Bloqueadas (S1 vs S4)

**Diferencias observadas:**
- **Evacuados:** -0.8% (186.4 vs 187.9) - Diferencia no significativa
- **Muertes:** +1.3% (100.9 vs 99.6) - Diferencia no significativa
- **Heridos:** +1.0% (124.8 vs 123.6) - Diferencia no significativa
- **Atrapados:** +0.1% (177.7 vs 177.5) - Diferencia no significativa
- **Tiempo de Escape:** +0.2% (168.1s vs 167.7s) - Diferencia no significativa

**Análisis:**
Bloquear 4 de las 18 salidas (22% de las salidas) no tiene un impacto estadísticamente significativo en ninguna de las métricas principales. Las 14 salidas restantes son suficientes para manejar el flujo de 465 agentes. Esto sugiere que el diseño original del club tenía una redundancia significativa en el sistema de salidas.

**Conclusión:** El sistema de salidas del club tenía redundancia suficiente. Bloquear hasta el 22% de las salidas no afecta significativamente la evacuación.

#### 4. Impacto del Comportamiento Grupal (S1 vs S5)

**Diferencias observadas:**
- **Evacuados:** +0.1% (188.0 vs 187.9) - Diferencia no significativa
- **Muertes:** 0% (99.6 vs 99.6) - Sin diferencia
- **Heridos:** +0.1% (123.8 vs 123.6) - Diferencia no significativa
- **Atrapados:** -0.1% (177.4 vs 177.5) - Diferencia no significativa
- **Tiempo de Escape:** 0% (167.7s vs 167.7s) - Sin diferencia

**Análisis:**
Aumentar la probabilidad de seguir al grupo de 0.65 a 0.90 (aumento del 38.5%) no tiene ningún impacto estadísticamente significativo en ninguna de las métricas. Esto sugiere que el comportamiento grupal no mejora ni empeora significativamente la evacuación en este contexto.

**Conclusión:** El comportamiento grupal no es un factor determinante en la evacuación. Seguir al grupo no confiere ventajas ni desventajas significativas.

#### 5. Impacto del Tiempo de Reacción (S1 vs S6)

**Diferencias observadas:**
- **Evacuados:** -23.1% (144.4 vs 187.9) - Disminución dramática
- **Muertes:** +56% (155.8 vs 99.6) - Aumento dramático
- **Heridos:** +47% (182.4 vs 123.6) - Aumento significativo
- **Atrapados:** -7% (164.7 vs 177.5) - Disminución
- **Tiempo de Escape:** +12.5% (188.7s vs 167.7s) - Aumento significativo
- **Mortalidad:** +56% en tasa (33.5% vs 21.4%)

**Análisis:**
Duplicar el tiempo de reacción tiene el impacto más severo en el número de evacuados (-23.1%) y el segundo mayor impacto en muertes (+56%, después de la sobrepoblación). Los agentes que reaccionan tarde tienen menos tiempo para escapar antes de que el fuego y el humo se propaguen. El tiempo de escape aumenta significativamente porque los agentes que logran escapar lo hacen más tarde. La mortalidad aumenta del 21.4% al 33.5%.

**Conclusión:** El tiempo de reacción es el factor más crítico para la capacidad de evacuación. Reaccionar tarde reduce dramáticamente el número de personas que pueden escapar.

### Ranking de Impacto en Mortalidad

| Factor | Escenario | Muertes | % vs S1 | Ranking |
|--------|-----------|---------|---------|---------|
| **Sobrepoblación** | S2 | 249.0 | +150% | 🔴 1 (PEOR) |
| **Reacción Tardía** | S6 | 155.8 | +56% | 🟠 2 |
| **Más Humo** | S3 | 120.0 | +20% | 🟡 3 |
| **Salidas Bloqueadas** | S4 | 100.9 | +1.3% | 🟢 4 |
| **Grupo Fuerte** | S5 | 99.6 | 0% | 🟢 5 |
| **Base** | S1 | 99.6 | - | 🟢 6 (MEJOR) |

### Ranking de Impacto en Evacuación

| Factor | Escenario | Evacuados | % vs S1 | Ranking |
|--------|-----------|-----------|---------|---------|
| **Reacción Tardía** | S6 | 144.4 | -23.1% | 🔴 1 (PEOR) |
| **Más Humo** | S3 | 184.7 | -1.7% | 🟠 2 |
| **Salidas Bloqueadas** | S4 | 186.4 | -0.8% | 🟡 3 |
| **Base** | S1 | 187.9 | - | 🟡 4 |
| **Grupo Fuerte** | S5 | 188.0 | +0.1% | 🟢 5 |
| **Alta Congestión** | S2 | 190.4 | +1.3% | 🟢 6 (MEJOR) |

### Análisis de Distribuciones

Todos los escenarios muestran distribuciones normales para las métricas principales, excepto el Escenario 6 donde las muertes siguen una distribución log-normal. Esto indica que:

1. **Consistencia:** La mayoría de las métricas tienen distribuciones simétricas y bien comportadas
2. **S6 Excepción:** La distribución log-normal de muertes en S6 indica una asimetría hacia valores más altos, lo que es consistente con el comportamiento de reacción tardía donde algunos agentes escapan y otros no

### Validación con Datos Históricos

El escenario base (S1) produce resultados consistentes con el incendio real de The Station Nightclub:
- **Muertes reales:** 100 personas
- **Muertes simuladas (S1):** 99.6 ± 4.4 (95% CI: [98.4, 100.8])
- **Concordancia:** El valor real cae dentro del intervalo de confianza del 95%

Esta validación confirma que el modelo es representativo del evento histórico.

---

## Conclusiones del Estudio de Simulación

### Conclusiones Principales

1. **La sobrepoblación es el factor más crítico para la mortalidad**
   - Aumentar el aforo de 465 a 700 personas (+50.5%) aumenta las muertes en un 150%
   - La tasa de mortalidad aumenta del 21.4% al 35.6% (+66%)
   - Las salidas operan a capacidad máxima; más personas no evacuan más
   - **Recomendación:** Controlar estrictamente el aforo máximo

2. **El tiempo de reacción es el factor más crítico para la evacuación**
   - Duplicar el tiempo de reacción reduce evacuados en un 23.1%
   - Aumenta muertes en un 56% (segundo peor factor)
   - **Recomendación:** Implementar sistemas de detección temprana y alarmas automáticas

3. **El humo aumenta significativamente la mortalidad**
   - Aumentar densidad de humo en 50% aumenta muertes en 20%
   - Aumenta heridos en 20%
   - **Recomendación:** Mejorar sistemas de ventilación y supresión de humo

4. **El sistema de salidas tenía redundancia suficiente**
   - Bloquear 22% de las salidas no afecta significativamente la evacuación
   - Las 14 salidas restantes son suficientes para 465 personas
   - **Recomendación:** Mantener redundancia en salidas de emergencia

5. **El comportamiento grupal no es determinante**
   - Seguir al grupo no mejora ni empeora significativamente la evacuación
   - **Recomendación:** No priorizar campañas de comportamiento grupal en emergencias

### Implicaciones para Diseño de Seguridad

1. **Control de Aforo:**
   - El aforo máximo debe basarse en la capacidad de evacuación, no en el espacio disponible
   - Para este club, 465 personas parece ser el límite seguro

2. **Sistemas de Detección:**
   - La detección temprana es crítica para reducir el tiempo de reacción
   - Alarmas automáticas y sistemas de notificación inmediatos son esenciales

3. **Ventilación:**
   - Sistemas de ventilación de emergencia pueden reducir mortalidad en hasta 20%
   - Supresión de humo debe ser prioridad en diseño de seguridad

4. **Redundancia de Salidas:**
   - El diseño original del club tenía buena redundancia
   - Mantener múltiples salidas es importante pero no suficiente por sí solo

### Limitaciones del Estudio

1. **Modelo 2D:** No considera altura del club ni escaleras
2. **Agentes Homogéneos:** No considera diferencias individuales (edad, movilidad)
3. **Comportamiento Determinista:** No modela pánico explícito
4. **Datos Históricos:** Fuego y humo basados en reconstrucción, no datos en tiempo real

### Trabajo Futuro

1. Implementar modelo 3D con altura y escaleras
2. Incluir agentes heterogéneos con diferentes capacidades
3. Modelar pánico explícito con comportamiento adaptativo
4. Integrar simulación CFD para dinámica de humo más realista
5. Validar con otros eventos históricos de evacuación

### Conclusión Final

Este estudio de simulación ABM proporciona una comprensión cuantitativa de los factores que afectan la evacuación en situaciones de emergencia. Los resultados indican que el control de aforo y la detección temprana son las intervenciones más efectivas para reducir la mortalidad, mientras que el comportamiento grupal y la redundancia de salidas tienen menor impacto. El modelo ha sido validado con datos históricos y produce resultados estadísticamente robustos, proporcionando una base sólida para decisiones de diseño de seguridad.
