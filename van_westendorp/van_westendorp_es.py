import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import shapely
from shapely.geometry import LineString


def van_westendorp(data, moneda="EUR"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(current_dir, data)
    if os.path.exists(file):
        if data.endswith("json"):
            df = pd.read_json(file)
        elif data.endswith("csv"):
            df = pd.read_csv(file)
        elif data.endswith("xlsx") or data.endswith("xls"):
            df = pd.read_excel(file)
        else:
            raise Exception("Tipo de archivo no admitido")
    else:
        raise Exception("Archivo no encontrado, revisa errores en el nombre")

    df.columns = df.columns.str.strip().str.lower()
    columns = columns = ["demasiado barato", "barato", "caro", "demasiado caro"]

    if set(df.columns) != set(columns):
        raise Exception(
            "Las columnas no cumplen con los requerimientos. Verifica los nombres"
        )

    df.columns = df.columns.str.strip().str.lower()
    df["FRA"] = (np.arange(1, df.index.stop + 1, 1) / df.index.stop).round(3)
    df["1 - FRA"] = 1 - df["FRA"]

    """
  PI= Punto de Indiferencia
  PMCB = Punto Marginal de Costo Bajo
  PMCA = Punto Marginal de Costo Alto
  PPO = Punto de Precio Óptimo
  """

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["demasiado caro"].sort_values(), df["FRA"])
    ax.plot(df["caro"].sort_values(), df["FRA"])
    ax.plot(df["barato"].sort_values(), df["1 - FRA"])
    ax.plot(df["demasiado barato"].sort_values(), df["1 - FRA"])
    ax.legend(["demasiado caro", "caro", "barato", "demasiado barato"], loc="best")
    ax.set_title(
        """Medición de Sensibilidad de \n Precio de Van Westendorp""",
        pad=10,
        size=18,
        fontweight="bold",
        loc="center",
    )
    ax.set_xlabel(f"Precio: {moneda}")
    ax.set_ylabel("Número de respuestas (porcentaje acumulado)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
    ax.grid(True)
    demasiado_caro = LineString(
        list(zip(df["demasiado caro"].sort_values(), df["FRA"]))
    )
    caro = LineString(list(zip(df["caro"].sort_values(), df["FRA"])))
    barato = LineString(list(zip(df["barato"].sort_values(), df["1 - FRA"])))
    demasiado_barato = LineString(
        list(zip(df["demasiado barato"].sort_values(), df["1 - FRA"]))
    )

    """
    - Intersección de "barato" y "caro" es el Punto de Indiferencia (PI)
    - Intersección de "barato" y "demasiado caro" es el Punto Marginal de Coste Alto (PMCA)
    - Intersección de "demasiado barato" y "caro" es el Punto Marginal de Coste Bajo (PMCB)
    - Intersección de "demasiado barato" y "demasiado caro" es el Punto de Precio Óptimo
  """

    interseccion_1 = caro.intersection(barato)
    interseccion_2 = demasiado_caro.intersection(barato)
    interseccion_3 = caro.intersection(demasiado_barato)
    interseccion_4 = demasiado_caro.intersection(demasiado_barato)
    puntos_interseccion = [
        interseccion_1,
        interseccion_2,
        interseccion_3,
        interseccion_4,
    ]

    for i, interseccion in enumerate(puntos_interseccion):
        if type(interseccion) != shapely.geometry.point.Point:
            puntos_interseccion[i] = interseccion.interpolate(0)

    indicadores = ["ro", "go", "yo", "bo"]
    for punto, indicador in zip(puntos_interseccion, indicadores):
        ax.plot(*punto.xy, indicador)

    PI = round(puntos_interseccion[0].x)
    PMCA = round(puntos_interseccion[1].x)
    PMCB = round(puntos_interseccion[2].x)
    PPO = round(puntos_interseccion[3].x)

    ax.annotate(
        "PI", xy=(puntos_interseccion[0].x + 2.5, puntos_interseccion[0].y - 0.02)
    )
    ax.annotate(
        "PMCA", xy=(puntos_interseccion[1].x + 2.5, puntos_interseccion[1].y - 0.02)
    )
    ax.annotate(
        "PMCB", xy=(puntos_interseccion[2].x + 2.5, puntos_interseccion[2].y - 0.02)
    )
    ax.annotate(
        "PPO", xy=(puntos_interseccion[3].x + 2.5, puntos_interseccion[3].y - 0.02)
    )
    ax.text(
        5,
        -0.5,
        f"""  Punto de Indiferencia(IP)= {moneda} {str(f'{PI:,}')}
  Punto Marginal de Coste Bajo(PMCB)= {moneda} {str(f'{PMCB:,}')}
  Punto Marginal de Coste Alto(PMCA)= {moneda} {str(f'{PMCA:,}')}
  Punto de Precio Óptimo(PPO)= {moneda} {str(f'{PPO:,}')}""",
        fontsize=12,
    )

    plt.show()

    fig.savefig(
        os.path.join(current_dir, "grafico.png"), bbox_inches="tight", transparent=False
    )
