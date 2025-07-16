import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from io import BytesIO

# 🔐 Conexión Supabase
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="Panel Estratégico de Liquidación", layout="wide")

# 🔄 Cargar datos
@st.cache_data
def cargar_tabla(nombre):
    try:
        return pd.read_sql(f"SELECT * FROM {nombre}", con=engine)
    except Exception as e:
        st.warning(f"No se pudo cargar la tabla: {nombre}. Error: {e}")
        return pd.DataFrame()

# 📊 KPIs
df_kpis = cargar_tabla("panel_control_kpis")
if not df_kpis.empty:
    df_kpis['fecha'] = pd.to_datetime(df_kpis['fecha'])

# 🔔 Alertas IA
df_alertas = cargar_tabla("alertas_predictivas")
if not df_alertas.empty:
    df_alertas['fecha'] = pd.to_datetime(df_alertas['fecha'])

# 🏢 Activos
df_activos = cargar_tabla("activos")

# 🧑 Recursos humanos
df_rh = cargar_tabla("recursos_humanos")

# 📄 Contratos
df_contratos = cargar_tabla("contratos")

# 📒 Bitácora de acciones
df_bitacora = cargar_tabla("bitacora_acciones")
if not df_bitacora.empty:
    df_bitacora['fecha'] = pd.to_datetime(df_bitacora['fecha'])

# 🎛️ Filtros generales
st.sidebar.title("🎚️ Filtros de KPIs")
modulos_disponibles = df_kpis['modulo'].unique() if not df_kpis.empty else []
modulo_seleccionado = st.sidebar.multiselect("Módulo", options=modulos_disponibles, default=modulos_disponibles)

# ⏱️ Fechas para KPIs
if not df_kpis.empty:
    fecha_min_kpi = df_kpis['fecha'].dropna().min()
    fecha_max_kpi = df_kpis['fecha'].dropna().max()
else:
    fecha_min_kpi = fecha_max_kpi = datetime.today()

fecha_inicio = st.sidebar.date_input("Desde", value=fecha_min_kpi.date(), key="desde_kpi")
fecha_fin = st.sidebar.date_input("Hasta", value=fecha_max_kpi.date(), key="hasta_kpi")

# 🔍 Filtrar KPIs
df_kpi_filtrado = df_kpis[
    (df_kpis['modulo'].isin(modulo_seleccionado)) &
    (df_kpis['fecha'] >= pd.to_datetime(fecha_inicio)) &
    (df_kpis['fecha'] <= pd.to_datetime(fecha_fin))
] if not df_kpis.empty else pd.DataFrame()

# 📊 Panel KPI
st.title("📊 Panel Estratégico de Gestión")
st.subheader("Tendencias e Indicadores por módulo")

if df_kpi_filtrado.empty:
    st.info("No hay datos disponibles en KPIs para los filtros seleccionados.")
else:
    for mod in modulo_seleccionado:
        df_mod = df_kpi_filtrado[df_kpi_filtrado['modulo'] == mod]
        with st.expander(f"📌 Módulo: {mod}", expanded=False):
            st.dataframe(df_mod[['fecha', 'kpi_nombre', 'valor', 'estado_semaforo', 'interpretacion']], use_container_width=True)
            st.line_chart(df_mod.set_index('fecha')['valor'])

# ⚠️ Panel de Alertas Predictivas
st.header("⚠️ Alertas generadas por IA")

df_alertas_filtradas = df_alertas[df_alertas['modulo'].isin(modulo_seleccionado)] if not df_alertas.empty else pd.DataFrame()

if df_alertas_filtradas.empty:
    st.info("No hay alertas predictivas generadas para los módulos seleccionados.")
else:
    st.dataframe(df_alertas_filtradas[['modulo', 'probabilidad_retraso', 'fecha', 'recomendacion', 'estatus']], use_container_width=True)

# 🗂️ Vista general de recursos clave
st.header("📁 Recursos activos, contratos y personal")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔧 Activos totales", len(df_activos))
    st.dataframe(df_activos[['nombre', 'tipo', 'ubicacion', 'estado']], height=250)

with col2:
    st.metric("👨‍💼 Empleados registrados", len(df_rh))
    st.dataframe(df_rh[['nombre', 'puesto', 'estatus_liquidacion', 'reubicado']], height=250)

with col3:
    activos_contrato = df_contratos[df_contratos['estatus'] == "Activo"] if not df_contratos.empty else pd.DataFrame()
    st.metric("📑 Contratos activos", len(activos_contrato))
    st.dataframe(activos_contrato[['proveedor', 'objeto', 'estatus', 'monto']], height=250)

# 📒 Panel de Auditoría de acciones
st.header("📒 Bitácora de acciones registradas")

if df_bitacora.empty:
    st.info("No hay registros en la bitácora.")
else:
    # 🗓️ Fechas seguras
    fecha_min_bita = df_bitacora['fecha'].dropna().min()
    fecha_max_bita = df_bitacora['fecha'].dropna().max()
    if pd.isna(fecha_min_bita): fecha_min_bita = datetime.today()
    if pd.isna(fecha_max_bita): fecha_max_bita = datetime.today()

    # 🎚️ Filtros
    with st.expander("📋 Filtrar acciones"):
        modulo_audit = st.multiselect("Módulo", df_bitacora['modulo'].unique(), default=df_bitacora['modulo'].unique())
        responsable_sel = st.multiselect("Responsable", df_bitacora['responsable'].unique(), default=df_bitacora['responsable'].unique())
        fecha_ini = st.date_input("Desde", value=fecha_min_bita.date(), key="desde_bitacora")
        fecha_fin = st.date_input("Hasta", value=fecha_max_bita.date(), key="hasta_bitacora")

    df_audit_filtrado = df_bitacora[
        (df_bitacora['modulo'].isin(modulo_audit)) &
        (df_bitacora['responsable'].isin(responsable_sel)) &
        (df_bitacora['fecha'] >= pd.to_datetime(fecha_ini)) &
        (df_bitacora['fecha'] <= pd.to_datetime(fecha_fin))
    ]

    st.dataframe(df_audit_filtrado[['modulo', 'descripcion', 'responsable', 'fecha', 'resultado']], use_container_width=True)

    # ⬇️ Exportar a Excel
    excel_buffer = BytesIO()
    df_audit_filtrado.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)

    st.download_button(
        label="📥 Descargar auditoría en Excel",
        data=excel_buffer,
        file_name=f"auditoria_liquidacion_{datetime.today().date()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )