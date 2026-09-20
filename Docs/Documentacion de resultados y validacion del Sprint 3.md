# Sprint 3 — Resultados y validación del ILS

## Objetivo y metodología

Implementamos **Iterated Local Search (ILS)** como primera optimización propia del despliegue 5G FWA. A partir de una solución aleatoria reproducible, realizamos búsqueda local exhaustiva con intercambios **1-swap**; al llegar a un óptimo local, perturbamos la solución con **2-swap** y repetimos la búsqueda. Conservamos la mejor configuración encontrada. Evaluamos cada alternativa con `evaluate_plan_sprint2()`, sin modificar el modelo técnico validado.

Utilizamos la función objetivo **J = cobertura + capacidad satisfecha − 0.15 × (S/12)**. Ejecutamos ILS con **20 iteraciones y semilla 42** para cada valor de **S = 2 a 12**, respetando los umbrales de cobertura **≥ 85 %** y capacidad satisfecha **≥ 80 %**.

## Resultados principales

| Configuración | S | Cobertura | Capacidad satisfecha | J |
|---|---:|---:|---:|---:|
| Referencia del Sprint 2 | 8 | 95.83 % | 97.96 % | 1.837917 |
| ILS: menor S factible encontrado | 3 | 85.83 % | 88.83 % | 1.709167 |
| ILS: mayor J encontrado | 8 | 95.67 % | 98.42 % | 1.840833 |

Entre las **11 configuraciones evaluadas**, S=2 incumple ambos umbrales y S=3 a S=12 los cumplen. El máximo J encontrado corresponde a **S=8**; respecto a la referencia de ocho sitios, ILS cambia **−0.17 puntos porcentuales de cobertura**, **+0.46 puntos porcentuales de capacidad satisfecha** y **+0.002917 en J**. En el SINR p05 se observa además una mejora de **3.63 dB**, aunque el SINR medio desciende **0.27 dB**.

## Hallazgos y PB35 — Complejidad

Aumentar S tiende a mejorar cobertura y capacidad en las configuraciones obtenidas, pero sus ganancias adicionales se reducen y no siempre compensan la penalización de J. El SINR no varía de forma monótona, debido a la interferencia *reuse-1* y a que las configuraciones optimizadas para distintos S no siempre conservan los mismos sitios.

En cada pasada, la búsqueda local considera **S(36−S)** intercambios 1-swap; para S=8 son **224 vecinos**. ILS repite esta búsqueda después de las perturbaciones, por lo que exige más evaluaciones que una única búsqueda local. No garantiza el óptimo global.

## Validación y siguiente paso

Comprobamos límites de sitios, ausencia de duplicados y coherencia de J con las métricas calculadas. Para comparar ILS con la referencia usamos el **mismo evaluador corregido del Sprint 2**; las cifras reportadas son resultados de una heurística con semilla fija, no una garantía de que sean las mejores combinaciones posibles. En el Sprint 4 contrastaremos el ILS con recocido simulado y analizaremos la robustez de las soluciones.


### Cobertura y capacidad vs número de sitios

![Cobertura y capacidad](../Results/pb36_1_cobertura_capacidad_vs_S.png)

La cobertura poblacional y la fracción de demanda satisfecha tienden a mejorar al aumentar el número de sitios, aunque las ganancias adicionales se reducen progresivamente. Se encontraron configuraciones desde tres sitios que cumplen simultáneamente los umbrales del curso (85 % de cobertura y 80 % de capacidad). Sin embargo, cumplir los requisitos mínimos no implica necesariamente obtener la mejor función objetivo.

### Calidad de radio vs número de sitios

![SINR y eficiencia espectral](../Results/pb36_2_sinr_se_vs_S.png)

El SINR y la eficiencia espectral no mejoran necesariamente al aumentar la cantidad de sitios, debido a la interferencia generada bajo el modelo frequency reuse 1. Además, las configuraciones evaluadas fueron optimizadas independientemente, por lo que las diferencias también dependen de las ubicaciones seleccionadas y no solamente de la cantidad de estaciones desplegadas.

### Función objetivo vs número de sitios

![Función objetivo J](../Results/pb36_3_funcion_objetivo_J.png)

La función objetivo permite identificar el compromiso entre cobertura, capacidad y cantidad de sitios. En las configuraciones evaluadas, el mayor valor se obtuvo con ocho sitios. A partir de este punto, las mejoras técnicas adicionales no compensaron la penalización por infraestructura establecida en nuestra función objetivo. Esto evidencia que desplegar más estaciones no necesariamente produce una mejor solución según los criterios de optimización definidos.