# Guía de Deploy en Render

## Variables de Entorno Necesarias

Agrega las siguientes variables en tu proyecto de Render:

```
DATABASE_URL=postgresql://tu_usuario:tu_contraseña@tu_host:5432/tu_database
SECRET_KEY=tu_clave_secreta_aqui
FLASK_ENV=production
```

## Configuración en Render

1. **Database**: Usa tu base de datos PostgreSQL de Render
   - Render automáticamente proporciona `DATABASE_URL`

2. **Build Command**: 
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command** (en Procfile):
   ```
   web: gunicorn app:app
   ```

## Archivos Configurados

- ✅ `.env.example` - Template de variables (ya existe)
- ✅ `.env` - Configuración local (git ignored)
- ✅ `Procfile` - Configuración de gunicorn
- ✅ `requirements.txt` - Dependencias instaladas
- ✅ `runtime.txt` - Python 3.11.9

## Verificación Local

Antes de hacer deploy:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## Testing de API

```bash
python test_api.py
```

## Estado Actual

- [x] Dependencias instaladas
- [x] Modelo de IA cargado correctamente
- [x] API Flask funcional
- [x] Base de datos SQLAlchemy configurada
- [x] Variables de entorno configuradas
