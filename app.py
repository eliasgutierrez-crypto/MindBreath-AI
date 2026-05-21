import os
import threading
import time
from flask import Flask, jsonify, redirect
from config import get_config
from models.database import init_db, db

# Importar modelos
from models.biometric_data import BiometricData


def run_sensor_simulator():
    """Ejecuta el simulador de sensores en segundo plano"""
    from services.simulator import BiometricSimulator
    import requests
    
    simulator = BiometricSimulator()
    
    # Obtener URL de la API (localhost en desarrollo, URL propia en producción)
    api_url = os.environ.get('API_URL', 'http://localhost:5000/api/biometric-data')
    
    while True:
        try:
            # Generar datos
            data = simulator.generate_data()
            
            # Enviar a la API
            response = requests.post(
                api_url,
                json=data,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print(f"[Simulator] Data sent: {data['state']} - BR:{data['breathing_rate']} HR:{data['heart_rate']}")
            
        except Exception as e:
            print(f"[Simulator] Error: {e}")
        
        # Esperar 5 segundos antes del siguiente envío
        time.sleep(5)


def create_app(config_name=None):

    app = Flask(__name__)

    config = get_config(config_name)
    app.config.from_object(config)

    # Inicializar base de datos
    init_db(app)

    # Crear tablas automáticamente
    with app.app_context():
        db.create_all()

    # Registrar blueprint con prefijo /api
    from routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        # Redirigir a Streamlit Cloud
        streamlit_url = os.environ.get('STREAMLIT_URL', 'https://mindbreath-ai-dashboard.onrender.com')
        return redirect(streamlit_url)

    @app.route('/dashboard')
    def dashboard():
        # Redirigir a Streamlit Cloud
        streamlit_url = os.environ.get('STREAMLIT_URL', 'https://mindbreath-ai-dashboard.onrender.com')
        return redirect(streamlit_url)

    @app.route('/api/status')
    def status():

        return jsonify({
            'status': 'healthy'
        })

    # Iniciar simulador de sensores en segundo plano
    if os.environ.get('FLASK_ENV') != 'testing':
        simulator_thread = threading.Thread(target=run_sensor_simulator, daemon=True)
        simulator_thread.start()

    return app


app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port
    )