import csv
import random

# Configuración de datos realistas para cada estado
states_config = {
    'relaxed': {
        'breathing_rate': (10, 16),
        'heart_rate': (60, 75),
        'movement': (5, 20),
        'frequency': 0.35
    },
    'stressed': {
        'breathing_rate': (20, 30),
        'heart_rate': (90, 130),
        'movement': (40, 90),
        'frequency': 0.35
    },
    'meditation': {
        'breathing_rate': (6, 10),
        'heart_rate': (50, 65),
        'movement': (0, 10),
        'frequency': 0.30
    }
}

def generate_dataset(total_records=200):
    """
    Genera un dataset realista para entrenar la IA
    """
    records = []
    
    # Calcular cantidad de registros por estado
    for state, config in states_config.items():
        count = int(total_records * config['frequency'])
        for _ in range(count):
            breathing_rate = random.randint(*config['breathing_rate'])
            heart_rate = random.randint(*config['heart_rate'])
            movement = random.randint(*config['movement'])
            records.append({
                'breathing_rate': breathing_rate,
                'heart_rate': heart_rate,
                'movement': movement,
                'state': state
            })
    
    # Mezclar registros aleatoriamente
    random.shuffle(records)
    
    return records

def save_dataset(records, filename='data/training_data.csv'):
    """
    Guarda el dataset en un archivo CSV
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['breathing_rate', 'heart_rate', 'movement', 'state'])
        writer.writeheader()
        writer.writerows(records)

def print_statistics(records):
    """
    Imprime estadísticas del dataset
    """
    total = len(records)
    relaxed = sum(1 for r in records if r['state'] == 'relaxed')
    stressed = sum(1 for r in records if r['state'] == 'stressed')
    meditation = sum(1 for r in records if r['state'] == 'meditation')
    
    print('\n' + '='*60)
    print('✅ Dataset creado exitosamente!')
    print('='*60)
    print(f'📊 Total de registros: {total}')
    print(f'   - Relaxed: {relaxed} ({relaxed/total*100:.1f}%)')
    print(f'   - Stressed: {stressed} ({stressed/total*100:.1f}%)')
    print(f'   - Meditation: {meditation} ({meditation/total*100:.1f}%)')
    print('='*60)
    
    # Estadísticas por estado
    print('\n📈 Estadísticas por Estado:\n')
    for state in ['relaxed', 'stressed', 'meditation']:
        state_records = [r for r in records if r['state'] == state]
        if state_records:
            avg_breathing = sum(r['breathing_rate'] for r in state_records) / len(state_records)
            avg_heart = sum(r['heart_rate'] for r in state_records) / len(state_records)
            avg_movement = sum(r['movement'] for r in state_records) / len(state_records)
            
            print(f'{state.upper()}:')
            print(f'  Breathing Rate: {avg_breathing:.1f} breaths/min')
            print(f'  Heart Rate: {avg_heart:.1f} bpm')
            print(f'  Movement: {avg_movement:.1f}%\n')

if __name__ == '__main__':
    # Generar dataset
    records = generate_dataset(total_records=200)
    
    # Guardar en CSV
    save_dataset(records)
    
    # Imprimir estadísticas
    print_statistics(records)
    
    print(f'💾 Archivo guardado en: data/training_data.csv\n')
