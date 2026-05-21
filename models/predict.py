import pickle
import numpy as np
from pathlib import Path

MODEL_PATH = 'models/model.pkl'

def load_model(filepath):
    """
    Carga el modelo entrenado desde pickle
    """
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Modelo no encontrado en: {filepath}")
    
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    
    return model

def predict_state(model, breathing_rate, heart_rate, movement):
    """
    Predice el estado mental basado en los datos biométricos
    
    Args:
        model: Modelo RandomForestClassifier
        breathing_rate: Frecuencia respiratoria (breaths/min)
        heart_rate: Frecuencia cardíaca (bpm)
        movement: Movimiento (0-100)
    
    Returns:
        tuple: (estado_predicho, confianza)
    """
    # Preparar datos para predicción
    X = np.array([[breathing_rate, heart_rate, movement]])
    
    # Predicción
    prediction = model.predict(X)[0]
    
    # Confianza (probabilidad máxima)
    probabilities = model.predict_proba(X)[0]
    confidence = max(probabilities)
    
    return prediction, confidence

def predict_batch(model, data_list):
    """
    Realiza predicciones en lote
    
    Args:
        model: Modelo RandomForestClassifier
        data_list: Lista de tuplas (breathing_rate, heart_rate, movement)
    
    Returns:
        list: Lista de predicciones con confianza
    """
    results = []
    
    for breathing_rate, heart_rate, movement in data_list:
        state, confidence = predict_state(model, breathing_rate, heart_rate, movement)
        results.append({
            'breathing_rate': breathing_rate,
            'heart_rate': heart_rate,
            'movement': movement,
            'predicted_state': state,
            'confidence': confidence
        })
    
    return results

def main():
    """
    Función principal para demostración
    """
    print("="*60)
    print("🧠 MindBreath AI - Model Prediction")
    print("="*60)
    
    try:
        # Cargar modelo
        print("\n📂 Cargando modelo...")
        model = load_model(MODEL_PATH)
        print(f"✅ Modelo cargado exitosamente!")
        print(f"   Estados posibles: {model.classes_.tolist()}")
        
        # Ejemplos de predicción
        print("\n📊 Ejemplos de Predicción:\n")
        
        # Caso 1: Relajado
        br, hr, mv = 12, 65, 10
        state, conf = predict_state(model, br, hr, mv)
        print(f"1️⃣  Datos: BR={br}, HR={hr}, MOV={mv}")
        print(f"   Predicción: {state.upper()}")
        print(f"   Confianza: {conf*100:.2f}%\n")
        
        # Caso 2: Estresado
        br, hr, mv = 26, 115, 75
        state, conf = predict_state(model, br, hr, mv)
        print(f"2️⃣  Datos: BR={br}, HR={hr}, MOV={mv}")
        print(f"   Predicción: {state.upper()}")
        print(f"   Confianza: {conf*100:.2f}%\n")
        
        # Caso 3: Meditación
        br, hr, mv = 8, 55, 5
        state, conf = predict_state(model, br, hr, mv)
        print(f"3️⃣  Datos: BR={br}, HR={hr}, MOV={mv}")
        print(f"   Predicción: {state.upper()}")
        print(f"   Confianza: {conf*100:.2f}%\n")
        
        # Predicción en lote
        print("📈 Predicciones en Lote:\n")
        test_data = [
            (14, 68, 15),      # Relajado
            (28, 120, 80),     # Estresado
            (7, 52, 3),        # Meditación
            (25, 105, 70),     # Estresado
            (11, 62, 8)        # Relajado
        ]
        
        predictions = predict_batch(model, test_data)
        
        for i, result in enumerate(predictions, 1):
            print(f"{i}. BR={result['breathing_rate']}, HR={result['heart_rate']}, MOV={result['movement']}")
            print(f"   → {result['predicted_state'].upper()} (confianza: {result['confidence']*100:.2f}%)\n")
        
        print("="*60)
        print("✅ PREDICCIONES COMPLETADAS")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
