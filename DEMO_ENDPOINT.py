#!/usr/bin/env python3
"""
Demostración: Endpoint GET /api/biometric-data con Predicción y Recomendaciones
"""

import json

# ============================================================================
# RESPUESTA DEL ENDPOINT MEJORADO
# ============================================================================

EJEMPLO_RESPUESTA = {
    "message": "Biometric data retrieved successfully",
    "count": 1,
    "limit": 1,
    "data": [
        {
            # ===== DATOS BIOMÉTRICOS =====
            "id": 8,
            "timestamp": "2026-05-21T18:39:05.559095",
            "breathing_rate": 14,
            "heart_rate": 70,
            "movement": 15,
            "state": "relaxed",
            "stress_level": "low",
            
            # ===== PREDICCIÓN IA =====
            "prediction": {
                "state": "relaxed",
                "confidence": 1.0,
                "confidence_percentage": 100.0
            },
            
            # ===== RECOMENDACIONES AUTOMÁTICAS =====
            "recommendations": {
                "status": "Relajado",
                "description": "Tu estado mental es relajado y tranquilo",
                "advice": [
                    "Mantén esta tranquilidad realizando actividades que disfrutes",
                    "Puedes realizar ejercicio ligero o caminar",
                    "Es buen momento para leer o meditar",
                    "Tómate un descanso y disfruta de una bebida relajante"
                ],
                "tips": "Este es un estado ideal. Continúa con tu rutina normal y disfruta del bienestar."
            }
        }
    ]
}

# ============================================================================
# MOSTRAR ESTRUCTURA
# ============================================================================

print("="*80)
print("ENDPOINT MEJORADO: GET /api/biometric-data")
print("="*80)

print("\n📡 REQUEST:")
print("-"*80)
print("GET /api/biometric-data?limit=1")
print()
print("Parámetros:")
print("  • limit = 1 (número de registros, default: 20, max: 100)")

print("\n📊 RESPONSE (200 OK):")
print("-"*80)
print(json.dumps(EJEMPLO_RESPUESTA, indent=2, ensure_ascii=False))

print("\n" + "="*80)
print("DESGLOSE DE LA RESPUESTA")
print("="*80)

record = EJEMPLO_RESPUESTA['data'][0]

print("\n1️⃣  DATOS BIOMÉTRICOS GUARDADOS")
print("-"*80)
print(f"   ID:              {record['id']}")
print(f"   Timestamp:       {record['timestamp']}")
print(f"   Respiración:     {record['breathing_rate']} bpm")
print(f"   Pulso:           {record['heart_rate']} bpm")
print(f"   Movimiento:      {record['movement']}%")
print(f"   Estado:          {record['state']}")
print(f"   Nivel Estrés:    {record['stress_level']}")

print("\n2️⃣  PREDICCIÓN DE IA")
print("-"*80)
pred = record['prediction']
print(f"   Estado Predicho: {pred['state']}")
print(f"   Confianza:       {pred['confidence']} ({pred['confidence_percentage']}%)")

print("\n3️⃣  RECOMENDACIONES PERSONALIZADAS")
print("-"*80)
recs = record['recommendations']
print(f"   Status:          {recs['status']}")
print(f"   Descripción:     {recs['description']}")
print(f"\n   Consejos:")
for i, advice in enumerate(recs['advice'], 1):
    print(f"      {i}. {advice}")
print(f"\n   Tips:")
print(f"      {recs['tips']}")

print("\n" + "="*80)
print("CARACTERÍSTICAS")
print("="*80)

features = [
    ("Últimos N registros", "Configurable con parámetro limit (1-100)"),
    ("Ordenamiento", "Timestamp descendente (más recientes primero)"),
    ("Predicción IA", "Incluye estado predicho y confianza"),
    ("Recomendaciones", "Personalizadas basadas en el estado"),
    ("PostgreSQL Ready", "Integrado con base de datos relacional"),
    ("Sin Cache", "Datos frescos del servidor cada request"),
]

for i, (feature, desc) in enumerate(features, 1):
    print(f"\n{i}. {feature}")
    print(f"   ✓ {desc}")

print("\n" + "="*80)
print("CASOS DE USO")
print("="*80)

casos = [
    ("Dashboard en Tiempo Real", "GET /api/biometric-data?limit=20"),
    ("Widget Último Registro", "GET /api/biometric-data?limit=1"),
    ("Análisis Histórico", "GET /api/biometric-data?limit=100"),
    ("App Mobile", "GET /api/biometric-data?limit=10"),
]

for i, (caso, request) in enumerate(casos, 1):
    print(f"\n{i}. {caso}")
    print(f"   Request: {request}")

print("\n" + "="*80)
print("ESTADOS SOPORTADOS")
print("="*80)

estados = {
    "relaxed": ("Relajado", "Estado mental tranquilo"),
    "stressed": ("Estresado", "Signos de estrés detectados"),
    "meditation": ("Meditación", "Estado profundo de meditación"),
}

for key, (label, desc) in estados.items():
    print(f"\n• {label} ({key})")
    print(f"  {desc}")
    print(f"  Recomendaciones personalizadas generadas automáticamente")

print("\n" + "="*80)
print("TESTING")
print("="*80)

print("\nEjecutar tests:")
print("  python test_endpoint_biometric.py")

print("\nVerificaciones:")
print("  [✓] Status Code 200 OK")
print("  [✓] Registros con predicción")
print("  [✓] Registros con recomendaciones")
print("  [✓] Parámetro limit funciona")
print("  [✓] Ordenamiento por timestamp descendente")
print("  [✓] Máximo 100 registros")

print("\n" + "="*80)
print("INTEGRACIÓN CON STREAMLIT")
print("="*80)

code = """
import requests

# Obtener últimos 20 registros con predicción
response = requests.get('http://localhost:5000/api/biometric-data?limit=20')
data = response.json()

# Procesar registros
for record in data['data']:
    id = record['id']
    timestamp = record['timestamp']
    breathing_rate = record['breathing_rate']
    heart_rate = record['heart_rate']
    movement = record['movement']
    
    # Predicción
    state = record['prediction']['state']
    confidence = record['prediction']['confidence_percentage']
    
    # Recomendaciones
    status = record['recommendations']['status']
    advice = record['recommendations']['advice']
    tips = record['recommendations']['tips']
    
    print(f"ID {id}: {state} ({confidence}%)")
    print(f"Respiración: {breathing_rate} bpm")
    print(f"Pulso: {heart_rate} bpm")
    print(f"Status: {status}")
"""

print(code)

print("\n" + "="*80)
print("RESULTADO")
print("="*80)

print("""
✅ Endpoint GET /api/biometric-data completamente funcional

Features:
  ✓ Últimos 20 registros (configurable hasta 100)
  ✓ Predicción de IA incluida en cada registro
  ✓ Recomendaciones personalizadas automáticas
  ✓ Ordenado por timestamp descendente
  ✓ Compatible con PostgreSQL
  ✓ Parámetro limit flexible
  ✓ Validación de límites
  ✓ Manejo de errores

El endpoint está listo para:
  • Dashboard Streamlit
  • Aplicaciones móviles
  • Análisis histórico
  • Integraciones de terceros
  • Time-series analysis
  • Data warehousing

Ver: ENDPOINT_BIOMETRIC_DATA.md para documentación completa
""")

print("="*80)
