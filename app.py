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

st.sidebar.markdown("### 🎯 Misiones · Semana 1")
st.sidebar.markdown(
    f"{'✅' if m4 else '🔒'} **Ej. 4** · `cargar_todos()` → dataset completo y filtros  \n"
    f"{'✅' if m5 else '🔒'} **Ej. 5** · `clasificar_cobertura()` → mapa por clases"
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
c4.metric("DL mediano", f"{dfn['DL_bitrate'].median():,.0f}".replace(",", ".") + " kbps*")
st.caption("*Unidad de DL_bitrate por confirmar en el paper del dataset (pregunta del ejercicio 6).")

tab_mapa, tab_dist, tab_datos = st.tabs(["🗺️ Mapa", "📊 Distribuciones", "🧾 Datos"])

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

# ── Datos ────────────────────────────────────────────────────────────────────
with tab_datos:
    st.markdown("**Tipos de cada columna tal y como los carga `cargar_csv()`**")
    st.caption("Si un KPI aparece como `object` en vez de número, hay algo que arreglar (ejercicio 2).")
    tipos = pd.DataFrame({"tipo": df.dtypes.astype(str), "nulos": df.isna().sum()})
    st.dataframe(tipos, width="stretch")
    st.markdown("**Primeras filas**")
    st.dataframe(df.head(200), width="stretch")
