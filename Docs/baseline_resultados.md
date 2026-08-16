# Resultados del Baseline – Sprint 1

El objetivo del sprint 1 es verificar la reproducibilidad del escenario base suministrado para el proyecto de planificación de una red 5G FWA rural.
El notebook base fue ejecutado utilizando los archivos originales del dataset y se comprobaron sus principales resultados.

## Verificación de insumos

| Elemento              | Resultado |
| --------------------- | --------: |
| Puntos de demanda     |       220 |
| Sitios candidatos     |        36 |
| Dimensión matriz RSRP |  220 × 36 |
| Hogares totales       |      2400 |

La matriz RSRP es coherente con el escenario, ya que contiene un valor para cada combinación entre los 220 puntos de demanda y los 36 sitios candidatos.

## Ruido térmico

Para un ancho de banda de 40 MHz y una figura de ruido de 7 dB se obtuvo:

**Noise = -90.9794 dBm**

## Plan de prueba

El notebook evalúa inicialmente los sitios:

`[0, 1, 2, 3, 4]`

Resultados:

| Métrica                   |     Resultado |
| ------------------------- | ------------: |
| Sitios desplegados        |             5 |
| `pop_covered_frac`        |        1.0000 |
| `capacity_satisfied_frac` |        0.7000 |
| `avg_sinr_db`             |    -0.9241 dB |
| `p05_sinr_db`             |   -24.1234 dB |
| `avg_se_bphz`             | 1.8886 bps/Hz |

## Selección greedy incluida en el baseline

Para `S = 8` se obtuvo:

`[3, 2, 0, 7, 4, 16, 6, 11]`

| Métrica                   |     Resultado |
| ------------------------- | ------------: |
| Sitios desplegados        |             8 |
| `pop_covered_frac`        |        1.0000 |
| `capacity_satisfied_frac` |        0.9583 |
| `avg_sinr_db`             |     6.5409 dB |
| `p05_sinr_db`             |   -10.5555 dB |
| `avg_se_bphz`             | 2.5770 bps/Hz |

## Búsqueda local incluida en el baseline

Con:

* `S = 8`
* `iters = 600`
* `seed = 1`

se obtuvo:

`[0, 3, 6, 7, 11, 12, 13, 16]`

| Métrica                   |     Resultado |
| ------------------------- | ------------: |
| Sitios desplegados        |             8 |
| `pop_covered_frac`        |        1.0000 |
| `capacity_satisfied_frac` |        0.9796 |
| `avg_sinr_db`             |     7.9073 dB |
| `p05_sinr_db`             |    -9.5859 dB |
| `avg_se_bphz`             | 2.8854 bps/Hz |
| Función objetivo `J`      |        1.8796 |

La ejecución de los algoritmos incluidos en el notebook se realizó en Sprint 1 únicamente para comprobar la reproducción completa del baseline. Su análisis y modificación corresponden a sprints posteriores.

## Conclusión

El notebook base fue ejecutado satisfactoriamente de principio a fin utilizando los insumos suministrados.

Se reprodujeron correctamente la carga del dataset, las dimensiones de las matrices, el cálculo del ruido y las métricas producidas por el escenario base.

Por lo tanto, se considera **reproducido satisfactoriamente el baseline del proyecto**.
