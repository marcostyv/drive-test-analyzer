"""
Cálculo y clasificación de KPIs radio.
"""
import pandas as pd

# Umbrales de RSRP (dBm) habituales en drive test. No son un estándar 3GPP:
# cada operadora usa los suyos. Por eso viven aquí, en un solo sitio,
# y en la semana 3 los moveremos a un fichero de configuración.
UMBRALES_RSRP = {
    "Excelente": -80,   # RSRP >= -80
    "Buena": -90,       # -90 <= RSRP < -80
    "Regular": -100,    # -100 <= RSRP < -90
    "Mala": None,       # RSRP < -100
}

ORDEN_CLASES = ["Excelente", "Buena", "Regular", "Mala"]


def clasificar_cobertura(rsrp: pd.Series) -> pd.Series:
    """EJERCICIO 5: clasifica cada muestra de RSRP en una de ORDEN_CLASES.

    Entrada: una Serie de pandas con valores de RSRP en dBm (puede tener NaN).
    Salida: una Serie de la misma longitud con 'Excelente', 'Buena',
            'Regular' o 'Mala' (NaN se queda como NaN).

    Restricción: hazlo SIN bucles for. Pista: pd.cut (fíjate en el
    parámetro `right` para que los límites caigan en la clase correcta).
    """
    raise NotImplementedError
