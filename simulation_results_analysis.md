# Resultados y análisis de simulación

## 1. Fuentes de resultados

La comparación de escenarios se basó en los reportes Monte Carlo generados para cada alternativa y en los archivos estadísticos por escenario.

- Reportes estadísticos por escenario:
  - `statistical_report_s1_n50.md`
  - `statistical_report_s2_n50.md`
  - `statistical_report_s3_n50.md`
  - `statistical_report_s4_n50.md`
  - `statistical_report_s5_n50.md`
  - `statistical_report_s6_n50.md`
- Archivos CSV de simulaciones Monte Carlo:
  - `montecarlo_results_s1_n50.csv`
  - `montecarlo_results_s2_n50.csv`
  - `montecarlo_results_s3_n50.csv`
  - `montecarlo_results_s4_n50.csv`
  - `montecarlo_results_s5_n50.csv`
  - `montecarlo_results_s6_n50.csv`
- Figuras y histogramas por escenario disponibles en los directorios `scenario_* /plots/` y `scenario_* /heatmaps/`.

Las figuras de distribución, intervalos de confianza y bootstrap se guardan por escenario, por ejemplo:
- `scenario_1/plots/histogram_evacuated_s1_n50.png`
- `scenario_1/plots/boxplot_metrics_s1_n50.png`
- `scenario_2/plots/histogram_deaths_s2_n50.png`
- `scenario_6/plots/bootstrap_total_dead_s6_n50.png`

---

## 2. Resultados por escenario (promedios Monte Carlo)

Los valores muestran el promedio de 50 réplicas por escenario para cada variable de interés.

| Escenario | Evacuados | Muertos | Heridos | Atrapados | Tiempo de escape (s) | Humo promedio | Densidad máxima |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 187.9 | 99.6 | 123.6 | 177.5 | 167.7 | 915.7 | 4.1 |
| Alta congestión | 190.4 | 249.0 | 347.5 | 260.6 | 160.1 | 913.3 | 5.9 |
| Más humo | 184.7 | 120.0 | 148.9 | 160.3 | 165.5 | 1004.2 | 4.1 |
| Salidas bloqueadas | 186.4 | 100.9 | 124.8 | 177.7 | 168.1 | 917.5 | 4.1 |
| Grupo fuerte | 188.0 | 99.6 | 123.8 | 177.4 | 167.7 | 915.3 | 4.1 |
| Reacción tardía | 144.4 | 155.8 | 182.4 | 164.7 | 188.7 | 917.6 | 4.1 |

### Interpretación rápida de los resultados

- **Base:** el escenario nominal mantiene un balance intermedio entre evacuados, muertos y tiempo de escape.
- **Alta congestión:** genera la peor degradación global, con **249.0 muertos**, **347.5 heridos** y **260.6 atrapados**, aunque el tiempo medio de escape se reduce a **160.1 s** porque el modelo concentra a muchos agentes en movimiento, pero con alto daño acumulado.
- **Más humo:** incrementa el humo promedio a **1004.2** y eleva los daños (
  **120.0 muertos** y **148.9 heridos**) respecto a la base.
- **Salidas bloqueadas:** mantiene resultados muy cercanos al base en mortalidad y heridas, con una pequeña degradación (100.9 muertos y 124.8 heridos).
- **Grupo fuerte:** prácticamente reproduce el comportamiento base, lo que indica que, en esta configuración, el incremento del seguimiento grupal no altera de forma relevante los resultados agregados.
- **Reacción tardía:** es el caso más severo en términos de pérdida de evacuación efectiva: solo **144.4 evacuados**, **155.8 muertos** y **182.4 heridos**, además del mayor tiempo medio de escape (**188.7 s**).

---

## 3. Comparación relativa respecto al escenario base

La tabla siguiente muestra cómo cambian los indicadores frente al escenario base (Δ %).

| Escenario | Δ Evacuados | Δ Muertos | Δ Heridos | Δ Tiempo de escape | Δ Humo promedio |
|---|---:|---:|---:|---:|---:|
| Alta congestión | +1.3% | +150.1% | +181.1% | -4.5% | -0.3% |
| Más humo | -1.7% | +20.5% | +20.4% | -1.3% | +9.7% |
| Salidas bloqueadas | -0.8% | +1.3% | +1.0% | +0.3% | +0.2% |
| Grupo fuerte | +0.0% | +0.0% | +0.1% | +0.0% | -0.0% |
| Reacción tardía | -23.1% | +56.5% | +47.5% | +12.6% | +0.2% |

### Análisis de comparación

1. **Alta congestión** es el escenario más dañino en términos de salud y atrapamiento. El aumento de población de 465 a 700 agentes dispara la mortalidad y las lesiones, especialmente por acumulación local de personas y congestión sostenida. Aunque el tiempo medio de escape disminuye, ello no indica mejor desempeño: el sistema presenta más daño por colisiones, exposición acumulada y crowding.
2. **Más humo** incrementa claramente la severidad ambiental. Se observa un aumento de **9.7%** en humo promedio, con **20.5%** más muertos y **20.4%** más heridos. Este escenario muestra que el deterioro del ambiente afecta tanto movilidad como supervivencia.
3. **Salidas bloqueadas** tiene un efecto moderado. Reducir rutas de evacuación no genera un cambio dramático en los indicadores agregados, pero sí mantiene pérdidas ligeramente superiores a la base, sobre todo en atrapados y tiempo de escape.
4. **Grupo fuerte** casi no altera los resultados respecto al base. Esto sugiere que, bajo estas condiciones, el comportamiento grupal no es el factor dominante en los indicadores agregados.
5. **Reacción tardía** es el peor escenario en evacuación efectiva. La demora en reaccionar reduce los evacuados en **23.1%**, incrementa muertos en **56.5%** y heridos en **47.5%**, además de aumentar el tiempo medio de escape en **12.6%**. Es la alternativa más severa en términos de desempeño de evacuación.

---

## 4. Evidencia visual y estadística

Las distribuciones de resultados muestran la variabilidad entre réplicas y deben consultarse junto con los promedios.

- Histogramas y boxplots por escenario: `scenario_1/plots/histogram_evacuated_s1_n50.png`, `scenario_1/plots/boxplot_metrics_s1_n50.png`, `scenario_2/plots/histogram_deaths_s2_n50.png`, `scenario_6/plots/histogram_escape_times_s6_n50.png`.
- Intervalos de confianza y bootstrap por escenario: `scenario_1/plots/confidence_intervals_s1_n50.png`, `scenario_1/plots/bootstrap_total_dead_s1_n50.png`, `scenario_6/plots/bootstrap_total_trapped_s6_n50.png`.
- Heatmaps espaciales de congestión, humo y mortalidad por escenario en los directorios `scenario_*/heatmaps/`.

La dispersión de resultados es consistente con la naturaleza estocástica del modelo: los escenarios más extremos muestran mayor variabilidad en muertes, heridos y tiempos de escape, especialmente en la congestión y la reacción tardía.

---

## 5. Conclusiones del análisis

1. El **escenario base** sirve como referencia estable y produce resultados intermedios.
2. **Alta congestión** es la alternativa más severa en daños humanos y atrapamiento, confirmando que la densidad de población es un factor crítico.
3. **Más humo** incrementa de forma relevante la severidad del incendio al elevar la exposición ambiental y el daño.
4. **Reacción tardía** es la alternativa con mayor impacto negativo sobre evacuación real, con una caída fuerte en evacuados y aumento marcado de mortalidad y lesiones.
5. **Salidas bloqueadas** y **grupo fuerte** generan cambios menores en los indicadores agregados; sus efectos son secundarios frente a la congestión y al retraso en la reacción.
6. En términos de desempeño, los peores resultados se concentran en escenarios con **alta densidad**, **mayor exposición al humo** y **retraso en la respuesta**.

Este informe consolida los resultados numéricos y la comparación entre alternativas, y permite identificar de forma directa cuáles escenarios son los más críticos para la evacuación.
