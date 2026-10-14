# Documentación de resultados y validación del Sprint 5

El propósito de este sprint es pasar de los resultados de optimización técnica obtenidos en el Sprint 4 a una evaluación económica del despliegue. Para ello se emplea el archivo `Capstone_FWA_Rural_Financial_Model_Base.xlsx` suministrado por el profesor, que permite relacionar el diseño seleccionado con los costos de inversión y operación, los ingresos y los indicadores de viabilidad financiera.

## 1. Selección del diseño e integración del modelo económico — Felipe

### Diseño técnico seleccionado

Se tomó como referencia el análisis comparativo del Sprint 4, en particular las configuraciones candidatas identificadas en la PB44. Para el escenario económico base se seleccionó la solución de **8 estaciones**, cuyos identificadores son:

`[0, 2, 6, 7, 10, 13, 15, 35]`

La configuración seleccionada obtuvo el mayor valor de la función objetivo con los pesos originales del proyecto (**J ≈ 1,8408**) y fue la que apareció con mayor frecuencia entre las configuraciones evaluadas en el Sprint 4 (**11 apariciones**). Aunque existen alternativas de tres estaciones que cumplen los requisitos mínimos, se prefirió la de ocho por su mayor margen técnico, especialmente en cobertura y satisfacción de demanda. Esta decisión no supone por sí misma que sea la alternativa más rentable; esa valoración corresponde al análisis financiero del sprint.

| Métrica técnica | Resultado del diseño | Requisito del escenario |
|---|---:|---:|
| Estaciones desplegadas | 8 | Máximo 12 |
| Cobertura poblacional (`pop_covered_frac`) | 95,67 % | Mínimo 85 % |
| Capacidad satisfecha (`capacity_satisfied_frac`) | 98,42 % | Mínimo 80 % |
| SINR promedio (`avg_sinr_db`) | 7,64 dB | Métrica de reporte |
| SINR percentil 5 (`p05_sinr_db`) | −5,96 dB | Métrica de reporte |
| Eficiencia espectral promedio (`avg_se_bphz`) | 2,77 bps/Hz | Métrica de reporte |

Estos valores provienen de la evaluación técnica del notebook y se trasladaron a las hojas `Inputs` y `Results` del modelo financiero, sin recalcular las métricas de radio en Excel.

### Consistencia de los suscriptores y la demanda

El escenario oficial establece **2.400 hogares** y una **penetración inicial del 30 %**, lo que produce **720 suscriptores teóricos**. No obstante, al sumar la columna `subscribers_initial` de los 220 puntos de `data/demand_points.csv`, se obtienen **711 suscriptores**. La diferencia de nueve usuarios proviene de aplicar y redondear la penetración en cada punto de demanda, en vez de hacerlo una sola vez sobre el total de hogares.

Para conservar los parámetros globales definidos por el profesor, en el modelo financiero se mantuvieron **30 % de penetración y 720 suscriptores iniciales**. El notebook técnico permanece con los 711 usuarios distribuidos espacialmente. Esta decisión implica una pequeña diferencia entre ambas representaciones, que debe tenerse presente al interpretar los resultados económicos; no se alteró el dataset para forzar su coincidencia.

Con los valores globales, la demanda agregada en hora pico que muestra el Excel es **2.880 Mbps** (`720 × 20 Mbps × 0,20`). Además, siguiendo la fórmula simplificada de la plantilla, los suscriptores efectivamente servidos se estiman como `720 × capacity_satisfied_frac`, obteniendo aproximadamente **708,6 suscriptores**. Esta cifra es una aproximación financiera y no un conteo exacto de los usuarios que cumplen simultáneamente todos los criterios técnicos.

### Configuración y validación de los costos

Se actualizaron las entradas económicas del Excel usando como referencia principal `data/scenario_params.json`. Los supuestos empleados son:

| Parámetro | Valor base | Procedencia |
|---|---:|---|
| ARPU mensual | USD 12 | `scenario_params.json` |
| Costo de instalación por suscriptor | USD 120 | `scenario_params.json` |
| CAPEX de radio por estación | USD 65.000 | `scenario_params.json` |
| CAPEX de backhaul por estación | USD 12.000 | `scenario_params.json` |
| CAPEX adicional por estación de 3 sectores | USD 18.000 | `scenario_params.json` |
| OPEX anual de radio por estación | USD 11.000 | `scenario_params.json` |
| OPEX anual de backhaul por estación | USD 3.500 | `scenario_params.json` |
| Tasa de descuento | 10 % | `scenario_params.json` |
| Horizonte de evaluación | 5 años | `scenario_params.json` |
| Crecimiento anual de suscriptores | 15 % | Supuesto precargado en el Excel del profesor; no está definido en el JSON |

Se conservó la fracción de estaciones con tres sectores igual a **1**, coherente con el campo `sectors_default = 3` de los 36 sitios candidatos del dataset.

La verificación de costos del diseño seleccionado quedó así:

| Componente | Cálculo | Resultado |
|---|---|---:|
| CAPEX de estaciones | `8 × (65.000 + 12.000 + 18.000)` | USD 760.000 |
| CAPEX de instalación | `708,6 × 120` | USD 85.032 |
| **CAPEX inicial total** | `760.000 + 85.032` | **USD 845.032** |
| **OPEX anual** | `8 × (11.000 + 3.500)` | **USD 116.000/año** |

Estos cálculos reproducen los importes mostrados por el Excel para el escenario de ocho estaciones. El CAPEX se considera una inversión del año 0 y el OPEX un gasto anual desde el año 1, de acuerdo con la estructura de la plantilla. En esta etapa se validaron los componentes de inversión y operación; la revisión de ingresos, flujos de caja e indicadores corresponde a la siguiente sección.

**Archivos de referencia:** notebook del Sprint 4 (`Capstone_FWA_Rural_Base.ipynb`), `data/demand_points.csv`, `data/candidate_sites.csv`, `data/scenario_params.json` y modelo financiero `.xlsx` diligenciado por el equipo.

## 2. Proyección financiera, rentabilidad y escenarios — Emanuel

> **Pendiente de completar por Emanuel con los resultados del Excel verificado.** Esta sección debe explicar de forma integrada cómo se estiman los suscriptores atendidos y los ingresos, cómo se construye el flujo de caja de los años 0 a 5 y qué muestran los indicadores VPN/NPV, ROI y payback. También debe presentar los escenarios pesimista, base y optimista, sus supuestos y una comparación breve de resultados. No es necesario desarrollar aquí cada tarea del backlog por separado.

**Verificación necesaria antes de cerrar la sección:** comprobar que `Economics!C10:G10` (flujo neto) y `Economics!C12:G12` (flujo descontado) tengan fórmulas que respondan a los cambios de parámetros; en la copia revisada contenían valores fijos. Evitar presentar indicadores como definitivos hasta completar esa comprobación.

## 3. Sensibilidad económica y conclusión técnico-económica — Jhon

> **Pendiente de completar por Jhon con los resultados integrados del equipo.** Esta sección debe reunir el efecto de las variaciones de ARPU, CAPEX y OPEX sobre la viabilidad, identificar y justificar cuál variable resulta más crítica para el proyecto y cerrar con una conclusión que conecte las ventajas técnicas de las ocho estaciones con su costo y rentabilidad. Deben mencionarse las limitaciones relevantes y las condiciones bajo las cuales el despliegue sería o no recomendable.

**Cierre del documento:** una vez completadas las tres secciones, revisar la consistencia de las cifras entre `Inputs`, `Economics`, `Results` y `Sensitivity`, y utilizar esta documentación como soporte de la tercera entrega y la exposición de los Sprints 4 y 5.
