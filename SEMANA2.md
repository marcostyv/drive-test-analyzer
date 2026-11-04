# Semana 2 — Throughput, calidad radio y handovers

**Tiempo estimado:** 8–10 h, repartidas en 2 sesiones de **fundamentos** y 2–3 sesiones de **proyecto**.
**Objetivo:** al acabar la semana, la app tiene una pestaña nueva **📶 Análisis radio** con:
- throughput frente a SNR / RSRP / CQI, separable por tecnología;
- un mapa de **handovers** por recorrido;

y tú sabes explicar, con datos, **por qué** salen las curvas que salen.

**Reglas del juego (las mismas):**
- 🧠 = respondes **antes** de ejecutar, en `notas/semana2.md`, y luego compruebas.
- Las funciones con `raise NotImplementedError` las escribes tú. Puedes pedir pistas y correcciones, no la solución.
- Commit pequeño al acabar cada ejercicio.

---

## Preparación (≈15 min)

1. **Sustituye `app.py`** por la versión nueva que acompaña a esta guía. Incluye:
   - la pestaña **📶 Análisis radio**, con dos misiones nuevas 🔒;
   - la tarjeta **"DL mediano (descargando)"** en Mbps, sin el asterisco (unidad confirmada en el paper: kbps).
   Antes de sustituir, comprueba con `git status` que no tienes cambios en `app.py` sin guardar en un commit.
2. **Añade al final de `src/kpis.py`** el bloque de la semana 2 (está al final de esta guía, en el *Anexo*). **No borres** tu `clasificar_cobertura()`.
3. Arranca la app (`python -m streamlit run app.py`), limpia caché (`C`) y comprueba que en la barra lateral aparecen las **Misiones · Semana 2** con 🔒.
4. Commit: `git commit -m "Semana 2: app con pestaña de análisis radio y plantillas"`.

---

## Fundamentos A · *Automate the Boring Stuff*, capítulo 4: listas (≈1,5 h)

Lee el capítulo y escribe los ejemplos en `notebooks/00_fundamentos.ipynb`. Después, estos mini-retos **sin pandas**, solo Python:

a) Crea la lista `cqi = [7, 9, 15, 3, 9, 12, 0, 9]`. Calcula **a mano** (con un bucle) la media, el máximo y cuántas veces aparece el 9. Después compruébalo con `sum()`, `max()` y `.count()`.
b) Crea una **lista nueva** solo con los CQI ≥ 9: primero con un `for` + `append`, después con una *list comprehension*.
c) ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)`? Demuéstralo con un ejemplo.

## Fundamentos B · capítulos 5 y 6: diccionarios y textos (≈1,5 h)

a) **Contar a mano.** Con `modos = ["5G", "LTE", "5G", "HSPA+", "5G", "LTE"]`, construye con un bucle el diccionario `{"5G": 3, "LTE": 2, "HSPA+": 1}`. Usa `.get(clave, 0)`.
b) **Trocear textos.** Del nombre de fichero `"B_2019.11.23_13.28.26.csv"` saca, usando solo métodos de texto (`.split()`, `.replace()`, *slicing*):
   - la fecha `"2019-11-23"`;
   - la hora `"13:28:26"`;
   - el operador `"B"`.
c) 🧠 ¿Por qué en el proyecto es mejor usar `Path(...).name` y `pd.to_datetime(...)` que trocear textos a mano? ¿Cuándo sí tiene sentido hacerlo a mano?

---

## Sesión de proyecto 1 · Ejercicio 7: throughput frente a calidad radio (≈2,5 h)

### 7.1 Antes de nada: ¿qué muestras sirven para medir throughput?
En el notebook, con el dataset completo:
- Mira los valores de la columna `State` con `value_counts()`. El paper dice que `I` = *idle* (no descarga) y `D` = *downloading*. Aparecen también `V` y `VD`, que el paper no explica.
  🧠 **P1.** ¿Qué crees que significan `V` y `VD`? Plantéalo como **hipótesis** (no hay fuente que lo confirme) y explica qué mirarías en los datos para apoyarla.
- Calcula la **mediana de `DL_Mbps`** por `servicio` y `State` (`groupby` con dos columnas).
  🧠 **P2.** ¿Por qué tiene sentido analizar la relación throughput–calidad **solo** con muestras de `Download` en estado `D`? ¿Qué pasaría con las de Netflix, aunque estén en `D`?

### 7.2 Escribe `resumen_por_tramos()` (en `src/kpis.py`) 🔓
Sigue el *docstring*. Es una combinación de cosas que ya sabes (`pd.cut`, `groupby`, `.agg` con nombres). Lo nuevo:
- **`groupby` sobre el resultado de `pd.cut`**: puedes agrupar por una Serie que no es columna de `df`, siempre que tenga el mismo índice.
- **`observed=True`**: hace que los tramos sin ninguna muestra **no aparezcan** en el resultado.

**Prueba en el notebook** con este caso pequeño:
```python
inf = float("inf")
t = pd.DataFrame({"SNR": [-3, 2, 4, 12, 15], "DL_Mbps": [1, 5, 7, 20, None]})
kpis.resumen_por_tramos(t, "SNR", [-inf, 0, 10, 20, 30, inf])
```
Resultado esperado (fíjate en `muestras` del último tramo y en que los tramos vacíos no salen):
```
              muestras  mediana
SNR
[-inf, 0.0)          1      1.0
[0.0, 10.0)          2      6.0
[10.0, 20.0)         1     20.0
```
Al recargar la app (limpiando caché), la sección **Throughput frente a calidad radio** se desbloquea.

### 7.3 Aplica y compara con lo que esperabas
🧠 **P3.** **Antes de mirar la app**, dibuja en papel cómo esperas que sea la curva "DL mediano frente a SNR" y "DL mediano frente a CQI". ¿Siempre creciente? ¿Se satura? ¿Por qué? (Piensa en Shannon y en la tabla de CQI.)

Después, en la app (pestaña 📶) y en el notebook:
- `Download` + `D`: mediana de `DL_Mbps` **por cada valor de CQI** (aquí no hacen falta tramos: CQI ya es un número entero).
- Mediana por **tramos de SNR** con tu función.

🧠 **P4.** ¿Coincide con tu dibujo? Describe la forma real de la curva.

### 7.4 Investiga la sorpresa
Si la curva no es lo que esperabas, no te quedes en "los datos están mal": **busca la variable que lo explica**.
1. Separa LTE y 5G (casilla **Separar LTE y 5G** en la app, o `isin` + tu función en el notebook). ¿Cuál de las dos se comporta "como dice la teoría"?
2. Para la que no, repite el análisis separando por **`movilidad`** (Driving / Static). Mira también **cuántas muestras** de cada movilidad hay en cada tramo de SNR.

🧠 **P5.** Explica en 4–5 líneas qué está pasando. Palabras clave para buscar: *variable de confusión* (*confounding variable*) y *paradoja de Simpson*. Relaciónalo con lo que ya descubriste en la semana 1 sobre Driving frente a Static y sobre el sesgo de selección LTE/5G.

`git commit -m "resumen_por_tramos y análisis throughput vs calidad"`

---

## Sesión de proyecto 2 · Ejercicio 8: handovers (≈2,5 h)

### 8.1 Lo nuevo: `.shift()`
`shift()` desplaza una columna **una posición hacia abajo**: cada fila pasa a ver el valor de la fila **anterior**.
```python
s = pd.Series([10, 20, 30])
s.shift()          # → [NaN, 10, 20]
```
Así puedes comparar cada muestra con la anterior **sin bucles**:
```python
cambio = s != s.shift()
```
🧠 **P6.** Si aplicas `df["CellID"].shift()` sobre el dataset completo, ¿qué problema hay en la primera fila de cada fichero? ¿Cómo lo evita `df.groupby("fichero")["CellID"].shift()`?

### 8.2 Escribe `detectar_handovers()` (en `src/kpis.py`) 🔓
Sigue el *docstring*. Lo nuevo:
- `sort_values(["fichero", "Timestamp"])`: ordenar por varias columnas.
- `groupby(...)["col"].shift()`: el "valor anterior" **dentro de cada grupo**.

**Prueba en el notebook:**
```python
h = pd.DataFrame({
    "fichero":   ["a.csv"] * 5 + ["b.csv"] * 2,
    "Timestamp": pd.to_datetime([f"2020-01-01 10:00:0{i}" for i in range(5)]
                                + ["2020-01-01 09:00:00", "2020-01-01 09:00:01"]),
    "Latitude": 0.0, "Longitude": 0.0,
    "CellID":      [1, 1, 2, 2, 1, 5, 5],
    "NetworkMode": ["LTE", "LTE", "5G", "5G", "LTE", "LTE", "LTE"],
    "RSRP":        [-90, -91, -92, -93, -94, -80, -81],
})
kpis.detectar_handovers(h)
```
Deben salir **exactamente 2 handovers**, los dos del fichero `a.csv` (1→2 y 2→1). Si te sale un tercero entre `a.csv` y `b.csv`, revisa la P6.

Al recargar la app, la sección **Handovers** se desbloquea: métricas, mapa por recorrido y tabla de handovers por minuto.

### 8.3 Preguntas al dataset
🧠 **P7.** Antes de mirar: ¿cuántos handovers por minuto esperas en **Driving** y en **Static**? ¿Por qué?

Después, comprueba con la tabla **Handovers por recorrido** de la app (o en el notebook):
- Total de handovers y mediana de HO por minuto en Driving y en Static.
- ¿Qué recorrido tiene más? Míralo en el mapa: ¿dónde se concentran?

🧠 **P8.** La app separa los handovers **con cambio de tecnología** (LTE ↔ 5G). En 5G NSA, cuando el terminal "pasa de LTE a 5G", ¿cambia realmente de celda servidora, o se **añade** una pata NR manteniendo el ancla LTE? ¿Deberíamos contar esos eventos como handovers? Justifícalo con lo que sabes de EN-DC, y propón cómo lo reflejarías en el análisis.

### 8.4 Reto opcional: ping-pong
Un **ping-pong** es un handover A→B seguido de B→A en poco tiempo (por ejemplo, ≤ 10 s). Es síntoma de parámetros de handover mal ajustados (histéresis / *time-to-trigger*) o de una zona sin celda dominante.
- Escribe en el notebook (no hace falta en `src/`) un cálculo que cuente cuántos de los handovers detectados son ping-pong.
  Pista: sobre la tabla de handovers, vuelve a usar `groupby("fichero").shift(-1)` (el `-1` mira la fila **siguiente**) y la resta de dos `Timestamp`.
- 🧠 **P9.** ¿Qué porcentaje sale? ¿Cuántos de ellos son en realidad alternancias LTE ↔ 5G (ver P8)?

`git commit -m "detectar_handovers y análisis de handovers"`

---

## Cierre de semana (≈1 h)
- Respuestas en `notas/semana2.md`. Pásamelas para corregirlas.
- **README (en inglés):** añade una sección *"Findings"* con 3 hallazgos de verdad (por ejemplo: SINR vs throughput, Driving vs Static, handovers). Una captura de la pestaña 📶.
- `git push`.
- Pide que se actualice el documento de contexto del proyecto.

**Lo que habrás practicado:** listas, diccionarios y textos en Python puro; `pd.cut` + `groupby(observed=True)` + `.agg`; `groupby` con varias columnas; `sort_values` con varias columnas; `shift()` dentro de grupos; y, sobre todo, a **no fiarte de una curva** sin buscar las variables que la explican.

**Semana 3 (adelanto):** convertir el análisis en una **herramienta de terminal** (`python analyze.py datos/ --report informe.html`), umbrales en un fichero de configuración y primeros **tests** con `pytest`.

---

## Anexo · Bloque para añadir al final de `src/kpis.py`

```python
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
```
