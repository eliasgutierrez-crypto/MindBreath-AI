import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

# Rutas
DATA_PATH = 'data/training_data.csv'
MODEL_PATH = 'models/model.pkl'

def load_data(filepath):
    """
    Carga el dataset CSV
    """
    print(f"📂 Cargando dataset desde: {filepath}")
    df = pd.read_csv(filepath)
    print(f"✅ Dataset cargado: {len(df)} registros")
    return df

def prepare_data(df):
    """
    Separa features (X) y labels (y)
    """
    print("\n🔧 Preparando datos...")
    
    # Features: breathing_rate, heart_rate, movement
    X = df[['breathing_rate', 'heart_rate', 'movement']]
    
    # Labels: state
    y = df['state']
    
    print(f"   Features (X): {X.shape}")
    print(f"   Labels (y): {y.shape}")
    print(f"   Estados únicos: {y.unique().tolist()}")
    
    return X, y

def train_model(X, y):
    """
    Entrena el modelo RandomForestClassifier
    """
    print("\n🤖 Entrenando modelo RandomForestClassifier...")
    
    # Dividir datos: 80% entrenamiento, 20% prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Datos de entrenamiento: {X_train.shape[0]} registros")
    print(f"   Datos de prueba: {X_test.shape[0]} registros")
    
    # Crear y entrenar modelo
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print(f"✅ Modelo entrenado exitosamente!")
    
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evalúa el rendimiento del modelo
    """
    print("\n📊 Evaluando modelo...\n")
    
    # Predicciones
    y_pred = model.predict(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"🎯 Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Reporte de clasificación
    print("\n📈 Reporte de Clasificación:")
    print("-" * 60)
    print(classification_report(y_test, y_pred, target_names=model.classes_))
    
    # Matriz de confusión
    print("\n🔍 Matriz de Confusión:")
    print("-" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Feature importance
    print("\n⭐ Importancia de Features:")
    print("-" * 60)
    feature_names = ['breathing_rate', 'heart_rate', 'movement']
    for name, importance in zip(feature_names, model.feature_importances_):
        print(f"   {name}: {importance:.4f} ({importance*100:.2f}%)")
    
    return accuracy

def save_model(model, filepath):
    """
    Guarda el modelo usando pickle
    """
    print(f"\n💾 Guardando modelo...")
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✅ Modelo guardado en: {filepath}")
    print(f"   Tamaño: {os.path.getsize(filepath) / 1024:.2f} KB")

def main():
    """
    Función principal
    """
    print("="*60)
    print("🧠 MindBreath AI - Model Training")
    print("="*60)
    
    try:
        # 1. Cargar datos
        df = load_data(DATA_PATH)
        
        # 2. Preparar datos
        X, y = prepare_data(df)
        
        # 3. Entrenar modelo
        model, X_test, y_test = train_model(X, y)
        
        # 4. Evaluar modelo
        accuracy = evaluate_model(model, X_test, y_test)
        
        # 5. Guardar modelo
        save_model(model, MODEL_PATH)
        
        # Resumen final
        print("\n" + "="*60)
        print("✅ ENTRENAMIENTO COMPLETADO")
        print("="*60)
        print(f"Accuracy final: {accuracy*100:.2f}%")
        print(f"Modelo guardado en: {MODEL_PATH}")
        print("="*60 + "\n")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {DATA_PATH}")
        print("   Ejecuta primero: python data/generate_dataset.py")
        
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
