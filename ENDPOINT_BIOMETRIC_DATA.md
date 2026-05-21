# 📊 Endpoint GET /api/biometric-data - Documentación

## Descripción

Obtiene los últimos registros biométricos almacenados con **predicciones de IA** y **recomendaciones personalizadas**.

Los registros se retornan ordenados por **timestamp descendente** (más recientes primero).

---

## Request

### URL
```
GET /api/biometric-data
GET /api/biometric-data?limit=10
```

### Parámetros de Query

| Parámetro | Tipo | Default | Rango | Descripción |
|-----------|------|---------|-------|-------------|
| `limit` | integer | 20 | 1-100 | Número de registros a retornar |

### Headers
```
Content-Type: application/json
```

### Ejemplos

```bash
# Obtener últimos 20 registros (default)
curl -X GET "http://localhost:5000/api/biometric-data"

# Obtener últimos 10 registros
curl -X GET "http://localhost:5000/api/biometric-data?limit=10"

# Obtener solo el último registro
curl -X GET "http://localhost:5000/api/biometric-data?limit=1"
```

---

## Response

### Status Code
- `200 OK` - Registros obtenidos exitosamente
- `500 Internal Server Error` - Error en el servidor

### Body (Success)

```json
{
  "message": "Biometric data retrieved successfully",
  "count": 8,
  "limit": 20,
  "data": [
    {
      "id": 8,
      "timestamp": "2026-05-21T18:39:05.559095",
      "breathing_rate": 14,
      "heart_rate": 70,
      "movement": 15,
      "state": "relaxed",
      "stress_level": "low",
      "prediction": {
        "state": "relaxed",
        "confidence": 1.0,
        "confidence_percentage": 100.0
      },
      "recommendations": {
        "status": "Relajado",
        "description": "Tu estado mental es relajado y tranquilo",
        "advice": [
          "Mantén esta tranquilidad realizando actividades que disfrutes",
          "Puedes realizar ejercicio ligero o caminar",
          "Es buen momento para leer o meditar",
          "Tómate un descanso y disfruta de una bebida relajante"
        ],
        "tips": "Este es un estado ideal. Continúa con tu rutina normal y disfruta del bienestar."
      }
    },
    {
      "id": 7,
      "timestamp": "2026-05-21T18:38:45.123456",
      "breathing_rate": 18,
      "heart_rate": 80,
      "movement": 40,
      "state": "relaxed",
      "stress_level": "medium",
      "prediction": {
        "state": "relaxed",
        "confidence": 0.95,
        "confidence_percentage": 95.0
      },
      "recommendations": {
        "status": "Relajado",
        "description": "Tu estado mental es relajado y tranquilo",
        "advice": [...],
        "tips": "..."
      }
    }
  ]
}
```

### Body (Error)

```json
{
  "error": "Descripción del error"
}
```

---

## Estructura de Respuesta

### Campo `data` (Array de Registros)

Cada registro contiene:

#### Datos Biométricos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID único del registro |
| `timestamp` | ISO 8601 | Fecha/hora del registro |
| `breathing_rate` | integer | Respiraciones por minuto (0-100) |
| `heart_rate` | integer | Latidos por minuto (0-200) |
| `movement` | integer | Porcentaje de movimiento (0-100) |
| `state` | string | Estado guardado (relaxed, stressed, meditation) |
| `stress_level` | string | Nivel de estrés (low, medium, high) |

#### Predicción IA
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `prediction.state` | string | Estado predicho por IA |
| `prediction.confidence` | float | Confianza (0.0-1.0) |
| `prediction.confidence_percentage` | float | Confianza en % (0-100) |

#### Recomendaciones
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `recommendations.status` | string | Etiqueta del estado |
| `recommendations.description` | string | Descripción de la situación |
| `recommendations.advice` | array | Lista de 4 consejos |
| `recommendations.tips` | string | Consejo general |

---

## Estados y Recomendaciones

### Estado: `relaxed` (Relajado)
```json
{
  "status": "Relajado",
  "description": "Tu estado mental es relajado y tranquilo",
  "advice": [
    "Mantén esta tranquilidad realizando actividades que disfrutes",
    "Puedes realizar ejercicio ligero o caminar",
    "Es buen momento para leer o meditar",
    "Tómate un descanso y disfruta de una bebida relajante"
  ],
  "tips": "Este es un estado ideal. Continúa con tu rutina normal y disfruta del bienestar."
}
```

### Estado: `stressed` (Estresado)
```json
{
  "status": "Estresado",
  "description": "Detectamos que tu estado mental muestra signos de estrés",
  "advice": [
    "Realiza ejercicios de respiración profunda (4-7-8)",
    "Haz una caminata al aire libre para despejar la mente",
    "Escucha música relajante o sonidos de la naturaleza",
    "Comparte tus preocupaciones con alguien de confianza",
    "Toma un descanso de tus actividades actuales"
  ],
  "tips": "El estrés es temporal. Practica técnicas de relajación y cuida tu bienestar."
}
```

### Estado: `meditation` (Meditación)
```json
{
  "status": "Meditación",
  "description": "Te encuentras en un estado profundo de meditación",
  "advice": [
    "Continúa con tu sesión de meditación",
    "Practica mindfulness y enfócate en tu respiración",
    "Siente la conexión con tu cuerpo y mente",
    "Después de meditar, dedica tiempo a reflexionar",
    "Aprovecha este estado para recuperar energía"
  ],
  "tips": "Excelente estado de meditación. Mantente en esta paz interior y disfruta del momento."
}
```

---

## Casos de Uso

### 1. Obtener Últimos 20 Registros
```bash
GET /api/biometric-data
```
Retorna los 20 registros más recientes con predicción y recomendaciones.

### 2. Obtener Últimos 5 Registros
```bash
GET /api/biometric-data?limit=5
```
Útil para un dashboard que necesita pocos datos.

### 3. Obtener Un Solo Registro Más Reciente
```bash
GET /api/biometric-data?limit=1
```
Obtiene solo el registro más reciente.

### 4. Obtener Registro Completo
```bash
GET /api/biometric-data?limit=1
```
Retorna el registro con toda la información de predicción y recomendaciones.

---

## Características

✅ **Últimos 20 Registros** - Default, configurables hasta 100

✅ **Ordenamiento** - Timestamp descendente (más recientes primero)

✅ **Predicción IA** - Incluye estado predicho y confianza

✅ **Recomendaciones** - Personalizadas basadas en el estado

✅ **Parámetro Limit** - Control de cantidad de registros

✅ **Validación** - Limite máximo de 100 registros

---

## Integración con Frontend

### Streamlit Dashboard
```python
import requests

response = requests.get(
    "http://localhost:5000/api/biometric-data?limit=20"
)
data = response.json()

# data['data'] contiene los registros
for record in data['data']:
    breathing_rate = record['breathing_rate']
    heart_rate = record['heart_rate']
    state = record['prediction']['state']
    advice = record['recommendations']['advice']
```

### JavaScript/Web
```javascript
fetch('/api/biometric-data?limit=20')
  .then(res => res.json())
  .then(data => {
    console.log(`Total: ${data.count} registros`);
    
    data.data.forEach(record => {
      console.log(`ID: ${record.id}`);
      console.log(`Estado: ${record.prediction.state}`);
      console.log(`Confianza: ${record.prediction.confidence_percentage}%`);
    });
  });
```

---

## Notas Técnicas

- Los registros están **ordenados por timestamp descendente** (más recientes primero)
- El parámetro `limit` acepta **1-100** (default: 20)
- Si hay menos registros que el limit, retorna todos los disponibles
- La predicción se calcula **en tiempo real** basada en los datos biométricos
- Las recomendaciones son **determinísticas** basadas en el estado predicho
- Todos los timestamps están en **ISO 8601**

---

## Ejemplo de Respuesta Completa

```python
{
    "message": "Biometric data retrieved successfully",
    "count": 1,
    "limit": 1,
    "data": [
        {
            "id": 8,
            "timestamp": "2026-05-21T18:39:05.559095",
            "breathing_rate": 14,
            "heart_rate": 70,
            "movement": 15,
            "state": "relaxed",
            "stress_level": "low",
            "prediction": {
                "state": "relaxed",
                "confidence": 1.0,
                "confidence_percentage": 100.0
            },
            "recommendations": {
                "status": "Relajado",
                "description": "Tu estado mental es relajado y tranquilo",
                "advice": [
                    "Mantén esta tranquilidad realizando actividades que disfrutes",
                    "Puedes realizar ejercicio ligero o caminar",
                    "Es buen momento para leer o meditar",
                    "Tómate un descanso y disfruta de una bebida relajante"
                ],
                "tips": "Este es un estado ideal. Continúa con tu rutina normal y disfruta del bienestar."
            }
        }
    ]
}
```

---

## Testing

Ver `test_endpoint_biometric.py` para script de prueba completo.

```bash
python test_endpoint_biometric.py
```

---

*Última actualización: Mayo 21, 2026*
