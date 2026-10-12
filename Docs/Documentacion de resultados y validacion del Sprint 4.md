# Sprint 4 — Resultados y validación del recocido simulado

## 1. Objetivo y alcance

El Sprint 4 incorporó **recocido simulado (Simulated Annealing, SA)** como segunda estrategia de optimización del despliegue 5G FWA, y comparó su desempeño con la **búsqueda local del profesor** y con **Iterated Local Search (ILS)**, implementado en el Sprint 3. Se mantuvo `evaluate_plan_sprint2()`, incluyendo el criterio de cobertura basado en el umbral de SINR, y la función objetivo ponderada `objective_sprint3()`.

El análisis se concentró en **PB37–PB45**: implementación de SA, comparación, sensibilidad a la cantidad de sitios y a los pesos, sensibilidad a umbrales técnicos, robustez ante semillas y selección de diseños candidatos. Este documento corresponde a **PB46**.

## 2. Metodología

SA parte de una configuración inicial de **S sitios**, genera vecinos mediante intercambios **1-swap** (retira un sitio desplegado e incorpora otro candidato) y evalúa cada vecino con la función del Sprint 2. Si el valor de la función objetivo mejora, acepta el cambio; si empeora, puede aceptarlo con probabilidad `exp(ΔJ/T)`, donde `T` disminuye progresivamente. En todo momento conserva la mejor solución encontrada.

Con los pesos originales, la función objetivo es:

**J = cobertura poblacional + capacidad satisfecha − 0.15 × (S/12)**.

Las metas del escenario son **cobertura ≥ 85 %**, **capacidad satisfecha ≥ 80 %** y **S ≤ 12**. La capacidad satisfecha corresponde al **modelo simplificado por punto de demanda** del Sprint 2; no incorpora una restricción adicional de capacidad agregada por estación.

Los experimentos utilizaron búsqueda local, ILS y SA con sus configuraciones de ejecución documentadas en el notebook. Los valores finales de todas las configuraciones se recalcularon con `evaluate_plan_sprint2()` y `objective_sprint3()`. Debe tenerse presente que la búsqueda local original del profesor **optimiza internamente con `evaluate_plan()` y `objective()`**, mientras ILS y SA usan las funciones corregidas: esto limita una comparación estrictamente equivalente entre los tres procedimientos, aunque las métricas finales publicadas estén calculadas con el mismo evaluador.

## 3. Comparación principal de algoritmos (PB39)

Para **S = 8** y los pesos originales se obtuvieron:

| Solución | Cobertura | Capacidad satisfecha | J |
|---|---:|---:|---:|
| Referencia / búsqueda local del profesor | 95.83 % | 97.96 % | 1.837917 |
| ILS (Sprint 3) | 95.67 % | 98.42 % | **1.840833** |
| SA (inicio aleatorio) | 95.79 % | 98.21 % | 1.840000 |
| SA (inicio en referencia) | 95.67 % | 98.42 % | **1.840833** |

ILS y SA desde la referencia encontraron la misma configuración: **`[0, 2, 6, 7, 10, 13, 15, 35]`**. Frente a la referencia del Sprint 2, mejora la capacidad satisfecha en **0.46 puntos porcentuales**, con una reducción de **0.17 puntos porcentuales** de cobertura, y aumenta **J en 0.002917**. Las cuatro configuraciones cumplen los umbrales exigidos.

## 4. Sensibilidad y robustez (PB40–PB43)

- **Cantidad de sitios (PB40):** se compararon **S = 2, 3, 4, 6, 8, 10 y 12**. Las soluciones encontradas con **S = 2** no alcanzaron las metas; **S = 3 fue la menor cantidad probada con soluciones que sí cumplieron**. El mejor valor de J de ese barrido apareció con ocho sitios. Esto no constituye una demostración de optimalidad global ni de imposibilidad para otros conjuntos.
- **Pesos (PB41):** se analizaron seis escenarios. Al eliminar la penalización por sitios, la selección de S entre los valores probados pasó a **12**; con penalización **0.30**, a **6**; y con penalización **0.60**, a **4**. Con S fijo, variar solamente el peso de penalización por sitios no modifica el orden de soluciones del ILS o de SA, pues agrega una constante a todas sus evaluaciones.
- **Umbrales (PB42):** se variaron los requisitos de aceptación y los parámetros técnicos, incluyendo el umbral de SINR de cobertura y la demanda por suscriptor. Las soluciones también fueron verificadas nuevamente bajo los parámetros originales del escenario. Los mínimos de S informados proceden de las **cantidades de sitios experimentadas**, no de una enumeración exhaustiva.
- **Semillas (PB43):** con **10 semillas** para S = 8, la búsqueda local del profesor produjo **7 configuraciones distintas**, ILS **1** y SA **3**. La desviación estándar de J fue aproximadamente **0.00516**, **0** y **0.00386**, respectivamente. En estas pruebas ILS fue más estable, aunque la estabilidad observada está limitada a las semillas, el modelo y los parámetros evaluados. Los tiempos medidos dependen del computador y no deben interpretarse como comparación de igual número de evaluaciones.

## 5. Diseños técnicamente candidatos (PB44)

Se reunieron **35 configuraciones distintas encontradas** que cumplieron los requisitos originales. Dentro de ese conjunto, **16 no están dominadas** al minimizar S y maximizar cobertura y capacidad. Se trata del **frente de Pareto de las soluciones encontradas**, no del frente global de las 36 estaciones candidatas.

| Papel en la comparación | S | Sitios desplegados | Cobertura | Capacidad | J |
|---|---:|---|---:|---:|---:|
| Mayor J con pesos originales (candidato técnico principal) | 8 | `[0, 2, 6, 7, 10, 13, 15, 35]` | 95.67 % | 98.42 % | **1.840833** |
| Menor S encontrado que cumple | 3 | `[3, 4, 11]` | 85.00 % | 89.12 % | 1.703750 |
| Mayor capacidad satisfecha encontrada (empata con S=12) | 10 | `[0, 3, 6, 7, 10, 13, 15, 16, 34, 35]` | 96.38 % | 99.08 % | 1.829583 |
| Mayor cobertura encontrada | 12 | `[0, 3, 6, 7, 8, 11, 13, 15, 16, 23, 32, 34]` | 97.75 % | 99.08 % | 1.818333 |

El candidato **S = 8** resulta atractivo por su mayor J entre los diseños encontrados y por aparecer repetidamente en distintos experimentos. El diseño **S = 3** cumple formalmente, pero su cobertura queda exactamente en el límite de 85 % y tiene un SINR del percentil 5 considerablemente menor (aproximadamente **−14.17 dB**). El diseño de **10 sitios** empata en máxima capacidad satisfecha con el de 12 sitios, pero utiliza menos estaciones. La **decisión económica final** debe tomarse en el Sprint 5, con CAPEX, OPEX e indicadores de rentabilidad; no se concluye que el diseño técnicamente mejor sea el más rentable.

## 6. Visualizaciones (PB45)

### Función objetivo frente al número de sitios

![Función objetivo por algoritmo](../Results/pb45_1_J_vs_S_por_algoritmo.png)

El máximo de J encontrado se sitúa alrededor de ocho estaciones; incrementar S no implica necesariamente mejorar la función objetivo, pues también aumenta su penalización.

### Frente de Pareto y diseños candidatos

![Frente de Pareto y candidatos](../Results/pb45_2_pareto_candidatos.png)

Se observa el compromiso entre desplegar menos estaciones y alcanzar mayores porcentajes de cobertura y capacidad satisfecha.

### Sensibilidad a los pesos

![Sensibilidad a los pesos](../Results/pb45_3_sensibilidad_pesos.png)

La penalización por infraestructura influye en la cantidad de estaciones elegida como óptima dentro de los valores analizados.

### Sensibilidad del umbral de SINR

![Sensibilidad al umbral de SINR](../Results/pb45_4_sensibilidad_umbral_sinr.png)

Al endurecer el umbral de SINR, disminuye la fracción de hogares clasificados como cubiertos en los escenarios estudiados.

### Estabilidad y tiempos de ejecución

![Robustez y tiempos](../Results/pb45_5_robustez_y_tiempo.png)

Las repeticiones con diferentes semillas muestran poca dispersión de J para ILS y SA frente a la búsqueda local. Los tiempos son orientativos y no representan un presupuesto computacional idéntico entre algoritmos.

## 7. Validaciones y limitaciones

Se comprobó que las soluciones reportadas respetan el máximo de estaciones y que las métricas publicadas corresponden a la función de evaluación corregida del Sprint 2. Como verificación independiente del material entregado, se **recalcularon las métricas de 212 registros** de los CSV de PB39, PB40, PB41, PB42-B, PB43 y del consolidado de configuraciones; no se encontraron discrepancias en las métricas de cobertura, capacidad y J que se contrastaron. También se reprodujo el conteo de **16 configuraciones no dominadas entre las 35 encontradas**.

Los resultados dependen del dataset determinístico y de las semillas, parámetros e implementaciones ensayados. Ni SA ni ILS garantizan el óptimo global; las comparaciones con la búsqueda local original requieren la salvedad metodológica indicada. Los puntos de demanda se evalúan con el **modelo simplificado de capacidad individual** que el equipo ya había validado, sin una asignación explícita de recursos agregados por estación o por sector.

## 8. Conclusión y paso al Sprint 5

El Sprint 4 implementó SA y completó el análisis técnico de sensibilidad, estabilidad y selección de candidatos. **SA alcanzó el valor de J encontrado por ILS** cuando partió de la configuración de referencia, mientras las pruebas con semillas mostraron mayor estabilidad del ILS. Se identifica como **candidato técnico principal** la configuración de ocho estaciones **`[0, 2, 6, 7, 10, 13, 15, 35]`**, sin descartar los diseños de tres, diez y doce sitios para el análisis de compromisos técnico-económicos.

En el **Sprint 5** se transferirán los resultados técnicos seleccionados al **modelo financiero XLSX del profesor** y se evaluarán CAPEX, OPEX, VPN/NPV, ROI, payback y sensibilidad a supuestos de negocio. La elección definitiva dependerá de esa evaluación económica.
