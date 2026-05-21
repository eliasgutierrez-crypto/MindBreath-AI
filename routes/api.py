from flask import Blueprint, jsonify, request

from models.database import db
from models.biometric_data import BiometricData
from services.ai_service import get_ai_service

api_bp = Blueprint('api', __name__)


@api_bp.route('/v1', methods=['GET'])
def api_root():

    return jsonify({
        'message': 'MindBreath AI API v1',
        'endpoints': [
            {
                'path': '/biometric-data',
                'method': 'GET',
                'description': 'Get all biometric data'
            },
            {
                'path': '/biometric-data',
                'method': 'POST',
                'description': 'Save biometric data'
            },
            {
                'path': '/predict',
                'method': 'POST',
                'description': 'Predict mental state using AI',
                'body': {'breathing_rate': 'int', 'heart_rate': 'int', 'movement': 'int'}
            },
            {
                'path': '/model-info',
                'method': 'GET',
                'description': 'Get trained model information'
            }
        ]
    })


@api_bp.route('/biometric-data', methods=['POST'])
def save_biometric_data():

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No JSON data received'
        }), 400

    required_fields = [
        'state',
        'breathing_rate',
        'heart_rate',
        'movement',
        'stress_level'
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                'error': f'Missing field: {field}'
            }), 400

    valid_states = [
        'relaxed',
        'stressed',
        'meditation'
    ]

    if data['state'] not in valid_states:
        return jsonify({
            'error': 'Invalid state'
        }), 400

    try:

        biometric_data = BiometricData(
            state=data['state'],
            breathing_rate=int(data['breathing_rate']),
            heart_rate=int(data['heart_rate']),
            movement=int(data['movement']),
            stress_level=data['stress_level']
        )

        db.session.add(biometric_data)
        db.session.commit()

        return jsonify({
            'message': 'Biometric data saved successfully',
            'data': biometric_data.to_dict()
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/biometric-data', methods=['GET'])
def get_biometric_data():

    try:
        records = BiometricData.query.order_by(BiometricData.timestamp.desc()).all()
        
        return jsonify({
            'message': 'Biometric data retrieved successfully',
            'data': [record.to_dict() for record in records]
        }), 200

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/predict', methods=['POST'])
def predict_state():
    """
    Realiza una predicción de estado mental basado en datos biométricos
    
    Expected JSON:
    {
        "breathing_rate": int,
        "heart_rate": int,
        "movement": int
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No JSON data received'
        }), 400

    # Validar campos requeridos
    required_fields = ['breathing_rate', 'heart_rate', 'movement']
    
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing field: {field}'
            }), 400

    try:
        # Obtener servicio de IA
        ai_service = get_ai_service()
        
        # Realizar predicción
        result = ai_service.predict(
            breathing_rate=float(data['breathing_rate']),
            heart_rate=float(data['heart_rate']),
            movement=float(data['movement'])
        )
        
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """
    Retorna información sobre el modelo entrenado
    """
    try:
        ai_service = get_ai_service()
        info = ai_service.get_model_info()
        
        return jsonify({
            'message': 'Model information retrieved successfully',
            'data': info
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500