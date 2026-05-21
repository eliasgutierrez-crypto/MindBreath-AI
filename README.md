# MindBreath AI API

Aplicación Flask preparada para deploy en Render con PostgreSQL y SQLAlchemy.

## Estructura del Proyecto

```
.
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración de la aplicación
├── requirements.txt    # Dependencias de Python
├── Procfile           # Configuración de deploy en Render
├── runtime.txt        # Versión de Python
├── models/
│   └── database.py    # Inicialización de SQLAlchemy
├── routes/
│   └── api.py         # Rutas de la API (Blueprint)
├── services/          # Servicios de la aplicación
├── static/            # Archivos estáticos
└── templates/         # Plantillas HTML
```

## Configuración de Base de Datos

La aplicación usa la variable de entorno `DATABASE_URL` para conectarse a PostgreSQL.

### Localmente

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita `.env` con tu configuración local:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### En Render

Render automáticamente configura la variable `DATABASE_URL` cuando creas una base de datos PostgreSQL.

## Instalación Local

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Deploy en Render

### Prerrequisitos

- Cuenta en [Render](https://render.com)
- Repositorio en GitHub con este código

### Pasos

1. **Crear base de datos PostgreSQL en Render**
   - Ve a Render → New → PostgreSQL
   - Configura la base de datos
   - Copia la `Internal Database URL` (se usará automáticamente como `DATABASE_URL`)

2. **Crear Web Service**
   - Ve a Render → New → Web Service
   - Conecta tu repositorio de GitHub
   - Configura:
     - **Root Directory**: `.` (raíz del proyecto)
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Environment Variables**:
       - `FLASK_ENV`: `production`
       - `SECRET_KEY`: (genera una clave segura)

3. **Conectar Web Service con PostgreSQL**
   - En la configuración del Web Service, ve a "Environment"
   - Render detectará automáticamente la base de datos PostgreSQL creada
   - La variable `DATABASE_URL` se configurará automáticamente

4. **Deploy**
   - Haz commit y push de tus cambios a GitHub
   - Render detectará los cambios y hará deploy automáticamente

## Endpoints

- `GET /` - Endpoint principal con estado de la API
- `GET /health` - Health check
- `GET /api/v1` - Documentación de endpoints de la API

## Agregar Nuevas Rutas

Para agregar nuevas rutas, edita `routes/api.py`:

```python
@api_bp.route('/api/v1/nueva-ruta', methods=['GET'])
def nueva_ruta():
    return jsonify({'message': 'Nueva ruta'})
```

## Agregar Modelos de Base de Datos

Crea nuevos archivos en `models/` para tus modelos SQLAlchemy:

```python
# models/user.py
from models.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}
```

Luego importa y usa el modelo en tus rutas.
