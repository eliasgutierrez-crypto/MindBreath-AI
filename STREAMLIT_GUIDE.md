# 🧠 MindBreath AI - Dashboard Streamlit

Dashboard moderno y en tiempo real para visualizar datos biométricos y predicciones de IA.

## Características

✨ **Visualización en Tiempo Real**
- Métricas actuales de respiración, pulso, movimiento
- Estado mental predicho (Relajado, Estresado, Meditación)
- Nivel de estrés actual

📊 **Gráficas Interactivas**
- Tendencias de respiración vs pulso
- Evolución del movimiento
- Distribución de estados mentales
- Análisis de niveles de estrés
- Importancia de características del modelo IA

🔄 **Auto-Actualización**
- Refresco automático cada N segundos (configurable)
- Botón manual para actualizar datos
- Conexión en tiempo real a API Flask

🎨 **Diseño Moderno**
- Tema oscuro personalizado
- Colores degradados para cada estado
- Interfaz responsiva y limpia

## Instalación Local

### Requisitos
- Python 3.11+
- API Flask de MindBreath AI ejecutándose

### Pasos

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Iniciar la API Flask** (en otra terminal):
```bash
python app.py
```

3. **Ejecutar el dashboard:**
```bash
streamlit run streamlit_app.py
```

4. **Abrir en navegador:**
   - Streamlit abrirá automáticamente en `http://localhost:8501`

## Uso

### Seleccionar Servidor
En la barra lateral izquierda, elige entre:
- **Local (Desarrollo)**: Conecta a `http://localhost:5000/api`
- **Render (Producción)**: Pega tu URL de Render

### Configurar Auto-actualización
Usa el slider para ajustar el intervalo de refresco (1-60 segundos)

### Interpretar Datos
- **Respiración**: Frecuencia respiratoria en respiraciones por minuto
- **Pulso**: Frecuencia cardíaca en latidos por minuto  
- **Movimiento**: Porcentaje de movimiento detectado (0-100%)
- **Estado Mental**: Predicción del modelo IA
  - 🟢 Relajado: Estado mental tranquilo
  - 🔴 Estresado: Signos de estrés detectados
  - 🟣 Meditación: Estado profundo de meditación

## Desplegar en Streamlit Cloud

### 1. Preparar Repositorio GitHub
```bash
git add .
git commit -m "Add Streamlit dashboard"
git push
```

### 2. Conectar con Streamlit Cloud
1. Ve a https://share.streamlit.io
2. Conecta tu repositorio GitHub
3. Selecciona:
   - Repository: tu-repo/MindBreath-AI
   - Branch: main
   - Main file path: streamlit_app.py

### 3. Configurar Variables de Entorno
En las settings del deploy en Streamlit Cloud, agrega:
```
API_BASE_URL=https://tu-app.onrender.com/api
```

### 4. Deploy
Streamlit Cloud desplegará automáticamente en: 
`https://tu-usuario-streamlit-mindbreath.streamlit.app`

## Problemas Comunes

### "No se puede conectar a la API"
- Verifica que el servidor Flask esté corriendo
- En desarrollo local, usa "Local (Desarrollo)"
- Para Render, pega la URL correcta con https://

### Las gráficas no actualizan
- Ajusta el intervalo de refresco hacia la izquierda
- Presiona el botón "🔄 Actualizar Ahora"

### Error de CORS
- Si usas Render, asegúrate de agregar headers CORS en Flask:
```python
from flask_cors import CORS
CORS(app)
```

## Estructura del Proyecto

```
streamlit_app.py        # Dashboard principal
.streamlit/
  └── config.toml       # Configuración de Streamlit
app.py                  # API Flask
requirements.txt        # Dependencias
```

## Próximos Pasos

- [ ] Agregar autenticación de usuarios
- [ ] Guardar recomendaciones personalizadas
- [ ] Exportar datos a PDF/CSV
- [ ] Notificaciones en tiempo real
- [ ] Historial detallado con filtros
- [ ] Comparativa de períodos

## Licencia

MIT - Libre para usar y modificar
