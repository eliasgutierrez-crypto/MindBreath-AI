"""
MindBreath AI - Dashboard Futurista y Profesional
Interfaz moderna tipo aplicación de salud con Streamlit
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="MindBreath AI - Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "MindBreath AI v1.0 - Mental Health Monitor"}
)

# ============================================================================
# ESTILOS CSS FUTURISTAS
# ============================================================================

st.markdown("""
<style>
    /* Fuente personalizada */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Tema oscuro profesional */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        padding: 2rem;
    }
    
    /* Contenedores */
    [data-testid="stContainer"] {
        border-radius: 12px;
    }
    
    /* Tarjetas modernas */
    .modern-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Métrica grande */
    .metric-big {
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .metric-big-value {
        font-size: 3.5rem;
        font-weight: 800;
        color: #fff;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .metric-big-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
    }
    
    .metric-big-unit {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Indicador de estrés */
    .stress-indicator {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stress-low {
        background: linear-gradient(135deg, rgba(84, 234, 176, 0.2), rgba(143, 211, 244, 0.2));
        border: 1px solid rgba(84, 234, 176, 0.3);
    }
    
    .stress-medium {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(255, 152, 0, 0.2));
        border: 1px solid rgba(255, 152, 0, 0.3);
    }
    
    .stress-high {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(255, 87, 34, 0.2));
        border: 1px solid rgba(244, 67, 54, 0.3);
    }
    
    /* Recomendación destacada */
    .recommendation-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .recommendation-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.8rem;
    }
    
    .recommendation-text {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
    }
    
    .recommendation-tips {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-style: italic;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    /* Barra de progreso personalizada */
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #fff;
        margin: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0.5rem;
    }
    
    /* Cards de estado */
    .state-card {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        backdrop-filter: blur(10px);
    }
    
    .state-relaxed {
        background: linear-gradient(135deg, rgba(84, 234, 176, 0.25), rgba(143, 211, 244, 0.25));
        border: 1px solid rgba(84, 234, 176, 0.4);
    }
    
    .state-stressed {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.25), rgba(255, 152, 0, 0.25));
        border: 1px solid rgba(244, 67, 54, 0.4);
    }
    
    .state-meditation {
        background: linear-gradient(135deg, rgba(168, 237, 234, 0.25), rgba(254, 214, 227, 0.25));
        border: 1px solid rgba(168, 237, 234, 0.4);
    }
    
    .state-emoji {
        font-size: 4rem;
        margin: 1rem 0;
    }
    
    .state-name {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 20, 25, 0.9), rgba(26, 31, 46, 0.9));
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.1), rgba(255,255,255,0));
        margin: 2rem 0;
    }
    
    /* Text colors */
    .text-success {
        color: #54eab0;
    }
    
    .text-warning {
        color: #ffc107;
    }
    
    .text-danger {
        color: #f44336;
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    # Selección de servidor
    api_mode = st.radio(
        "Servidor",
        ["🏠 Local", "🚀 Render"],
        help="Elige dónde está desplegada tu API"
    )
    
    if api_mode == "🏠 Local":
        API_BASE_URL = "http://localhost:5000/api"
    else:
        api_url_input = st.text_input(
            "URL de Render:",
            placeholder="https://tu-app.onrender.com/api"
        )
        API_BASE_URL = api_url_input if api_url_input else "https://mindbreath-api.onrender.com/api"
    
    st.divider()
    
    # Intervalo de actualización
    refresh_interval = st.slider(
        "Actualizar cada (segundos):",
        1, 60, 10
    )
    
    st.divider()
    
    # Info del proyecto
    st.markdown("### 📱 Acerca de")
    st.info("""
    **MindBreath AI v1.0**
    
    Monitoreo inteligente de salud mental mediante análisis biométrico en tiempo real.
    
    [Documentación](https://github.com)
    """)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data(ttl=5)
def fetch_biometric_data():
    """Obtiene los últimos registros biométricos"""
    try:
        response = requests.get(f"{API_BASE_URL}/biometric-data?limit=20", timeout=5)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    except:
        return []

@st.cache_data(ttl=5)
def fetch_model_info():
    """Obtiene información del modelo IA"""
    try:
        response = requests.get(f"{API_BASE_URL}/model-info", timeout=5)
        if response.status_code == 200:
            return response.json().get('data', {})
        return {}
    except:
        return {}

def get_stress_color(stress_level):
    """Retorna color basado en nivel de estrés"""
    colors = {
        'low': ('#54eab0', 'text-success'),
        'medium': ('#ffc107', 'text-warning'),
        'high': ('#f44336', 'text-danger')
    }
    return colors.get(stress_level, ('#667eea', 'text-info'))

def get_stress_emoji(stress_level):
    """Retorna emoji basado en nivel de estrés"""
    emojis = {
        'low': '✅',
        'medium': '⚠️',
        'high': '🔴'
    }
    return emojis.get(stress_level, '❓')

def get_state_emoji(state):
    """Retorna emoji basado en estado mental"""
    emojis = {
        'relaxed': '😌',
        'stressed': '😰',
        'meditation': '🧘'
    }
    return emojis.get(state, '🧠')

def get_state_label(state):
    """Retorna etiqueta legible del estado mental"""
    labels = {
        'relaxed': 'Relajado',
        'stressed': 'Estresado',
        'meditation': 'Meditación'
    }
    return labels.get(state, state)

def render_progress_bar(value, max_value=100, color="#667eea"):
    """Renderiza barra de progreso personalizada"""
    percentage = min(100, (value / max_value) * 100)
    return f"""
    <div class="progress-container">
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {percentage}%; background: linear-gradient(90deg, {color}, {color}80);"></div>
        </div>
    </div>
    """

# Header principal
st.title("🧠 MindBreath AI")
st.markdown("Dashboard de Monitoreo de Estado Mental en Tiempo Real")

# Placeholder para actualizaciones
placeholder_metrics = st.empty()
placeholder_charts = st.empty()
placeholder_recent = st.empty()

# Loop de actualización
def update_dashboard():
    """Actualiza el dashboard con nuevos datos"""
    
    # Obtener datos
    biometric_data = fetch_biometric_data()
    model_info = fetch_model_info()
    
    if not biometric_data:
        st.error("No hay datos disponibles. Verifica que la API Flask esté corriendo.")
        return
    
    # Convertir a DataFrame
    df = pd.DataFrame(biometric_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp', ascending=False)
    
    # Datos más recientes
    latest = df.iloc[0] if len(df) > 0 else None
    
    if latest is None:
        st.error("No hay registros biométricos disponibles.")
        return
    
    with placeholder_metrics.container():
        # Métricas principales
        st.subheader("📊 Métricas Actuales")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Respiración (bpm)",
                value=int(latest['breathing_rate']),
                delta=None,
                delta_color="off"
            )
        
        with col2:
            st.metric(
                label="Pulso (bpm)",
                value=int(latest['heart_rate']),
                delta=None,
                delta_color="off"
            )
        
        with col3:
            st.metric(
                label="Movimiento (%)",
                value=int(latest['movement']),
                delta=None,
                delta_color="off"
            )
        
        with col4:
            state_label = get_state_label(latest['state'])
            st.metric(
                label="Estado Mental",
                value=state_label,
                delta=None,
                delta_color="off"
            )
        
        with col5:
            stress_levels = {'low': 'Bajo', 'medium': 'Medio', 'high': 'Alto'}
            stress_label = stress_levels.get(latest['stress_level'], latest['stress_level'])
            st.metric(
                label="Nivel de Estrés",
                value=stress_label,
                delta=None,
                delta_color="off"
            )
    
    # Gráficas
    with placeholder_charts.container():
        st.subheader("📈 Gráficas de Tendencia")
        
        # Preparar datos para las últimas 20 lecturas
        df_recent = df.tail(20).sort_values('timestamp')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfica de Respiración y Pulso
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_recent['timestamp'],
                y=df_recent['breathing_rate'],
                mode='lines+markers',
                name='Respiración (bpm)',
                line=dict(color='#667eea', width=2),
                fill='tozeroy'
            ))
            fig1.add_trace(go.Scatter(
                x=df_recent['timestamp'],
                y=df_recent['heart_rate'],
                mode='lines+markers',
                name='Pulso (bpm)',
                line=dict(color='#764ba2', width=2),
                fill='tozeroy'
            ))
            fig1.update_layout(
                title="Respiración vs Pulso",
                xaxis_title="Tiempo",
                yaxis_title="bpm",
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Gráfica de Movimiento
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_recent['timestamp'],
                y=df_recent['movement'],
                mode='lines+markers',
                name='Movimiento (%)',
                line=dict(color='#84fab0', width=2),
                fill='tozeroy'
            ))
            fig2.update_layout(
                title="Nivel de Movimiento",
                xaxis_title="Tiempo",
                yaxis_title="Porcentaje (%)",
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfica de Distribución de Estados
        col1, col2 = st.columns(2)
        
        with col1:
            state_counts = df['state'].value_counts()
            colors_map = {'relaxed': '#84fab0', 'stressed': '#fa709a', 'meditation': '#a8edea'}
            fig3 = go.Figure(data=[
                go.Pie(
                    labels=[get_state_label(s) for s in state_counts.index],
                    values=state_counts.values,
                    marker=dict(colors=[colors_map.get(s, '#667eea') for s in state_counts.index])
                )
            ])
            fig3.update_layout(
                title="Distribución de Estados",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Gráfica de Niveles de Estrés
            stress_counts = df['stress_level'].value_counts()
            stress_labels = {'low': 'Bajo', 'medium': 'Medio', 'high': 'Alto'}
            fig4 = go.Figure(data=[
                go.Bar(
                    x=[stress_labels.get(s, s) for s in stress_counts.index],
                    y=stress_counts.values,
                    marker_color=['#84fab0', '#ffa500', '#fa709a'],
                )
            ])
            fig4.update_layout(
                title="Distribución de Niveles de Estrés",
                xaxis_title="Nivel de Estrés",
                yaxis_title="Cantidad",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Registros recientes
    with placeholder_recent.container():
        st.subheader("📋 Últimos Registros")
        
        df_display = df.head(10)[['timestamp', 'state', 'breathing_rate', 'heart_rate', 'movement', 'stress_level']].copy()
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df_display['state'] = df_display['state'].apply(get_state_label)
        df_display.columns = ['Timestamp', 'Estado', 'Respiración (bpm)', 'Pulso (bpm)', 'Movimiento (%)', 'Nivel Estrés']
        
        st.dataframe(df_display, use_container_width=True)
    
    # Recomendaciones de IA
    st.subheader("💡 Recomendaciones de IA")
    
    # Debug: mostrar qué datos tiene latest
    with st.expander("🔍 Debug - Datos recibidos"):
        st.json(latest)
    
    if 'recommendations' in latest and latest['recommendations']:
        rec = latest['recommendations']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="recommendation-box">
                <div class="recommendation-title">{get_state_emoji(latest['state'])} {rec.get('status', 'Estado Actual')}</div>
                <div class="recommendation-text">{rec.get('description', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if rec.get('advice'):
                st.markdown("**Consejos:**")
                for advice in rec['advice']:
                    st.markdown(f"- {advice}")
            
            if rec.get('tips'):
                st.markdown(f"*{rec['tips']}*", unsafe_allow_html=True)
        
        with col2:
            # Mostrar confianza de la predicción si está disponible
            if 'prediction' in latest:
                pred = latest['prediction']
                confidence = pred.get('confidence_percentage', 0)
                st.metric("Confianza IA", f"{confidence:.1f}%")
                
                # Barra de confianza
                st.progress(confidence / 100)
                st.caption(f"Confianza del modelo en la predicción")
    else:
        st.warning("No hay recomendaciones disponibles. Verifica que el servicio de IA esté funcionando.")
    
    # Información del modelo
    if model_info:
        st.subheader("🤖 Información del Modelo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tipo de Modelo", model_info.get('model_type', 'N/A'))
        
        with col2:
            st.metric("Número de Estimadores", model_info.get('n_estimators', 'N/A'))
        
        with col3:
            st.metric("Estado", model_info.get('status', 'N/A'))
        
        # Feature importances
        importances = model_info.get('feature_importances', {})
        if importances:
            fig_imp = go.Figure(data=[
                go.Bar(
                    x=list(importances.values()),
                    y=[f"{'Respiración' if k == 'breathing_rate' else 'Pulso' if k == 'heart_rate' else 'Movimiento'}" for k in importances.keys()],
                    orientation='h',
                    marker_color='#667eea'
                )
            ])
            fig_imp.update_layout(
                title="Importancia de Características",
                xaxis_title="Importancia",
                height=300,
                template='plotly_white'
            )
            st.plotly_chart(fig_imp, use_container_width=True)

# Actualizar dashboard
update_dashboard()

# Auto-refresh
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"⏱️ Datos actualizados automáticamente cada {refresh_interval} segundos")
with col2:
    if st.button("🔄 Actualizar Ahora"):
        st.rerun()

# Script de auto-refresh
time.sleep(refresh_interval)
st.rerun()
