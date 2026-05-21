# sensor_sender.py

import time
import requests
import sys
from simulator import BiometricSimulator

# URL de la API - Cambiar por tu URL de Render
API_URL = "http://localhost:5000/api/biometric-data"  # Local
# API_URL = "https://tu-app-mindbreath.onrender.com/api/biometric-data"  # Render (comentado)

# Timeout para las peticiones
REQUEST_TIMEOUT = 5

def send_biometric_data(simulator):
    """
    Genera datos biométricos y los envía a la API
    """
    try:
        # Generar datos aleatorios
        data = simulator.generate_data()
        
        print("\n" + "="*60)
        print(f"📊 Enviando datos biométricos...")
        print(f"   Estado: {data['state'].upper()}")
        print(f"   Frecuencia Respiratoria: {data['breathing_rate']} breaths/min")
        print(f"   Frecuencia Cardíaca: {data['heart_rate']} bpm")
        print(f"   Movimiento: {data['movement']}%")
        print(f"   Nivel de Estrés: {data['stress_level']}")
        
        # Enviar datos a la API
        response = requests.post(
            API_URL,
            json=data,
            timeout=REQUEST_TIMEOUT,
            headers={'Content-Type': 'application/json'}
        )
        
        # Procesar respuesta
        if response.status_code == 201:
            print(f"✅ Datos guardados exitosamente (Status: {response.status_code})")
            result = response.json()
            print(f"   Mensaje: {result.get('message', 'Sin mensaje')}")
            if 'data' in result:
                print(f"   ID Registrado: {result['data'].get('id', 'N/A')}")
        else:
            print(f"⚠️  Error en la respuesta (Status: {response.status_code})")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Error de conexión: No se puede conectar a {API_URL}")
        print("   Verifica que:")
        print("   1. La API Flask esté ejecutándose")
        print("   2. La URL sea correcta")
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: La API tardó más de {REQUEST_TIMEOUT} segundos en responder")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def main():
    """
    Función principal que ejecuta el bucle infinito
    """
    print("🚀 MindBreath AI - Sensor Data Sender")
    print(f"📍 API URL: {API_URL}")
    print("⏱️  Interval: 5 segundos")
    print("🛑 Presiona Ctrl+C para detener\n")
    
    # Inicializar simulador
    simulator = BiometricSimulator()
    
    try:
        while True:
            send_biometric_data(simulator)
            
            # Esperar 5 segundos antes de enviar el siguiente dato
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n⛔ Programa detenido por el usuario")
        print("Adiós! 👋")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
