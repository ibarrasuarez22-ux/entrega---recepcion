from sqlalchemy import create_engine, text
from datetime import date

# 🔐 Conexión a Supabase (ajuste necesario: tu contraseña real)
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Crear motor SQLAlchemy
engine = create_engine(DATABASE_URL)

# Datos de la alerta IA
alerta = {
    'modulo': 'activos',
    'probabilidad_retraso': 0.79,
    'fecha': date.today(),
    'recomendacion': 'Revisar asignación en activos.',
    'estatus': 'pendiente'
}

# Insertar alerta en la base de datos Supabase
try:
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO alertas_predictivas (modulo, probabilidad_retraso, fecha, recomendacion, estatus)
            VALUES (:modulo, :probabilidad_retraso, :fecha, :recomendacion, :estatus)
        """), alerta)
        print(f"✅ Alerta registrada correctamente para {alerta['modulo']} (probabilidad: {alerta['probabilidad_retraso']})")
except Exception as e:
    print("❌ Error al registrar alerta:", e)