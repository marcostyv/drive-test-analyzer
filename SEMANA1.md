# Semana 1 — Entorno, datos reales y primeras funciones

**Tiempo estimado:** 6–8 h, repartidas en 3–4 sesiones.
**Objetivo:** al acabar la semana tienes el proyecto en GitHub, la app web corriendo en tu PC con el dataset completo y el mapa coloreado por cobertura, y entiendes cada línea que has escrito.

**Reglas del juego:**
- Las preguntas marcadas con 🧠 se responden **antes** de ejecutar nada. Escribe la respuesta en `notas/semana1.md` y luego compruébala.
- Las funciones con `raise NotImplementedError` las escribes tú. Puedes preguntarme dudas o pasarme tu código para que lo corrija, pero no pidas la solución directa: si no la escribes tú, no la vas a poder defender en una entrevista.
- Commit pequeño al acabar cada ejercicio.

---

## Sesión 1 · Entorno (≈1,5 h)

### 0.1 Instalar herramientas (Windows 11)
En PowerShell:
```powershell
winget install Python.Python.3.12
winget install Git.Git
winget install Microsoft.VisualStudioCode
```
Cierra y abre la terminal. Comprueba: `py --version` y `git --version`.
En VS Code instala las extensiones **Python** y **Jupyter** (de Microsoft).

### 0.2 Crear el repositorio
1. Descomprime el proyecto en una carpeta, por ejemplo `C:\proyectos\drive-test-analyzer`.
2. Crea un repo vacío en GitHub llamado `drive-test-analyzer` (público, sin README).
3. En la carpeta:
```powershell
git init
git add .
git commit -m "Estructura inicial del proyecto"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/drive-test-analyzer.git
git push -u origin main
```

### 0.3 Entorno virtual
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Si PowerShell bloquea el script de activación:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repite.

🧠 **P1.** ¿Por qué un entorno virtual por proyecto y no instalar todo en el Python del sistema? ¿Por qué `.venv/` está en `.gitignore`?

### 0.4 Descargar el dataset
```powershell
git clone https://github.com/uccmisl/5gdataset.git ..\5gdataset
```
Descomprime `5G-production-dataset.zip` dentro de `data\raw\`. Debe quedar `data\raw\5G-production-dataset\Download\...`, etc. Borra la carpeta `__MACOSX` si aparece.

🧠 **P2.** El dataset tiene licencia GPL-3 y no lo subimos al repo (mira `.gitignore`). Aparte de la licencia, ¿qué otra razón hay para no versionar datos en git?

### 0.5 Arrancar la app
```powershell
streamlit run app.py
```
Se abre en `http://localhost:8501`. Ahora mismo funciona en **modo un solo fichero**, con dos misiones bloqueadas 🔒 en la barra lateral. Juega con ella: cambia de fichero, mira el mapa y las pestañas.

---

## Sesión 2 · Explorar un fichero (≈2 h)

Crea `notebooks/01_exploracion.ipynb` en VS Code y elige como kernel el `.venv`.

### Ejercicio 1 — Conocer los datos
Carga **un** fichero de `Download/Driving` con `pd.read_csv` y responde con código:
- ¿Cuántas filas y columnas tiene? (`shape`)
- ¿Qué tipo tiene cada columna? (`dtypes`)
- ¿Cada cuánto tiempo hay una muestra? Mira la columna `Timestamp`.

🧠 **P3.** Antes de mirar `dtypes`: ¿qué tipo esperas que tenga `PINGAVG`? Después compruébalo. Si no coincide, ¿por qué?

🧠 **P4.** Para cada una de estas columnas, explica en una frase qué mide y su rango físico razonable: `RSRP`, `RSRQ`, `SNR`, `CQI`, `RSSI`. Escríbelo de memoria, luego contrasta.

### Ejercicio 2 — Arreglar `cargar_csv()` (en `src/loader.py`)
La versión actual es ingenua. Mejórala para que:
- Las celdas con `-` se lean como valores nulos (no como texto).
- `Timestamp` sea de tipo fecha. El formato es `2020.02.14_09.38.22`.

Pistas: parámetro `na_values` de `read_csv`; `pd.to_datetime(..., format=...)`.
Comprobación: en la app, pestaña **🧾 Datos**, ya no debería haber KPIs como `object`.

### Ejercicio 3 — Valores imposibles
Ejecuta `df["RSRP"].describe()` sobre **todos** los ficheros (de momento, en el notebook, con un bucle rápido; el ejercicio 4 lo hará bien).

🧠 **P5.** El valor mínimo que vas a ver no es físicamente posible. ¿Cuál es el rango de RSRP que puede reportar un terminal LTE según 3GPP? ¿Qué crees que significa ese valor en realidad?

Añade a `cargar_csv()` la limpieza: los RSRP fuera del rango válido pasan a ser nulos. Haz lo mismo con `NRxRSRP`.
Pregunta extra: ¿es mejor **borrar** esas filas o poner el valor a nulo? Justifícalo.

`git commit -m "cargar_csv: nulos, timestamps y RSRP inválidos"`

---

## Sesión 3 · Todo el dataset y clasificación (≈2–3 h)

### Ejercicio 4 — `cargar_todos()` 🔓
Implementa la función siguiendo su docstring en `src/loader.py`.
Pruébala en el notebook: debes obtener unas **188.000 filas**.
Comprueba: `df.groupby(["servicio", "movilidad"]).size()`.

Al guardar y recargar la app (botón **Rerun** o tecla `R`), la misión 4 pasa a ✅ y aparecen los filtros por servicio, movilidad y tecnología.

### Ejercicio 5 — `clasificar_cobertura()` 🔓
Implementa la función en `src/kpis.py` con `pd.cut` y sin bucles.
Pruébala con casos límite:
```python
kpis.clasificar_cobertura(pd.Series([-79, -80, -81, -100, -101, None]))
```
🧠 **P6.** Antes de ejecutarlo, escribe qué clase esperas para cada valor. ¿En qué clase cae exactamente −80? ¿Y −100?

Al recargar la app: mapa coloreado por clases. 🎉

`git commit -m "cargar_todos y clasificar_cobertura"` y `git push`.

---

## Sesión 4 · Interpretar como ingeniero (≈1 h)

### Ejercicio 6 — Preguntas al dataset
Responde en `notas/semana1.md`, apoyándote en la app y el notebook:
1. ¿Qué porcentaje de muestras es de cada `NetworkMode`? ¿Qué % de cada clase de cobertura hay en Driving frente a Static?
2. Cuando `NetworkMode` es `5G`, existen tanto `RSRP` como `NRxRSRP`. 🧠 Antes de investigar: ¿qué crees que mide cada una? Pista: piensa en cómo se desplegó 5G comercial en 2019–2020 (NSA, EN-DC). Después busca qué dice el paper sobre esas columnas.
3. ¿En qué unidad está `DL_bitrate`? Búscalo en el paper (Raca et al., MMSys 2020) y corrige la etiqueta "kbps*" de la app si hace falta.
4. Encuentra un tramo en el mapa con RSRP bueno pero SNR malo. ¿Qué explicación radio tiene?

### Cierre de semana
- Escribe en `README.md` (en inglés) 4–5 líneas: qué es el proyecto y qué hace ya.
- Pásame tus respuestas de `notas/semana1.md` y te las corrijo.

---

**Lo que habrás practicado:** git y GitHub, entornos virtuales, pandas (lectura, tipos, nulos, fechas, concat, groupby, cut), limpieza de datos con criterio físico, y la interpretación de RSRP/RSRQ/SNR y NSA.

**Semana 2 (adelanto):** throughput frente a SNR/CQI, detección de handovers por cambio de celda y una nueva pestaña "Análisis radio" en la app.
