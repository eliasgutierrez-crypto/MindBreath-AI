# ai_service.py

import pickle
import numpy as np
from pathlib import Path

MODEL_PATH = 'models/model.pkl'

class MindBreathAIService:
    """
    Servicio de IA para MindBreath AI
    Realiza predicciones de estado mental y proporciona recomendaciones
    """
    
    def __init__(self, model_path=MODEL_PATH):
        """
        Inicializa el servicio cargando el modelo entrenado
        
        Args:
            model_path: Ruta al archivo model.pkl
        """
        self.model_path = model_path
        self.model = None
        self.load_model()
        
        # Recomendaciones por estado
        self.recommendations = {
            'relaxed': {
                'status': '😌 Relajado',
                'description': 'Tu estado mental es relajado y tranquilo',
                'advice': [
                    '✨ Mantén esta tranquilidad realizando actividades que disfrutes',
                    '🏃 Puedes realizar ejercicio ligero o caminar',
                    '📚 Es buen momento para leer o meditar',
                    '☕ Tómate un descanso y disfruta de una bebida relajante'
                ],
                'tips': 'Este es un estado ideal. Continúa con tu rutina normal y disfruta del bienestar.',
                'emoji': '😌'
            },
            'stressed': {
                'status': '😰 Estresado',
                'description': 'Detectamos que tu estado mental muestra signos de estrés',
                'advice': [
                    '🧘 Realiza ejercicios de respiración profunda (4-7-8)',
                    '🚶 Haz una caminata al aire libre para despejar la mente',
                    '🎵 Escucha música relajante o sonidos de la naturaleza',
                    '💬 Comparte tus preocupaciones con alguien de confianza',
                    '⏸️ Toma un descanso de tus actividades actuales'
                ],
                'tips': 'El estrés es temporal. Practica técnicas de relajación y cuida tu bienestar.',
                'emoji': '😰'
            },
            'meditation': {
                'status': '🧘 Meditación',
                'description': 'Te encuentras en un estado profundo de meditación',
                'advice': [
                    '🕉️ Continúa con tu sesión de meditación',
                    '📿 Practica mindfulness y enfócate en tu respiración',
                    '🌿 Siente la conexión con tu cuerpo y mente',
                    '✍️ Después de meditar, dedica tiempo a reflexionar',
                    '💆 Aprovecha este estado para recuperar energía'
                ],
                'tips': 'Excelente estado de meditación. Mantente en esta paz interior y disfruta del momento.',
                'emoji': '🧘'
            }
        }
    
    def load_model(self):
        """
        Carga el modelo entrenado desde pickle
        """
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Modelo no encontrado en: {self.model_path}")
        
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"[OK] Modelo cargado exitosamente desde: {self.model_path}")
        except Exception as e:
            raise Exception(f"Error cargando el modelo: {e}")
    
    def predict(self, breathing_rate, heart_rate, movement):
        """
        Realiza una predicción del estado mental
        
        Args:
            breathing_rate: Frecuencia respiratoria (breaths/min)
            heart_rate: Frecuencia cardíaca (bpm)
            movement: Movimiento (0-100)
        
        Returns:
            dict: Predicción con estado, confianza y recomendaciones
        """
        if self.model is None:
            raise Exception("El modelo no ha sido cargado")
        
        # Validar datos
        try:
            br = float(breathing_rate)
            hr = float(heart_rate)
            mv = float(movement)
        except (ValueError, TypeError):
            raise ValueError("Los valores deben ser números")
        
        # Validar rangos
        if br < 0 or br > 100:
            raise ValueError("Breathing rate debe estar entre 0 y 100")
        if hr < 0 or hr > 200:
            raise ValueError("Heart rate debe estar entre 0 y 200")
        if mv < 0 or mv > 100:
            raise ValueError("Movement debe estar entre 0 y 100")
        
        # Preparar datos para predicción
        X = np.array([[br, hr, mv]])
        
        # Predicción
        try:
            predicted_state = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(max(probabilities))
        except Exception as e:
            raise Exception(f"Error durante la predicción: {e}")
        
        # Obtener recomendaciones
        recommendations = self.get_recommendations(predicted_state)
        
        # Construir respuesta
        result = {
            'input': {
                'breathing_rate': br,
                'heart_rate': hr,
                'movement': mv
            },
            'prediction': {
                'state': predicted_state,
                'confidence': round(confidence, 4),
                'confidence_percentage': round(confidence * 100, 2)
            },
            'recommendations': recommendations,
            'status': 'success'
        }
        
        return result
    
    def get_recommendations(self, state):
        """
        Obtiene las recomendaciones para el estado predicho
        
        Args:
            state: Estado predicho (relaxed, stressed, meditation)
        
        Returns:
            dict: Recomendaciones personalizadas
        """
        if state not in self.recommendations:
            return {
                'status': '❓ Estado desconocido',
                'description': 'No se pudo identificar el estado',
                'advice': ['Intenta nuevamente con datos válidos'],
                'tips': 'Verifica que los datos biométricos sean correctos',
                'emoji': '❓'
            }
        
        return self.recommendations[state]
    
    def predict_batch(self, data_list):
        """
        Realiza predicciones en lote
        
        Args:
            data_list: Lista de tuplas (breathing_rate, heart_rate, movement)
        
        Returns:
            list: Lista de predicciones
        """
        results = []
        
        for breathing_rate, heart_rate, movement in data_list:
            try:
                result = self.predict(breathing_rate, heart_rate, movement)
                results.append(result)
            except Exception as e:
                results.append({
                    'error': str(e),
                    'status': 'error'
                })
        
        return results
    
    def get_model_info(self):
        """
        Retorna información sobre el modelo entrenado
        
        Returns:
            dict: Información del modelo
        """
        if self.model is None:
            return {'status': 'error', 'message': 'Modelo no cargado'}
        
        return {
            'model_type': 'RandomForestClassifier',
            'classes': list(self.model.classes_),
            'n_estimators': self.model.n_estimators,
            'features': ['breathing_rate', 'heart_rate', 'movement'],
            'feature_importances': {
                'breathing_rate': round(float(self.model.feature_importances_[0]), 4),
                'heart_rate': round(float(self.model.feature_importances_[1]), 4),
                'movement': round(float(self.model.feature_importances_[2]), 4)
            },
            'status': 'active'
        }


# Inicialización global del servicio
_ai_service = None

def get_ai_service():
    """
    Obtiene la instancia global del servicio de IA
    
    Returns:
        MindBreathAIService: Instancia del servicio
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = MindBreathAIService()
    return _ai_service


# Ejemplo de uso
if __name__ == '__main__':
    print("="*70)
    print("🧠 MindBreath AI - AI Service")
    print("="*70)
    
    try:
        # Inicializar servicio
        ai_service = MindBreathAIService()
        
        # Información del modelo
        print("\n📊 Información del Modelo:")
        print("-"*70)
        model_info = ai_service.get_model_info()
        for key, value in model_info.items():
            print(f"{key}: {value}")
        
        # Ejemplos de predicción
        print("\n\n🔮 Ejemplos de Predicción:\n")
        
        test_cases = [
            (12, 65, 10, "Relajado"),
            (26, 115, 75, "Estresado"),
            (8, 55, 5, "Meditación")
        ]
        
        for br, hr, mv, label in test_cases:
            print(f"\n{'='*70}")
            print(f"Caso: {label}")
            print(f"Datos: BR={br} breaths/min, HR={hr} bpm, MOV={mv}%")
            print(f"{'='*70}")
            
            result = ai_service.predict(br, hr, mv)
            
            # Mostrar predicción
            pred = result['prediction']
            print(f"\n✅ Predicción: {pred['state'].upper()}")
            print(f"   Confianza: {pred['confidence_percentage']}%")
            
            # Mostrar recomendaciones
            rec = result['recommendations']
            print(f"\n{rec['emoji']} {rec['status']}")
            print(f"   {rec['description']}")
            print(f"\n   Consejos:")
            for advice in rec['advice']:
                print(f"   {advice}")
            print(f"\n   💡 {rec['tips']}")
        
        print(f"\n\n{'='*70}")
        print("✅ AI SERVICE FUNCIONANDO CORRECTAMENTE")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
