@echo off
REM Script para ejecutar MindBreath AI - Development
REM Ejecuta la API Flask y el Dashboard Streamlit

echo.
echo ========================================
echo   MindBreath AI - Development Setup
echo ========================================
echo.

REM Verificar si el virtual environment existe
if not exist ".venv\Scripts\activate.bat" (
    echo Creando virtual environment...
    python -m venv .venv
)

REM Activar virtual environment
call .venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
echo.
echo Verificando dependencias...
pip install -q -r requirements.txt

REM Mostrar opciones
echo.
echo Selecciona qué quieres ejecutar:
echo.
echo 1) API Flask (localhost:5000)
echo 2) Dashboard Streamlit (localhost:8501)
echo 3) Ambos (en ventanas separadas)
echo.

set /p choice="Opcion (1-3): "

if "%choice%"=="1" (
    echo.
    echo Iniciando API Flask...
    echo.
    python app.py
) else if "%choice%"=="2" (
    echo.
    echo Iniciando Dashboard Streamlit...
    echo.
    streamlit run streamlit_app.py
) else if "%choice%"=="3" (
    echo.
    echo Iniciando API Flask en una nueva ventana...
    start cmd /k "python app.py"
    
    echo.
    echo Esperando 3 segundos...
    timeout /t 3 /nobreak
    
    echo Iniciando Dashboard Streamlit...
    streamlit run streamlit_app.py
) else (
    echo Opcion invalida
)

pause
