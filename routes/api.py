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
    """
    Guarda datos biométricos y ejecuta predicción de IA
    
    Expected JSON:
    {
        "state": "relaxed|stressed|meditation",
        "breathing_rate": int (0-100),
        "heart_rate": int (0-200),
        "movement": int (0-100),
        "stress_level": "low|medium|high"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No JSON data received'
        }), 400

    required_fields = [
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

    valid_stress_levels = ['low', 'medium', 'high']
    
    if data.get('stress_level') not in valid_stress_levels:
        return jsonify({
            'error': f'Invalid stress_level. Must be one of: {", ".join(valid_stress_levels)}'
        }), 400

    try:
        # Parsear valores biométricos
        breathing_rate = float(data['breathing_rate'])
        heart_rate = float(data['heart_rate'])
        movement = float(data['movement'])
        
        # Obtener servicio de IA y ejecutar predicción
        ai_service = get_ai_service()
        prediction_result = ai_service.predict(
            breathing_rate=breathing_rate,
            heart_rate=heart_rate,
            movement=movement
        )
        
        predicted_state = prediction_result['prediction']['state']
        
        # Guardar datos biométricos en BD
        biometric_data = BiometricData(
            state=predicted_state,
            breathing_rate=int(breathing_rate),
            heart_rate=int(heart_rate),
            movement=int(movement),
            stress_level=data['stress_level']
        )

        db.session.add(biometric_data)
        db.session.commit()

        # Retornar datos guardados + predicción + recomendaciones
        return jsonify({
            'message': 'Biometric data saved and analyzed successfully',
            'data': {
                'stored': biometric_data.to_dict(),
                'analysis': {
                    'prediction': {
                        'state': predicted_state,
                        'confidence': prediction_result['prediction']['confidence'],
                        'confidence_percentage': prediction_result['prediction']['confidence_percentage']
                    },
                    'recommendations': prediction_result['recommendations']
                }
            },
            'status': 'success'
        }), 201

    except ValueError as e:
        return jsonify({
            'error': f'Invalid input values: {str(e)}'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/biometric-data', methods=['GET'])
def get_biometric_data():
    """
    Obtiene los últimos 20 registros biométricos con predicciones y recomendaciones
    
    Query Parameters:
    - limit: Número de registros a retornar (default: 20, max: 100)
    
    Response:
    {
        "message": "Biometric data retrieved successfully",
        "count": 10,
        "data": [
            {
                "id": 1,
                "timestamp": "2026-05-21T14:30:00",
                "breathing_rate": 15,
                "heart_rate": 75,
                "movement": 25,
                "state": "relaxed",
                "stress_level": "low",
                "prediction": {
                    "state": "relaxed",
                    "confidence": 1.0,
                    "confidence_percentage": 100.0
                },
                "recommendations": {
                    "status": "Relajado",
                    "description": "...",
                    "advice": [...],
                    "tips": "..."
                }
            },
            ...
        ]
    }
    """
    try:
        # Obtener límite de parámetros de query (default 20, máximo 100)
        limit = request.args.get('limit', 20, type=int)
        limit = min(limit, 100)  # No permitir más de 100 registros
        limit = max(limit, 1)    # Mínimo 1 registro
        
        # Obtener últimos registros ordenados por timestamp descendente
        records = BiometricData.query.order_by(
            BiometricData.timestamp.desc()
        ).limit(limit).all()
        
        # Obtener servicio de IA
        ai_service = get_ai_service()
        
        # Construir respuesta con predicciones y recomendaciones
        data = []
        for record in records:
            record_dict = record.to_dict()
            
            # Agregar predicción basada en los datos
            try:
                prediction = ai_service.predict(
                    breathing_rate=record.breathing_rate,
                    heart_rate=record.heart_rate,
                    movement=record.movement
                )
                
                record_dict['prediction'] = prediction['prediction']
                record_dict['recommendations'] = prediction['recommendations']
            except Exception as e:
                # Si hay error en predicción, usar valores por defecto
                record_dict['prediction'] = {
                    'state': record.state,
                    'confidence': 0,
                    'confidence_percentage': 0
                }
                record_dict['recommendations'] = {
                    'status': 'Datos disponibles',
                    'description': 'Predicción no disponible',
                    'advice': [],
                    'tips': 'Intenta con datos más precisos'
                }
            
            data.append(record_dict)
        
        return jsonify({
            'message': 'Biometric data retrieved successfully',
            'count': len(data),
            'limit': limit,
            'data': data
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