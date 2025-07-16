from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, Date, Text, Boolean

# Conexión Supabase (ajusta tu contraseña real)
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tabla: alertas_predictivas
alertas_predictivas = Table('alertas_predictivas', metadata,
    Column('id', Integer, primary_key=True),
    Column('modulo', String),
    Column('probabilidad_retraso', Numeric),
    Column('fecha', Date),
    Column('recomendacion', Text),
    Column('estatus', String)
)

# Tabla: panel_control_kpis
panel_control_kpis = Table('panel_control_kpis', metadata,
    Column('id', Integer, primary_key=True),
    Column('modulo', String),
    Column('kpi_nombre', String),
    Column('valor', Numeric),
    Column('fecha', Date),
    Column('interpretacion', Text),
    Column('estado_semaforo', String)
)

# Tabla: bitacora_acciones
bitacora_acciones = Table('bitacora_acciones', metadata,
    Column('id', Integer, primary_key=True),
    Column('modulo', String),
    Column('descripcion', Text),
    Column('responsable', String),
    Column('fecha', Date),
    Column('resultado', Text)
)

# Crear tablas
try:
    metadata.create_all(engine)
    print("✅ Tablas de IA, KPIs y auditoría creadas correctamente.")
except Exception as e:
    print("❌ Error al crear tablas:", e)