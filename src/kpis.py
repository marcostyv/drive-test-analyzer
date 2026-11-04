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

    ## Saco los valores de los umbrales definidos arriba. Los de valor "None", como es el caso de la clave "Mala", no los incluyo. (Ver UMBRALES_RSP)
    umbrales = [v for v in UMBRALES_RSRP.values() if v is not None] ## Esta expresión devuelve una lista al estar entre corchetes cuadrados.
                                                                    ## Lo que hace crear un umbrales = [], y hacer un umbrales.append() a cada valor del bucle (Con la condición del if)
    umbrales.sort(reverse=False) ## Para ponerla de MENOR A MAYOR.

    ## Añadimos a los intervalos el -inf y el +inf. Se pueden concatenar listas así! como suma de listas!
    umbrales = [-float("inf")] + umbrales + [float("inf")] ## Ahora tenemos [-inf, -100, -90, -80, inf]

    ## Cogemos los valores de labels. Pero hay que darles la vuelta para que coincidan con los rangos!
    orden_clases = ORDEN_CLASES[::-1] ## La lista desde el final, y coge todo "::"

    rangos_df = pd.cut(rsrp, bins=umbrales, labels = orden_clases, right=False)

    return rangos_df    


# ═════════════════════════════ SEMANA 2 ═════════════════════════════

def resumen_por_tramos(df: pd.DataFrame, columna: str, bins: list,
                       metrica: str = "DL_Mbps") -> pd.DataFrame:
    """EJERCICIO 7: resume `metrica` por tramos de `columna`.

    Ejemplo: resumen_por_tramos(df, "SNR", [-inf, 0, 5, 10, inf])
    agrupa las muestras en los tramos de SNR [-inf,0), [0,5), [5,10), [10,inf)
    y, para cada tramo, calcula sobre la columna `metrica`:
        'muestras' -> cuántos valores válidos (no nulos) hay
        'mediana'  -> la mediana

    Salida: un DataFrame con un tramo por fila (índice) y las columnas
            'muestras' y 'mediana'. Los tramos vacíos NO deben aparecer.

    Pistas: pd.cut (con right=False, igual que en clasificar_cobertura),
    groupby sobre el resultado de pd.cut (parámetro observed=True),
    .agg con nombres propios.
    """
    raise NotImplementedError


def detectar_handovers(df: pd.DataFrame) -> pd.DataFrame:
    """EJERCICIO 8: detecta los cambios de celda servidora (CellID).

    Un handover es una muestra cuyo CellID es distinto del de la muestra
    ANTERIOR del MISMO fichero (cada fichero es un recorrido distinto:
    la última muestra de un fichero y la primera del siguiente no tienen
    nada que ver).

    Salida: un DataFrame con UNA FILA POR HANDOVER y estas columnas:
        'fichero', 'Timestamp', 'Latitude', 'Longitude',
        'CellID_anterior', 'CellID',
        'NetworkMode_anterior', 'NetworkMode', 'RSRP'

    Pistas: ordenar por fichero y Timestamp (sort_values con una lista),
    groupby("fichero")["CellID"].shift() para obtener el valor anterior
    dentro de cada fichero, una máscara para quedarte con los cambios.
    Ojo con la primera muestra de cada fichero: su "anterior" es NaN.
    """
    raise NotImplementedError
