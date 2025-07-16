import pandas as pd
from xgboost import XGBClassifier
from sqlalchemy import create_engine

# Conexión a Supabase
DATABASE_URL = "postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# Simular datos de módulos
datos = pd.DataFrame({
    'modulo': ['activos', 'recursos_humanos', 'contratos', 'archivos_expedientes'],
    'recursos_procesados': [120, 300, 22, 190],
    'dias_estimados': [10, 15, 7, 12],
    'dias_reales': [11, 18, 6, 20]
})

# Crear variable objetivo: retraso (1) si días reales > estimados
datos['retraso'] = (datos['dias_reales'] > datos['dias_estimados']).astype(int)

# Preparar datos
X = datos[['recursos_procesados', 'dias_estimados']]
y = datos['retraso']

# Entrenar modelo
modelo = XGBClassifier()
modelo.fit(X, y)

# Predicción para nuevo módulo
nuevo = pd.DataFrame({'recursos_procesados': [150], 'dias_estimados': [12]})
pred = modelo.predict(nuevo)[0]
proba = modelo.predict_proba(nuevo)[0][1]

print(f"🔍 Retraso predicho: {bool(pred)}, probabilidad: {proba:.2f}")