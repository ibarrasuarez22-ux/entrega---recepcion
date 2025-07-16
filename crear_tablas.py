from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, Date, Boolean, Text

# Conexión a Supabase
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tabla: recursos_humanos
Table('recursos_humanos', metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String),
    Column('puesto', String),
    Column('tipo_contrato', String),
    Column('fecha_ingreso', Date),
    Column('estatus_liquidacion', String),
    Column('reubicado', Boolean),
    Column('dependencia_origen', String)
)

# Tabla: contratos
Table('contratos', metadata,
    Column('id', Integer, primary_key=True),
    Column('proveedor', String),
    Column('objeto', String),
    Column('monto', Numeric),
    Column('fecha_inicio', Date),
    Column('fecha_fin', Date),
    Column('entregables', Text),
    Column('estatus', String)
)

# Tabla: servicios_generales
Table('servicios_generales', metadata,
    Column('id', Integer, primary_key=True),
    Column('proveedor', String),
    Column('tipo_servicio', String),
    Column('fecha_inicio', Date),
    Column('fecha_fin', Date),
    Column('cumplimiento', Boolean),
    Column('comentarios', Text)
)

# Tabla: archivos_expedientes
Table('archivos_expedientes', metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String),
    Column('clasificacion', String),
    Column('fecha_creacion', Date),
    Column('digitalizado', Boolean),
    Column('responsable', String)
)

# Tabla: panel_control_kpis
Table('panel_control_kpis', metadata,
    Column('id', Integer, primary_key=True),
    Column('modulo', String),
    Column('kpi_nombre', String),
    Column('valor', Numeric),
    Column('fecha', Date),
    Column('interpretacion', Text),
    Column('estado_semaforo', String)
)

# Tabla: alertas_predictivas
Table('alertas_predictivas', metadata,
    Column('id', Integer, primary_key=True),
    Column('modulo', String),
    Column('probabilidad_retraso', Numeric),
    Column('fecha', Date),
    Column('recomendacion', Text),
    Column('estatus', String)
)

# Crear tablas en Supabase
try:
    metadata.create_all(engine)
    print("✅ Todas las tablas fueron creadas correctamente.")
except Exception as e:
    print("❌ Error al crear tablas:", e)