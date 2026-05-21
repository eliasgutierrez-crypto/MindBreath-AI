import requests
import json
from pprint import pprint

# URL base de la API
API_BASE_URL = "http://localhost:5000/api"

def test_api():
    """
    Prueba los endpoints de la API
    """
    print("="*70)
    print("🧪 MindBreath AI - API Testing")
    print("="*70)
    
    # 1. Obtener información de la API
    print("\n1️⃣  GET /v1 - Información de la API")
    print("-"*70)
    try:
        response = requests.get(f"{API_BASE_URL}/v1")
        print(f"Status: {response.status_code}")
        pprint(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Obtener información del modelo
    print("\n\n2️⃣  GET /model-info - Información del Modelo")
    print("-"*70)
    try:
        response = requests.get(f"{API_BASE_URL}/model-info")
        print(f"Status: {response.status_code}")
        pprint(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Pruebar predicción - Caso Relajado
    print("\n\n3️⃣  POST /predict - Predicción (Relajado)")
    print("-"*70)
    try:
        data = {
            "breathing_rate": 12,
            "heart_rate": 65,
            "movement": 10
        }
        print(f"Input: {data}")
        response = requests.post(f"{API_BASE_URL}/predict", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        print(f"\n✅ Predicción: {result['prediction']['state'].upper()}")
        print(f"   Confianza: {result['prediction']['confidence_percentage']}%")
        print(f"\n{result['recommendations']['emoji']} {result['recommendations']['status']}")
        print(f"   {result['recommendations']['description']}")
        print(f"\n   Consejos:")
        for advice in result['recommendations']['advice'][:3]:
            print(f"   {advice}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Prueba predicción - Caso Estresado
    print("\n\n4️⃣  POST /predict - Predicción (Estresado)")
    print("-"*70)
    try:
        data = {
            "breathing_rate": 26,
            "heart_rate": 115,
            "movement": 75
        }
        print(f"Input: {data}")
        response = requests.post(f"{API_BASE_URL}/predict", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        print(f"\n✅ Predicción: {result['prediction']['state'].upper()}")
        print(f"   Confianza: {result['prediction']['confidence_percentage']}%")
        print(f"\n{result['recommendations']['emoji']} {result['recommendations']['status']}")
        print(f"   {result['recommendations']['description']}")
        print(f"\n   Consejos:")
        for advice in result['recommendations']['advice'][:3]:
            print(f"   {advice}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Prueba predicción - Caso Meditación
    print("\n\n5️⃣  POST /predict - Predicción (Meditación)")
    print("-"*70)
    try:
        data = {
            "breathing_rate": 8,
            "heart_rate": 55,
            "movement": 5
        }
        print(f"Input: {data}")
        response = requests.post(f"{API_BASE_URL}/predict", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        print(f"\n✅ Predicción: {result['prediction']['state'].upper()}")
        print(f"   Confianza: {result['prediction']['confidence_percentage']}%")
        print(f"\n{result['recommendations']['emoji']} {result['recommendations']['status']}")
        print(f"   {result['recommendations']['description']}")
        print(f"\n   Consejos:")
        for advice in result['recommendations']['advice'][:3]:
            print(f"   {advice}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 6. Prueba guardar datos y luego predecir
    print("\n\n6️⃣  POST /biometric-data - Guardar Datos")
    print("-"*70)
    try:
        data = {
            "state": "relaxed",
            "breathing_rate": 13,
            "heart_rate": 68,
            "movement": 12,
            "stress_level": "low"
        }
        print(f"Input: {data}")
        response = requests.post(f"{API_BASE_URL}/biometric-data", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"   ID: {result['data']['id']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 7. Obtener todos los datos
    print("\n\n7️⃣  GET /biometric-data - Obtener Datos")
    print("-"*70)
    try:
        response = requests.get(f"{API_BASE_URL}/biometric-data")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"   Total de registros: {len(result['data'])}")
        if result['data']:
            print(f"   Último registro: {result['data'][0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_api()
