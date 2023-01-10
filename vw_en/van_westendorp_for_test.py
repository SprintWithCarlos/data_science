import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use(
    "PDF"
)  # For automatic testing purposes is better to use a non-GUI backend
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import shapely
from shapely.geometry import LineString


def van_westendorp(data, currency="EUR"):
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
            raise Exception("Unsupported file type")
    else:
        raise Exception("File not found, check typos")

    df.columns = df.columns.str.strip().str.lower()
    columns = columns = ["too cheap", "cheap", "expensive", "too expensive"]

    if set(df.columns) != set(columns):
        raise Exception("Columns do not conform to requirements")

    df.columns = df.columns.str.strip().str.lower()
    df["CPer"] = (np.arange(1, df.index.stop + 1, 1) / df.index.stop).round(3)
    df["1 - CPer"] = 1 - df["CPer"]

    """
  IP = Indifference Point
  PMC = Point of Marginal cheapness
  PME = Point of Marginal Expensiveness
  OPP = Optimal Price Point
  """

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["too expensive"].sort_values(), df["CPer"])
    ax.plot(df["expensive"].sort_values(), df["CPer"])
    ax.plot(df["cheap"].sort_values(), df["1 - CPer"])
    ax.plot(df["too cheap"].sort_values(), df["1 - CPer"])
    ax.legend(["too expensive", "expensive", "cheap", "too cheap"], loc="best")
    ax.set_title(
        "Van Westerdorp's Price Sensitivity Meter", pad=10, size=18, fontweight="bold"
    )
    ax.set_xlabel(f"Price: {currency}")
    ax.set_ylabel("Number of respondents (cumulative %)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
    ax.grid(True)
    too_expensive = LineString(list(zip(df["too expensive"].sort_values(), df["CPer"])))
    expensive = LineString(list(zip(df["expensive"].sort_values(), df["CPer"])))
    cheap = LineString(list(zip(df["cheap"].sort_values(), df["1 - CPer"])))
    too_cheap = LineString(list(zip(df["too cheap"].sort_values(), df["1 - CPer"])))

    """
    - Intersection of "cheap" and expensive" is the Indifference Point(IP)
    - Intersection of "cheap" and "too expensive" is the Point of Marginal Expensiveness (PME) 
    - Intersection of "too cheap" and "expensive" is the Point of Marginal Cheapness (PMC)
    - Intersection of "too cheap" and "too expensive" is the Optimal Price Point (OPP)
  """

    intersection_1 = expensive.intersection(cheap)
    intersection_2 = too_expensive.intersection(cheap)
    intersection_3 = expensive.intersection(too_cheap)
    intersection_4 = too_expensive.intersection(too_cheap)
    intersection_points = [
        intersection_1,
        intersection_2,
        intersection_3,
        intersection_4,
    ]

    for i, intersection in enumerate(intersection_points):
        if type(intersection) != shapely.geometry.point.Point:
            intersection_points[i] = intersection.interpolate(0)

    indicators = ["ro", "go", "yo", "bo"]
    for point, indicator in zip(intersection_points, indicators):
        ax.plot(*point.xy, indicator)

    IP = round(intersection_points[0].x)
    PME = round(intersection_points[1].x)
    PMC = round(intersection_points[2].x)
    OPP = round(intersection_points[3].x)

    ax.annotate(
        "IP", xy=(intersection_points[0].x + 2.5, intersection_points[0].y - 0.02)
    )
    ax.annotate(
        "PME", xy=(intersection_points[1].x + 2.5, intersection_points[1].y - 0.02)
    )
    ax.annotate(
        "PMC", xy=(intersection_points[2].x + 2.5, intersection_points[2].y - 0.02)
    )
    ax.annotate(
        "OPP", xy=(intersection_points[3].x + 2.5, intersection_points[3].y - 0.02)
    )

    ax.text(
        5,
        -0.5,
        f"""  Indifference Point(IP)= {currency} {str(f'{IP:,}')}
  Point of Marginal Cheapness(PMC)= {currency} {str(f'{PMC:,}')}
  Point of Marginal Expensiveness(PME)= {currency} {str(f'{PME:,}')}
  Optimal Price Point(OPP)= {currency} {str(f'{OPP:,}')}""",
        fontsize=12,
    )

    # plt.show() In order to avoid this warning "UserWarning: Matplotlib is
    # currently using pdf, which is a non-GUI backend, so cannot show the figure."

    plt.savefig(
        os.path.join(current_dir, "plot.png"), bbox_inches="tight", transparent=False
    )
