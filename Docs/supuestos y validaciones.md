# Supuestos y Validaciones – Sprint 1

## Escenario base

| Parámetro                   |              Valor |
| --------------------------- | -----------------: |
| Área                        |      20 km × 10 km |
| Hogares                     |               2400 |
| Penetración inicial         |               30 % |
| Throughput objetivo         | 20 Mbps/suscriptor |
| Concurrencia BH             |               0.20 |
| Frecuencia                  |            3.5 GHz |
| Ancho de banda              |             40 MHz |
| EIRP                        |             46 dBm |
| Figura de ruido             |               7 dB |
| Ganancia Rx                 |               8 dB |
| Sitios candidatos           |                 36 |
| Máximo de sitios            |                 12 |
| Cobertura mínima requerida  |               0.85 |
| Capacidad satisfecha mínima |               0.80 |

El escenario emplea frequency reuse 1. Para cada punto de demanda, el sitio desplegado con mayor RSRP actúa como servidor y los demás sitios desplegados generan interferencia.

## Sanity checks

### SC-01 – Puntos de demanda

Resultado: `220`

**Estado: OK**

### SC-02 – Sitios candidatos

Resultado: `36`

**Estado: OK**

### SC-03 – Matriz RSRP

Resultado: `(220, 36)`

La dimensión es consistente con los 220 puntos de demanda y 36 sitios candidatos.

**Estado: OK**

### SC-04 – Hogares

La suma del dataset corresponde a:

`2400 hogares`

**Estado: OK**

### SC-05 – Ruido térmico

Para BW = 40 MHz y NF = 7 dB:

`Noise = -90.9794 dBm`

**Estado: OK**

## Hallazgos

### H-01 – Definición de cobertura

El archivo `scenario_params.json` contiene:

`coverage_min_sinr_db = -3 dB`

Sin embargo, el baseline calcula `pop_covered_frac` utilizando la condición:

`cap_bps > 0`

Por este motivo pueden obtenerse valores de cobertura de 1.0 incluso cuando algunos puntos presentan valores bajos de SINR.

**Decisión Sprint 1:** conservar la implementación original para garantizar la reproducción del baseline.

**Acción posterior:** revisar formalmente la definición de cobertura durante el desarrollo del modelo técnico.

### H-02 – Suscriptores iniciales

Según el escenario:

`2400 × 30 % = 720 suscriptores`

Sin embargo, la suma de `subscribers_initial` del dataset es:

`711 suscriptores`

La diferencia puede corresponder al redondeo realizado en los puntos de demanda.

**Decisión Sprint 1:** conservar los valores originales del dataset.

**Acción posterior:** mantener esta diferencia documentada para la integración técnico-económica.

### H-03 – Supuestos económicos

Los valores económicos presentes en `scenario_params.json` y los valores iniciales del modelo financiero XLSX no coinciden completamente.

**Decisión Sprint 1:** no modificar ninguno de los archivos.

**Acción posterior:** definir y justificar los supuestos utilizados al desarrollar el modelo económico.


## Estado

Se verificó satisfactoriamente:

* carga del dataset;
* dimensiones de las matrices;
* cantidad de hogares;
* cálculo de ruido térmico;
* ejecución completa del notebook;
* reproducción de las métricas iniciales;
* identificación de supuestos e inconsistencias pendientes de análisis.
