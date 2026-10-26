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
    df = pd.read_csv(ruta, na_values='-') ## Añadimos el argumento de la función de leer csv para que los valores '-' se conviertan en un valor NaN (sin valor), y por tanto los ignore. 
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y.%m.%d_%H.%M.%S") ## Además, es importante que la columna Timestamp esté en formato datetime64[us]. Esto lo hace la función pd.to_datetime.
    ## Estas funciones pueden tener dentro otras columnas o filas! El tipo de dato siempre es ese que he dicho, que es el tiempo en us desde un punto de referencia (enero de 1970) para así operar con fechas
    ## de forma muy sencilla... Lo del formato es para ayudar a pandas a que lo entienda directamente, ya que a veces cada app (como G-NetTrack) tiene su formato de fecha.

    ## Para "2019.12.14_10.16.30" sería "%Y.%m.%d_%H.%M.%S". Sabes?
    
    return df

  ### Ahora sí, los tipos de datos van a ser correctos en el df. Se verán con df.dtypes. Las fechas en foramto "datetime64[us]", los PING_AVG en formato "Float64", etc. Preparamos correctamente un dataset/dataframe!


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
