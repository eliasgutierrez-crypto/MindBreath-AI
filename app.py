from flask import Flask, jsonify
from config import get_config
from models.database import init_db, db

# Importar modelos
from models.biometric_data import BiometricData


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

        return jsonify({
            'message': 'MindBreath AI API',
            'status': 'running',
            'database': 'connected' if db.engine else 'not connected'
        })

    @app.route('/health')
    def health():

        return jsonify({
            'status': 'healthy'
        })

    return app


app = create_app()


if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )