# Documentación de resultados y validación del Sprint 2

### 1. Configuración evaluada

El modelo técnico del Sprint 2 se evaluó utilizando la solución obtenida mediante la búsqueda local del escenario base.

- **Sitios desplegados:** `[0, 3, 6, 7, 11, 12, 13, 16]`
- **Número de sitios:** 8
- **Sitios candidatos disponibles:** 36
- **Esquema de interferencia:** frequency reuse-1
- **Ancho de banda:** 40 MHz
- **Umbral mínimo de cobertura:** SINR ≥ -3 dB

Para cada punto de demanda se selecciona como servidor el sitio desplegado con mayor RSRP. Los demás sitios desplegados se consideran interferentes.

### 2. Métricas finales del Sprint 2

Las métricas obtenidas con el modelo técnico validado son:

- **Sitios desplegados (`sites_deployed`):** 8
- **Cobertura poblacional (`pop_covered_frac`):** 0.9583 — **95.83 %**
- **Fracción de capacidad satisfecha (`capacity_satisfied_frac`):** 0.9796 — **97.96 %**
- **SINR promedio (`avg_sinr_db`):** **7.91 dB**
- **Percentil 5 del SINR (`p05_sinr_db`):** **-9.59 dB**
- **Eficiencia espectral promedio (`avg_se_bphz`):** **2.89 bps/Hz**

La solución cumple los objetivos técnicos mínimos del escenario de cobertura poblacional y satisfacción de capacidad.

### 3. Validación frente al baseline

Durante el Sprint 2 se revisó de manera separada la cadena completa del modelo técnico:

**RSRP → asociación → interferencia → ruido → SINR → eficiencia espectral → capacidad → demanda Busy Hour → cobertura y satisfacción**

Los cálculos de asociación por mejor RSRP, interferencia reuse-1, ruido térmico, SINR, eficiencia espectral, capacidad y satisfacción de demanda fueron consistentes con la implementación original del baseline.

La principal diferencia identificada corresponde al cálculo de cobertura poblacional.

El baseline considera cubierto un punto cuando:

`cap_bps > 0`

Este criterio produce una cobertura poblacional de **100 %**.

Sin embargo, `scenario_params.json` define explícitamente un umbral mínimo de cobertura de:

`SINR >= -3 dB`

Al utilizar este criterio, **198 de los 220 puntos de demanda cumplen el umbral**, representando **2300 de los 2400 hogares** del escenario.

Por lo tanto, la cobertura poblacional corregida es:

**2300 / 2400 = 0.9583 = 95.83 %**

La diferencia respecto al baseline es de **4.17 puntos porcentuales**.

### 4. Validaciones realizadas

Durante el Sprint 2 se realizaron pruebas y sanity checks sobre todas las etapas principales del modelo.

Se verificó que:

- Cada punto de demanda tenga exactamente un sitio servidor.
- El sitio servidor corresponda al mayor RSRP entre los sitios desplegados.
- La interferencia reuse-1 sea no negativa y no incluya la potencia del sitio servidor.
- El cálculo de ruido térmico y la conversión entre dBm y watts sean consistentes.
- Los valores de SINR sean positivos en escala lineal y finitos en dB.
- La eficiencia espectral se encuentre entre 0 y 6 bps/Hz.
- La capacidad y la demanda Busy Hour sean no negativas.
- Las máscaras de cobertura y satisfacción sean booleanas.
- Las métricas poblacionales se encuentren entre 0 y 1.
- El número de sitios desplegados respete el máximo permitido por el escenario.
- Las métricas obtenidas coincidan con el baseline en aquellos cálculos cuya metodología no fue modificada.

También se realizó la trazabilidad manual de puntos individuales desde el RSRP servidor hasta la capacidad y satisfacción de demanda.

### 5. Interpretación técnica

La red obtiene un SINR promedio de aproximadamente **7.91 dB**, aunque el percentil 5 de **-9.59 dB** evidencia que existe un grupo reducido de puntos con condiciones de radio considerablemente inferiores al promedio.

El comportamiento es consistente con un esquema frequency reuse-1: todos los sitios desplegados reutilizan el mismo recurso de frecuencia, por lo que una mayor presencia de estaciones puede aumentar la potencia útil recibida, pero también incrementar la interferencia.

La cobertura poblacional de **95.83 %** indica que la mayoría de los hogares supera el umbral mínimo de SINR, aunque existen 22 puntos de demanda que no lo cumplen.

Por otra parte, la fracción de capacidad satisfecha de **97.96 %** indica que la capacidad disponible permite atender la demanda Busy Hour de la gran mayoría de los hogares.

Los resultados muestran que cobertura y capacidad representan criterios relacionados pero diferentes: un punto puede presentar señal útil, pero su desempeño final depende también de la interferencia, el ruido y la demanda que debe atender.

### 6. Conclusión del Sprint 2

El Sprint 2 permitió revisar, descomponer y validar el modelo técnico completo de la red 5G FWA.

Se confirmó la correcta implementación de la asociación por mejor RSRP, interferencia reuse-1, ruido térmico, SINR, eficiencia espectral, capacidad y demanda Busy Hour. Además, se corrigió formalmente el criterio de cobertura utilizando el umbral de SINR definido en los parámetros del escenario.

Finalmente, el modelo validado fue encapsulado en `evaluate_plan_sprint2()`, permitiendo evaluar cualquier conjunto de sitios mediante una única función y utilizando criterios técnicos consistentes.

Con esto, el modelo queda preparado para el **Sprint 3**, en el cual se utilizará como función de evaluación para desarrollar y comparar estrategias de optimización de selección de sitios.