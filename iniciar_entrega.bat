@echo off
echo 🟢 Iniciando dashboard de liquidación...
start "" http://localhost:8501
start /B "" "C:\Users\ibarr\AppData\Local\Programs\Python\Python310\Scripts\streamlit.exe" run "C:\Users\ibarr\Documents\entrega\dashboard_liquidacion.py"