"""
Carga de logs de drive test (formato G-NetTrack Pro).

Semana 1: aquí vas a escribir tú el código. Las funciones marcadas con
`raise NotImplementedError` son tus ejercicios (ver SEMANA1.md).
La app (app.py) detecta automáticamente cuándo las completas y
desbloquea las secciones correspondientes.
"""
from pathlib import Path

import pandas as pd


def cargar_csv(ruta: str | Path) -> pd.DataFrame:
    """Carga UN fichero CSV de drive test y devuelve un DataFrame.

    Versión inicial (ingenua): funciona, pero tiene problemas que vas a
    descubrir y corregir en los ejercicios 2 y 3 de SEMANA1.md:
      - ¿Qué pasa con las celdas que contienen "-"?
      - ¿De qué tipo es la columna Timestamp?
      - ¿Hay valores de RSRP físicamente imposibles?
    """
    df = pd.read_csv(ruta)
    return df


def cargar_todos(carpeta: str | Path) -> pd.DataFrame:
    """EJERCICIO 4: carga TODOS los CSV del dataset en un único DataFrame.

    Requisitos:
      - Buscar los .csv de forma recursiva dentro de `carpeta`.
      - Reutilizar cargar_csv() para cada fichero (no copies código).
      - Añadir tres columnas nuevas a partir de la ruta de cada fichero:
          'servicio'  -> Download / Netflix / Amazon_Prime
          'movilidad' -> Driving / Static
          'fichero'   -> nombre del fichero (ej. B_2020.02.14_09.38.22.csv)
      - Devolver un único DataFrame con todo concatenado.

    Pistas: pathlib.Path.rglob, ruta.parts, pd.concat
    """
    raise NotImplementedError
