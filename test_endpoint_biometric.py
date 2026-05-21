#!/usr/bin/env python3
"""
Script de prueba para el endpoint GET /api/biometric-data mejorado
Verifica que retorna últimos 20 registros con predicción y recomendaciones
"""

import sys
import os
import json

os.chdir(r'c:\Users\JuanE\OneDrive\Documentos\MindBreath AI')
sys.path.insert(0, r'c:\Users\JuanE\OneDrive\Documentos\MindBreath AI')

from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

print("="*80)
print("TEST: GET /api/biometric-data - Endpoint Mejorado")
print("="*80)

# Crear 5 registros de prueba primero
print("\n[1/3] Generando 5 registros de prueba...")

test_data = [
    {"breathing_rate": 15, "heart_rate": 75, "movement": 25, "stress_level": "low"},
    {"breathing_rate": 22, "heart_rate": 95, "movement": 60, "stress_level": "high"},
    {"breathing_rate": 12, "heart_rate": 65, "movement": 10, "stress_level": "low"},
    {"breathing_rate": 18, "heart_rate": 80, "movement": 40, "stress_level": "medium"},
    {"breathing_rate": 14, "heart_rate": 70, "movement": 15, "stress_level": "low"},
]

with app.test_client() as client:
    for i, payload in enumerate(test_data, 1):
        response = client.post(
            '/api/biometric-data',
            json=payload,
            content_type='application/json'
        )
        if response.status_code == 201:
            print(f"  [OK] Registro {i} creado")
        else:
            print(f"  [ERROR] Registro {i} falló: {response.status_code}")

# Probar GET endpoint
print("\n[2/3] Obteniendo últimos 20 registros...")
print("-"*80)

with app.test_client() as client:
    # Test 1: Sin parámetros (default 20)
    response = client.get('/api/biometric-data')
    
    print(f"\nStatus Code: {response.status_code}")
    result = response.get_json()
    
    print(f"Mensaje: {result.get('message')}")
    print(f"Total de registros retornados: {result.get('count')}")
    print(f"Límite: {result.get('limit')}")
    
    if response.status_code == 200:
        print("\n[3/3] Validando estructura de respuesta...")
        print("-"*80)
        
        data = result.get('data', [])
        
        if len(data) > 0:
            print(f"[OK] {len(data)} registros obtenidos\n")
            
            # Mostrar primer registro completo
            first_record = data[0]
            print("PRIMER REGISTRO (Más reciente):")
            print(json.dumps(first_record, indent=2, default=str))
            
            # Validar estructura
            print("\n" + "="*80)
            print("VALIDACIÓN DE ESTRUCTURA")
            print("="*80)
            
            required_fields = ['id', 'timestamp', 'state', 'stress_level']
            prediction_fields = ['state', 'confidence', 'confidence_percentage']
            recommendation_fields = ['status', 'description', 'advice', 'tips']
            
            all_valid = True
            
            # Validar campos biométricos
            print("\nCampos Biométricos:")
            for field in required_fields:
                if field in first_record:
                    print(f"  [OK] {field}: {first_record[field]}")
                else:
                    print(f"  [ERROR] {field} - FALTA")
                    all_valid = False
            
            # Validar predicción
            print("\nCampos de Predicción:")
            prediction = first_record.get('prediction', {})
            for field in prediction_fields:
                if field in prediction:
                    print(f"  [OK] prediction.{field}: {prediction[field]}")
                else:
                    print(f"  [ERROR] prediction.{field} - FALTA")
                    all_valid = False
            
            # Validar recomendaciones
            print("\nCampos de Recomendaciones:")
            recommendations = first_record.get('recommendations', {})
            for field in recommendation_fields:
                if field in recommendations:
                    value = recommendations[field]
                    if isinstance(value, list):
                        print(f"  [OK] recommendations.{field}: {len(value)} items")
                    else:
                        print(f"  [OK] recommendations.{field}: {str(value)[:50]}...")
                else:
                    print(f"  [ERROR] recommendations.{field} - FALTA")
                    all_valid = False
            
            # Resumen
            print("\n" + "="*80)
            if all_valid:
                print("[SUCCESS] ✓ Todas las validaciones pasaron")
            else:
                print("[WARNING] ✗ Algunas validaciones fallaron")
            
            # Test 2: Con parámetro limit
            print("\n" + "-"*80)
            print("TEST 2: Obtener solo 3 registros (limit=3)")
            print("-"*80)
            
            response = client.get('/api/biometric-data?limit=3')
            result = response.get_json()
            
            print(f"Status: {response.status_code}")
            print(f"Límite solicitado: 3")
            print(f"Registros retornados: {result.get('count')}")
            print(f"Límite en respuesta: {result.get('limit')}")
            
            if result.get('count') == 3:
                print("[OK] ✓ Parámetro limit funciona correctamente")
            else:
                print(f"[ERROR] ✗ Se esperaban 3, se obtuvieron {result.get('count')}")
            
            # Mostrar datos en tabla
            print("\n" + "="*80)
            print("TABLA RESUMIDA (Últimos 5 registros)")
            print("="*80)
            print(f"\n{'ID':<5} {'Respiración':<12} {'Pulso':<8} {'Movimiento':<12} {'Estado':<15} {'Estrés':<10}")
            print("-"*80)
            
            for record in data[:5]:
                print(
                    f"{record.get('id'):<5} "
                    f"{record.get('breathing_rate'):<12} "
                    f"{record.get('heart_rate'):<8} "
                    f"{record.get('movement'):<12} "
                    f"{record.get('state'):<15} "
                    f"{record.get('stress_level'):<10}"
                )
        
        else:
            print("[ERROR] No hay registros en la respuesta")
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(result)

print("\n" + "="*80)
print("TEST COMPLETADO")
print("="*80)
