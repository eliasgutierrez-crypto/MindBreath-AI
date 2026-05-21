#!/usr/bin/env python3
"""
Script de prueba para verificar que el dashboard Streamlit funciona
Prueba la conexión a la API y valida que todos los componentes estén listos
"""

import sys
import os
import json

os.chdir(r'c:\Users\JuanE\OneDrive\Documentos\MindBreath AI')
sys.path.insert(0, r'c:\Users\JuanE\OneDrive\Documentos\MindBreath AI')

from dotenv import load_dotenv
load_dotenv()

print("="*70)
print("TEST: MindBreath AI - Dashboard Streamlit")
print("="*70)

# 1. Verificar dependencias
print("\n[1/4] Verificando dependencias...")
try:
    import streamlit as st
    print("  [OK] Streamlit")
except ImportError as e:
    print(f"  [ERROR] Streamlit: {e}")

try:
    import plotly.graph_objects as go
    print("  [OK] Plotly")
except ImportError as e:
    print(f"  [ERROR] Plotly: {e}")

try:
    import pandas as pd
    print("  [OK] Pandas")
except ImportError as e:
    print(f"  [ERROR] Pandas: {e}")

try:
    import requests
    print("  [OK] Requests")
except ImportError as e:
    print(f"  [ERROR] Requests: {e}")

# 2. Verificar API Flask
print("\n[2/4] Verificando API Flask...")
try:
    from app import create_app
    app = create_app()
    print("  [OK] App Flask creada")
    print(f"  [OK] Debug: {app.debug}")
    print(f"  [OK] Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')[:50]}...")
except Exception as e:
    print(f"  [ERROR] {e}")

# 3. Verificar AI Service
print("\n[3/4] Verificando AI Service...")
try:
    from services.ai_service import MindBreathAIService
    ai = MindBreathAIService()
    print("  [OK] AI Service cargado")
    
    model_info = ai.get_model_info()
    print(f"  [OK] Modelo: {model_info.get('model_type')}")
    print(f"  [OK] Estados: {model_info.get('classes')}")
    print(f"  [OK] Estimadores: {model_info.get('n_estimators')}")
    
    # Test predicción
    result = ai.predict(breathing_rate=15, heart_rate=75, movement=25)
    print(f"  [OK] Predicción test: {result['prediction']['state']} ({result['prediction']['confidence_percentage']}%)")
except Exception as e:
    print(f"  [ERROR] {e}")

# 4. Verificar archivos
print("\n[4/4] Verificando archivos necesarios...")
files_to_check = [
    'streamlit_app.py',
    '.streamlit/config.toml',
    'app.py',
    'requirements.txt',
    '.env.example',
    'STREAMLIT_GUIDE.md'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"  [OK] {file}")
    else:
        print(f"  [ERROR] {file} - NO ENCONTRADO")

# Resumen final
print("\n" + "="*70)
print("RESUMEN")
print("="*70)
print("""
Dashboard Streamlit configurado correctamente.

Para ejecutar:
1. API Flask:
   python app.py
   
2. Dashboard (en otra terminal):
   streamlit run streamlit_app.py
   
3. O usa el script helper:
   run.bat (Windows)

En el dashboard:
- Selecciona "Local" para desarrollo
- Configura el intervalo de actualización
- Las gráficas se mostrarán cuando haya datos

Para más info, lee: STREAMLIT_GUIDE.md
""")
print("="*70)
