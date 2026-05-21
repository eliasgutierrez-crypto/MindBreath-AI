# MindBreath AI

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)

Sistema inteligente de monitoreo de estado mental mediante análisis biométrico en tiempo real.

## 🚀 Características Principales

### Backend (API Flask)
- ✅ API REST con endpoints para datos biométricos
- ✅ Predicción de estado mental con IA (RandomForestClassifier)
- ✅ Recomendaciones personalizadas automáticas
- ✅ Base de datos PostgreSQL en Render
- ✅ Autenticación y validación de datos

### Frontend (Dashboard Streamlit)
- ✅ Dashboard moderno y responsivo
- ✅ Visualización en tiempo real
- ✅ Gráficas interactivas con Plotly
- ✅ Auto-actualización cada N segundos
- ✅ Métricas principales: respiración, pulso, movimiento, estado mental
- ✅ Análisis de distribución de estados y estrés
- ✅ Información detallada del modelo IA

## 📋 Estructura del Proyecto

```
MindBreath AI/
├── app.py                 # Aplicación Flask principal
├── config.py              # Configuración de Flask
├── streamlit_app.py       # Dashboard Streamlit
├── requirements.txt       # Dependencias Python
├── Procfile              # Config para Render
├── runtime.txt           # Versión de Python
├── .env.example          # Template de variables
├── .env                  # Variables locales (git ignored)
├── .streamlit/
│   └── config.toml       # Config de Streamlit
├── models/
│   ├── database.py       # SQLAlchemy setup
│   ├── biometric_data.py # Modelo de datos
│   ├── predict.py        # Funciones de predicción
│   └── model.pkl         # Modelo IA entrenado
├── routes/
│   └── api.py            # Endpoints de API
├── services/
│   ├── ai_service.py     # Servicio de IA
│   └── sensor_sender.py  # Envío de datos
├── templates/            # HTML (obsoleto, usa Streamlit)
└── static/               # CSS/JS (obsoleto, usa Streamlit)
```

## 🛠️ Instalación Local

### Requisitos
- Python 3.11+
- pip
- PostgreSQL (opcional, desarrollo puede usar SQLite)

### Pasos

1. **Clonar repositorio:**
```bash
git clone <tu-repo>
cd MindBreath\ AI
```

2. **Crear virtual environment:**
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Edita .env con tus valores locales
```

5. **Ejecutar la aplicación:**

**Opción A - Ejecución manual:**
```bash
# Terminal 1 - API Flask
python app.py
# Disponible en: http://localhost:5000

# Terminal 2 - Dashboard Streamlit
streamlit run streamlit_app.py
# Disponible en: http://localhost:8501
```

**Opción B - Script helper (Windows):**
```bash
run.bat
# Selecciona qué componente quieres ejecutar
```

## 📊 Uso del Dashboard

### Conectarse a la API

1. Abre http://localhost:8501 (o tu URL de Render)
2. En la barra lateral, selecciona:
   - **Local**: Para desarrollo local
   - **Render**: Para API desplegada en Render

### Interpretar Datos

| Métrica | Rango | Descripción |
|---------|-------|-------------|
| Respiración | 0-100 bpm | Frecuencia respiratoria |
| Pulso | 0-200 bpm | Frecuencia cardíaca |
| Movimiento | 0-100% | Nivel de movimiento detectado |
| Estado | 3 opciones | Relajado, Estresado, Meditación |
| Estrés | Bajo/Medio/Alto | Nivel de estrés percibido |

## 🚀 Deploy en Render

### 1. Preparar Repositorio
```bash
git add .
git commit -m "Deploy setup"
git push
```

### 2. Crear Web Service en Render
1. Ve a https://render.com
2. Click "New +" → "Web Service"
3. Conecta tu repositorio GitHub
4. Configuración:
   - Name: `mindbreath-api`
   - Runtime: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

### 3. Agregar PostgreSQL
1. En Render, crea una base de datos PostgreSQL
2. Copia la `DATABASE_URL`
3. En Environment variables de tu Web Service, agrega:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=tu-clave-secreta
   FLASK_ENV=production
   ```

### 4. Desplegar Dashboard en Streamlit Cloud

1. Push al repositorio GitHub:
```bash
git push
```

2. Ve a https://share.streamlit.io
3. Conecta repositorio y selecciona `streamlit_app.py`
4. En Advanced Settings, agrega variable:
   ```
   API_BASE_URL=https://tu-api.onrender.com/api
   ```

## 📡 Endpoints de API

### GET /api/v1
Información de la API

**Response:**
```json
{
  "message": "MindBreath AI API v1",
  "endpoints": [...]
}
```

### POST /api/biometric-data
Guardar datos biométricos y obtener predicción

**Request:**
```json
{
  "breathing_rate": 15,
  "heart_rate": 75,
  "movement": 25,
  "stress_level": "low"
}
```

**Response:**
```json
{
  "message": "Biometric data saved and analyzed successfully",
  "data": {
    "stored": {...},
    "analysis": {
      "prediction": {...},
      "recommendations": {...}
    }
  },
  "status": "success"
}
```

### GET /api/biometric-data
Obtiene los últimos 20 registros biométricos con predicción y recomendaciones

**Query Parameters:**
- `limit` (opcional): Número de registros (1-100, default: 20)

**Request:**
```bash
GET /api/biometric-data           # Últimos 20
GET /api/biometric-data?limit=10  # Últimos 10
```

**Response:**
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
        "advice": [...],
        "tips": "..."
      }
    }
  ]
}
```

**Ver documentación completa:** [ENDPOINT_BIOMETRIC_DATA.md](ENDPOINT_BIOMETRIC_DATA.md)

### GET /api/model-info
Información del modelo IA entrenado

### POST /api/predict
Predicción de estado mental

## 🤖 Modelo IA

- **Tipo**: RandomForest Classifier
- **Estimadores**: 100
- **Features**: 3 (breathing_rate, heart_rate, movement)
- **Clases**: relaxed, stressed, meditation
- **Accuracy**: Entrenado en datos sintéticos de prueba

## 🔒 Seguridad

- [x] Variables de entorno para secretos
- [x] HTTPS en Render
- [x] Validación de entrada en API
- [ ] Autenticación JWT (próxima iteración)
- [ ] Rate limiting (próxima iteración)

## 🐛 Troubleshooting

### "Cannot connect to API"
- Verifica que el servidor Flask esté corriendo
- Usa URL correcta en dashboard (local o Render)
- Revisa la consola del servidor para errores

### "No data available"
- Ejecuta test_api.py para generar datos
- O usa un cliente HTTP para hacer POST

### Gráficas vacías
- Necesitas al menos 2 registros
- Verifica que API esté retornando datos correctos

## 📝 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Exportar datos a PDF/CSV
- [ ] Alertas en tiempo real
- [ ] Análisis de tendencias avanzadas
- [ ] Mobile app con React Native
- [ ] Integración con wearables

## 📞 Soporte

Para problemas, revisa:
- STREAMLIT_GUIDE.md - Guía detallada del dashboard
- DEPLOY.md - Guía de deployment

## 🧪 Testing

### Ejecutar Tests

```bash
# Test de API
python test_api.py

# Test de Dashboard
python test_dashboard.py

# Test de Endpoint Biométrico
python test_endpoint_biometric.py
```

### Generar Datos de Prueba

```bash
# Ejecutar simulador de sensores
cd services
python sensor_sender.py
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **[Tu Nombre]** - *Trabajo Inicial* - [Tu GitHub]

## 🙏 Agradecimientos

- Flask y SQLAlchemy por las excelentes herramientas de desarrollo
- Streamlit por el framework de dashboard
- Scikit-learn por las herramientas de Machine Learning
- Render por el hosting gratuito

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella! ⭐**

Made with ❤️ by MindBreath AI Team

</div>

---

**Última actualización**: Mayo 2026  
**Versión**: 1.0.0
