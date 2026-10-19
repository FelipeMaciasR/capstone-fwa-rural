import openpyxl

PATH = r"C:\Users\Barrios\Desktop\capstone-fwa-rural-main (2)\capstone-fwa-rural-main\Docs\Capstone_FWA_Rural_Financial_Model_Base.xlsx"
wb = openpyxl.load_workbook(PATH, data_only=True)
inp, eco, res = wb["Inputs"], wb["Economics"], wb["Results"]

# ---- Parametros base tal como quedaron en el Excel de Felipe (hoja Inputs) ----
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
    cruzado los resultados del Excel y para poder evaluar escenarios sin
    tener que sobreescribir las celdas azules del Inputs original."""
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

    return {
        "subs": subs, "flujo_neto": flujo_neto, "flujo_desc": flujo_desc,
        "acumulado": acumulado, "npv": npv, "roi": roi, "payback": payback,
        "inversion_inicial": inversion_inicial, "opex_anual": opex_anual,
    }

# ============================================================
# PB54-PB58: VALIDACION CRUZADA DEL CASO BASE DEL EXCEL
# ============================================================
base = flujo_caja(arpu, crecim, capex_r, opex_r)

print("PB54-58 — validacion cruzada contra Economics/Results del Excel")
print("-" * 70)
excel_vals = {
    "Suscriptores servidos (año 5)": (eco["G5"].value, base["subs"][5]),
    "Ingresos año 1 (USD)":          (eco["C6"].value, base["subs"][1] * arpu * 12),
    "Flujo neto año 0 (USD)":        (eco["B10"].value, base["flujo_neto"][0]),
    "Flujo neto año 5 (USD)":        (eco["G10"].value, base["flujo_neto"][5]),
    "Flujo descontado año 5 (USD)":  (eco["G12"].value, base["flujo_desc"][5]),
    "NPV (USD)":                     (eco["B15"].value, base["npv"]),
    "ROI simple":                    (eco["B16"].value, base["roi"]),
}
ok = True
for nombre, (v_excel, v_py) in excel_vals.items():
    diff = abs(v_excel - v_py)
    coincide = diff < 0.01
    ok &= coincide
    print(f"  {nombre:35s} Excel={v_excel:14,.4f}  Python={v_py:14,.4f}  "
          f"{'OK' if coincide else 'DIFIERE'}")

payback_excel = res["B20"].value
payback_txt = f"año {base['payback']}" if base["payback"] is not None else "No hay Payback"
print(f"  {'Payback':35s} Excel={payback_excel!r:>14}  Python={payback_txt!r:>14}  "
      f"{'OK' if (payback_excel == payback_txt) else 'DIFIERE'}")
print(f"\n==> Formulas de Economics/Results {'validadas: coinciden con el calculo independiente.' if ok else 'NO coinciden, revisar celdas.'}")

# ============================================================
# PB59: ESCENARIOS PESIMISTA / BASE / OPTIMISTA
# ============================================================
ESCENARIOS = {
    "Pesimista": dict(arpu=9,  crecim=0.03, capex_radio=85000, opex_radio=16000),
    "Base":      dict(arpu=12, crecim=0.15, capex_radio=65000, opex_radio=11000),
    "Optimista": dict(arpu=15, crecim=0.15, capex_radio=50000, opex_radio=8000),
}

print("\nPB59 — escenarios economicos")
print("-" * 70)
print(f"{'Escenario':12s} {'ARPU':>6s} {'Crec.':>7s} {'CAPEX/sitio':>12s} "
      f"{'OPEX/sitio':>11s} {'NPV (USD)':>14s} {'ROI':>8s} {'Payback':>14s}")
for nombre, p in ESCENARIOS.items():
    r = flujo_caja(p["arpu"], p["crecim"], p["capex_radio"], p["opex_radio"])
    pb = f"año {r['payback']}" if r["payback"] is not None else "No hay Payback"
    print(f"{nombre:12s} {p['arpu']:6.0f} {p['crecim']:7.0%} {p['capex_radio']:12,.0f} "
          f"{p['opex_radio']:11,.0f} {r['npv']:14,.0f} {r['roi']:8.1%} {pb:>14s}")

    