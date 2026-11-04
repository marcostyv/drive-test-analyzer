"""
Drive Test Analyzer — interfaz web local.

Arranque:  streamlit run app.py
Se abre en el navegador (http://localhost:8501).

Esta app es el "escaparate" del proyecto. La lógica de análisis vive en
src/ y la escribes tú; la app va desbloqueando secciones a medida que
completas los ejercicios de cada semana.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src import kpis, loader

# ── Configuración ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Drive Test Analyzer", page_icon="📡", layout="wide")

CARPETA_POR_DEFECTO = "data/raw/5G-production-dataset"
KPIS_NUMERICOS = ["RSRP", "RSRQ", "SNR", "CQI", "DL_bitrate", "UL_bitrate", "NRxRSRP", "NRxRSRQ"]

# Colores de estado para las clases de cobertura (de mejor a peor).
# Siempre van acompañados de etiqueta en la leyenda: el color nunca es la única pista.
COLORES_COBERTURA = {
    "Excelente": "#0ca30c",
    "Buena": "#fab219",
    "Regular": "#ec835a",
    "Mala": "#d03b3b",
}


# ── Comprobación de ejercicios ("misiones") ──────────────────────────────────
def mision_completada(funcion, *args) -> bool:
    try:
        funcion(*args)
        return True
    except NotImplementedError:
        return False
    except Exception:
        # Implementada pero con algún error: cuenta como empezada,
        # el error real se mostrará al usarla.
        return True


def numerico(df: pd.DataFrame) -> pd.DataFrame:
    """Copia con los KPI convertidos a número SOLO para dibujar.
    No arregla tus datos: eso es trabajo de cargar_csv() (ejercicio 2)."""
    out = df.copy()
    for col in KPIS_NUMERICOS + ["Latitude", "Longitude"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


@st.cache_data(show_spinner="Cargando dataset…")
def cargar_todo_cacheado(carpeta: str) -> pd.DataFrame:
    return loader.cargar_todos(carpeta)


@st.cache_data(show_spinner="Cargando fichero…")
def cargar_uno_cacheado(ruta: str) -> pd.DataFrame:
    return loader.cargar_csv(ruta)


# ── Barra lateral ────────────────────────────────────────────────────────────
st.sidebar.title("📡 Drive Test Analyzer")
carpeta = st.sidebar.text_input("Carpeta del dataset", CARPETA_POR_DEFECTO)

if not Path(carpeta).exists():
    st.title("📡 Drive Test Analyzer")
    st.error(
        f"No encuentro la carpeta `{carpeta}`. "
        "Descomprime el dataset en `data/raw/` (paso 0.4 de SEMANA1.md)."
    )
    st.stop()

m4 = mision_completada(loader.cargar_todos, carpeta)
m5 = mision_completada(kpis.clasificar_cobertura, pd.Series([-75, -95, -110]))

# Datos mínimos para comprobar si las funciones de la semana 2 ya existen
_prueba = pd.DataFrame({
    "fichero": ["a.csv"] * 3,
    "Timestamp": pd.to_datetime(["2020-01-01 10:00:00", "2020-01-01 10:00:01", "2020-01-01 10:00:02"]),
    "Latitude": [51.9, 51.9, 51.9], "Longitude": [-8.4, -8.4, -8.4],
    "CellID": [1, 1, 2], "NetworkMode": ["LTE", "LTE", "5G"],
    "RSRP": [-90.0, -95.0, -100.0], "SNR": [5.0, 10.0, 15.0], "DL_Mbps": [1.0, 2.0, 3.0],
})
m7 = hasattr(kpis, "resumen_por_tramos") and mision_completada(
    kpis.resumen_por_tramos, _prueba, "SNR", [-float("inf"), 10, float("inf")])
m8 = hasattr(kpis, "detectar_handovers") and mision_completada(kpis.detectar_handovers, _prueba)

st.sidebar.markdown("### 🎯 Misiones · Semana 1")
st.sidebar.markdown(
    f"{'✅' if m4 else '🔒'} **Ej. 4** · `cargar_todos()` → dataset completo y filtros  \n"
    f"{'✅' if m5 else '🔒'} **Ej. 5** · `clasificar_cobertura()` → mapa por clases"
)
st.sidebar.markdown("### 🎯 Misiones · Semana 2")
st.sidebar.markdown(
    f"{'✅' if m7 else '🔒'} **Ej. 7** · `resumen_por_tramos()` → throughput vs calidad  \n"
    f"{'✅' if m8 else '🔒'} **Ej. 8** · `detectar_handovers()` → mapa de handovers"
)
st.sidebar.divider()

# ── Carga de datos ───────────────────────────────────────────────────────────
if m4:
    df = cargar_todo_cacheado(carpeta)
    st.sidebar.markdown("### Filtros")
    for col in ["servicio", "movilidad", "NetworkMode"]:
        if col in df.columns:
            opciones = sorted(df[col].dropna().unique())
            elegidas = st.sidebar.multiselect(col, opciones, default=opciones)
            df = df[df[col].isin(elegidas)]
    origen = "dataset completo"
else:
    ficheros = sorted(Path(carpeta).rglob("*.csv"))
    if not ficheros:
        st.error("La carpeta existe pero no tiene ficheros .csv.")
        st.stop()
    elegido = st.sidebar.selectbox(
        "Fichero (modo un solo fichero)",
        ficheros,
        format_func=lambda p: str(p.relative_to(carpeta)),
    )
    df = cargar_uno_cacheado(str(elegido))
    origen = elegido.name

dfn = numerico(df)

# ── Cabecera y KPIs ──────────────────────────────────────────────────────────
st.title("📡 Drive Test Analyzer")
st.caption(f"Fuente: {origen} · {len(df):,} muestras".replace(",", "."))

if dfn.empty:
    st.warning("Los filtros no dejan ninguna muestra.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Muestras", f"{len(dfn):,}".replace(",", "."))
c2.metric("RSRP mediano", f"{dfn['RSRP'].median():.0f} dBm")
c3.metric("SNR mediano", f"{dfn['SNR'].median():.1f} dB")
descargando = dfn.loc[dfn["State"] == "D", "DL_bitrate"] / 1000
c4.metric("DL mediano (descargando)",
          f"{descargando.median():.1f} Mbps".replace(".", ",") if len(descargando) else "—")

tab_mapa, tab_dist, tab_radio, tab_datos = st.tabs(
    ["🗺️ Mapa", "📊 Distribuciones", "📶 Análisis radio", "🧾 Datos"]
)

# ── Mapa ─────────────────────────────────────────────────────────────────────
with tab_mapa:
    geo = dfn.dropna(subset=["Latitude", "Longitude", "RSRP"])
    if geo.empty:
        st.info("No hay muestras con coordenadas válidas.")
    else:
        comunes = dict(
            lat="Latitude",
            lon="Longitude",
            hover_data={"RSRP": True, "SNR": True, "NetworkMode": True, "CellID": True},
            center=dict(lat=geo["Latitude"].mean(), lon=geo["Longitude"].mean()),
            zoom=12,
            height=600,
            map_style="carto-positron",
        )
        if m5:
            geo = geo.assign(Cobertura=kpis.clasificar_cobertura(geo["RSRP"]).astype(str))
            fig = px.scatter_map(
                geo,
                color="Cobertura",
                color_discrete_map=COLORES_COBERTURA,
                category_orders={"Cobertura": kpis.ORDEN_CLASES},
                **comunes,
            )
        else:
            st.info("🔒 Completa el ejercicio 5 para colorear el mapa por clases de cobertura.")
            fig = px.scatter_map(
                geo, color="RSRP", color_continuous_scale="Purples", **comunes
            )
        fig.update_traces(marker=dict(size=8))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(title="Cobertura (RSRP)"))
        st.plotly_chart(fig, width="stretch")

# ── Distribuciones ───────────────────────────────────────────────────────────
with tab_dist:
    izq, der = st.columns(2)
    with izq:
        kpi = st.selectbox("KPI", [k for k in KPIS_NUMERICOS if k in dfn.columns])
        fig = px.histogram(dfn, x=kpi, nbins=60, color_discrete_sequence=["#6c4cf5"])
        fig.update_traces(marker_line_width=2, marker_line_color="rgba(0,0,0,0)")
        fig.update_layout(bargap=0.05, yaxis_title="Muestras", margin=dict(t=30))
        st.plotly_chart(fig, width="stretch")
    with der:
        st.markdown("**Muestras por tecnología**")
        cuenta = dfn["NetworkMode"].value_counts().reset_index()
        fig = px.bar(cuenta, x="count", y="NetworkMode", orientation="h",
                     color_discrete_sequence=["#6c4cf5"], text="count")
        fig.update_layout(yaxis=dict(categoryorder="total ascending"),
                          xaxis_title="Muestras", yaxis_title=None, margin=dict(t=30))
        st.plotly_chart(fig, width="stretch")

# ── Análisis radio (semana 2) ────────────────────────────────────────────────
TRAMOS = {
    "SNR (dB)": ("SNR", [-float("inf"), 0, 5, 10, 15, 20, float("inf")]),
    "RSRP (dBm)": ("RSRP", [-float("inf"), -110, -100, -90, -80, float("inf")]),
    "CQI": ("CQI", [0, 3, 6, 9, 12, 16]),
}
COLORES_TEC = {"LTE": "#6c4cf5", "5G": "#1D9E75"}
COLORES_HO = {"Misma tecnología": "#6c4cf5", "Cambio de tecnología": "#D85A30"}

with tab_radio:
    # ---------- Ejercicio 7: throughput frente a calidad radio ----------
    st.subheader("Throughput frente a calidad radio")
    if not m7:
        st.info("🔒 Completa el ejercicio 7 (`resumen_por_tramos()`) para desbloquear esta sección.")
    else:
        base = dfn.assign(DL_Mbps=dfn["DL_bitrate"] / 1000)
        if "servicio" in base.columns:
            base = base[base["servicio"] == "Download"]
        base = base[base["State"] == "D"]
        st.caption("Solo muestras de **Download** en estado **D** (descargando): es cuando el throughput "
                   "refleja la capacidad del enlace.")
        a, b = st.columns([1, 1])
        eje = a.selectbox("Agrupar por", list(TRAMOS))
        separar = b.checkbox("Separar LTE y 5G", value=False)
        columna, bins = TRAMOS[eje]
        if base.empty:
            st.warning("Con los filtros actuales no hay muestras de Download descargando.")
        else:
            try:
                if separar:
                    partes = []
                    for tec in ["LTE", "5G"]:
                        sub = base[base["NetworkMode"] == tec]
                        if not sub.empty:
                            r = kpis.resumen_por_tramos(sub, columna, bins).reset_index()
                            partes.append(r.assign(Tecnología=tec))
                    res = pd.concat(partes, ignore_index=True)
                else:
                    res = kpis.resumen_por_tramos(base, columna, bins).reset_index()
                res["tramo"] = res.iloc[:, 0].astype(str)
                fig = px.bar(
                    res, x="tramo", y="mediana", hover_data=["muestras"],
                    color="Tecnología" if separar else None,
                    color_discrete_map=COLORES_TEC, barmode="group",
                    color_discrete_sequence=["#6c4cf5"],
                )
                fig.update_layout(xaxis_title=eje, yaxis_title="DL mediano (Mbps)", margin=dict(t=30))
                st.plotly_chart(fig, width="stretch")
                with st.expander("Ver tabla"):
                    st.dataframe(res.drop(columns="tramo"), width="stretch")
            except Exception as e:
                st.error(f"`resumen_por_tramos()` ha dado un error: {e!r}")

    st.divider()

    # ---------- Ejercicio 8: handovers ----------
    st.subheader("Handovers (cambios de celda servidora)")
    if not m8:
        st.info("🔒 Completa el ejercicio 8 (`detectar_handovers()`) para desbloquear esta sección.")
    elif "fichero" not in dfn.columns:
        st.info("Esta sección necesita el dataset completo (ejercicio 4).")
    else:
        try:
            ho = kpis.detectar_handovers(dfn)
            ho = ho.assign(Tipo=(ho["NetworkMode"] == ho["NetworkMode_anterior"]).map(
                {True: "Misma tecnología", False: "Cambio de tecnología"}))

            dur = dfn.groupby("fichero")["Timestamp"].agg(lambda t: (t.max() - t.min()).total_seconds() / 60)
            tabla = pd.DataFrame({
                "movilidad": dfn.groupby("fichero")["movilidad"].first(),
                "duración (min)": dur.round(1),
                "handovers": ho.groupby("fichero").size(),
            }).fillna({"handovers": 0})
            tabla["handovers"] = tabla["handovers"].astype(int)
            tabla["HO por minuto"] = (tabla["handovers"] / tabla["duración (min)"]).round(2)

            k1, k2, k3 = st.columns(3)
            k1.metric("Handovers detectados", f"{len(ho):,}".replace(",", "."))
            k2.metric("Con cambio de tecnología",
                      f"{(ho['Tipo'] == 'Cambio de tecnología').mean() * 100:.0f} %" if len(ho) else "—")
            k3.metric("HO por minuto (mediana)", f"{tabla['HO por minuto'].median():.2f}".replace(".", ","))

            con_ho = tabla[tabla["handovers"] > 0].sort_values("handovers", ascending=False)
            if con_ho.empty:
                st.info("Con los filtros actuales no hay handovers.")
            else:
                fich = st.selectbox("Recorrido", con_ho.index,
                                    format_func=lambda f: f"{f} · {con_ho.loc[f, 'handovers']} HO")
                ruta = dfn[dfn["fichero"] == fich].dropna(subset=["Latitude", "Longitude"])
                puntos = ho[ho["fichero"] == fich].dropna(subset=["Latitude", "Longitude"])
                fig = px.scatter_map(
                    puntos, lat="Latitude", lon="Longitude", color="Tipo",
                    color_discrete_map=COLORES_HO,
                    hover_data={"Timestamp": True, "CellID_anterior": True, "CellID": True,
                                "NetworkMode_anterior": True, "NetworkMode": True, "RSRP": True},
                    center=dict(lat=ruta["Latitude"].mean(), lon=ruta["Longitude"].mean()),
                    zoom=13, height=550, map_style="carto-positron",
                )
                fig.update_traces(marker=dict(size=12))
                fig.add_scattermap(lat=ruta["Latitude"], lon=ruta["Longitude"], mode="markers",
                                   marker=dict(size=5, color="#b4b2a9"), name="Recorrido",
                                   hoverinfo="skip")
                fig.data = fig.data[-1:] + fig.data[:-1]   # recorrido debajo de los handovers
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(title=None))
                st.plotly_chart(fig, width="stretch")
            with st.expander("Handovers por recorrido"):
                st.dataframe(tabla.sort_values("HO por minuto", ascending=False), width="stretch")
        except Exception as e:
            st.error(f"`detectar_handovers()` ha dado un error: {e!r}")

# ── Datos ────────────────────────────────────────────────────────────────────
with tab_datos:
    st.markdown("**Tipos de cada columna tal y como los carga `cargar_csv()`**")
    st.caption("Si un KPI aparece como `str` en vez de número, hay algo que arreglar (ejercicio 2).")
    tipos = pd.DataFrame({"tipo": df.dtypes.astype(str), "nulos": df.isna().sum()})
    st.dataframe(tipos, width="stretch")
    st.markdown("**Primeras filas**")
    st.dataframe(df.head(200), width="stretch")
