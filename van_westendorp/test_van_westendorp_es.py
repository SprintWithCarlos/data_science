import os
import pytest
from van_westendorp_para_test import van_westendorp

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, "grafico.png")


@pytest.fixture
def check_file():
    if os.path.exists(filename):
        os.remove(filename)


def test_van_westendorp_function_creates_plot_with_json_input():
    van_westendorp("vwsurvey_es.json")
    assert os.path.exists(filename)


def test_van_westendorp_function_creates_plot_with_csv_input():
    van_westendorp("vwsurvey_es.csv")
    assert os.path.exists(filename)


def test_van_westendorp_function_creates_plot_with_xls_input():
    van_westendorp("vwsurvey_es.xls")
    assert os.path.exists(filename)


def test_van_westendorp_function_creates_plot_with_xlsx_input():
    van_westendorp("vwsurvey_es.xlsx")
    assert os.path.exists(filename)


def test_van_westendorp_raises_exception_on_unexistent_file():
    with pytest.raises(Exception) as excinfo:
        van_westendorp("vwsurvey.png")
    assert excinfo.match(
        "Archivo no encontrado, revisa errores en el nombre"
    ), f"Unexpected exception message: {excinfo.value}"


def test_van_westendorp_raises_exception_on_invalid_file_type():
    with pytest.raises(Exception) as excinfo:
        van_westendorp("output.png")

    assert excinfo.match(
        "Tipo de archivo no admitido"
    ), f"Unexpected exception message: {excinfo.value}"


def test_van_westendorp_raises_exception_on_features_names():
    with pytest.raises(Exception) as excinfo:
        van_westendorp("vwsurveybad.csv")

    assert excinfo.match(
        "Las columnas no cumplen con los requerimientos. Verifica los nombres"
    ), f"Unexpected exception message: {excinfo.value}"
