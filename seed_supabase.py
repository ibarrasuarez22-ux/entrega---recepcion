from sqlalchemy import create_engine, text
from datetime import date, timedelta
import random

# 🔐 Conexión Supabase
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# 📅 Fechas base
hoy = date.today()
dias = [hoy - timedelta(days=i) for i in range(5)]

# 🧮 Inserción robusta con confirmación
def insertar_batch(tabla, registros):
    if not registros:
        print(f"⚠️ {tabla}: sin registros para insertar.")
        return
    columnas = ", ".join(registros[0].keys())
    valores = ", ".join([f":{k}" for k in registros[0].keys()])
    query = text(f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})")
    try:
        with engine.begin() as conn:
            conn.execute(query, registros)
        print(f"✔ {tabla}: {len(registros)} registros insertados.")
    except Exception as e:
        print(f"❌ {tabla}: error al insertar → {e}")

# 🟩 Activos
activos = [{
    'nombre': f'Equipo-{i}',
    'tipo': random.choice(['Computadora', 'Servidor', 'Escáner']),
    'ubicacion': f'Dependencia-{i%3 + 1}',
    'valor': round(random.uniform(5000, 35000), 2),
    'estado': random.choice(['Operativo', 'Pendiente', 'Desincorporado']),
    'responsable': f'Usuario-{i%4 + 1}',
    'fecha_adquisicion': dias[i%5],
    'codigo_interno': f'ACT{i:03d}'
} for i in range(12)]

# 👥 Recursos humanos
recursos_humanos = [{
    'nombre': f'Empleado-{i}',
    'puesto': random.choice(['Auxiliar', 'Coordinador', 'Técnico']),
    'tipo_contrato': random.choice(['Base', 'Temporal']),
    'fecha_ingreso': dias[i%5] - timedelta(days=random.randint(100, 1000)),
    'estatus_liquidacion': random.choice(['En proceso', 'Finalizado', 'Pendiente']),
    'reubicado': random.choice([True, False]),
    'dependencia_origen': f'Dependencia-{i%3 + 1}'
} for i in range(10)]

# 📄 Contratos
contratos = [{
    'proveedor': f'Proveedor-{i}',
    'objeto': random.choice(['Mantenimiento', 'Consultoría', 'Suministro']),
    'monto': round(random.uniform(20000, 150000), 2),
    'fecha_inicio': dias[i%5] - timedelta(days=30),
    'fecha_fin': dias[i%5] + timedelta(days=60),
    'entregables': f'Informe-{i}, Plano-{i}',
    'estatus': random.choice(['Activo', 'Cerrado', 'Suspendido'])
} for i in range(8)]

# 🧹 Servicios generales
servicios = [{
    'proveedor': f'Servicio-{i}',
    'tipo_servicio': random.choice(['Limpieza', 'Seguridad', 'Soporte TI']),
    'fecha_inicio': dias[i%5] - timedelta(days=15),
    'fecha_fin': dias[i%5] + timedelta(days=45),
    'cumplimiento': random.choice([True, False]),
    'comentarios': f'Revisión ciclo {i}'
} for i in range(6)]

# 🗂️ Expedientes
expedientes = [{
    'nombre': f'Exp-{i}',
    'clasificacion': random.choice(['Legal', 'Técnico', 'Administrativo']),
    'fecha_creacion': dias[i%5] - timedelta(days=50),
    'digitalizado': random.choice([True, False]),
    'responsable': f'Usuario-{i%3 + 1}'
} for i in range(10)]

# 📊 KPIs
kpis = []
modulos_kpi = ['activos', 'recursos_humanos', 'contratos', 'archivos_expedientes']
semaforos = ['verde', 'amarillo', 'rojo']
for m in modulos_kpi:
    for f in dias:
        kpis.append({
            'modulo': m,
            'kpi_nombre': f'Indicador-{m}',
            'valor': random.randint(60, 150),
            'fecha': f,
            'interpretacion': f'Desempeño {m} el {f}.',
            'estado_semaforo': random.choice(semaforos)
        })

# 🔔 Alertas IA
alertas = [{
    'modulo': m,
    'probabilidad_retraso': round(random.uniform(0.65, 0.95), 2),
    'fecha': hoy,
    'recomendacion': f"Revisar asignación en {m}.",
    'estatus': 'pendiente'
} for m in modulos_kpi]

# 📝 Bitácora
bitacora = [{
    'modulo': random.choice(modulos_kpi),
    'descripcion': f'Revisión interna módulo {i}',
    'responsable': f'Responsable-{i%4 + 1}',
    'fecha': dias[i%5],
    'resultado': random.choice(['Validado', 'Observado', 'Requiere seguimiento'])
} for i in range(8)]

# 🚀 Poblar Supabase
insertar_batch('activos', activos)
insertar_batch('recursos_humanos', recursos_humanos)
insertar_batch('contratos', contratos)
insertar_batch('servicios_generales', servicios)
insertar_batch('archivos_expedientes', expedientes)
insertar_batch('panel_control_kpis', kpis)
insertar_batch('alertas_predictivas', alertas)
insertar_batch('bitacora_acciones', bitacora)

print("\n✅ Todas las tablas fueron procesadas.")