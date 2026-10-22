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

Se verificó que las fórmulas de `Economics!C10:G10` (flujo neto) y `Economics!C12:G12` (flujo descontado) responden a cambios de parámetros en `Inputs` — no contienen valores fijos en esta copia del archivo. Se validaron cruzado con un cálculo independiente en Python, reproduciendo exactamente los valores de `Economics`/`Results` (suscriptores servidos, ingresos, flujo neto, flujo descontado, NPV, ROI y payback).

**Ingresos y suscriptores atendidos (PB54).** Los suscriptores servidos parten de 708,6 (`Inputs!B22`) y crecen 15% anual según `Economics!B5:G5`, alcanzando 1.425 al año 5. Los ingresos (`Economics!B6:G6`) se calculan como suscriptores × ARPU (12 USD/mes) × 12.

**Flujo de caja a 5 años (PB55).** El CAPEX (845.032 USD) se concentra en el año 0 y el OPEX (116.000 USD/año) desde el año 1. El flujo neto es negativo en el año 0 y positivo pero pequeño del año 1 al 5; descontado al 10%, el flujo acumulado nunca vuelve a ser positivo.

**Indicadores (PB56-PB58).**

| Indicador | Resultado | Interpretación |
|---|---:|---|
| NPV | −598.598 USD | Negativo: a 10% de descuento, el proyecto no recupera la inversión en 5 años. |
| ROI simple | 25,0% | Positivo pero no descuenta el valor del dinero en el tiempo; por eso difiere del NPV. |
| Payback | No hay Payback | El flujo acumulado no cruza cero dentro del horizonte evaluado. |

**Escenarios pesimista/base/optimista (PB59).** Usando los rangos Bajo/Alto ya definidos por el profesor en `Sensitivity` (ARPU, CAPEX y OPEX por sitio variando juntos):

| Escenario | ARPU | Crec. | CAPEX/sitio | OPEX/sitio | NPV (USD) | ROI | Payback |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pesimista | 9 | 3% | 85.000 | 16.000 | −1.204.362 | −36,0% | No hay Payback |
| Base | 12 | 15% | 65.000 | 11.000 | −598.598 | 25,0% | No hay Payback |
| Optimista | 15 | 15% | 50.000 | 8.000 | −216.078 | 73,0% | No hay Payback |

En los tres escenarios el NPV es negativo y no hay payback dentro de los 5 años, incluso en el optimista. Esto indica que la rentabilidad del diseño de 8 sitios depende más de supuestos estructurales (horizonte de evaluación, tasa de descuento, ARPU/penetración) que de variaciones típicas de CAPEX/OPEX — punto de partida para la sensibilidad que desarrolla Jhon en PB60-PB63.

### Script de validación utilizado

Para la validación cruzada de PB54-PB58 y el cálculo de los escenarios de PB59 se usó el siguiente script en Python (`openpyxl`), que replica las fórmulas de la hoja `Economics` sin modificar el archivo original:

​```python
import openpyxl

PATH = "Capstone_FWA_Rural_Financial_Model_Base.xlsx"
wb = openpyxl.load_workbook(PATH, data_only=True)
inp, eco, res = wb["Inputs"], wb["Economics"], wb["Results"]

# Parametros base tal como quedaron en el Excel de Felipe (hoja Inputs)
subs_ini   = inp["B11"].value   # 720
arpu       = inp["B25"].value   # 12
crecim     = inp["B26"].value   # 0.15
inst_cost  = inp["B27"].value   # 120
capex_r    = inp["B28"].value   # 65000
capex_bh   = inp["B29"].value   # 12000
capex_sec  = inp["B30"].value   # 18000
opex_r     = inp["B32"].value   # 11000
opex_bh    = inp["B33"].value   # 3500
tasa       = inp["B34"].value   # 0.10
horizonte  = inp["B35"].value   # 5
S          = inp["B19"].value   # 8
frac_cap   = inp["B21"].value   # capacity_satisfied_frac

def flujo_caja(arpu, crecim, capex_radio, opex_radio, S=S, subs_ini=subs_ini,
               frac_cap=frac_cap, inst_cost=inst_cost, capex_bh=capex_bh,
               capex_sec=capex_sec, opex_bh=opex_bh, tasa=tasa, horizonte=horizonte):
    """Replica exacta de las formulas de la hoja Economics, para validar
    cruzado los resultados del Excel y para evaluar escenarios sin
    sobreescribir las celdas azules del Inputs original."""
    subs_servidos_ini = subs_ini * frac_cap
    subs = [subs_servidos_ini]
    for _ in range(horizonte):
        subs.append(subs[-1] * (1 + crecim))

    capex_sitios = S * (capex_radio + capex_bh + capex_sec)
    capex_instalacion = subs[0] * inst_cost
    opex_anual = S * (opex_radio + opex_bh)

    flujo_neto, flujo_desc, acumulado = [], [], []
    for t in range(horizonte + 1):
        ingresos = subs[t] * arpu * 12
        capex_t = capex_sitios if t == 0 else 0
        capex_inst_t = capex_instalacion if t == 0 else 0
        opex_t = 0 if t == 0 else opex_anual
        neto = ingresos - capex_t - capex_inst_t - opex_t
        desc = neto / (1 + tasa) ** t
        flujo_neto.append(neto)
        flujo_desc.append(desc)
        acumulado.append((acumulado[-1] if acumulado else 0) + neto)

    npv = sum(flujo_desc)
    inversion_inicial = capex_sitios + capex_instalacion
    roi = sum(flujo_neto[1:]) / inversion_inicial if inversion_inicial else 0
    payback = next((t for t, a in enumerate(acumulado) if a >= 0), None)

    return {"subs": subs, "flujo_neto": flujo_neto, "flujo_desc": flujo_desc,
            "acumulado": acumulado, "npv": npv, "roi": roi, "payback": payback,
            "inversion_inicial": inversion_inicial, "opex_anual": opex_anual}

# Validacion cruzada del caso base (PB54-PB58)
base = flujo_caja(arpu, crecim, capex_r, opex_r)

# Escenarios pesimista/base/optimista (PB59), usando los rangos Bajo/Alto
# ya definidos por el profesor en la hoja Sensitivity
ESCENARIOS = {
    "Pesimista": dict(arpu=9,  crecim=0.03, capex_radio=85000, opex_radio=16000),
    "Base":      dict(arpu=12, crecim=0.15, capex_radio=65000, opex_radio=11000),
    "Optimista": dict(arpu=15, crecim=0.15, capex_radio=50000, opex_radio=8000),
}
resultados = {nombre: flujo_caja(**p) for nombre, p in ESCENARIOS.items()}
​```

El script compara cada resultado calculado en Python contra la celda equivalente de `Economics`/`Results` (diferencia < 0,01 USD en los 8 valores verificados), confirmando que las fórmulas del archivo no están rotas ni contienen valores fijos.

## 3. Sensibilidad económica y conclusión técnico-económica — Jhon

**Efecto de ARPU, CAPEX y OPEX (PB60–PB62).** Partiendo del escenario base (VPN = −598.598 USD), se varió una variable a la vez en `Inputs`, manteniendo las demás constantes y usando los rangos sugeridos en la hoja `Sensitivity`. Con ARPU entre 9 y 15 USD/mes el VPN va de −770.140 a −427.057 USD; con CAPEX de radio por sitio entre 50.000 y 85.000 USD va de −478.598 a −758.598 USD; y con OPEX de radio por sitio entre 8.000 y 16.000 USD/año va de −507.620 a −750.230 USD. En ningún punto de los rangos sugeridos el VPN es positivo ni se recupera la inversión en 5 años.

**Variable más crítica (PB63).** Con una variación de ±20 % sobre el valor base de cada variable, el ARPU produce el mayor cambio en el VPN (rango de 274.466 USD), seguido por el CAPEX de radio (208.000 USD), el OPEX de radio (133.436 USD) y el crecimiento de suscriptores (94.202 USD). El ARPU es la variable más crítica: el VPN llega a 0 con un ARPU ≈ 22,47 USD/mes, es decir, 87 % por encima del valor base. En cambio, ni llevando el CAPEX o el OPEX de radio a cero se alcanza VPN = 0, lo que muestra que el problema principal es de ingresos y no solo de costos. Esto es coherente con un despliegue FWA rural, donde hay pocos usuarios por sitio y una capacidad de pago limitada frente a una infraestructura con costo fijo por estación.

**Conclusión técnico-económica (PB64).** Técnicamente, el diseño de ocho estaciones es sólido: alcanza una cobertura poblacional del 95,7 % y una capacidad satisfecha del 98,4 %, por encima de los umbrales exigidos (85 % y 80 %), con un SINR promedio de 7,64 dB. Sin embargo, económicamente no es viable en condiciones comerciales: VPN = −598.598 USD, ROI simple = 25,0 % y sin payback en el horizonte de 5 años. El CAPEX inicial (845.032 USD) es muy alto frente a ingresos anuales que solo superan levemente el OPEX (116.000 USD/año).

**Limitaciones.** El modelo es simplificado: no incluye impuestos, depreciación ni valor residual de la infraestructura, cuya vida útil supera el horizonte de 5 años analizado; asume que todos los sitios tienen tres sectores; y la sensibilidad se hizo variando una variable a la vez, sin combinar cambios simultáneos.

**Recomendación.** El despliegue no es recomendable como inversión puramente privada con los supuestos actuales. Sería recomendable si se cuenta con cofinanciación o subsidio cercano a 598.598 USD en valor presente (por ejemplo, programas estatales de conectividad rural), o con una combinación de mayor ARPU, mayor adopción de suscriptores y menor CAPEX por sitio.


