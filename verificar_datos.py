from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://postgres.mvclmuerspbtzxmwhogc:N25608565n3@aws-0-us-west-1.pooler.supabase.com:6543/postgres")

tablas = ["activos", "recursos_humanos", "contratos", "servicios_generales", "archivos_expedientes", "panel_control_kpis", "alertas_predictivas", "bitacora_acciones"]

for nombre in tablas:
    try:
        df = pd.read_sql(f"SELECT * FROM {nombre}", con=engine)
        print(f"🗂️ {nombre}: {len(df)} registros")
    except Exception as e:
        print(f"❌ {nombre}: error al consultar →", e)